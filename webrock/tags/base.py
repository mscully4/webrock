from typing import Optional

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class BaseTag(BaseModel):
    xpath: str = Field(exclude=True)
    tag_name: str
    id_number: int
    inner_text: str
    aria_label: Optional[str] = None

    class Config:
        alias_generator = to_camel
