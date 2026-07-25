// Test geocoding with first 10 stores

async function testGeocode() {
    const response = await fetch('http://localhost:8899/stores_with_coords.json');
    const data = await response.json();
    const stores = data.stores.slice(0, 10); // First 10 stores only
    
    console.log(`Testing with ${stores.length} stores`);
    
    const results = [];
    
    for (let i = 0; i < stores.length; i++) {
        const store = stores[i];
        const query = encodeURIComponent(`${store.name} ${store.neighborhood} 西東京市`);
        const url = `https://www.google.co.jp/maps/search/${query}`;
        
        console.log(`\n[${i+1}/${stores.length}] Searching: ${store.name}`);
        
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            const currentUrl = page.url;
            console.log(`URL: ${currentUrl.substring(0, 100)}...`);
            
            const match = currentUrl.match(/\/@(-?\d+\.?\d*),(-?\d+\.?\d*),/);
            
            if (match) {
                results.push({
                    id: store.id,
                    name: store.name,
                    lat: parseFloat(match[1]),
                    lng: parseFloat(match[2]),
                    source: 'google_maps'
                });
                console.log(`✓ Found: ${match[1]}, ${match[2]}`);
            } else {
                results.push({
                    id: store.id,
                    name: store.name,
                    source: 'not_found'
                });
                console.log(`✗ Not found`);
            }
        } catch (error) {
            console.error(`Error: ${error.message}`);
            results.push({
                id: store.id,
                name: store.name,
                source: 'error'
            });
        }
    }
    
    console.log(`\n=== Results ===`);
    console.log(JSON.stringify(results, null, 2));
    
    return results;
}

return testGeocode();
