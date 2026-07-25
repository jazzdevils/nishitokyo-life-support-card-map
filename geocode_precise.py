#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocode stores using Google Maps via Playwright — Click results to get coords.
Handles EPIPE errors by restarting browser.

Usage:
    python geocode_precise.py [search_urls.json] [output_file]

This script now uses modular components:
    - BrowserManager   (browser_manager.py)
    - ProgressTracker   (progress_tracker.py)
    - GeocodeEngine     (geocode_engine.py)
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

from browser_manager import BrowserManager
from progress_tracker import ProgressTracker
from geocode_engine import GeocodeEngine


async def main():
    # Determine input/output files
    search_urls_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('search_urls.json')
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None  # Not used yet; progress saved to geocoding_progress.json

    # Load search URLs
    with open(search_urls_file, 'r', encoding='utf-8') as f:
        search_data = json.load(f)

    # Instantiate components
    progress_tracker = ProgressTracker()
    geocode_engine = GeocodeEngine()

    async with async_playwright() as p:
        browser_manager = BrowserManager(p)

        await geocode_engine.geocode_all(search_data, progress_tracker, browser_manager)


if __name__ == '__main__':
    asyncio.run(main())