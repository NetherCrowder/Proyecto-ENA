document.addEventListener("DOMContentLoaded", function() {
    function fetchGetGPS() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                // Invertir el orden de los datos para que estén en orden cronológico
                data.reverse();

                updateMap(data);
            })
            .catch(error => console.error('Error al obtener datos históricos:', error));
    }
    
    // Inicialización del mapa
    var map = L.map('map').setView([6.2442, -75.5812], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    var polyline = L.polyline([], {color: 'red'}).addTo(map);

    function updateMap(data) {
        const gpsData = data.map(item => [item.gps.latitud, item.gps.longitud]);
        
        // Agregar el nuevo punto al polígono
        if (gpsData.length > 0) {
            const lastPoint = gpsData[gpsData.length - 1];
            polyline.addLatLng(lastPoint);
        }

        // Ajustar el mapa a los límites de la polilínea
        map.fitBounds(polyline.getBounds());
    }

    fetchGetGPS();
    setInterval(fetchGetGPS, 1000);
});