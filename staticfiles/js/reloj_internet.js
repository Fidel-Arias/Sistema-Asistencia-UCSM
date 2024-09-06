document.addEventListener("DOMContentLoaded", () => {
    const statusNetwork = document.getElementById('status-network');
    setInterval(() => {
        statusNetwork.className = navigator.onLine ? 'connect-network' : 'disconnect-network'
        document.getElementById('status').textContent = navigator.onLine? 'Conectado' : 'Desconectado';
    }, 250);

    setInterval(iniciarReloj,1000);
});

function iniciarReloj() {
    const reloj = document.getElementById('reloj');

    const horaActual = new Date();
    var horas = horaActual.getHours();
    var minutos = horaActual.getMinutes();
    let periodo = 'AM';

    if (horas >= 12)
        periodo = 'PM';
    else 
        periodo = 'AM';
    minutos = (minutos < 10) ? '0' + minutos : minutos;
    horas = (horas < 10) ? '0' + horas : horas
    
    reloj.textContent = `${horas}:${minutos} ${periodo}`; 

}