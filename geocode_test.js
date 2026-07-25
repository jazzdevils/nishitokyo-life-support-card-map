// Google Maps geocoding script for stores
// This script searches each store on Google Maps and extracts coordinates

const stores = [
    { id: "store_0001", name: "オーケーひばりが丘店", neighborhood: "谷戸町" },
    { id: "store_0002", name: "ChanQ Coffee", neighborhood: "谷戸町" },
    { id: "store_0003", name: "Ｂｏｕｌａｎｇｅｒｉｅ５２５", neighborhood: "谷戸町" },
    { id: "store_0004", name: "ル マグノリア", neighborhood: "谷戸町" },
    { id: "store_0005", name: "Maison Jouer", neighborhood: "谷戸町" }
];

async function geocodeStore(store) {
    const query = encodeURIComponent(`${store.name} ${store.neighborhood} 西東京市`);
    const url = `https://www.google.co.jp/maps/search/${query}`;
    
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url;
    if (currentUrl.includes('/@')) {
        const match = currentUrl.match(/\/@(-?\d+\.?\d*),(-?\d+\.?\d*),/);
        if (match) {
            return {
                id: store.id,
                lat: parseFloat(match[1]),
                lng: parseFloat(match[2]),
                source: 'google_maps'
            };
        }
    }
    
    return {
        id: store.id,
        source: 'failed'
    };
}

// Run geocoding
const results = [];
for (const store of stores) {
    console.log(`Searching: ${store.name}`);
    const result = await geocodeStore(store);
    results.push(result);
    console.log(`Result: ${JSON.stringify(result)}`);
    await page.waitForTimeout(2000);
}

console.log(`\nResults: ${JSON.stringify(results, null, 2)}`);
