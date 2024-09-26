document.addEventListener("DOMContentLoaded", () => {
    //CONSTANTES DEL HTML
    const audio = document.getElementById('audioScaner');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const bloqueSelect = document.querySelector('[name=bloque]');
    const warningImgUrl = document.querySelector('.success-message').dataset.warningImgUrl;
    const successImgUrl = document.querySelector('.success-message').dataset.successImgUrl;
    const formJson = document.getElementById('form-json');
    const url = formJson.getAttribute('data-url');
    const mensajeFondo = document.querySelectorAll(".mostrar-msg");

    //CONSTANTES y configuraciones para la camara
    const html5QrCode = new Html5Qrcode(
        "reader", {
            formatsToSupport: [Html5QrcodeSupportedFormats.QR_CODE]
        }
    );

    const config = {
        fps: 10,
        qrbox: {
            width: 250,
            height: 250
        }
    };

    // Variable para controlar el estado del escaneo
    let isScanning = false;

    const qrCodeSuccessCallBack = (decodedText, decodedResult) => {
        if (isScanning) return;  // Si ya estamos procesando un código, no hacer nada más
        isScanning = true; // Marcamos que estamos escaneando para evitar múltiples registros
        audio.play();
        console.log(decodedText);

        if (bloqueSelect.value) {
            if (!navigator.onLine) {
                mensajeFondo.forEach((elemento) => {
                    elemento.style.display = 'block';
                });

                document.getElementById('logo_message').classList.add('hidden');
                document.querySelector('.success-message__title').innerHTML = 'Sin conexión';
                document.querySelector('.success-message__title').style.color = 'red';
                document.querySelector('.success-message__content h4').innerHTML = '<b>Conéctate a una red</b>';

                mostrarAlerta(mensajeFondo);
            }
            if (decodedText) {
                document.getElementById('logo_message').classList.remove('hidden');
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        qr_code: decodedText,
                        bloque: bloqueSelect.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data['status'] === 'warning'){
                        mostrarMensaje(data.title, data.message, 'red', warningImgUrl);
                    } else if (data['status'] === 'error'){
                        mostrarMensaje(data.title, data.message, 'red', warningImgUrl);
                    } else {
                        mostrarMensaje(data.title, data.message, 'green', successImgUrl);
                    }
                })
                .catch(err => {
                    console.error('Error:', err);
                });
            }

        } else {
            mostrarMensaje('Error', 'Primero selecciona un bloque', 'red', warningImgUrl);
        }

        // Detener la cámara
        html5QrCode.stop().then(() => {
            console.log('Escaneo detenido.');
        });

        setTimeout(() => {
            isScanning = false;  // Permitir nuevos escaneos
            camaraStart(config, qrCodeSuccessCallBack)
        }, 3000);
    }

    //BOTONES DE INICIAR Y DETENER LA CAMARA
    const startCamera = document.getElementById('startCamera');
    const stopCamera = document.getElementById('stopCamera');

    //FUNCIONES PARA INICIAR Y PARAR LA CAMARA
    function camaraStart(config, qrCodeSuccessCallBack) {
        html5QrCode.start(
            { facingMode: "environment" },  // cámara trasera
            config,
            qrCodeSuccessCallBack
        ).then(() => {
            stopCamera.disabled = false;
            startCamera.disabled = true;  // botón de inicio deshabilitado
            console.log("Cámara iniciada correctamente");
        }).catch(err => {
            console.log("No se pudo acceder a la cámara trasera");
        });
    }

    function camaraStop() {
        html5QrCode.stop().then(() => {
            stopCamera.disabled = true;
            startCamera.disabled = false;  // botón de inicio habilitado
            console.log("Cámara detenida correctamente");
        }).catch(err => {
            console.log("No se pudo detener la cámara");
        })
    }

    //FUNCION PARA MOSTRAR LOS MENSAJES DE ALERTA POR UN TIEMPO DETERMINADO
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
        }, 1000);
    }

    //FUNCIONES PARA LOS BOTONES DE INICIO Y DETENCION
    startCamera.addEventListener('click', () => {
        camaraStart(config, qrCodeSuccessCallBack);
    });

    stopCamera.addEventListener('click', () => {
        camaraStop();
    });

});

