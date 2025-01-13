from typing import Literal, Optional

from .base import BaseTag


class AnchorTag(BaseTag):
    tag_name: Literal["A"]
    role: Optional[str] = None


class DivTag(BaseTag):
    tag_name: Literal["DIV"]
    role: Optional[str] = None
    has_on_click_event: Optional[bool] = None


class InputTag(BaseTag):
    tag_name: Literal["INPUT"]
    type: Optional[str] = None
    value: Optional[str] = None
    placeholder: Optional[str] = None


class ButtonTag(BaseTag):
    tag_name: Literal["BUTTON"]
