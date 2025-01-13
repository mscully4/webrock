from typing import Any

from playwright.async_api import Page
from typing_extensions import override

from .base import AsyncBrowserPage


class PlaywrightBrowserPage(AsyncBrowserPage):
    def __init__(self, page: Page) -> None:
        self._page = page

    @override
    async def take_screenshot(self) -> bytes:
        return await self._page.screenshot(type="png", full_page=False)

    @override
    async def run_js(self, js: str) -> Any:
        return await self._page.evaluate(js)

    @override
    async def click(self, x_path: str) -> None:
        element = self._page.locator(x_path)
        await self._page.wait_for_timeout(1000)
        await element.click()
        await self._page.wait_for_timeout(2000)

    @override
    async def enter_text(self, x_path: str, text: str) -> None:
        element = self._page.locator(x_path)
        await element.fill(text)

    @override
    async def press_key(self, key: str) -> None:
        await self._page.keyboard.press(key)
        await self._page.wait_for_timeout(2000)
