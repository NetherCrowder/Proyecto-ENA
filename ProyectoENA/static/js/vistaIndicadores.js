document.addEventListener('DOMContentLoaded', function () {
    // Adaptamos layoutConfig para Chart.js
    const layoutConfig = (title, yAxisTitle) => ({
        plugins: {
            title: {
                display: true,
                text: title
            },
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 10
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Tiempo'
                }
            },
            y: {
                title: {
                    display: true,
                    text: yAxisTitle
                },
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false
    });

    // Configuración del gráfico
    var ctx1 = document.getElementById('chart1').getContext('2d');
    var chart1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Dx',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dy',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dz',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: layoutConfig('Gráfico del Magnetómetro', 'Medidas (uT)')
    });

    var ctx2 = document.getElementById('chart2').getContext('2d');
    var chart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Presión atmosférica',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: layoutConfig('Gráfico de Barómetro', 'Presión (hPa)')
    });

    var ctx3 = document.getElementById('chart3').getContext('2d');
    var chart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Decibelios',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: layoutConfig('Gráfico de Ruido', 'Nivel (dB)')
    });

    var ctx4 = document.getElementById('chart4').getContext('2d');
    var chart4 = new Chart(ctx4, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Dx',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dy',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dz',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: layoutConfig('Gráfico de Giroscopio', 'Velocidad angular (°/s)')
    });

    var ctx5 = document.getElementById('chart5').getContext('2d');
    var chart5 = new Chart(ctx5, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Dx',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dy',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Dz',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: layoutConfig('Gráfico de Acelerómetro', 'Aceleración (m/s²)')
    });

    var ctx6 = document.getElementById('chart6').getContext('2d');
    var chart6 = new Chart(ctx6, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Vibracion',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: layoutConfig('Gráfico de Vibración', 'Amplitud (mm/s)')
    });
    
    function fetchGetData() {
        fetch('GetData')
            .then(response => response.json())
            .then(data => {
                // Invertir el orden de los datos para que estén en orden cronológico
                data.reverse();

                updateCharts(data);
            })
            .catch(error => console.error('Error al obtener datos históricos:', error));
    }
    
    var i = 0

    function updateCharts(data) {
        var nuevadata = data[0];
        var maxDataPoints = 10; // Define la cantidad máxima de datos

        var charts = [chart1, chart2, chart3, chart4, chart5, chart6];
        var sensors = [
            { chart: chart1, data: nuevadata.magnetometro, keys: ['x', 'y', 'z'] },
            { chart: chart2, data: nuevadata.barometro, keys: [null] },
            { chart: chart3, data: nuevadata.ruido, keys: [null] },
            { chart: chart4, data: nuevadata.giroscopio, keys: ['x', 'y', 'z'] },
            { chart: chart5, data: nuevadata.acelerometro, keys: ['x', 'y', 'z'] },
            { chart: chart6, data: nuevadata.vibracion, keys: [null] }
        ];

        i += 1
    
        charts.forEach((chart, index) => {
            //chart.data.labels.push(nuevadata.timestamp);
            chart.data.labels.push(Math.round((i/60)*1000)/1000);
            sensors[index].keys.forEach((key, datasetIndex) => {
                if (key) {
                    chart.data.datasets[datasetIndex].data.push(sensors[index].data[key]);
                } else {
                    chart.data.datasets[datasetIndex].data.push(sensors[index].data);
                }
            });

            chart.update();
            // Eliminar el dato más antiguo si se supera el máximo de puntos de datos
            if (chart.data.labels.length == maxDataPoints) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => dataset.data.shift());
            }
        });
    }

    fetchGetData();

   setInterval(fetchGetData, 1000);
});
