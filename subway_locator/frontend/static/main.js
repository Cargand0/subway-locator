document.addEventListener('DOMContentLoaded', function() {
    // Initialize map centered on Kuala Lumpur
    const map = L.map('map').setView([3.1390, 101.6869], 12);
    
    // Add OpenStreetMap layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Store all outlet markers and circles
    const markers = [];
    const circles = [];
    const overlappingCircles = [];
    
    // Fetch outlets with coordinates from the API
    fetch('/api/outlets?geocoded_only=true')
        .then(response => response.json())
        .then(outlets => {
            // Add markers for each outlet
            outlets.forEach(outlet => {
                addOutletToMap(outlet);
            });
            
            // Calculate and display overlapping areas
            calculateOverlaps();
        })
        .catch(error => {
            console.error('Error fetching outlets:', error);
            document.getElementById('outlet-info').innerHTML = 
                '<p class="error">Failed to load outlets. Please try again later.</p>';
        });
    
    // Function to add an outlet to the map
    function addOutletToMap(outlet) {
        // Create marker
        const marker = L.marker([outlet.latitude, outlet.longitude])
            .addTo(map)
            .bindPopup(createPopupContent(outlet));
        
        markers.push(marker);
        
        // Create 5KM radius circle
        const circle = L.circle([outlet.latitude, outlet.longitude], {
            color: '#009959',
            fillColor: '#009959',
            fillOpacity: 0.2,
            radius: 5000 // 5KM in meters
        }).addTo(map);
        
        circle.outlet = outlet;
        circles.push(circle);
        
        // Add click handler to show outlet info
        marker.on('click', function() {
            showOutletInfo(outlet);
        });
    }
    
    // Function to create popup content
    function createPopupContent(outlet) {
        let content = `<strong>${outlet.name}</strong>`;
        
        if (outlet.address) {
            content += `<br><span>${outlet.address}</span>`;
        }
        
        if (outlet.operating_hours) {
            content += `<br><span>Hours: ${outlet.operating_hours}</span>`;
        }
        
        if (outlet.waze_link) {
            content += `<br><a href="${outlet.waze_link}" target="_blank">Navigate with Waze</a>`;
        }
        
        return content;
    }
    
    // Function to show outlet info in the panel
    function showOutletInfo(outlet) {
        let content = `<h3>${outlet.name}</h3>`;
        
        if (outlet.address) {
            content += `<p><strong>Address:</strong> ${outlet.address}</p>`;
        }
        
        if (outlet.operating_hours) {
            content += `<p><strong>Operating Hours:</strong> ${outlet.operating_hours}</p>`;
        }
        
        if (outlet.waze_link) {
            content += `<p><a href="${outlet.waze_link}" target="_blank">Navigate with Waze</a></p>`;
        }
        
        content += `<p><strong>Coordinates:</strong> ${outlet.latitude}, ${outlet.longitude}</p>`;
        
        document.getElementById('outlet-info').innerHTML = content;
    }
    
    // Function to calculate overlapping circles
    function calculateOverlaps() {
        // Clear previous overlapping circles
        overlappingCircles.forEach(circle => map.removeLayer(circle));
        overlappingCircles.length = 0;
        
        // Check each pair of circles for overlap
        for (let i = 0; i < circles.length; i++) {
            for (let j = i + 1; j < circles.length; j++) {
                const circle1 = circles[i];
                const circle2 = circles[j];
                
                // Calculate distance between circles
                const latlng1 = circle1.getLatLng();
                const latlng2 = circle2.getLatLng();
                const distance = latlng1.distanceTo(latlng2);
                
                // If distance is less than sum of radii, circles overlap
                if (distance < circle1.getRadius() + circle2.getRadius()) {
                    // Highlight the first circle that overlaps
                    highlightOverlappingOutlets(circle1.outlet, circle2.outlet);
                }
            }
        }
    }
    
    // Function to highlight overlapping outlets
    function highlightOverlappingOutlets(outlet1, outlet2) {
        // For each overlapping pair, we create a new circle in the center of the first outlet
        // with a different color to indicate overlap
        const overlappingCircle = L.circle([outlet1.latitude, outlet1.longitude], {
            color: '#ffcb00',
            fillColor: '#ffcb00',
            fillOpacity: 0.3,
            radius: 5000 // 5KM in meters
        }).addTo(map);
        
        overlappingCircles.push(overlappingCircle);
        
        // Add click handler to show both outlets
        overlappingCircle.on('click', function() {
            const content = `
                <h3>Overlapping Catchment Areas</h3>
                <p>This area is covered by multiple Subway outlets:</p>
                <ul>
                    <li>${outlet1.name}</li>
                    <li>${outlet2.name}</li>
                </ul>
            `;
            
            document.getElementById('outlet-info').innerHTML = content;
        });
    }
    
    // Handle search functionality
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    
    searchButton.addEventListener('click', function() {
        performSearch();
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    function performSearch() {
        const query = searchInput.value.trim();
        
        if (!query) return;
        
        // Check if it's a special query
        if (query.toLowerCase().includes('latest closing') || 
            query.toLowerCase().includes('close late')) {
            // Find outlets that close the latest
            fetch(`${API_BASE_URL}/outlets/latest-closing`)
                .then(response => response.json())
                .then(outlets => {
                    showSearchResults('Outlets that close the latest', outlets);
                })
                .catch(error => {
                    console.error('Error searching outlets:', error);
                });
        } else if (query.toLowerCase().includes('how many') || 
                  query.toLowerCase().includes('outlets in')) {
            // Extract location from query
            const locationMatch = query.match(/in\s+([a-zA-Z\s]+)$/i);
            
            if (locationMatch && locationMatch[1]) {
                const location = locationMatch[1].trim();
                
                fetch(`/api/location/${location}`)
                    .then(response => response.json())
                    .then(data => {
                        const count = data.count;
                        const outlets = data.outlets;
                        
                        showSearchResults(
                            `Found ${count} outlets in ${location}`, 
                            outlets
                        );
                    })
                    .catch(error => {
                        console.error('Error searching outlets by location:', error);
                    });
            }
        } else {
            // Regular search
            fetch(`/api/search/${query}`)
                .then(response => response.json())
                .then(outlets => {
                    showSearchResults(`Search results for "${query}"`, outlets);
                })
                .catch(error => {
                    console.error('Error searching outlets:', error);
                });
        }
    }
    
    function showSearchResults(title, outlets) {
        let content = `<h3>${title}</h3>`;
        
        if (outlets.length === 0) {
            content += '<p>No outlets found.</p>';
        } else {
            content += '<ul class="outlet-list">';
            
            outlets.forEach(outlet => {
                content += `
                    <li class="outlet-item" data-id="${outlet.id}">
                        <strong>${outlet.name}</strong>
                        ${outlet.operating_hours ? `<br>Hours: ${outlet.operating_hours}` : ''}
                    </li>
                `;
                
                // If outlet has coordinates, pan the map to it
                if (outlet.latitude && outlet.longitude) {
                    // Find the marker for this outlet
                    const marker = markers.find(m => 
                        m.getLatLng().lat === outlet.latitude && 
                        m.getLatLng().lng === outlet.longitude
                    );
                    
                    if (marker) {
                        map.panTo(marker.getLatLng());
                        marker.openPopup();
                    }
                }
            });
            
            content += '</ul>';
        }
        
        document.getElementById('outlet-info').innerHTML = content;
        
        // Add click handlers to outlet list items
        document.querySelectorAll('.outlet-item').forEach(item => {
            item.addEventListener('click', function() {
                const outletId = this.getAttribute('data-id');
                
                fetch(`${API_BASE_URL}/outlets/${outletId}`)
                    .then(response => response.json())
                    .then(outlet => {
                        showOutletInfo(outlet);
                        
                        // Pan map to outlet if it has coordinates
                        if (outlet.latitude && outlet.longitude) {
                            map.panTo([outlet.latitude, outlet.longitude]);
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching outlet details:', error);
                    });
            });
        });
    }
});