from typing import Any, Literal

from pydantic import BaseModel


class BaseAction(BaseModel):
    action: str
    action_input: dict[str, Any] = {}


class DefaultAction(BaseAction):
    thoughts: str
    reasoning: str
    uncertainties: str
    summary_of_previous_actions: str
    confidence_level: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
