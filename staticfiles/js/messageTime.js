// Ocultar el mensaje después de 3 segundos
setTimeout(function() {
    var messages = document.querySelectorAll('.message');
    var mainContent = document.getElementById('main');

    messages.forEach(msg => {
        msg.style.display = 'none';   
    });

    if (mainContent)
        mainContent.style.gap = '2em';
}, 3000); // 3000 milisegundos = 3 segundos