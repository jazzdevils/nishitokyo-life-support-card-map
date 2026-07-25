"""
GeocodeEngine — extracts coordinates from Google Maps URLs using Playwright.
"""

import asyncio
import re
from playwright.async_api import Page


class GeocodeEngine:
    """
    Stateless engine that:
    1. Navigates to a Google Maps search URL
    2. Clicks the first result to get a detailed place page
    3. Extracts lat/lng from the final URL
    """

    @staticmethod
    def extract_coords(url: str):
        """Extract lat/lng from a Google Maps URL like /@lat,lng,zoom."""
        m = re.search(r'/@([-\d.]+),([-\d.]+)', url)
        if m:
            return float(m.group(1)), float(m.group(2))
        return None, None

    async def geocode_store(self, page: Page, store: dict, total: int, index: int):
        """
        Geocode a single store using a Playwright page.
        Returns a dict with id, name, lat, lng, source or None on failure.
        """
        url = store['url']
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(2)

        results = await page.query_selector_all('[data-item-id]')
        if results:
            await results[0].click()
            await asyncio.sleep(2)
            lat, lng = self.extract_coords(page.url)
            if lat and lng:
                return {
                    'id': store['id'],
                    'name': store['name'],
                    'lat': lat,
                    'lng': lng,
                    'source': 'google_maps'
                }
            else:
                print(f'{index+1}/{total} FAIL(no coords): {store["name"]}', flush=True)
                return None
        else:
            print(f'{index+1}/{total} FAIL(no results): {store["name"]}', flush=True)
            return None

    async def geocode_all(self, search_data: list, progress_tracker, browser_manager):
        """
        Process all stores using the browser and progress tracker.
        """
        total = len(search_data)
        next_index, processed = progress_tracker.load()
        print(f'Start: {next_index + 1}/{total}', flush=True)

        browser = await browser_manager.launch(headless=True)

        for i in range(next_index, total):
            store = search_data[i]

            try:
                page = await browser_manager.create_page()
                result = await self.geocode_store(page, store, total, i)
                await page.close()

                if result:
                    processed[store['id']] = result
                    print(f'{i+1}/{total} OK: {store["name"]} ({result["lat"]}, {result["lng"]})', flush=True)

            except Exception as e:
                print(f'{i+1}/{total} ERROR: {store["name"]} - {e}', flush=True)
                browser = await browser_manager.restart(headless=True)

            progress_tracker.save(processed, i + 1, total)

        try:
            await browser_manager.close()
        except Exception:
            pass

        print(f'Complete! {len(processed)}/{total}', flush=True)