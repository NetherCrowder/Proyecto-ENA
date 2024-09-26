function fetchHistoricalData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            // Invertir el orden de los datos para que estén en orden cronológico
            data.reverse();

            //updatePlots(data);
            //updateMap(data);

            // Visualizar los datos en la consola
            console.log('Datos históricos:', data);

            // Visualizar los datos en un contenedor HTML
            const resultContainer = document.getElementById('result');
            resultContainer.innerHTML = JSON.stringify(data, null, 2);

            // Añadir funcionalidad para consultar por posición
            const positionInput = document.getElementById('positionInput');
            const positionButton = document.getElementById('positionButton');
            positionButton.addEventListener('click', () => {
                const position = parseInt(positionInput.value, 10);
                if (position >= 0 && position < data.length) {
                    const selectedData = data[position];
                    console.log('Datos en la posición', position, ':', selectedData);
                    alert(`Datos en la posición ${position}: ${JSON.stringify(selectedData, null, 2)}`);
                } else {
                    alert('Posición inválida');
                }
            });
        })
        .catch(error => console.error('Error al obtener datos históricos:', error));
}

// ... código existente ...
document.addEventListener('DOMContentLoaded', function() {
    fetchHistoricalData();
});