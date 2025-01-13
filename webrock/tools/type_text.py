from typing import ClassVar

from typing_extensions import override

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage
from .base import BasePageTool


class TypeTextTool(BasePageTool):
    name: ClassVar[str] = "type_text"
    description: ClassVar[str] = "Input text into a textbox based on element_id and return the new page state"

    element_id: int
    text: str

    @override
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        x_path = element_mapping[str(self.element_id)].xpath
        await page.enter_text(x_path=x_path, text=self.text)
