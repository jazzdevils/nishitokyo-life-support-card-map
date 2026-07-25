# 西東京市 生活応援カード 参加店舗マップ

Nishitokyo City "Life Support Card" participating stores interactive map.

## 개요 (Overview)

西東京市の「生活応援カード」参加店舗の位置をインタラクティブな地図上に表示します。  
Leaflet.js + OpenStreetMap を使用し、データは JSON ファイルとして提供されます。

## 데이터 (Data)

- `stores_with_coords.json` — 667개 매장의 좌표 (570개 정확한 Google Maps 좌표 + 97개 동네 중심점 좌표)
- `search_urls.json` — 667개 Google Maps 검색 URL (원본 데이터)
- `geocoding_progress.json` — 지오코딩 진행 상황 (중간 파일)

## 사용 방법 (Usage)

### 로컬에서 열기
로컬 HTTP 서버가 필요합니다 (모듈 스크립트와 `fetch()`가 `file://`에서 동작하지 않음).

```bash
python3 -m http.server 9001
# 또는
npx http-server . -p 9001
```

이후 `http://localhost:9001` 접속.

### GitHub Pages 배포
`https://jazzdevils.github.io/nishitokyo-life-support-card-map` 에서 바로 접속 가능.

## 기술 스택 (Tech Stack)

- **지도 렌더링**: Leaflet.js + OpenStreetMap
- **좌표 획득**: Playwright 브라우저 자동화 + Google Maps 검색 (Option A), 동네 중심점 fallback (Option B)
- **데이터 처리**: Python (geocode_precise.py, validate_data.py 등)
- **프로젝트 구성**: ES modules (`map.js`), HTML (`index.html`)

## 파일 구조 (File Structure)

```
.
├── index.html          # 메인 페이지 (ES module import)
├── map.js              # 지도 렌더링 및 필터링 로직
├── stores_with_coords.json  # 최종 좌표 데이터
├── search_urls.json    # Google Maps 검색 URL
├── geocoding_progress.json  # 지오코딩 진행 상황
├── geocode_precise.py  # Playwright 기반 좌표 추출 스크립트
├── validate_data.py    # 데이터 검증 스크립트
├── browser_manager.py  # Playwright 브라우저 관리 클래스
├── progress_tracker.py # 진행 상황 추적 클래스
├── geocode_engine.py   # 좌표 추출 엔진 클래스
├── CONTEXT.md          # 도메인 모델 문서
├── docs/adr/           # 아키텍처 결정 기록
└── README.md           # (본 파일)
```

## 라이선스 (License)

- 데이터: 西東京市 공개 데이터 (출처: 西東京市役所)
- 코드: MIT License (자유 사용)

---

**참고**: 西東京市役所의 공식 「生活応援カード」 데이터를 기반으로 합니다.  
정확한 좌표는 Google Maps 검색으로 획득하였으며, 약 100개 매장은 동네 중심점 좌표를 fallback으로 사용합니다.