let aux_email = ''
const btn_user = document.getElementById('btn_generate_user_login');
const btn_seller = document.getElementById('btn_generate_seller_login');

const login = async (email, password, type) => {
    sessionStorage.setItem('user_email', email);
    //TODO implemantar el parametro type, para definir si se trata de un usuario o vendedor, ya q este la bd
    const response = await fetch('/login_usr',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        }),
    })

    const result = await response.json();
    if(response.ok){
        console.log(result.user.name);
        aux_email = email;
        console.log(aux_email)
        window.location.href = type == 0 ? 'home.html' : 'home_seller.html';
    } else { console.error(result.message) }
}

function generate_login(id, type){
    type == 0 ? 
        document.getElementById('login_seller').innerHTML = '' 
        : document.getElementById('login_usr').innerHTML = '' 

    const div = document.getElementById(id);
    div.innerHTML = '';
    const label1 = document.createElement('label');
    label1.textContent = 'INGRESA TU CORREO'
    const input1 = document.createElement('input');
    
    const label2 = document.createElement('label');
    label2.textContent = 'INGRESA TU CONTRASEÑA'
    const input2 = document.createElement('input');

    const btn_submit = document.createElement('button');
    btn_submit.textContent = 'Login';

    btn_submit.addEventListener('click', () => {
        login(input1.value, input2.value, type);
    });

    div.append(label1, input1, label2, input2, btn_submit);
}

btn_user.addEventListener('click', () => generate_login('login_usr', 0));
btn_seller.addEventListener('click', () => generate_login('login_seller'), 1);