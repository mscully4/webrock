import json
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Union

from pydantic import BaseModel, field_validator


# For a list of model ids, see:
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html#model-ids-arns
class BedrockModel(ABC, BaseModel):
    bedrock_model_id: ClassVar[str]

    class Config:
        arbitrary_types_allowed = True

    bedrock_runtime: Any

    @field_validator("bedrock_runtime")
    @classmethod
    def _validate_bedrock_runtime(cls, val: Any) -> Any:
        if val.__module__ + "." + val.__class__.__name__ == "botocore.client.BedrockRuntime":
            return val

        raise ValueError("Must be a BedrockRuntime instance")

    @classmethod
    @abstractmethod
    def generate_payload(cls, *, encoded_image: str, system: str, prompt: str) -> dict[str, Any]:
        """ """

    def submit_request(self, payload: Union[str, dict[str, Any]]) -> dict[str, Any]:
        response = self.bedrock_runtime.invoke_model(
            modelId=self.bedrock_model_id,
            contentType="application/json",
            accept="application/json",
            body=payload if isinstance(payload, str) else json.dumps(payload),
        )

        return json.loads(response["body"].read())
