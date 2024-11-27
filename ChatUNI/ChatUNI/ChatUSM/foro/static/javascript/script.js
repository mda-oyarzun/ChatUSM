function toggleRespuesta(comentarioId) {
    var form = document.getElementById('respuesta-form-' + comentarioId);
    var button = document.getElementById('btn-responder-' + comentarioId);
    
    if (form.style.display === "none") {
        form.style.display = "block";
        button.textContent = "Cancelar";
    } else {
        form.style.display = "none";
        button.textContent = "Responder";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const specificUrlPattern = /^\/categorias\/[^\/]+\/\d+\/$/;

    window.onbeforeunload = function() {
        if (specificUrlPattern.test(window.location.pathname)) {
            localStorage.setItem('scrollPosition', window.scrollY);
            console.log("Scroll Position Saved:", window.scrollY);
        }
    };

    window.onload = function() {
        if (specificUrlPattern.test(window.location.pathname)) {
            const scrollPosition = localStorage.getItem('scrollPosition');
            console.log("Scroll Position Retrieved:", scrollPosition);
            if (scrollPosition) {
                window.scrollTo(0, scrollPosition);
                localStorage.removeItem('scrollPosition'); // Opcional: eliminar la posición guardada
            }
        }
    };
});