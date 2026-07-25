#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse storelist0702.txt and generate stores.json

This script reads the raw text file containing store information
and produces a structured JSON file with:
- stores: list of store objects (id, name, neighborhood, category)
- categories: list of unique business categories
- neighborhoods: list of unique neighborhoods
"""

import json
import re
import sys
from pathlib import Path


def parse_store_list(input_file: str, output_file: str) -> dict:
    """
    Parse the store list text file and output structured JSON.
    
    Args:
        input_file: Path to storelist0702.txt
        output_file: Path for output stores.json
    
    Returns:
        Dictionary containing stores, categories, and neighborhoods
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    stores = []
    categories = set()
    neighborhoods = set()
    store_id = 1
    
    # The file has a pattern:
    # {neighborhood}\n\n{store_name}\n\n{category}\n\n
    # with blank lines between each field
    lines = content.split('\n')
    
    # Remove empty lines and collect non-empty lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Filter out header/footer lines
    filtered_lines = []
    for line in non_empty_lines:
        # Skip headers and footers
        if line.startswith('西東京市') or line.startswith('2026/') or \
           line.startswith('店舗住所') or line.startswith('店の名称') or \
           line.startswith('業種') or '/' in line and line.endswith('/15') or \
           line.startswith('1/') or line.startswith('2/') or \
           line.startswith('3/') or line.startswith('4/') or \
           line.startswith('5/') or line.startswith('6/') or \
           line.startswith('7/') or line.startswith('8/') or \
           line.startswith('9/') or line.startswith('10/') or \
           line.startswith('11/') or line.startswith('12/') or \
           line.startswith('13/') or line.startswith('14/') or \
           line.startswith('15/'):
            continue
        filtered_lines.append(line)
    
    # Now process in groups of 3: neighborhood, store_name, category
    i = 0
    while i + 2 < len(filtered_lines):
        neighborhood = filtered_lines[i]
        store_name = filtered_lines[i + 1]
        category = filtered_lines[i + 2]
        
        # Validate entry
        if neighborhood and store_name and category:
            stores.append({
                'id': f'store_{store_id:04d}',
                'name': store_name,
                'neighborhood': neighborhood,
                'category': category
            })
            
            categories.add(category)
            neighborhoods.add(neighborhood)
            store_id += 1
        
        i += 3
    
    # Sort for consistency
    categories = sorted(list(categories))
    neighborhoods = sorted(list(neighborhoods))
    
    result = {
        'stores': stores,
        'categories': categories,
        'neighborhoods': neighborhoods
    }
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Parsed {len(stores)} stores")
    print(f"Found {len(categories)} categories")
    print(f"Found {len(neighborhoods)} neighborhoods")
    print(f"Output written to {output_file}")
    
    return result


def main():
    input_file = 'storelist0702.txt'
    output_file = 'stores.json'
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    parse_store_list(input_file, output_file)


if __name__ == '__main__':
    main()
