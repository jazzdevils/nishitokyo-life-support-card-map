# CONTEXT.md - Store Location Map Domain

## Glossary

### 매장 (Store)
西東京市「生活応援カード」에 participating 한 구체적인 사업장 위치.  
각 매장은 고유한 식별자를 가지며, 다음 속성을 가진다:
- 이름 (店名): 가게의 상호명 (예: "オーケーひばりが丘店")
- 동네 (町名): 소재한 행정 구역 (예: "谷戸町", "田無町")
- 업종 (業種): 사업 분류 (예: "スーパー・コンビニ", "飲食業")
- 위치 (位置): 위도/경도 좌표

### 동네 (Neighborhood)
西東京市の 행정 구역 단위. 매장이 소재하는 지역.  
예시: 谷戸町，緑町，北原町，西原町，田無町，南町，向台町，芝久保町, ひばりが丘, ひばりが丘北, 北町，下保谷，住吉町，栄町，泉町，東町，中町，富士町，保谷町，東伏見，柳沢，新町

### 업종 (Business Category)
매장의 사업 유형 분류. 실제 데이터에는 다음과 같은 67개 카테고리가 존재한다:
- 슈퍼・コンビニ (Supermarket/Convenience Store)
- 食料品（米・酒・茶・日用雑貨等）(Food Items)
- パン・和菓子・洋菓子 (Bakery/Sweets)
- 薬局・化粧品・コンタクトレンズ (Pharmacy/Cosmetics)
- 衣料品・靴・雑貨・寝具 (Clothing/Footwear/Accessories/Bedding)
- 飲食業（和食・中華・洋食・カフェ）(Restaurant - Japanese/Chinese/Western/Cafe)
- 居酒屋・スナック (Izakaya/Snack Bar)
- 健康・医療 (Health/Medical)
- 理容・美容・エステティック (Beauty/Hair Salon/Aesthetic)
- 書籍・事務用品 (Books/Stationery)
- 電気製品・時計・メガネ・写真 (Electronics/Watches/Eyeglasses/Photography)
- 趣味・花園芸・玩具・ペット関連 (Hobbies/Gardening/Toys/Pets)
- ガソリンスタンド・車・自転車・タクシー (Gas Station/Cars/Bicycles/Taxis)
- 生鮮食品（肉・魚・青果・豆腐・乳製品・惣菜・弁当等）(Fresh Food - Meat/Fish/Vegetables/Tofu/Dairy/Prepared meals/Lunch boxes)
- クリーニング (Dry Cleaning)
- 住まい・環境・工事・修理 (Housing/Environment/Construction/Repair)
- その他 お直し (Other - Alterations)
- その他 アンテナショップ (Other - Antenna Shop)
- その他 インテリア (Other - Interior)
- その他 インドアゴルフスクール (Other - Indoor Golf School)
- その他 エステ、化粧品販売 (Other - Aesthetic/Cosmetics Sales)
- その他 カフェ及びミニばら盆栽の販売 (Other - Cafe/Mini Rose Bonsai Sales)
- その他 ゴルフ練習場 (Other - Golf Practice Range)
- その他 サービス (Other - Services)
- その他 ジャム各種と季節のピクルス (Other - Jams/Seasonal Pickles)
- その他 スポーツクラブ (Other - Sports Club)
- その他 チャリティショップ (Other - Charity Shop)
- その他 ドラッグストア (Other - Drug Store)
- その他 パソコン・スマホ・プログラミング教室 (Other - PC/Smartphone/Programming School)
- その他 パソコン修理・販売 (Other - PC Repair/Sales)
- その他 パーソナルジム (Other - Personal Gym)
- その他 ホームセンター (Other - Home Center)
- その他 リサイクルショップ (Other - Recycle Shop)
- その他 リラクゼーションサロン (Other - Relaxation Salon)
- その他 リラクゼーション業 (Other - Relaxation Business)
- その他 介護用品 (Other - Care Supplies)
- その他 児童福祉 (Other - Child Welfare)
- その他 公衆浴場 (Other - Public Bath)
- その他 写真店(フィルム現像・撮影) (Other - Photo Shop/Film Development/Photography)
- その他 写真業 (Other - Photography Business)
- その他 動物病院 (Other - Animal Hospital)
- その他 化粧品、食器、キッチン雑貨 (Other - Cosmetics/Tableware/Kitchen Goods)
- その他 印刷物の製作・販売 (Other - Printing/Production/Sales)
- その他 宝飾 (Other - Jewelry)
- その他 宝飾品 (Other - Jewelry Items)
- その他 家庭金物・荒物・雑貨 (Other - Household Hardware/Rough Goods/Miscellaneous)
- その他 小売 バック (Other - Retail Bags)
- その他 教育 (Other - Education)
- その他 教育・学習支援業 (Other - Education/Learning Support)
- その他 整体・リラクゼーション (Other - Osteopathic/Relaxation)
- その他 新聞販売店 (Other - Newspaper Sales)
- その他 書店 （文房具の取り扱いはありません）(Other - Bookstore/No Stationery)
- その他 洋服の仕立て・直し・リメイク (Other - Clothing Tailoring/Alteration/Remake)
- その他 漢方相談(保険調剤不可) (Other - Kampo Consultation/Insurance Dispensing not available)
- その他 珈琲前販売と喫茶 (Other - Coffee Sales/Cafe)
- その他 生活用品 金物店 (Other - Living Supplies/Hardware Store)
- その他 生花店 (Other - Fresh Flower Shop)
- その他 産前産後助産師相談/女性対象リラクゼーションサロン (Other - Pre/Postnatal Midwife Consultation/Women's Relaxation Salon)
- その他 終活支援（遺言・相続）、創業支援（法人設立・融資申請）等 (Other - End-of-Life Support/Will/Inheritance/Startup Support/Corporate Establishment/Financing)
- その他 総合スポーツ施設 (Other - Comprehensive Sports Facility)
- その他 自然食品、健康食品販売 (Other - Natural Food/Health Food Sales)
- その他 葬祭業・お線香お数珠販売 (Other - Funeral/Burial/Incense/Beads Sales)
- その他 行政書士事務所 (Other - Administrative Lawyer Office)
- その他 貴金属、補聴器 (Other - Precious Metals/Hearing Aids)
- その他 野菜直売 (Other - Direct Vegetable Sales)
- その他 駄菓子・駄玩具 (Other - Cheap Sweets/Cheap Toys)
- その他 駄菓子屋 (Other - Cheap Sweets Shop)

### 위치 (Location)
매장의 지리적 좌표 (위도, 경도).  
OpenStreetMap 기반의 좌표계를 사용하며, 정확한 주소 기반 좌표 또는 동네 중심점을 사용할 수 있다.

### 좌표 출처 (Location Source)
좌표 데이터의 출처. `stores_with_coords.json`의 각 매장은 다음 중 하나의 `location_source` 값을 가진다:
- `google_maps`: Google Maps 검색 결과에서 직접 추출한 정확한 좌표 (Playwright 브라우저 자동화로 획득)
- `neighborhood_centroid`: 동네 중심점 좌표 (정확한 주소 검색이 실패했을 때 fallback으로 사용)

### 지도 (Map)
매장 위치를 시각적으로 표시하는 인터랙티브한 웹 컴포넌트.  
Leaflet.js 라이브러리를 사용하여 구현하며, OpenStreetMap 타일을 렌더링한다.

### 핀 (Marker)
지도 위에 표시되는 매장 위치 마커. 클릭 시 매장 정보 (이름, 업종) 를 표시한다.

### 데이터 파일 (Data Files)
매장 정보와 좌표를 저장하는 JSON 파일:
- `stores_with_coords.json`: 최종 출력 파일. `map.js`가 `fetch()`로 로드하여 지도를 렌더링한다. 667개 매장 중 570개는 정확한 Google Maps 좌표, 97개는 동네 중심점 좌표를 포함한다.
- `search_urls.json`: 667개 Google Maps 검색 URL (원본 데이터). `geocode_precise.py`가 이 파일을 읽어 좌표를 추출한다.
- `geocoding_progress.json`: 진행 상황을 저장하는 중간 파일. 브라우저 재시작이나 EPIPE 오류 발생 시 마지막 처리 지점부터 재개할 수 있게 한다.
