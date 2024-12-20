const register = document.getElementById('btn_register');

register.addEventListener('click', () => {
    const name = document.getElementById('input_name').value;
    const cell_phone = document.getElementById('input_cellphone').value;
    const email = document.getElementById('input_email').value;
    const password = document.getElementById('input_password').value;

    const userData = {
        name: name,
        email: email,
        password: password,
        cell_phone: cell_phone
    }

    fetch('/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())  
    .then(data => {
        console.log(data.message);  
        window.location.href = "login.html";
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
})