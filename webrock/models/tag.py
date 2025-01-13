from typing import NewType, Optional

from pydantic import BaseModel


class Tag(BaseModel):
    xpath: str
    tag_name: str
    id_number: int
    inner_text: str
    value: Optional[str]


TagToXPath = NewType("TagToXPath", dict[Tag, str])
