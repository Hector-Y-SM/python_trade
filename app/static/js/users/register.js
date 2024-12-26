const register = document.getElementById('btn_register');

register.addEventListener('click', async (e) => {
    e.preventDefault();
    const name = document.getElementById('input_name').value.trim();
    const cell_phone = document.getElementById('input_cellphone').value.trim();
    const email = document.getElementById('input_email').value.trim();
    const password = document.getElementById('input_password').value.trim();

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
    .then(response => response.json().then(data => {
        if (response.status === 201) {
            alert(data.message); 
            window.location.href = "login.html";  
            return;
        }      
        alert(data.message);  
    }))
    .catch(error => {
        alert(error.message); 
    });
});
