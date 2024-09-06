document.addEventListener('DOMContentLoaded', () => {
    const nombresAdmin = document.getElementById('nombreInput'),
        apellidosAdmin = document.getElementById('apellidoInput'),
        correoAdmin = document.getElementById('correoInput'),
        contrasenaAdmin = document.getElementById('contrasenaInput'),
        nombreCongreso = document.getElementById('nombreCongreso'),
        asistencia = document.getElementById('asistencias'),
        fechaInicioCongreso = document.getElementById('inicioCongreso'),
        fechaFinCongreso = document.getElementById('finCongreso'),
        csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
        messageSuccessOrFailed = document.querySelector('.message.alert-failed'),
        messageAlert = document.querySelector('.alert-error'),
        messageAlertCongreso = document.querySelector('.alert-error-congreso'),
        formularioAdmin = document.getElementById('formulario-admin'),
        formularioCongreso = document.getElementById('formulario'),
        containerRegister = document.querySelector('.container'),
        containerRegisterCongreso = document.querySelector('.container-congreso'),
        buttonSiguiente = document.querySelector('.submit-btn'),
        buttonAnterior = document.querySelector('.back-btn');

    // Botón siguiente para mover al segundo formulario
    buttonSiguiente.addEventListener('click', function () {
        if (nombresAdmin.value && apellidosAdmin.value && correoAdmin.value && contrasenaAdmin.value) {
            if ((!validarDominiosDeCorreo(correoAdmin.value)) || (!validarContenidoDeCorreo(nombresAdmin.value, apellidosAdmin.value.toLowerCase(), correoAdmin.value))) {
                mostrarAlerta(messageAlert, 'Ingresa un correo válido');
            } else {
                // Si todo está bien, pasa al siguiente formulario (no toca las animaciones aquí)
                containerRegister.classList.add('hide-izquierda');
                containerRegisterCongreso.classList.remove('hide-derecha');
            }
        } else {
            mostrarAlerta(messageAlert, 'Ingrese todos los campos');
        }
    });

    // Botón anterior para regresar al primer formulario
    buttonAnterior.addEventListener('click', function () {
        containerRegisterCongreso.classList.add('hide-derecha');
        containerRegister.classList.remove('hide-izquierda');
    });

    // Manejo de la acción del formulario de congreso
    formularioCongreso.addEventListener('submit', function (event) {
        event.preventDefault();
        if (nombreCongreso.value && asistencia.value && fechaInicioCongreso.value && fechaFinCongreso.value) {
            if (fechaFinCongreso.value < fechaInicioCongreso.value){
                mostrarAlerta(messageAlertCongreso, 'Ingrese las fechas correctamente');
                return;
            } else {
                // Crear el objeto datosFormulario con los datos del formulario
                const datosFormulario = {
                    nombres: nombresAdmin.value,
                    apellidos: apellidosAdmin.value,
                    correo: correoAdmin.value,
                    contrasenia: contrasenaAdmin.value,
                    nombreCongreso: nombreCongreso.value,
                    asistencia: asistencia.value,
                    fechaInicioCongreso: fechaInicioCongreso.value,
                    fechaFinCongreso: fechaFinCongreso.value
                };

                containerRegisterCongreso.classList.remove('hide-derecha');
                containerRegister.classList.add('hide-izquierda');

                // Deshabilitar el botón de registro y anterior para evitar múltiples envíos
                event.target.querySelector('button[type="submit"]').disabled = true;
                event.target.querySelector('button[type="submit"]').style.backgroundColor = '#979797';
                event.target.querySelector('button[type="submit"]').style.cursor = 'not-allowed';

                document.querySelector('.back-btn').disabled = true;
                document.querySelector('.back-btn').style.backgroundColor = '#979797';
                document.querySelector('.back-btn').style.cursor = 'not-allowed';

                // Enviar los datos del formulario
                enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario, formularioAdmin, formularioCongreso);
            }
            
        } else {
            mostrarAlerta(messageAlertCongreso, 'Ingrese todos los campos');
        }
    });
});

function mostrarAlerta(messageAlert, message) {
    messageAlert.textContent = message;
    messageAlert.classList.add('mostrar');
    setTimeout(() => {
        messageAlert.classList.remove('mostrar');
    }, 3000);
}

function validarDominiosDeCorreo(correoAdmin) {
    const prefixEmail = ['@ucsm.edu.pe'];
    return prefixEmail.some(dominio => correoAdmin.includes(dominio));
}

function validarContenidoDeCorreo(nombre, apellido, correo) {
    // Normalizar datos
    nombre = nombre.toLowerCase().trim();
    apellido = apellido.toLowerCase().trim();
    correo = correo.toLowerCase().trim();
  
    // Dividir nombre y apellido en un arreglo
    const nombres = nombre.split(' ');
    const apellidos = apellido.split(' ');
  
    // Buscar coincidencias más flexibles (ejemplo con expresiones regulares)
    const regex = new RegExp(`\\b(${nombres.join('|')}|${apellidos.join('|')})\\b`, 'gi');
    return regex.test(correo);
  }

// Función para enviar los datos del formulario al backend
function enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario, formularioAdmin, formularioCongreso) {
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            formulario: datosFormulario
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Si Django retorna un success, ejecutar la animación
            messageSuccessOrFailed.textContent = 'Se ha enviado un correo al área administrativa';
            messageSuccessOrFailed.classList.remove('alert-failed');
            messageSuccessOrFailed.classList.add('alert-success');
            messageSuccessOrFailed.classList.remove('top');
            messageSuccessOrFailed.classList.add('bottom');
            setTimeout(() => {
                messageSuccessOrFailed.classList.remove('bottom');
                messageSuccessOrFailed.classList.add('top');
            }, 2000);

            // Aquí es donde puedes agregar la animación de vuelta al primer formulario
            document.querySelector('.container-congreso').classList.add('hide-derecha');
            document.querySelector('.container').classList.remove('hide-izquierda');

        } else if (data.status === 'failed'){
            messageSuccessOrFailed.textContent = data.message;
            messageSuccessOrFailed.classList.add('alert-failed');
            messageSuccessOrFailed.classList.remove('alert-success');
            messageSuccessOrFailed.classList.remove('top');
            messageSuccessOrFailed.classList.add('bottom');
            setTimeout(() => {
                messageSuccessOrFailed.classList.remove('bottom');
                messageSuccessOrFailed.classList.add('top');
            }, 2000);

            // Aquí es donde puedes agregar la animación de vuelta al primer formulario
            document.querySelector('.container-congreso').classList.add('hide-derecha');
            document.querySelector('.container').classList.remove('hide-izquierda');
        }
        // Limpiar los formularios después de enviar los datos
        formularioCongreso.reset();
        formularioAdmin.reset();
    })
    .catch(error => {
        messageSuccessOrFailed.textContent = 'Error al recibir los datos del formulario';
        messageSuccessOrFailed.classList.remove('alert-success');
        messageSuccessOrFailed.classList.add('alert-failed');
        messageSuccessOrFailed.classList.remove('top');
        messageSuccessOrFailed.classList.add('bottom');
        setTimeout(() => {
            messageSuccessOrFailed.classList.remove('bottom');
            messageSuccessOrFailed.classList.add('top');
        }, 2000);

        // También puedes manejar aquí la animación de error
        document.querySelector('.container-congreso').classList.add('hide-derecha');
        document.querySelector('.container').classList.remove('hide-izquierda');

        formularioCongreso.reset();
        formularioAdmin.reset();
    })
    .finally(() => {
        // Habilitar el botón nuevamente de Registrar
        document.querySelector('button[type="submit"]').disabled = false;
        document.querySelector('button[type="submit"]').style.cursor = 'pointer';
        document.querySelector('button[type="submit"]').style.backgroundColor = '#1d99ff';
        
        // Habilitar el botón nuevamente de Anterior
        document.querySelector('.buttons .back-btn').disabled = false;
        document.querySelector('.buttons .back-btn').style.cursor = 'pointer';
        document.querySelector('.buttons .back-btn').style.backgroundColor = '#2ed254';
        
    });   
}
