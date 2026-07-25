# Specification: Store Location Map for 西東京市

## Problem Statement

西東京市「生活応援カード」에 participating 한 약 500 개 매장의 위치 정보를 사용자가 쉽게 확인할 수 없다. 현재는 텍스트 목록만 제공되어, 특정 지역의 매장을 찾거나 업종별 분포를 파악하기 어렵다.

## Solution

OpenStreetMap 기반의 인터랙티브한 웹 지도를 제공하여, 사용자가 매장의 위치를 시각적으로 확인하고 업종별로 필터링할 수 있도록 한다. 단일 HTML 파일로 구현하여 로컬에서 바로 실행 가능하다.

## User Stories

### 지도 기본 기능
1. As a 西東京市 주민, I want to see all participating stores on a map, so that I can understand the overall distribution of stores
2. As a user, I want to zoom and pan the map freely, so that I can focus on areas of interest
3. As a user, I want the map to center on 西東京市 by default, so that I immediately see the relevant area

### 핀 (Marker) 표시
4. As a user, I want each store to be represented by a marker pin on the map, so that I can see exact locations
5. As a user, I want markers to be distinguishable by color or icon based on business category, so that I can quickly identify store types
6. As a user, I want to see all ~500 store markers loaded when the map opens, so that I don't have to wait for additional loading

### 핀 클릭 정보 표시
7. As a user, I want to click on a marker and see the store name (店名), so that I can identify which store it is
8. As a user, I want to see the business category (業種) when clicking a marker, so that I know what type of store it is
9. As a user, I want to see the neighborhood name (町名) when clicking a marker, so that I know which area the store is in
10. As a user, I want the marker popup to close when I click elsewhere, so that the map remains clean

### 업종 필터링
11. As a user, I want to filter stores by business category (업종), so that I can focus on specific types of stores
12. As a user, I want to see a checkbox list of all available business categories, so that I can select multiple categories
13. As a user, I want markers to appear/disappear instantly when I toggle filters, so that I can quickly explore different categories
14. As a user, I want to select "all categories" to see all stores again, so that I can reset the view
15. As a user, I want to see how many stores match my current filter, so that I know if my selection is useful

### 동네 필터링 (Future Enhancement)
16. As a user, I want to filter stores by neighborhood (町名), so that I can focus on specific areas
17. As a user, I want to see which neighborhoods have the most stores, so that I can identify commercial hubs

### 데이터 정확성
18. As a user, I want store locations to be as accurate as possible, so that I can find them easily when visiting
19. As a user, I want to know if a marker's location is approximate (neighborhood centroid) vs. exact (address geocoded), so that I can plan accordingly
20. As a user, I want the map to work without requiring API keys or billing setup, so that it's accessible to everyone

### Performance
21. As a user, I want the map to load within 10 seconds even with 500 markers, so that I don't have to wait too long
22. As a user, I want the map to remain responsive when panning/zooming with many markers displayed, so that exploration feels smooth

### Usability
23. As a user, I want the interface to be in Japanese (matching the source data), so that it's familiar and accessible
24. As a user, I want clear labels for all UI elements (buttons, filters, popups), so that I understand what each control does
25. As a user, I want the map to work in modern browsers (Chrome, Firefox, Safari, Edge), so that I can use my preferred browser

### Maintenance
26. As an administrator, I want to easily update the store data when stores open/close/move, so that the map stays current
27. As an administrator, I want to regenerate coordinates when new stores are added, so that locations remain accurate

## Implementation Decisions

### Technical Stack
- **Map Library**: Leaflet.js (v1.9+) - lightweight, no API key required
- **Map Tiles**: OpenStreetMap - free, open-source tile provider
- **Geocoding**: Nominatim API - OpenStreetMap's geocoding service (free, rate-limited to 1 request/second)
- **Data Format**: JSON for store data with coordinates
- **Delivery**: Single HTML file with embedded CSS/JS for simplicity

### Data Flow
1. Source data (storelist0702.txt) is parsed into structured JSON
2. A Python script batches geocoding requests to Nominatim API
3. Geocoded data (store name + neighborhood → coordinates) is stored in a JSON file
4. The HTML file loads this JSON and renders markers using Leaflet.js

### Geocoding Strategy
- Query format: `"{store_name}, {neighborhood}, 西東京市，東京都，日本"`
- Rate limiting: 1 request per second to respect Nominatim's policy
- Fallback: If geocoding fails, use neighborhood centroid as approximate location
- Caching: Geocoded results are saved to avoid re-querying unchanged stores

### Filtering Architecture
- Client-side filtering: All store data loaded once, filters applied in JavaScript
- Filter state managed by simple checkbox event listeners
- Marker visibility toggled via Leaflet's `map.removeLayer()` / `map.addLayer()`
- No server-side filtering required (single-page application)

### UI Layout
- Full-screen map as primary content
- Floating filter panel (top-left corner) with:
  - Category checkboxes (scrollable if needed)
  - "Show All" / "Clear All" buttons
  - Store count display
- Popup content: Store name (H2), business category, neighborhood

### Performance Optimizations
- Marker clustering not implemented initially (keep simple)
- All markers rendered at once (Leaflet handles ~500 markers adequately)
- Lazy loading of map tiles (built into Leaflet)

### Data Model
```json
{
  "stores": [
    {
      "id": "unique_identifier",
      "name": "オーケーひばりが丘店",
      "neighborhood": "谷戸町",
      "category": "スーパー・コンビニ",
      "latitude": 35.7xxx,
      "longitude": 139.5xxx
    }
  ],
  "categories": ["スーパー・コンビニ", "食料品", ...],
  "neighborhoods": ["谷戸町", "緑町", ...]
}
```

### Testing Decisions

#### What Makes a Good Test
- Test external behavior only (user interactions, not implementation details)
- Verify that markers appear/disappear based on filters
- Confirm that popups show correct store information
- Validate that the map centers on 西東京市

#### Modules to Test
1. **Data parsing**: Verify text file → JSON conversion preserves all stores
2. **Geocoding script**: Test that valid queries return coordinates
3. **Filter logic**: Confirm checkbox state → marker visibility mapping
4. **Popup content**: Verify store data displays correctly

#### Testing Approach
- Manual testing preferred for this prototype (interactive map)
- Browser DevTools Console for debugging geocoding errors
- Visual inspection of marker placement accuracy

## Out of Scope

### Not Included in This Version
1. **Search functionality** - No search bar for store names
2. **Directions/navigation** - No integration with routing services
3. **Store details page** - No additional information beyond name/category/neighborhood
4. **Mobile app** - Web-only, responsive design not prioritized
5. **User reviews/ratings** - No social features
6. **Real-time updates** - Data is static, manually updated
7. **Multi-language support** - Japanese only (matching source data)
8. **Store photos** - No image display
9. **Operating hours** - No time-based filtering
10. **Route optimization** - No multi-store path planning

### Future Enhancements (Post-MVP)
- Neighborhood filtering (in addition to category filtering)
- Export filtered results as CSV/PDF
- Integration with public transit routes
- Progressive Web App (PWA) for offline use
- Automated data refresh from official sources

## Further Notes

### Data Source
- Original file: `storelist0702.txt` (西東京市「生活応援カード」参加店舗一覧)
- Date: 2026/7/2 現在
- Approximate store count: ~500 stores across ~20 neighborhoods

### Known Limitations
1. **Geocoding accuracy**: Nominatim may not find all stores; fallback to neighborhood centroid
2. **Rate limiting**: Initial geocoding takes ~8-10 minutes for 500 stores
3. **No API key**: Cannot use Google Maps features (street view, detailed business info)
4. **Static data**: Map does not auto-update when official data changes

### Maintenance Notes
- To update store data: Re-run parsing script with new text file
- To update coordinates: Re-run geocoding script (will skip already-geocoded stores)
- To add new categories: No code changes needed (categories derived from data)

### Deployment
- Single HTML file can be opened directly in browser (file:// protocol)
- No web server required for basic functionality
- For sharing: Host on GitHub Pages, Netlify, or similar static hosting

### ADRs Referenced
- **ADR-0001**: Map Provider Selection - OpenStreetMap + Leaflet.js chosen over Google Maps due to API key constraints
