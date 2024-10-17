document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Realizar la solicitud de autenticación
    fetch('GetUsers/' + username + '&' + password, {  // Asegúrate de que esta ruta sea correcta
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "Variables"; // Redirigir en caso de éxito
        } else {
            return response.json().then(data => {
                alert(data.error || "Error en la autenticación.");
            });
        }
    })
    .catch(error => {
        console.error("Error en la solicitud:", error);
        alert("Error en la conexión al servidor.");
    });
});