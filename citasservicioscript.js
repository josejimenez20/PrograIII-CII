function toggleContent(card) {
    const content = card.querySelector('.tip-info'); // Busca el contenido de la clase .tip-info
    if (content.style.display === "none" || content.style.display === "") {
        content.style.display = "block"; // Muestra el contenido
    } else {
        content.style.display = "none"; // Oculta el contenido
    }
}
