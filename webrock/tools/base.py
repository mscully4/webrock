from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict

from pydantic import BaseModel

from webrock.tags import BaseTag

from ..browser import AsyncBrowserPage


class BasePageTool(ABC, BaseModel):
    name: ClassVar[str]
    description: ClassVar[str]

    @abstractmethod
    async def arun(self, page: AsyncBrowserPage, element_mapping: dict[str, BaseTag]) -> None:
        """
        A method to asynchronously perform the tool's action
        """

    @classmethod
    def get_input_schema(self) -> Dict[str, Any]:
        return self.model_json_schema(mode="serialization")
