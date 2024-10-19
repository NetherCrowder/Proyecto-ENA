document.addEventListener("DOMContentLoaded", function() {
    function fetchGetGPS() {
        fetch('GetData')  // Asegúrate de que esta URL coincide con tu ruta en Django
            .then(response => response.json())
            .then(data => {
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
        console.log('Datos recibidos:', data);
    
        if (!map) {
            console.error('El mapa no está inicializado.');
            return;
        }
    
        if (data && data.gps && typeof data.gps.latitud === 'number' && typeof data.gps.longitud === 'number') {
            const gpsData = [data.gps.latitud, data.gps.longitud];
            console.log('Coordenadas GPS:', gpsData);
    
            var ruido = data.ruido;
            var color = getColor(ruido);
            console.log('Color obtenido:', color);
    
            // Agregar el nuevo punto como un marcador circular
            const marker = L.circleMarker(gpsData, {color: color, radius: 10}).addTo(map);
            markers.push(marker);
            console.log('Marcadores actuales:', markers);
    
            // Ajustar el mapa a los límites de los marcadores
            if (markers.length > 0) {
                const group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds());
            }
        } else {
            console.error('Datos GPS inválidos:', data);
        }
    }

    fetchGetGPS();
    setInterval(fetchGetGPS, 10000);
});