// Función para mostrar la animación de carga
function showLoader() {
    document.getElementById("loader").style.display = "block";
}

// Evento para mostrar la animación de carga cuando se envía el formulario
document.getElementById("loginForm").addEventListener("submit", function() {
    showLoader();
});