document.addEventListener("DOMContentLoaded", () => {
    const bloque_selected = document.getElementById('inlineFormCustomSelect');
    const statusNetwork = document.getElementById('status-network');
    setInterval(() => {
        statusNetwork.className = navigator.onLine ? 'connect-network' : 'disconnect-network'
        document.getElementById('status').textContent = navigator.onLine? 'Conectado' : 'Desconectado';
    }, 250);

    bloque_selected.addEventListener('change', ()=>{
        const opcion_escogida = bloque_selected.options[bloque_selected.selectedIndex];
        mostrarUbicacion(opcion_escogida);
    });

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

function mostrarUbicacion(bloqueSeleccionado){
    const ubicacion_actual = document.getElementById('ubicacion_actual');
    ubicacion_actual.innerHTML = bloqueSeleccionado.getAttribute('data-ubicacion');
    if (bloqueSeleccionado.value == "")
        ubicacion_actual.innerHTML = "Desconocido";
}