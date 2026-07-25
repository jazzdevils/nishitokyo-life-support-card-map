#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocode stores by extracting coordinates from Google Maps URLs

This script:
1. Reads stores_with_coords.json
2. For each store, constructs Google Maps search URL
3. Uses playwright MCP to navigate and extract coordinates
4. Saves results to stores_precise_coords.json
"""

import json
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus


def load_stores(input_file):
    """Load stores from JSON file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def create_search_urls(stores):
    """Create Google Maps search URLs for all stores."""
    urls = []
    for store in stores:
        query = f"{store['name']} {store['neighborhood']} 西東京市"
        url = f"https://www.google.co.jp/maps/search/{quote_plus(query)}"
        urls.append({
            'id': store['id'],
            'name': store['name'],
            'neighborhood': store['neighborhood'],
            'category': store['category'],
            'url': url
        })
    return urls


def extract_coords_from_url(url):
    """Extract latitude and longitude from Google Maps URL."""
    if '/@' not in url:
        return None
    
    try:
        parts = url.split('/@')[1].split('/')[0]
        lat_str = parts.split(',')[0]
        lng_str = parts.split(',')[1].split('z')[0]
        return {
            'lat': float(lat_str),
            'lng': float(lng_str)
        }
    except (IndexError, ValueError):
        return None


def main():
    input_file = 'stores_with_coords.json'
    output_file = 'stores_precise_coords.json'
    urls_file = 'search_urls.json'
    
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    print(f"Loading stores from {input_file}...")
    data = load_stores(input_file)
    stores = data['stores']
    
    print(f"Creating search URLs for {len(stores)} stores...")
    urls = create_search_urls(stores)
    
    # Save URLs for processing
    with open(urls_file, 'w', encoding='utf-8') as f:
        json.dump(urls, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(urls)} search URLs to {urls_file}")
    print("\nFirst 5 URLs:")
    for u in urls[:5]:
        print(f"  {u['name']}: {u['url'][:80]}...")
    
    print(f"\nTo process, navigate to each URL and extract coordinates from the URL.")
    print(f"Coordinates format in URL: /@lat,lng,zoom")


if __name__ == '__main__':
    main()
