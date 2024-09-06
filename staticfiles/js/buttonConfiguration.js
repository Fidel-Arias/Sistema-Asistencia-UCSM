const messageWarning = document.querySelector('.warning');
const messageSuccess = document.querySelector('.success');
const buttonRegister = document.getElementById('register-button');
const buttonDelete = document.getElementById('delete-button');
const buttonEdit = document.getElementById('edit-button');

if (messageWarning) {
    buttonRegister.disabled = true;
    buttonDelete.disabled = true;
    buttonEdit.disabled = true;
    //estilos
    buttonRegister.style.backgroundColor = '#c8c8c8';
    buttonRegister.style.cursor = 'not-allowed';
    buttonDelete.style.backgroundColor = '#c8c8c8';
    buttonDelete.style.cursor = 'not-allowed';
    buttonEdit.style.backgroundColor = '#c8c8c8';
    buttonEdit.style.cursor = 'not-allowed';
} else if (messageSuccess) {
    buttonRegister.disabled = false;
    buttonDelete.disabled = false;
    buttonEdit.disabled = false;
    //estilos
    buttonRegister.style.backgroundColor = '#007bff';
    buttonRegister.style.cursor = 'pointer';
    buttonDelete.style.backgroundColor = '#dc3545';
    buttonDelete.style.cursor = 'pointer';
    buttonEdit.style.backgroundColor = '#28a745';
    buttonEdit.style.cursor = 'pointer';
}