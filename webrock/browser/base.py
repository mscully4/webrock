from abc import ABC, abstractmethod
from typing import Any


class AsyncBrowserPage(ABC):
    @abstractmethod
    async def take_screenshot(self) -> bytes:
        """
        Takes a screenshot of the current page and returns it as bytes
        """

    @abstractmethod
    async def run_js(self, js: str) -> Any:
        """
        Executes a JS script and returns the result
        """

    @abstractmethod
    async def click(self, x_path: str) -> None:
        """
        Clicks on an element on the page
        """

    @abstractmethod
    async def enter_text(self, x_path: str, text: str) -> None:
        """
        Enters text into an element on the page
        """

    @abstractmethod
    async def press_key(self, key: str) -> None:
        """
        Presses a key on the keyboard
        """
