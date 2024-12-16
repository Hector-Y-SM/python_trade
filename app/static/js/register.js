const name = document.getElementById('input_name');
const cell_phone = document.getElementById('input_cellphone');
const email = document.getElementById('input_email');
const password = document.getElementById('input_password');
const register = document.getElementById('btn_register');


register.addEventListener('click', () => {
    if(name.value == '' || cell_phone.value == '' || email.value == '' || password.value == ''){
        alert('TODOS LOS CAMPOS SE DEBEN LLENAR PARA PODER CREAR UNA CUENTA');
    } else {
        const userData = {
            nombre: name.value,
            email: email.value,
            password: password.value,
            telefono: cell_phone.value
        }

        fetch('/crear_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())  
        .then(data => {
            console.log(data.message);  
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
    }
})