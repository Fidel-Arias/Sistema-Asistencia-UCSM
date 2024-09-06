const buttonSubir = document.getElementById("upload_files");

buttonSubir.disabled = true;
buttonSubir.style.backgroundColor = '#c8c8c8';
buttonSubir.style.cursor = 'not-allowed';


document.getElementById('uploadButton').addEventListener('click', function() {
    event.preventDefault();
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];
    console.log(file);

    if (file) {
        document.getElementById('fileName').innerHTML = 'Archivo seleccionado: ' + file.name;
        buttonSubir.disabled = false;
        buttonSubir.style.backgroundColor = '#28a745'
        buttonSubir.style.cursor = 'pointer'
    } else {
        document.getElementById('fileName').innerHTML = 'No se seleccionó ningún archivo.';
    }
});
