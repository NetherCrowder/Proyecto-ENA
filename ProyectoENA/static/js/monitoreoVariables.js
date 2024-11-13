// Gráfica 1
const ctx1 = document.getElementById('chart1').getContext('2d');
new Chart(ctx1, {
    type: 'line',
    data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
            label: 'Dataset 1',
            data: [30, 50, 40, 60, 70, 90],
            borderColor: 'rgb(255, 99, 132)',
            fill: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Gráfica 2
const ctx2 = document.getElementById('chart2').getContext('2d');
new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
            label: 'Dataset 2',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: 'rgba(54, 162, 235, 0.6)'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Gráfica 3
const ctx3 = document.getElementById('chart3').getContext('2d');
new Chart(ctx3, {
    type: 'pie',
    data: {
        labels: ['Rojo', 'Azul', 'Amarillo'],
        datasets: [{
            label: 'Dataset 3',
            data: [10, 20, 30],
            backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Gráfica 4
const ctx4 = document.getElementById('chart4').getContext('2d');
new Chart(ctx4, {
    type: 'radar',
    data: {
        labels: ['A', 'B', 'C', 'D', 'E'],
        datasets: [{
            label: 'Dataset 4',
            data: [20, 10, 40, 30, 50],
            backgroundColor: 'rgba(153, 102, 255, 0.6)'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
