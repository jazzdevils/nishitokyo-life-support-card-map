"""
BrowserManager — manages Playwright browser lifecycle (launch, restart, close).
"""

from playwright.async_api import async_playwright


class BrowserManager:
    """
    Encapsulates browser creation, restart on EPIPE errors, and cleanup.
    """

    def __init__(self, playwright: async_playwright):
        self.playwright = playwright
        self.browser = None

    async def launch(self, headless: bool = True):
        """Launch a new Chromium browser."""
        self.browser = await self.playwright.chromium.launch(headless=headless)
        return self.browser

    async def close(self):
        """Close the current browser if it's alive."""
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
            self.browser = None

    async def restart(self, headless: bool = True):
        """Close current browser and launch a new one."""
        await self.close()
        return await self.launch(headless=headless)

    async def create_page(self):
        """Create a new page within the current browser."""
        if not self.browser:
            raise RuntimeError("Browser not launched. Call launch() first.")
        return await self.browser.new_page()
