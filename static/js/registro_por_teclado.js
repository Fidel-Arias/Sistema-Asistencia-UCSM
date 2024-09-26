const btnRegisterManual = document.getElementById('btnManualRegister');
const btnRegresarScanner = document.getElementById('btnRegresarScanner');
const formRegisterManual = document.getElementById('registroManualParticipante');
const urlRegisterManual = formRegisterManual.getAttribute('data-url');

//FUNCIONES
// Función para mostrar el mensaje de resultado del escaneo
function mostrarMensaje(titulo, contenido, color, imgUrl) {
    const fondoBorroso = document.querySelector('.fondo-borroso');
    fondoBorroso.classList.remove('fondo-borroso__no-mostrar');
    document.getElementById('logo_message').setAttribute('src', imgUrl);
    document.querySelector('.success-message__title').innerHTML = titulo;
    document.querySelector('.success-message__title').style.color = color;
    document.querySelector('.success-message__content h4').innerHTML = `<b>${contenido}</b>`;
    mensajeFondo.forEach((elemento) => {
        elemento.style.display = 'block';
    });

    setTimeout(() => {
        mensajeFondo.forEach((elemento) => {
            elemento.style.display = 'none';
        });
        fondoBorroso.classList.add('fondo-borroso__no-mostrar');
    }, 900);
}

// CREACION DE EVENTOS PARA EL FORMULARIO Y EL REGISTRO MANUAL
btnRegisterManual.addEventListener('click', () => {
    const main_Scanner = document.querySelector('.main_scanner');
    const main_register_manual = document.querySelector('.main_register_manual');
    main_Scanner.classList.add('main_scanner-no-mostrar');
    main_register_manual.classList.remove('main_register_manual-no-mostrar');
});

btnRegresarScanner.addEventListener('click', () => {
    const dni_manual = document.querySelector('[name=dni_manual]');
    dni_manual.value = '';
    const main_Scanner = document.querySelector('.main_scanner');
    const main_register_manual = document.querySelector('.main_register_manual');
    main_register_manual.classList.add('main_register_manual-no-mostrar');
    main_Scanner.classList.remove('main_scanner-no-mostrar');
});

formRegisterManual.addEventListener('submit', (event) => {
    event.preventDefault();
    const dni_manual = document.querySelector('[name=dni_manual]').value;
    const bloque = document.getElementById('inlineFormCustomSelect').value;
    if ( bloque ) {
        fetch(urlRegisterManual, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                dni: dni_manual,
                bloque: bloque
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                mostrarMensaje(data.title, data.message, 'green', successImgUrl);
            } else {
                mostrarMensaje(data.title, data.message, 'red', warningImgUrl);
            }
            formRegisterManual.reset();
            const main_Scanner = document.querySelector('.main_scanner');
            const main_register_manual = document.querySelector('.main_register_manual');
            main_register_manual.classList.add('main_register_manual-no-mostrar');
            main_Scanner.classList.remove('main_scanner-no-mostrar');
        })
        .catch(err => {
            console.error('Error:', err);
            mostrarMensaje('Error', 'Error al intentar registrar', 'red', warningImgUrl);
            formRegisterManual.reset();
        })
    } else {
        mostrarMensaje('Espere', 'Selecciona un bloque', 'red', warningImgUrl);
    }
});