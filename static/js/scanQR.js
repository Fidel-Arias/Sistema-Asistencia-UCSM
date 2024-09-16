document.addEventListener("DOMContentLoaded", () => {
    const audio = document.getElementById('audioScaner');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const bloqueSelect = document.querySelector('[name=bloque]');
    const warningImgUrl = document.querySelector('.success-message').dataset.warningImgUrl;
    const successImgUrl = document.querySelector('.success-message').dataset.successImgUrl;
    const formJson = document.getElementById('form-json');
    const url = formJson.getAttribute('data-url');
    const mensajeFondo = document.querySelectorAll(".mostrar-msg");
    const formatsToSupport = [
        Html5QrcodeSupportedFormats.QR_CODE
    ];
    
    const scanner = new Html5QrcodeScanner('reader', {
        qrbox: {
            width: 250,
            height: 250,
        },
        fps: 20,
        formatsToSupport: formatsToSupport,
        facingMode: { exact: "environment" },
        compatibleScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CÁMARA]
    }, false);

    scanner.render(success, error);
    
    function success(result) {
        audio.play();
        if (bloqueSelect.value) {
            if (!navigator.onLine) {
                mensajeFondo.forEach((elemento) => {
                    elemento.style.display = 'block';
                });

                document.getElementById('logo_message').classList.add('hidden');
                document.querySelector('.success-message__title').innerHTML = 'Sin conexión';
                document.querySelector('.success-message__title').style.color = 'red';
                document.querySelector('.success-message__content h4').innerHTML = '<b>Conéctate a una red</b>';

                setTimeout(() => {
                    mensajeFondo.forEach((elemento) => {
                        elemento.style.display = 'none';
                    });
                }, 3000);
                
            }
            
            document.getElementById('logo_message').classList.remove('hidden');
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    qr_code: result,
                    bloque: bloqueSelect.value
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                mensajeFondo.forEach((elemento) => {
                    elemento.style.display = 'block';
                });

                if (data['status'] === 'warning'){
                    document.getElementById('logo_message').setAttribute('src', warningImgUrl);
                    document.querySelector('.success-message__title').innerHTML = 'Asistencia no marcada';
                    document.querySelector('.success-message__title').style.color = 'red';
                    document.querySelector('.success-message__content h4').innerHTML = '<b>'+data['message']+'</b>';
                } else if (data['status'] === 'error'){ 
                    document.getElementById('logo_message').setAttribute('src', warningImgUrl);
                    document.querySelector('.success-message__title').innerHTML = 'Error';
                    document.querySelector('.success-message__title').style.color ='red';
                    document.querySelector('.success-message__content h4').innerHTML = '<b>'+data['message']+'</b>';
                } else {
                    document.getElementById('logo_message').setAttribute('src', successImgUrl);
                    document.querySelector('.success-message__title').innerHTML = 'Asistencia marcada';
                    document.querySelector('.success-message__title').style.color = 'green';
                    document.querySelector('.success-message__content h4').innerHTML = '<b>'+data['message']+'</b>';
                }

                setTimeout(() => {
                    mensajeFondo.forEach((elemento) => {
                        elemento.style.display = 'none';
                    });
                }, 3000);
            });
        } else {
            mensajeFondo.forEach((elemento) => {
                elemento.style.display = 'block';
            });
            document.getElementById('logo_message').setAttribute('src', warningImgUrl);
            document.querySelector('.success-message__title').innerHTML = 'Error';
            document.querySelector('.success-message__title').style.color = 'red';
            document.querySelector('.success-message__content h4').innerHTML = '<b>'+'Primero selecciona un bloque'+'<b>';

            setTimeout(() => {
                mensajeFondo.forEach((elemento) => {
                    elemento.style.display = 'none';
                });
            }, 3000);
            
        }
    
    }
    
    function error(error) {}
});

