from typing import ClassVar

from typing_extensions import override

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage
from .base import BasePageTool


class _FatalErrorTool(BasePageTool):
    name: ClassVar[str] = "fatal_error"
    description: ClassVar[str] = (
        "If there is severe confusion or the task is impossible, use this tool with the reason why."
    )

    error_msg: str

    @override
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        raise RuntimeError(f"Fatal error while completing the task:\n{self.error_msg}")
