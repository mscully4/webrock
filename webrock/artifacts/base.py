from abc import ABC, abstractmethod

from PIL import Image


class BaseArtifactPublisher(ABC):
    @abstractmethod
    def publish_screenshot(self, *, image: Image.Image, run_id: str, seq_no: int) -> None:
        pass

    @abstractmethod
    def publish_system_prompt(self, *, prompt: str, run_id: str, seq_no: int) -> None:
        pass

    @abstractmethod
    def publish_model_response(self, *, response: str, run_id: str, seq_no: int) -> None:
        pass
