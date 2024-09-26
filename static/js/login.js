document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Simular login correcto (Por ahora sin validación real)
    if (username && password) {
        window.location.href = "monitoreoVariables";
    } else {
        alert("Por favor ingrese un usuario y contraseña válidos.");
    }
});