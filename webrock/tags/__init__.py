import json
from collections.abc import Mapping
from typing import Any, NewType, Union

from pydantic import BaseModel, Field
from pydantic_core._pydantic_core import ValidationError

from .base import BaseTag
from .element_tags import AnchorTag, ButtonTag, DivTag, InputTag

TagToXPath = NewType("TagToXPath", dict[BaseTag, str])


class _UnionTag(BaseModel):
    tag: Union[AnchorTag, InputTag, DivTag, ButtonTag] = Field(discriminator="tag_name")


def create_tag_from_json(data: Union[str, Mapping[str, Any]]) -> BaseTag:
    if not isinstance(data, (str, Mapping)):
        raise TypeError("data field must be str or Mapping")

    dct = json.loads(data) if isinstance(data, str) else data

    # Use a discriminated union to create the correct specific tag, if a specific tag
    # can't be used, try BaseTag
    try:
        return _UnionTag(tag=dct).tag
    except ValidationError:
        return BaseTag(**dct)


__all__ = [
    "BaseTag",
    "TagToXPath",
    "create_tag_from_json",
    "AnchorTag",
    "InputTag",
    "DivTag",
    "ButtonTag",
]
