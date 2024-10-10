document.addEventListener("DOMContentLoaded", function() {
    function fetchGetGPS() {
        fetch('GetData')
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
    var markers = [];

    function getColor(d) {
        return d >= 80 ? '#000078' :
               d >= 75  ? '#00c5ff' :
               d >= 70  ? '#ff00ff' :
               d >= 65  ? '#ff1111' :
               d >= 60  ? '#ff7777' :
               d >= 55   ? '#ffaa00' :
               d >= 50   ? '#ffcd69' :
               d >= 45   ? '#ffff02' :
               d >= 40   ? '#007800' :
               d >= 35    ? '#c3ff86' :
                          'transparent';
    }

    function updateMap(data) {
        const gpsData = data.map(item => [item.gps.latitud, item.gps.longitud]);
        var ruido = data.map(item => item.ruido);
        
        // Agregar el nuevo punto como un marcador circular
        if (gpsData.length > 0) {
            const lastPoint = gpsData[gpsData.length - 1];
            const marker = L.circleMarker(lastPoint, {color: getColor(ruido), radius: 10}).addTo(map);
            markers.push(marker);
        }

        // Ajustar el mapa a los límites de los marcadores
        if (markers.length > 0) {
            const group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds());
        }
    }

    fetchGetGPS();
    setInterval(fetchGetGPS, 1000);
});