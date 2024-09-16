const form = document.querySelector('#form');
const url = form.getAttribute('data-url');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const mensajeFondo = document.querySelectorAll(".mostrar-msg");
const warningImgUrl = document.querySelector('.success-message').dataset.warningImgUrl;
const successImgUrl = document.querySelector('.success-message').dataset.successImgUrl;

function mostrarFormRegister() {
    const form = document.querySelector('.form-register');
    const fondoBorroso = document.querySelector('.fondo-borroso');
    fondoBorroso.classList.remove('fondo-borroso__no-mostrar');
    form.classList.remove('form-register__no-mostrar');
}

function salirFormRegister() {
    const form = document.querySelector('.form-register');
    const fondoBorroso = document.querySelector('.fondo-borroso');
    form.classList.add('form-register__no-mostrar');
    fondoBorroso.classList.add('fondo-borroso__no-mostrar');
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const dni = document.querySelector('[name=dni]').value;
    const nombres = document.querySelector('[name=nombres]').value;
    const ap_paterno = document.querySelector('[name=ap_paterno]').value;
    const ap_materno = document.querySelector('[name=ap_materno]').value;
    const bloque = document.querySelector('[name=bloque_register]').value;
    
    salirFormRegister();
    // Enviar formulario al backend
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            dni: dni,
            nombres: nombres,
            ap_paterno: ap_paterno,
            ap_materno: ap_materno,
            bloque: bloque
        })
    })
    .then(response => response.json())
    .then(data => {
        mensajeFondo.forEach((elemento) => {
            elemento.style.display = 'block';
        });

        if (data.status === 'success'){
            document.getElementById('logo_message').setAttribute('src', successImgUrl);
            document.querySelector('.success-message__title').innerHTML = 'Asistencia marcada';
            document.querySelector('.success-message__title').style.color = 'green';
            document.querySelector('.success-message__content h4').innerHTML = '<b>'+data['message']+'</b>';
        } else if (data.status === 'error') {
            document.getElementById('logo_message').setAttribute('src', warningImgUrl);
            document.querySelector('.success-message__title').innerHTML = 'Error';
            document.querySelector('.success-message__title').style.color ='red';
            document.querySelector('.success-message__content h4').innerHTML = '<b>'+data['message']+'</b>';
        }

        setTimeout(() => {
            mensajeFondo.forEach((elemento) => {
                elemento.style.display = 'none';
            });
        }, 3000);

        form.reset();

    })
});