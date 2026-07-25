#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocode stores using Nominatim API and save coordinates to JSON

This script:
1. Reads stores.json (without coordinates)
2. Queries Nominatim API for each store's location
3. Saves results to stores_with_coords.json

Rate limiting: 1 request per second (Nominatim policy)
Fallback: Uses neighborhood centroid if geocoding fails
"""

import json
import sys
import time
import requests
from pathlib import Path


# Nominatim API endpoint
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# User-Agent required by Nominatim
HEADERS = {
    'User-Agent': 'NishitokyoStoreMap/1.0 (contact: nishitokyo-store-map@example.com)'
}

# Neighborhood centroids - geocoded from Google Maps (2026-07-24)
# These are accurate center points for each neighborhood in Nishitokyo City
NEIGHBORHOOD_CENTROIDS = {
    '谷戸町': {'lat': 35.7482288, 'lon': 139.5431003},
    '緑町': {'lat': 35.7354777, 'lon': 139.5375062},
    '北原町': {'lat': 35.7368902, 'lon': 139.5446272},
    '西原町': {'lat': 35.7330827, 'lon': 139.5378642},
    '田無町': {'lat': 35.7286659, 'lon': 139.5394156},
    '南町': {'lat': 35.727118, 'lon': 139.5408338},
    '向台町': {'lat': 35.7199332, 'lon': 139.5343636},
    '芝久保町': {'lat': 35.7325172, 'lon': 139.5254377},
    'ひばりが丘': {'lat': 35.7441717, 'lon': 139.536273},
    'ひばりが丘北': {'lat': 35.7531138, 'lon': 139.5439933},
    '北町': {'lat': 35.7530796, 'lon': 139.5575984},
    '下保谷': {'lat': 35.7488579, 'lon': 139.5591902},
    '住吉町': {'lat': 35.7465153, 'lon': 139.5477305},
    '栄町': {'lat': 35.7502334, 'lon': 139.5540967},
    '泉町': {'lat': 35.7408761, 'lon': 139.5521867},
    '東町': {'lat': 35.7446778, 'lon': 139.5630106},
    '中町': {'lat': 35.7429186, 'lon': 139.560782},
    '富士町': {'lat': 35.7293989, 'lon': 139.5623956},
    '保谷町': {'lat': 35.7290909, 'lon': 139.5529891},
    '東伏見': {'lat': 35.7277357, 'lon': 139.5579167},
    '柳沢': {'lat': 35.7189235, 'lon': 139.5502769},
    '新町': {'lat': 35.7166754, 'lon': 139.54139}
}


def geocode_store(store_name: str, neighborhood: str) -> dict:
    """
    Query Nominatim API to get coordinates for a store.
    Note: Nominatim has strict rate limits and policies.
    
    Args:
        store_name: Name of the store
        neighborhood: Neighborhood name
    
    Returns:
        Dictionary with 'lat' and 'lon' keys, or None if failed
    """
    # Build search query
    query = f"{store_name} {neighborhood} 西東京市 東京都"
    
    params = {
        'q': query,
        'format': 'json',
        'limit': 1
    }
    
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        
        if results and len(results) > 0:
            result = results[0]
            return {
                'lat': float(result['lat']),
                'lon': float(result['lon'])
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  Error querying Nominatim: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"  Error parsing response: {e}")
        return None


def get_fallback_coords(neighborhood: str) -> dict:
    """
    Get fallback coordinates from neighborhood centroid.
    
    Args:
        neighborhood: Neighborhood name
    
    Returns:
        Dictionary with 'lat' and 'lon' keys
    """
    if neighborhood in NEIGHBORHOOD_CENTROIDS:
        return NEIGHBORHOOD_CENTROIDS[neighborhood]
    
    # Default to center of Nishitokyo City
    return {'lat': 35.7600, 'lon': 139.4900}


def geocode_all_stores(input_file: str, output_file: str, use_api: bool = False) -> dict:
    """
    Add coordinates to all stores and save results.
    
    Args:
        input_file: Path to stores.json
        output_file: Path for output stores_with_coords.json
        use_api: If True, try Nominatim API; if False, use neighborhood centroids only
    
    Returns:
        Dictionary with geocoded stores
    """
    # Load stores
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stores = data['stores']
    total = len(stores)
    
    if use_api:
        print(f"Starting geocoding for {total} stores using Nominatim API...")
        print(f"Rate limit: 1 request/second (Nominatim policy)")
        print(f"Estimated time: ~{total // 60} minutes")
        print()
        
        geocoded_stores = []
        success_count = 0
        fallback_count = 0
        
        for i, store in enumerate(stores, 1):
            print(f"[{i}/{total}] {store['name']} ({store['neighborhood']})")
            
            # Try to geocode
            coords = geocode_store(store['name'], store['neighborhood'])
            
            if coords:
                store['latitude'] = coords['lat']
                store['longitude'] = coords['lon']
                store['location_source'] = 'geocoded'
                success_count += 1
                print(f"  ✓ Found: ({coords['lat']:.6f}, {coords['lon']:.6f})")
            else:
                # Use fallback
                fallback = get_fallback_coords(store['neighborhood'])
                store['latitude'] = fallback['lat']
                store['longitude'] = fallback['lon']
                store['location_source'] = 'neighborhood_centroid'
                fallback_count += 1
                print(f"  ⚠ Using neighborhood centroid")
            
            geocoded_stores.append(store)
            
            # Rate limiting: wait 1 second between requests
            if i < total:
                time.sleep(1)
    else:
        # Use neighborhood centroids only
        print(f"Using neighborhood centroids for {total} stores...")
        print()
        
        geocoded_stores = []
        
        for i, store in enumerate(stores, 1):
            print(f"[{i}/{total}] {store['name']} ({store['neighborhood']})")
            
            # Use neighborhood centroid
            coords = get_fallback_coords(store['neighborhood'])
            store['latitude'] = coords['lat']
            store['longitude'] = coords['lon']
            store['location_source'] = 'neighborhood_centroid'
            
            geocoded_stores.append(store)
        
        success_count = 0
        fallback_count = total
    
    # Save results
    result = {
        'stores': geocoded_stores,
        'categories': data['categories'],
        'neighborhoods': data['neighborhoods']
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print(f"Geocoding complete!")
    print(f"  API success: {success_count}")
    print(f"  Neighborhood centroid: {fallback_count}")
    print(f"  Total: {total}")
    print(f"Output: {output_file}")
    print("=" * 60)
    
    return result


def main():
    input_file = 'stores.json'
    output_file = 'stores_with_coords.json'
    use_api = False
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == '--api':
        use_api = True
    
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    geocode_all_stores(input_file, output_file, use_api=use_api)


if __name__ == '__main__':
    main()
