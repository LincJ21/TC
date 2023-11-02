$(document).ready(function() {
    $('#searchForm').submit(function(e) {
        e.preventDefault();
        var query = $('#searchInput').val().toLowerCase();
        
        // Define los términos de búsqueda y sus respectivas páginas de destino
        var searchTerms = {
            "servicios": "/servicios",
            "home": "/",
            "listacompras": "/listacompras",
            "about": "/about",
            // Agrega más términos de búsqueda y páginas aquí
        };

        // Comprueba si el término de búsqueda coincide con alguna entrada en searchTerms
        if (query in searchTerms) {
            window.location.href = searchTerms[query];
        } else {
            // Redirige a una página de resultados de búsqueda si no hay coincidencia
            window.location.href = "/resultados.html?q=" + encodeURIComponent(query);
        }
    });
});
