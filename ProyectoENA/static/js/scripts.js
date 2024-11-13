// Crime Categories Chart
const crimeCtx = document.getElementById('crimeChart').getContext('2d');
const crimeChart = new Chart(crimeCtx, {
    type: 'pie',
    data: {
        labels: ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden'],
        datasets: [{
            data: [7166, 11396, 9511, 9656, 11219, 8706],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
        }]
    }
});

// Age Distribution Chart
const ageCtx = document.getElementById('ageChart').getContext('2d');
const ageChart = new Chart(ageCtx, {
    type: 'boxplot',
    data: {
        labels: ['Aisle', 'Bathroom', 'Recreation room', 'Hospital room'],
        datasets: [{
            label: 'Age',
            data: [[20, 30, 40, 50], [25, 35, 45, 55], [22, 32, 42, 52], [28, 38, 48, 58]],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
        }]
    }
});

// Titanic Survival Chart
const titanicCtx = document.getElementById('titanicChart').getContext('2d');
const titanicChart = new Chart(titanicCtx, {
    type: 'doughnut',
    data: {
        labels: ['Yes', 'No'],
        datasets: [{
            data: [32, 68],
            backgroundColor: ['#4BC0C0', '#FF6384']
        }]
    }
});

// Density Plot of Total Bill
const billCtx = document.getElementById('billChart').getContext('2d');
const billChart = new Chart(billCtx, {
    type: 'line',
    data: {
        labels: [10, 20, 30, 40, 50, 60],
        datasets: [{
            label: 'Density',
            data: [0.12, 0.08, 0.05, 0.03, 0.01, 0.008],
            backgroundColor: '#36A2EB',
            fill: true
        }]
    }
});