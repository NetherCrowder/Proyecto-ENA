document.addEventListener("DOMContentLoaded", function() {
    // Configuraciones de layout para cada gráfica
    const layoutConfig = (title, yAxisTitle) => ({
        title: title,
        xaxis: {title: 'Tiempo'},
        yaxis: {title: yAxisTitle},
        legend: {x: 0, y: 1, traceorder: 'reversed', font: {size: 10}}
    });

    const layouts = {
        magnetometro: layoutConfig('Gráfico de Magnetómetro', 'Medidas (uT)'),
        barometro: layoutConfig('Gráfico de Barómetro', 'Presión (hPa)'),
        ruido: layoutConfig('Gráfico de Ruido', 'Nivel (dB)'),
        giroscopio: layoutConfig('Gráfico de Giroscopio', 'Velocidad angular (°/s)'),
        acelerometro: layoutConfig('Gráfico de Acelerómetro', 'Aceleración (m/s²)'),
        vibracion: layoutConfig('Gráfico de Vibración', 'Amplitud')
    };

    // Inicialización de gráficos
    Object.keys(layouts).forEach(sensor => {
        Plotly.newPlot(sensor, [], layouts[sensor]);
    });

    // Inicialización del mapa
    var map = L.map('map').setView([6.2442, -75.5812], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    var polyline = L.polyline([], {color: 'red'}).addTo(map);

    function fetchHistoricalData() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                // Invertir el orden de los datos para que estén en orden cronológico
                data.reverse();

                updatePlots(data);
                updateMap(data);
            })
            .catch(error => console.error('Error al obtener datos históricos:', error));
    }

    function updatePlots(data) {
        const sensors = ['magnetometro', 'barometro', 'ruido', 'giroscopio', 'acelerometro', 'vibracion'];
        
        sensors.forEach(sensor => {
            const plotData = {
                x: data.map(item => new Date(item.timestamp)),
                y: sensor === 'barometro' || sensor === 'ruido' || sensor === 'vibracion'
                    ? data.map(item => item[sensor])
                    : ['x', 'y', 'z'].map(axis => data.map(item => item[sensor][axis])),
                type: 'scatter',
                mode: 'lines'
            };

            if (sensor === 'barometro' || sensor === 'ruido' || sensor === 'vibracion') {
                Plotly.react(sensor, [plotData], layouts[sensor]);
            } else {
                const traces = ['x', 'y', 'z'].map((axis, i) => ({
                    x: plotData.x,
                    y: plotData.y[i],
                    name: axis,
                    type: 'scatter',
                    mode: 'lines'
                }));
                Plotly.react(sensor, traces, layouts[sensor]);
            }
        });
    }

    function updateMap(data) {
        const gpsData = data.map(item => [item.gps.latitud, item.gps.longitud]);
        polyline.setLatLngs(gpsData);
        map.fitBounds(polyline.getBounds());
    }

    // Cargar datos históricos al iniciar la página
    fetchHistoricalData();

    // Actualizar datos cada 30 segundos
    setInterval(fetchHistoricalData, 10000);
});
