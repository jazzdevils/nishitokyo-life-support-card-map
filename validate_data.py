#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_data.py — validates stores_with_coords.json against known constraints.

Rules:
1. All required fields present (id, name, neighborhood, category, latitude, longitude, location_source)
2. Latitude/longitude within plausible bounds for Nishitokyo City (35.7–35.8, 139.5–139.6)
3. No duplicate store IDs
4. location_source is one of 'google_maps' or 'neighborhood_centroid'
5. Category is one of the known categories from the domain model

Usage:
    python validate_data.py [stores_with_coords.json]
"""

import json
import sys
from pathlib import Path


# Known categories from the domain model (full list from actual data)
KNOWN_CATEGORIES = [
    'スーパー・コンビニ',
    '食料品（米・酒・茶・日用雑貨等）',
    'パン・和菓子・洋菓子',
    '薬局・化粧品・コンタクトレンズ',
    '衣料品・靴・雑貨・寝具',
    '飲食業（和食・中華・洋食・カフェ）',
    '居酒屋・スナック',
    '健康・医療',
    '理容・美容・エステティック',
    '書籍・事務用品',
    '電気製品・時計・メガネ・写真',
    '趣味・花園芸・玩具・ペット関連',
    'ガソリンスタンド・車・自転車・タクシー',
    '生鮮食品（肉・魚・青果・豆腐・乳製品・惣菜・弁当等）',
    'クリーニング',
    '住まい・環境・工事・修理',
    'その他 お直し',
    'その他 アンテナショップ',
    'その他 インテリア',
    'その他 インドアゴルフスクール',
    'その他 エステ、化粧品販売',
    'その他 カフェ及びミニばら盆栽の販売',
    'その他 ゴルフ練習場',
    'その他 サービス',
    'その他 ジャム各種と季節のピクルス',
    'その他 スポーツクラブ',
    'その他 チャリティショップ',
    'その他 ドラッグストア',
    'その他 パソコン・スマホ・プログラミング教室',
    'その他 パソコン修理・販売',
    'その他 パーソナルジム',
    'その他 ホームセンター',
    'その他 リサイクルショップ',
    'その他 リラクゼーションサロン',
    'その他 リラクゼーション業',
    'その他 介護用品',
    'その他 児童福祉',
    'その他 公衆浴場',
    'その他 写真店(フィルム現像・撮影)',
    'その他 写真業',
    'その他 動物病院',
    'その他 化粧品、食器、キッチン雑貨',
    'その他 印刷物の製作・販売',
    'その他 宝飾',
    'その他 宝飾品',
    'その他 家庭金物・荒物・雑貨',
    'その他 小売 バック',
    'その他 教育',
    'その他 教育・学習支援業',
    'その他 整体・リラクゼーション',
    'その他 新聞販売店',
    'その他 書店 （文房具の取り扱いはありません）',
    'その他 洋服の仕立て・直し・リメイク',
    'その他 漢方相談(保険調剤不可)',
    'その他 珈琲前販売と喫茶',
    'その他 生活用品 金物店',
    'その他 生花店',
    'その他 産前産後助産師相談/女性対象リラクゼーションサロン',
    'その他 終活支援（遺言・相続）、創業支援（法人設立・融資申請）等',
    'その他 総合スポーツ施設',
    'その他 自然食品、健康食品販売',
    'その他 葬祭業・お線香お数珠販売',
    'その他 行政書士事務所',
    'その他 貴金属、補聴器',
    'その他 野菜直売',
    'その他 駄菓子・駄玩具',
    'その他 駄菓子屋',
]

# Bounding box for Nishitokyo City (approximate)
LAT_MIN = 35.7
LAT_MAX = 35.8
LON_MIN = 139.5
LON_MAX = 139.6


def validate_store(store: dict, index: int) -> list:
    """Validate a single store. Returns list of error messages."""
    errors = []
    
    # Required fields
    required = ['id', 'name', 'neighborhood', 'category', 'latitude', 'longitude', 'location_source']
    for field in required:
        if field not in store:
            errors.append(f"[{index}] Missing field: {field}")
    
    if not errors:
        # Latitude bounds
        lat = store['latitude']
        if not (LAT_MIN <= lat <= LAT_MAX):
            errors.append(f"[{index}] Latitude {lat} out of bounds ({LAT_MIN}–{LAT_MAX})")
        
        # Longitude bounds
        lon = store['longitude']
        if not (LON_MIN <= lon <= LON_MAX):
            errors.append(f"[{index}] Longitude {lon} out of bounds ({LON_MIN}–{LON_MAX})")
        
        # Category check
        cat = store['category']
        if cat not in KNOWN_CATEGORIES:
            errors.append(f"[{index}] Unknown category: '{cat}'")
        
        # Location source
        source = store['location_source']
        if source not in ('google_maps', 'neighborhood_centroid'):
            errors.append(f"[{index}] Invalid location_source: '{source}'")
    
    return errors


def validate_file(input_file: str):
    """Load JSON and validate all stores."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stores = data.get('stores', [])
    total = len(stores)
    print(f"Validating {total} stores from {input_file}...\n")
    
    all_errors = []
    seen_ids = set()
    
    for i, store in enumerate(stores, 1):
        errors = validate_store(store, i)
        all_errors.extend(errors)
        
        # Check duplicate IDs
        store_id = store.get('id')
        if store_id in seen_ids:
            all_errors.append(f"[{i}] Duplicate ID: '{store_id}'")
        seen_ids.add(store_id)
    
    if all_errors:
        print(f"Found {len(all_errors)} issues:")
        for err in all_errors:
            print(f"  ❌ {err}")
        print("\n❌ Validation FAILED.")
        return False
    else:
        print("✅ All stores pass validation.")
        return True


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'stores_with_coords.json'
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    success = validate_file(input_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()