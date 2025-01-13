from typing import ClassVar

from typing_extensions import override

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage
from .base import BasePageTool


class ClickTool(BasePageTool):
    name: ClassVar[str] = "click"
    description: ClassVar[str] = "Click on an element based on element_id and return the new page state"

    element_id: int

    @override
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        x_path = element_mapping[str(self.element_id)].xpath
        await page.click(x_path=x_path)
