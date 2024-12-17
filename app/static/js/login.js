const btn_login = document.getElementById('btn_login');

btn_login.addEventListener('click', async () => {
    const email = document.getElementById('input_email').value;
    const password = document.getElementById('input_password').value;


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
        console.log(result.user.name)
        btn_login.href = 'home.html'
    } else { console.error(result.message) }
})