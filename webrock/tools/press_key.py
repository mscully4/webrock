from typing_extensions import override

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage
from .base import BasePageTool


class PressKeyTool(BasePageTool):
    name = "press_key"
    description = "Press a key on the keyboard and return the new page state"

    key: str

    @override
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        """
        Press a key on the keyboard and return the new page state
        """
        await page.press_key(self.key)
