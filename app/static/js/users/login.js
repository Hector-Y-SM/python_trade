const checkbox = document.getElementById('is_seller_checkbox');
const login_form_container = document.getElementById('login_form');

checkbox.addEventListener('change', () => {
    generate_login_form(checkbox.checked ? 1 : 0);
});

const login = async (email, password, type) => {
    console.log('Tipo de usuario:', type);
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
            type: type,
        }),
    });

    const result = await response.json();
    if (response.ok) {
        if (response.status === 200) {
            alert(result.message);
            type === 0
                ? sessionStorage.setItem('user_email', email)
                : sessionStorage.setItem('seller_email', email);
            window.location.href = type === 0 ? 'home.html' : 'home_seller.html';
            return;
        }
        alert(result.message);
    } else {
        alert(result.message);
    }
};

function generate_login_form(type) {
    login_form_container.innerHTML = '';  

    const label1 = document.createElement('label');
    label1.textContent = 'INGRESA TU CORREO';
    const input1 = document.createElement('input');

    const label2 = document.createElement('label');
    label2.textContent = 'INGRESA TU CONTRASEÑA';
    const input2 = document.createElement('input');
    input2.type = 'password';

    const btn_submit = document.createElement('button');
    btn_submit.textContent = 'Login';

    btn_submit.addEventListener('click', () => {
        login(input1.value.trim(), input2.value.trim(), type);
    });

    login_form_container.append(label1, input1, label2, input2, btn_submit);
}

 
generate_login_form(0);
