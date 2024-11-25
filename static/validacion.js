function validarFormulario(event) {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    // Validar campos vacíos
    if (!email || !password) {
        alert("Por favor, complete todos los campos.");
        event.preventDefault();
        return false;
    }

    // Validar formato de correo
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Por favor, introduzca un correo válido.");
        event.preventDefault();
        return false;
    }

    // Validar que la contraseña no contenga espacios
    if (/\s/.test(password)) {
        alert("La contraseña no puede contener espacios.");
        event.preventDefault();
        return false;
    }

    return true;
}
