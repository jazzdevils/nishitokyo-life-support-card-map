#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse store addresses from official website and geocode them

This script:
1. Scrapes store list from https://nishitokyo-cheering2026.com/list/
2. Extracts full addresses from each store's detail page
3. Geocodes addresses using Google Maps Geocoding API
4. Saves results to stores_with_addresses.json

Usage:
    python3 parse_addresses.py [google_api_key]
"""

import json
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


# Base URL
BASE_URL = 'https://nishitokyo-cheering2026.com'
LIST_URL = f'{BASE_URL}/list/'

# Headers for web scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Nominatim (OpenStreetMap) Geocoding API - Free, no API key needed
NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'

# User-Agent required by Nominatim
NOMINATIM_HEADERS = {
    'User-Agent': 'NishitokyoStoreMap/1.0 (contact: nishitokyo-store-map@example.com)'
}


def get_total_pages():
    """Get total number of pages from pagination."""
    response = requests.get(LIST_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find pagination links
    pagination = soup.find('div', class_='pagination') or soup.find('ul', class_='pagination')
    
    if not pagination:
        # Try to find page links manually
        page_links = soup.find_all('a', href=lambda href: href and 'page=' in href)
        if page_links:
            max_page = 0
            for link in page_links:
                href = link.get('href', '')
                if 'page=' in href:
                    try:
                        page_num = int(href.split('page=')[-1].split('&')[0])
                        max_page = max(max_page, page_num)
                    except ValueError:
                        pass
            return max(max_page, 1)
    
    # Look for page numbers in pagination
    page_links = pagination.find_all('a')
    max_page = 1
    for link in page_links:
        href = link.get('href', '')
        if 'page=' in href:
            try:
                page_num = int(href.split('page=')[-1].split('&')[0])
                max_page = max(max_page, page_num)
            except ValueError:
                pass
    
    return max_page


def parse_store_list_page(page_num: int) -> list:
    """
    Parse a single page of store listings.
    
    Args:
        page_num: Page number (1-indexed)
    
    Returns:
        List of store dictionaries with basic info
    """
    url = f'{LIST_URL}?page={page_num}' if page_num > 1 else LIST_URL
    
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    stores = []
    
    # Find all store boxes (div with class 'box')
    store_boxes = soup.find_all('div', class_='box')
    
    for box in store_boxes:
        # Extract store name from h3
        name_tag = box.find('h3')
        store_name = name_tag.get_text(strip=True) if name_tag else ''
        
        if not store_name:
            continue
        
        # Extract category (p tag before h3 or with specific class)
        category_tag = box.find('p')
        category = category_tag.get_text(strip=True) if category_tag else ''
        
        # Extract address if available on list page
        address = ''
        for tag in box.find_all(['p', 'span']):
            text = tag.get_text(strip=True)
            if '〒' in text or '東京都西東京市' in text:
                address = text
                break
        
        # Extract detail URL
        detail_url = ''
        detail_link = box.find('a', href=lambda href: href and '/list/detail/' in href)
        if detail_link:
            detail_url = detail_link.get('href', '')
            if detail_url.startswith('/'):
                detail_url = BASE_URL + detail_url
        
        stores.append({
            'name': store_name,
            'category': category,
            'address': address,
            'detail_url': detail_url
        })
    
    return stores


def get_store_detail(detail_url: str) -> dict:
    """
    Get detailed store information from detail page.
    
    Args:
        detail_url: URL to store detail page
    
    Returns:
        Dictionary with store details including full address
    """
    response = requests.get(detail_url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    info = {}
    
    # Extract store name
    name_tag = soup.find('h1') or soup.find('h2')
    info['name'] = name_tag.get_text(strip=True) if name_tag else ''
    
    # Extract address (look for postal code pattern 〒)
    address_text = ''
    for tag in soup.find_all(['p', 'dd', 'span']):
        text = tag.get_text(strip=True)
        if '〒' in text or '東京都西東京市' in text:
            address_text = text
            break
    
    info['address'] = address_text
    
    # Extract category
    category_tag = soup.find(['span', 'p'], class_='category') or \
                  soup.find(['span', 'p'], class_='genre') or \
                  soup.find('th', string='業種').find_next('dd') if soup.find('th', string='業種') else None
    info['category'] = category_tag.get_text(strip=True) if category_tag else ''
    
    # Extract neighborhood from address
    if '谷戸町' in address_text:
        info['neighborhood'] = '谷戸町'
    elif '緑町' in address_text:
        info['neighborhood'] = '緑町'
    elif '北原町' in address_text:
        info['neighborhood'] = '北原町'
    elif '西原町' in address_text:
        info['neighborhood'] = '西原町'
    elif '田無町' in address_text:
        info['neighborhood'] = '田無町'
    elif '南町' in address_text:
        info['neighborhood'] = '南町'
    elif '向台町' in address_text:
        info['neighborhood'] = '向台町'
    elif '芝久保町' in address_text:
        info['neighborhood'] = '芝久保町'
    elif 'ひばりが丘' in address_text:
        if 'ひばりが丘北' in address_text:
            info['neighborhood'] = 'ひばりが丘北'
        else:
            info['neighborhood'] = 'ひばりが丘'
    elif '北町' in address_text:
        info['neighborhood'] = '北町'
    elif '下保谷' in address_text:
        info['neighborhood'] = '下保谷'
    elif '住吉町' in address_text:
        info['neighborhood'] = '住吉町'
    elif '栄町' in address_text:
        info['neighborhood'] = '栄町'
    elif '泉町' in address_text:
        info['neighborhood'] = '泉町'
    elif '東町' in address_text:
        info['neighborhood'] = '東町'
    elif '中町' in address_text:
        info['neighborhood'] = '中町'
    elif '富士町' in address_text:
        info['neighborhood'] = '富士町'
    elif '保谷町' in address_text:
        info['neighborhood'] = '保谷町'
    elif '東伏見' in address_text:
        info['neighborhood'] = '東伏見'
    elif '柳沢' in address_text:
        info['neighborhood'] = '柳沢'
    elif '新町' in address_text:
        info['neighborhood'] = '新町'
    else:
        info['neighborhood'] = ''
    
    return info


def geocode_address(address: str) -> dict:
    """
    Geocode an address using Nominatim (OpenStreetMap) API.
    Free, no API key needed. Rate limit: 1 request/second.
    
    Args:
        address: Full address string
    
    Returns:
        Dictionary with 'lat' and 'lon', or None if failed
    """
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'jp',
        'addressdetails': 1
    }
    
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=NOMINATIM_HEADERS, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        
        if results and len(results) > 0:
            result = results[0]
            return {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', '')
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"  Parse error: {e}")
        return None


def main():
    print("=" * 60)
    print("西東京市 生活応援カード 参加店舗 주소 파싱")
    print("=" * 60)
    print()
    
    # Step 1: Get total pages
    print("Step 1: Getting total pages...")
    total_pages = get_total_pages()
    print(f"  Total pages: {total_pages}")
    print()
    
    # Step 2: Parse all store listings
    print("Step 2: Parsing store listings...")
    all_stores = []
    
    for page in range(1, total_pages + 1):
        print(f"  Page {page}/{total_pages}...", end=' ')
        stores = parse_store_list_page(page)
        print(f"Found {len(stores)} stores")
        all_stores.extend(stores)
        time.sleep(0.5)  # Be polite
    
    print(f"\n  Total stores found: {len(all_stores)}")
    print()
    
    # Step 3: Get details for each store and geocode
    print("Step 3: Getting store details and geocoding...")
    print("  Using Nominatim API (1 request/second)")
    print()
    stores_with_addresses = []
    
    for i, store in enumerate(all_stores, 1):
        print(f"[{i}/{len(all_stores)}] {store['name']}")
        
        # Address is already on list page, no need to fetch detail page
        address = store.get('address', '')
        
        if address:
            print(f"  Address: {address[:60]}...")
            
            # Geocode using Nominatim
            print(f"  Geocoding...", end=' ')
            coords = geocode_address(address)
            
            if coords:
                store['latitude'] = coords['lat']
                store['longitude'] = coords['lon']
                store['location_source'] = 'geocoded'
                print(f"✓ ({coords['lat']:.6f}, {coords['lon']:.6f})")
            else:
                print("✗ Failed")
                store['location_source'] = 'geocoding_failed'
            
            time.sleep(1)  # Nominatim rate limit: 1 request/second
        else:
            print(f"  No address found")
            store['location_source'] = 'no_address'
        
        stores_with_addresses.append(store)
    
    # Step 4: Save results
    output_file = 'stores_with_addresses.json'
    
    result = {
        'stores': stores_with_addresses,
        'metadata': {
            'total_stores': len(stores_with_addresses),
            'parsed_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'https://nishitokyo-cheering2026.com/list/'
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print(f"Complete!")
    print(f"  Stores with addresses: {len([s for s in stores_with_addresses if s.get('address')])}")
    print(f"  Stores geocoded: {len([s for s in stores_with_addresses if s.get('latitude')])}")
    print(f"  Output: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
