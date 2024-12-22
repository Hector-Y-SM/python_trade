const register = document.getElementById('btn_register');

register.addEventListener('click', (e) => {
    e.preventDefault();
    const name = document.getElementById('input_name').value.trim();
    const cell_phone = document.getElementById('input_cellphone').value.trim();
    const email = document.getElementById('input_email').value.trim();
    const password = document.getElementById('input_password').value.trim();

    if (!name || !cell_phone || !email || !password) {
        alert("todos los campos son obligatorios.");
        return;
    }
    if (!email.includes('@')) {
        alert("ingresa un correo electrónico válido.");
        return;
    }

    const userData = {
        name: name,
        email: email,
        password: password,
        cell_phone: cell_phone
    };

    fetch('/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); 
        window.location.href = "login.html";         
    })
    .catch(error => {
        alert(error.message); 
        console.error('Error:', error);
    });
});
