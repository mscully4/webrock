from abc import ABC
from typing import Any

from typing_extensions import override

from .base import BedrockModel


def make_payload(encoded_image: str, prompt: str, system: str) -> dict[str, Any]:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/webp",
                            "data": encoded_image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "system": system,
        "max_tokens": 1000,
        "anthropic_version": "bedrock-2023-05-31",
    }
    return payload


class ClaudeBedrockModel(BedrockModel, ABC):
    @override
    @classmethod
    def generate_payload(cls, *, encoded_image: str, system: str, prompt: str) -> dict[str, Any]:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/webp",
                                "data": encoded_image,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "system": system,
            "max_tokens": 1000,
            "anthropic_version": "bedrock-2023-05-31",
        }


class ClaudeSonnet_3_BedrockModel(ClaudeBedrockModel):
    bedrock_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


class ClaudeSonnet_3_5_BedrockModel(ClaudeBedrockModel):
    bedrock_model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"


class ClaudeSonnet_3_5_v2_BedrockModel(ClaudeBedrockModel):
    bedrock_model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
