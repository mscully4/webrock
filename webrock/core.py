import asyncio
import json
import logging
from typing import Any, Mapping, Optional, Type
from uuid import uuid4

from PIL import Image
from pydantic.json import pydantic_encoder

from webrock.artifacts import BaseArtifactPublisher
from webrock.bedrock import BedrockModel
from webrock.browser import AsyncBrowserPage
from webrock.exceptions import AgentExectorFatalError, MaxSequencesExceededError
from webrock.payload import BaseAction, DefaultAction, create_system_message
from webrock.tags import BaseTag, create_tag_from_json
from webrock.tools import BasePageTool, _FinalAnswerTool, _FatalErrorTool
from webrock.utils.image_processing import convert_image_to_base64, load_image

logger: logging.Logger = logging.getLogger(__name__)


_JS_TAG_UTILS = "./dist/webrock-js/main.min.js"

_SYSTEM_TOOLS: set[Type[BasePageTool]] = set([_FatalErrorTool, _FinalAnswerTool])


def _load_js(js_path: str) -> str:
    try:
        with open(js_path, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        raise ValueError(
            "Could not find main.js. Please ensure that you complied typescript using `npm run build`"
        ) from e


class WebrockAgentExecutor:
    def __init__(
        self,
        *,
        model: BedrockModel,
        browser_page: AsyncBrowserPage,
        tools: list[Type[BasePageTool]],
        action_class: type[BaseAction] = DefaultAction,
        js_file_path: str = _JS_TAG_UTILS,
    ) -> None:
        self._model = model
        logger.info(f"Creating AgentExector with model: {self._model}")

        self._page = browser_page

        # Create a set of all available tools, include some default tools that are necessary for things to work
        self._tools: set[Type[BasePageTool]] = set(tools)
        self._tools.update(_SYSTEM_TOOLS)

        self._action_class = action_class

        self._tool_map: Mapping[str, Type[BasePageTool]] = {tool.name: tool for tool in self._tools}
        logger.info(f"Creating AgentExector with tools: {[tool.name for tool in self._tools]}")

        self._js = _load_js(js_file_path)

    async def _tagify_page(self) -> dict[str, Any]:
        await self._page.run_js(self._js)
        return await self._page.run_js("tagifyWebpage();")

    async def _remove_tags(self) -> None:
        await self._page.run_js("removeTags();")

    def _strip_content(self, content: str) -> str:
        start = content.index("{")
        end = len(content) - content[::-1].index("}")
        return content[start:end]

    async def ainvoke(
        self,
        prompt: str,
        *,
        max_sequences: int = 10,
        run_id: Optional[str] = None,
        artifact_publisher: Optional[BaseArtifactPublisher] = None,
    ) -> list[BaseAction]:
        # Store actions taken by the model here
        actions: list[BaseAction] = []

        if not run_id:
            run_id = str(uuid4())

        logger.info(f"{run_id=}")

        for seq_no in range(max_sequences):
            # Wait a bit for any actions to take full effect
            await asyncio.sleep(2)

            logger.info(f"> Sequence {seq_no}")

            # Execute the JS file to load the needed utilities
            await self._page.run_js(self._js)

            # Execute the tagging script, which will tag the elements that our agent can interact with
            tagify_webpage_output: dict[str, Any] = await self._tagify_page()

            element_mapping: dict[str, BaseTag] = {k: create_tag_from_json(v) for k, v in tagify_webpage_output.items()}
            logger.debug(f"Element Mapping: {json.dumps(element_mapping, indent=4, default=pydantic_encoder)}")

            img: Image.Image = load_image(await self._page.take_screenshot())

            if artifact_publisher:
                artifact_publisher.publish_screenshot(image=img, run_id=run_id, seq_no=seq_no)

            # Convert the screenshot to base64, so it can be fed into the model
            base64_image = convert_image_to_base64(img)

            system = create_system_message(
                element_mapping=element_mapping,
                previous_actions=actions,
                tools=self._tools,
                action_class=self._action_class,
            )

            if artifact_publisher:
                artifact_publisher.publish_system_prompt(prompt=system, run_id=run_id, seq_no=seq_no)

            # Generate the payload to submit to the model
            payload = self._model.__class__.generate_payload(encoded_image=base64_image, system=system, prompt=prompt)

            # Submit the payload to the model via bedrock
            response = self._model.submit_request(payload=payload)

            if artifact_publisher:
                artifact_publisher.publish_model_response(response=json.dumps(response), run_id=run_id, seq_no=seq_no)

            # Remove any stray marks
            content = self._strip_content(response["content"][0]["text"])
            logger.info(f"Content: {content}")

            action = self._action_class.model_validate_json(content)
            logger.info(f"Action: {action.model_dump_json(indent=4)}")
            actions.append(action)

            # Remove tags before doing any actions, as tags might get in the way
            await self._remove_tags()

            tool: BasePageTool = self._tool_map[action.action](**action.action_input)
            logger.info(f"Created tool '{tool.name}'")

            if isinstance(tool, _FatalErrorTool):
                raise AgentExectorFatalError(tool.error_msg)

            if isinstance(tool, _FinalAnswerTool):
                logger.info("Agent is done!")
                return actions

            # Run the tool selected by the model
            await tool.arun(page=self._page, element_mapping=element_mapping)

        # If we've reached this point, then the agent was not able to complete successfully
        raise MaxSequencesExceededError(f"Executor has completed {max_sequences} sequences without completing")
