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
    const traces = {
        magnetometro: ['x', 'y', 'z'].map(axis => ({x: [], y: [], name: axis, type: 'scatter', mode: 'lines'})),
        barometro: [{x: [], y: [], name: 'Presión', type: 'scatter', mode: 'lines'}],
        ruido: [{x: [], y: [], name: 'Nivel', type: 'scatter', mode: 'lines'}],
        giroscopio: ['x', 'y', 'z'].map(axis => ({x: [], y: [], name: axis, type: 'scatter', mode: 'lines'})),
        acelerometro: ['x', 'y', 'z'].map(axis => ({x: [], y: [], name: axis, type: 'scatter', mode: 'lines'})),
        vibracion: [{x: [], y: [], name: 'Amplitud', type: 'scatter', mode: 'lines'}]
    };

    Object.keys(layouts).forEach(sensor => {
        Plotly.newPlot(sensor, traces[sensor], layouts[sensor]);
    });

    // Inicialización del mapa
    var map = L.map('map').setView([6.2442, -75.5812], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    var marker = L.marker([6.2442, -75.5812]).addTo(map);
    var polyline = L.polyline([], {color: 'red'}).addTo(map);

    // Función para obtener datos y actualizar gráficos y mapa
    function fetchDataAndUpdate() {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                const latestData = data[data.length - 1];
                const time = new Date(latestData.timestamp);

                updatePlot('magnetometro', time, latestData.magnetometro);
                updatePlot('barometro', time, {value: latestData.barometro});
                updatePlot('ruido', time, {value: latestData.ruido});
                updatePlot('giroscopio', time, latestData.giroscopio);
                updatePlot('acelerometro', time, latestData.acelerometro);
                updatePlot('vibracion', time, {value: latestData.vibracion});

                updateMap(latestData);
            });
    }

    function updatePlot(sensorName, time, values) {
        const update = {
            x: traces[sensorName].map(() => [time]),
            y: Object.values(values).map(v => [v])
        };
        Plotly.extendTraces(sensorName, update, [...Array(traces[sensorName].length).keys()]);
    }

    function updateMap(data) {
        const latlng = [data.gps.latitud, data.gps.longitud];
        marker.setLatLng(latlng);
        polyline.addLatLng(latlng);
        map.panTo(latlng);

        // Actualizar el popup del marcador con los datos de los sensores
        const popupContent = `
            <b>Tiempo:</b> ${new Date(data.timestamp).toLocaleString()}<br>
            <b>Magnetómetro:</b> x: ${data.magnetometro.x.toFixed(2)}, y: ${data.magnetometro.y.toFixed(2)}, z: ${data.magnetometro.z.toFixed(2)}<br>
            <b>Barómetro:</b> ${data.barometro.toFixed(2)} hPa<br>
            <b>Ruido:</b> ${data.ruido.toFixed(2)} dB<br>
            <b>Giroscopio:</b> x: ${data.giroscopio.x.toFixed(2)}, y: ${data.giroscopio.y.toFixed(2)}, z: ${data.giroscopio.z.toFixed(2)}<br>
            <b>Acelerómetro:</b> x: ${data.acelerometro.x.toFixed(2)}, y: ${data.acelerometro.y.toFixed(2)}, z: ${data.acelerometro.z.toFixed(2)}<br>
            <b>Vibración:</b> ${data.vibracion.toFixed(2)}
        `;
        marker.bindPopup(popupContent).openPopup();
    }

    // Actualizar gráficos y mapa cada segundo
    setInterval(fetchDataAndUpdate, 1000);

    // Función para obtener datos históricos
    function fetchHistoricalData() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                // Invertir el orden de los datos para que estén en orden cronológico
                data.reverse();

                // Preparar los datos para cada gráfica
                const plotData = {
                    magnetometro: { x: [], y: [], z: [] },
                    barometro: { values: [] },
                    ruido: { values: [] },
                    giroscopio: { x: [], y: [], z: [] },
                    acelerometro: { x: [], y: [], z: [] },
                    vibracion: { values: [] }
                };

                const timestamps = [];

                data.forEach(item => {
                    timestamps.push(new Date(item.timestamp));
                    
                    plotData.magnetometro.x.push(item.magnetometro.x);
                    plotData.magnetometro.y.push(item.magnetometro.y);
                    plotData.magnetometro.z.push(item.magnetometro.z);
                    
                    plotData.barometro.values.push(item.barometro);
                    plotData.ruido.values.push(item.ruido);
                    
                    plotData.giroscopio.x.push(item.giroscopio.x);
                    plotData.giroscopio.y.push(item.giroscopio.y);
                    plotData.giroscopio.z.push(item.giroscopio.z);
                    
                    plotData.acelerometro.x.push(item.acelerometro.x);
                    plotData.acelerometro.y.push(item.acelerometro.y);
                    plotData.acelerometro.z.push(item.acelerometro.z);
                    
                    plotData.vibracion.values.push(item.vibracion);
                });

                // Actualizar cada gráfica con los datos históricos
                updateHistoricalPlot('magnetometro', timestamps, plotData.magnetometro);
                updateHistoricalPlot('barometro', timestamps, plotData.barometro);
                updateHistoricalPlot('ruido', timestamps, plotData.ruido);
                updateHistoricalPlot('giroscopio', timestamps, plotData.giroscopio);
                updateHistoricalPlot('acelerometro', timestamps, plotData.acelerometro);
                updateHistoricalPlot('vibracion', timestamps, plotData.vibracion);

                // Actualizar el mapa con la última posición GPS
                const lastPosition = data[data.length - 1].gps;
                updateMapWithHistoricalData(data);
            })
            .catch(error => console.error('Error al obtener datos históricos:', error));
    }

    function updateHistoricalPlot(sensorName, timestamps, values) {
        const update = {
            x: [timestamps, timestamps, timestamps],
            y: [values.x || values.values, values.y, values.z]
        };

        const traceIndices = Object.keys(values).map((_, i) => i);
        Plotly.update(sensorName, update, {}, traceIndices);
    }

    function updateMapWithHistoricalData(data) {
        // Limpiar el polyline existente
        polyline.setLatLngs([]);

        // Añadir todos los puntos GPS al polyline
        data.forEach(item => {
            polyline.addLatLng([item.gps.latitud, item.gps.longitud]);
        });

        // Centrar el mapa en el último punto
        const lastPoint = data[data.length - 1].gps;
        map.panTo([lastPoint.latitud, lastPoint.longitud]);

        // Actualizar el marcador con la última posición
        marker.setLatLng([lastPoint.latitud, lastPoint.longitud]);

        // Actualizar el popup del marcador con los últimos datos
        const lastData = data[data.length - 1];
        const popupContent = `
            <b>Tiempo:</b> ${new Date(lastData.timestamp).toLocaleString()}<br>
            <b>Magnetómetro:</b> x: ${lastData.magnetometro.x.toFixed(2)}, y: ${lastData.magnetometro.y.toFixed(2)}, z: ${lastData.magnetometro.z.toFixed(2)}<br>
            <b>Barómetro:</b> ${lastData.barometro.toFixed(2)} hPa<br>
            <b>Ruido:</b> ${lastData.ruido.toFixed(2)} dB<br>
            <b>Giroscopio:</b> x: ${lastData.giroscopio.x.toFixed(2)}, y: ${lastData.giroscopio.y.toFixed(2)}, z: ${lastData.giroscopio.z.toFixed(2)}<br>
            <b>Acelerómetro:</b> x: ${lastData.acelerometro.x.toFixed(2)}, y: ${lastData.acelerometro.y.toFixed(2)}, z: ${lastData.acelerometro.z.toFixed(2)}<br>
            <b>Vibración:</b> ${lastData.vibracion.toFixed(2)}
        `;
        marker.bindPopup(popupContent).openPopup();
    }

    // Llamar a fetchHistoricalData cuando se carga la página
    fetchHistoricalData();
});
