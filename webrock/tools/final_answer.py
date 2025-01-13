from typing import ClassVar

from typing_extensions import override

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage
from .base import BasePageTool


class _FinalAnswerTool(BasePageTool):
    name: ClassVar[str] = "final_answer"
    description: ClassVar[str] = "Select this tool if you think you have accomplished your goal"

    @override
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        pass
