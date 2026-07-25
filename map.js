@ -0,0 +1,150 @@
/**
 * Map module — renders store locations on a Leaflet map.
 * 
 * Responsibilities:
 * - Initialize the map with OpenStreetMap tiles
 * - Load store data from a JSON file
 * - Create markers for each store
 * - Filter markers based on selected categories
 * - Update visible store count
 */

// --- State (module-scoped) ---
let stores = [];
let markers = [];
let categories = [];
let map = null;

// --- Map initialization ---
export function initMap() {
    map = L.map('map').setView([35.7600, 139.4900], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// --- Data loading ---
export async function loadStoreData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        stores = data.stores || [];
        categories = data.categories || [];
        
        document.getElementById('totalCount').textContent = stores.length;
        
        createMarkers();
        setupFilterPanel();
        updateStoreCount();
        
        return { stores, categories };
    } catch (error) {
        console.error('Error loading store data:', error);
        alert('店舗データの読み込みに失敗しました。');
        return null;
    }
}

// --- Marker creation ---
export function createMarkers() {
    markers = [];
    
    stores.forEach(store => {
        const marker = L.marker([store.latitude, store.longitude]);
        
        marker.bindPopup(`
            <div class="popup-content">
                <h3>${store.name}</h3>
                <p>業種: <span class="category">${store.category}</span></p>
                <p>町名: ${store.neighborhood}</p>
            </div>
        `);
        
        marker.category = store.category;
        marker.storeData = store;
        
        markers.push(marker);
        marker.addTo(map);
    });
}

// --- Filtering ---
export function filterMarkers(selectedCategories) {
    markers.forEach(marker => {
        if (selectedCategories.includes(marker.category)) {
            if (!map.hasLayer(marker)) {
                marker.addTo(map);
            }
        } else {
            if (map.hasLayer(marker)) {
                map.removeLayer(marker);
            }
        }
    });
    
    updateStoreCount();
}

// --- Count update ---
export function updateStoreCount() {
    const visibleCount = markers.filter(marker => map.hasLayer(marker)).length;
    document.getElementById('visibleCount').textContent = visibleCount;
}

// --- Filter panel setup ---
export function setupFilterPanel() {
    const categoryList = document.getElementById('categoryList');
    
    categories.forEach(category => {
        const li = document.createElement('li');
        
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = true;
        checkbox.dataset.category = category;
        
        checkbox.addEventListener('change', () => {
            const selected = getSelectedCategories();
            filterMarkers(selected);
        });
        
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(category));
        li.appendChild(label);
        categoryList.appendChild(li);
    });
    
    document.getElementById('selectAllBtn').addEventListener('click', () => {
        document.querySelectorAll('.category-list input[type="checkbox"]').forEach(cb => {
            cb.checked = true;
        });
        const selected = getSelectedCategories();
        filterMarkers(selected);
    });
    
    document.getElementById('clearAllBtn').addEventListener('click', () => {
        document.querySelectorAll('.category-list input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });
        const selected = getSelectedCategories();
        filterMarkers(selected);
    });
}

export function getSelectedCategories() {
    return Array.from(
        document.querySelectorAll('.category-list input[type="checkbox"]:checked')
    ).map(cb => cb.dataset.category);
}

// --- Expose for legacy compatibility ---
// Assign module-scoped variables to window so index.html can still access them
window.stores = stores;
window.markers = markers;
window.categories = categories;

// --- Default export ---
export default { initMap, loadStoreData, createMarkers, filterMarkers, updateStoreCount, setupFilterPanel, getSelectedCategories };