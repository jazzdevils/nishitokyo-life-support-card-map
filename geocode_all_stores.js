// Geocode all stores using Google Maps
// Run this with: playwright_browser_run_code_unsafe

async function geocodeAllStores() {
    // Load stores data
    const response = await fetch('http://localhost:8899/stores_with_coords.json');
    const data = await response.json();
    const stores = data.stores;
    
    console.log(`Loaded ${stores.length} stores`);
    
    const results = [];
    let successCount = 0;
    let failCount = 0;
    
    for (let i = 0; i < stores.length; i++) {
        const store = stores[i];
        const query = encodeURIComponent(`${store.name} ${store.neighborhood} 西東京市`);
        const url = `https://www.google.co.jp/maps/search/${query}`;
        
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const currentUrl = page.url;
            const match = currentUrl.match(/\/@(-?\d+\.?\d*),(-?\d+\.?\d*),/);
            
            if (match) {
                results.push({
                    id: store.id,
                    name: store.name,
                    neighborhood: store.neighborhood,
                    category: store.category,
                    latitude: parseFloat(match[1]),
                    longitude: parseFloat(match[2]),
                    location_source: 'google_maps'
                });
                successCount++;
                console.log(`[${i+1}/${stores.length}] ✓ ${store.name}: ${match[1]}, ${match[2]}`);
            } else {
                // Use existing coordinates as fallback
                results.push({
                    ...store,
                    location_source: 'neighborhood_centroid_fallback'
                });
                failCount++;
                console.log(`[${i+1}/${stores.length}] ✗ ${store.name}: using fallback`);
            }
        } catch (error) {
            console.error(`Error for ${store.name}: ${error.message}`);
            results.push({
                ...store,
                location_source: 'error_fallback'
            });
            failCount++;
        }
        
        // Save progress every 50 stores
        if ((i + 1) % 50 === 0) {
            const progressData = {
                stores: results,
                categories: data.categories,
                neighborhoods: data.neighborhoods,
                progress: `${i+1}/${stores.length}`
            };
            // Store in page for later retrieval
            window.geocodingProgress = progressData;
            console.log(`Progress saved: ${i+1}/${stores.length}`);
        }
    }
    
    const finalData = {
        stores: results,
        categories: data.categories,
        neighborhoods: data.neighborhoods
    };
    
    window.geocodingResults = finalData;
    
    console.log(`\nComplete! Success: ${successCount}, Fallback: ${failCount}`);
    
    return {
        success: successCount,
        fallback: failCount,
        total: stores.length
    };
}

// Start geocoding
return geocodeAllStores();
