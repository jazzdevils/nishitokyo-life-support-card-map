# Architecture Decision Record: Map Provider Selection

## Status

Accepted (2026-07-24)

## Context

The project requires displaying store locations on an interactive map. The stores are located in 東京都西東京市 (Nishitokyo City, Tokyo), Japan. There are approximately 500 store locations across ~20 neighborhoods.

## Decision

**Use OpenStreetMap with Leaflet.js for map rendering, but use Google Maps (via Playwright automation) for geocoding.**

### Rationale

- No Google Maps API key available
- Google Maps requires billing setup even for free tier
- Geocoding 500+ stores via API would incur additional costs
- OpenStreetMap provides free, open-source mapping alternative
- Leaflet.js is lightweight and requires no API key
- **Browser-based Google Maps search (Playwright) bypasses API costs** — clicking the first result and extracting `/@lat,lng,zoom` is free and highly accurate

## Consequences

### Positive
- No API key required
- No billing setup needed
- Completely free to use
- Open data source

### Negative
- May have different visual appearance than Google Maps
- Less detailed business information in some areas
- **Browser automation approach** requires Playwright runtime and may have reliability issues (EPIPE errors)
- Japanese place name search may be less accurate than Google
- Neighborhood centroid fallback still needed for ~100 stores where precise coordinates fail

## Implementation Approach

1. Use Leaflet.js for map rendering
2. Obtain coordinates via:
   - **Option A (final implementation)**: Playwright browser automation + Google Maps search — click first result, extract `/@lat,lng,zoom` URL pattern (highest accuracy, highest effort)
   - Option B: Neighborhood centroids only (low accuracy, low effort)
   - Option C: Nominatim OpenStreetMap geocoding API (moderate accuracy, moderate effort, rate-limited)
3. Display markers with store information on click

### Actual Geocoding Flow
- `geocode_precise.py`: Loads `search_urls.json`, opens each URL in Playwright headless browser, clicks first result, extracts coordinates from URL `/@lat,lng,zoom`, saves to `stores_with_coords.json`
- `stores_with_coords.json`: Final output — 570 stores with precise Google Maps coordinates, 97 fallback neighborhood centroids
- Playwright browser restarts on EPIPE errors to maintain reliability
