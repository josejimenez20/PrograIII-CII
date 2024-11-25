alertify.set('notifier', 'position', 'top-right');  // Ubicación de las notificaciones en la pantalla
alertify.defaults.delay = 5;  // Duración de las notificaciones (en segundos)

// Función para mostrar notificaciones de éxito, error o advertencia
function showNotification(type, message) {
    if (type === 'success') {
        alertify.success(message);  // Notificación de éxito
    } else if (type === 'error') {
        alertify.error(message);  // Notificación de error
    } else if (type === 'warning') {
        alertify.warning(message);  // Notificación de advertencia
    }
}

