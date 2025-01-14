# Webrock 🕸️🪨

Webrock is a Python library designed to simplify the creation of autonomous browser agents. It leverages the power of Playwright for browser automation and AWS Bedrock for integrating AI-driven functionalities.

## Features

- **Seamless Browser Automation**: Utilize Playwright to interact with web pages, simulate user behavior, and perform tasks.
- **AI-Driven Capabilities**: Use AWS Bedrock to integrate with LLMs.
- **Extensible Architecture**: Modular and flexible design to fit various automation and AI tasks.

## Installation

To start experimenting, clone this repo:
```
git clone git@github.com:mscully4/webrock.git
```

Once inside, run:

```bash
poetry install
poetry run playwright install
npm install
npm run build
```

Then you can start a Jupyter notebook using

```bash
poetry run jupyter notebook
```

Then open the `demo.ipynb` file

You also need AWS credentials configured for Bedrock integration. Follow the [AWS CLI setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) if you haven’t already.

## Usage

Here’s a quick example to demonstrate Webrock in action:

```python
import logging
from playwright.async_api import async_playwright
from boto3 import Session
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
from webrock.browser import AsyncBrowserPage, PlaywrightBrowserPage
from webrock.tools import ClickTool, TypeTextTool, PressKeyTool
from webrock.core import WebrockAgentExecutor
from webrock.bedrock import BedrockModel, ClaudeSonnet_3_5_BedrockModel
from webrock.artifacts import S3ArtifactPublisher
import webrock

logging.basicConfig(level=logging.INFO)

p = await async_playwright().__aenter__()
browser = await p.chromium.launch(headless=False)
page = await browser.new_page(viewport={'width': 1280, 'height': 1000})

session = Session(profile_name="default", region_name="us-west-2")
bedrock_runtime: BedrockRuntimeClient = session.client(
    service_name="bedrock-runtime",
)

s3 = session.client('s3')

await page.goto("https://www.amazon.com")

# Ensure that you have access to whatever model you choose
model = ClaudeSonnet_3_5_BedrockModel(bedrock_runtime=bedrock_runtime)
tools = [ClickTool, TypeTextTool, PressKeyTool]

browser_page: AsyncBrowserPage = PlaywrightBrowserPage(page)

agent = WebrockAgentExecutor(model=model, browser_page=browser_page, tools=tools)

prompt = "Search for 'bicycles', hit enter and click on one of the products. Once you reach the bicycle product page, stop"
actions = await agent.ainvoke(prompt, max_sequences=8)

await browser.close()
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For any issues or questions, please open an issue on the [GitHub repository](https://github.com/yourusername/webrock/issues)

---

Start building autonomous browser agents with Webrock today!