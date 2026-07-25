#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocode stores using Google Maps - Batch processor

This script processes stores in batches and saves intermediate results.
"""

import json
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus


def load_stores(input_file: str) -> list:
    """Load stores from JSON file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['stores']


def save_results(stores: list, output_file: str, categories: list = None, neighborhoods: list = None):
    """Save geocoded stores to JSON file."""
    result = {'stores': stores}
    if categories:
        result['categories'] = categories
    if neighborhoods:
        result['neighborhoods'] = neighborhoods
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def create_batch_files(stores: list, batch_size: int = 50):
    """Create batch files for processing."""
    batches = []
    for i in range(0, len(stores), batch_size):
        batch = stores[i:i + batch_size]
        batch_num = i // batch_size + 1
        batch_file = f'batch_{batch_num:03d}.json'
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        
        batches.append(batch_file)
        print(f"Created {batch_file} with {len(batch)} stores")
    
    return batches


def main():
    input_file = 'stores_with_coords.json'
    batch_size = 50
    
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    print(f"Loading stores from {input_file}...")
    stores = load_stores(input_file)
    print(f"Loaded {len(stores)} stores")
    
    print(f"\nCreating batches of {batch_size} stores...")
    batches = create_batch_files(stores, batch_size)
    print(f"\nCreated {len(batches)} batches")
    print("Process each batch using the geocoding tool, then merge results.")


if __name__ == '__main__':
    main()
