document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('cam-video');
    const canvas = document.getElementById('cam-canvas');
    const context = canvas.getContext('2d');
    const btnStart = document.getElementById('btn-cam');
    const btnStop = document.getElementById('btn-stop-cam');
    const audio = document.getElementById('audioScaner');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const bloqueSelect = document.querySelector('[name=bloque]');
    const warningImgUrl = document.querySelector('.success-message').dataset.warningImgUrl;
    const successImgUrl = document.querySelector('.success-message').dataset.successImgUrl;
    const mensajeFondo = document.querySelectorAll(".mostrar");
    
    let stream;
    let animationFrameId;

    btnStart.addEventListener('click', async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            video.srcObject = stream;
            video.play();
            canvas.classList.add('hidden');  // Mostrar el video
            video.classList.remove('hidden');  // Ocultar el canvas
            scanQRCode();
        }
    });

    btnStop.addEventListener('click', () => {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.srcObject = null;
            video.classList.add('hidden');  // Ocultar el video
            canvas.classList.add('hidden');  // Ocultar el canvas
        }

        // Cancelar la animación
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    });

    function scanQRCode() {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            canvas.hidden = false;
            canvas.height = video.videoHeight;
            canvas.width = video.videoWidth;
            context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

            const imageData = context.getImageData(0, 0, canvas.width, canvas.height); //canvas.height, canvas.width
            const code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts: "dontInvert",
            });

            if (code) {
                audio.play();
                //Envio al metodo
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
                    fetch('', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                        body: JSON.stringify({
                            qr_code: code.data,
                            bloque: bloqueSelect.value
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
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
                
                btnStop.click(); // Stop the camera after detecting a QR code
            }
        }

        animationFrameId = requestAnimationFrame(scanQRCode);
    }


});