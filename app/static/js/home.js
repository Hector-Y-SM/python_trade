const btn_user_to_seller = document.getElementById('btn_user_to_seller');
const btn_submit_seller = document.getElementById('btn_submit_seller');

const form_modal = document.getElementById('form_modal');
form_modal.style.display = 'none';
const btn_close_modal = document.getElementById('btn_close_modal');

btn_user_to_seller.addEventListener('click', async () => {
        const user_email = sessionStorage.getItem('user_email');

        const inp_name = document.getElementById('seller_name');
        const inp_email = document.getElementById('seller_email');
        const inp_number = document.getElementById('seller_phone');
        const inp_password = document.getElementById('seller_password');
        const response = await fetch('/get_user_data',{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({user_email}),  
        });

        if (response.ok){
            const user_data = await response.json();
            console.log(user_data)
            inp_name.value = user_data.name;
            inp_email.value = user_data.email;
            inp_number.value = user_data.cell_phone;

            btn_submit_seller.addEventListener('click', () => {
                const data = {
                    name: inp_name.value.toString(),
                    email: inp_email.value.toString(),
                    password: inp_password.value.toString(),
                    cell_phone: inp_number.value.toString()
                }

                console.log(data)
                fetch('/user_to_seller', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data),
                })
                .then(response => response.json().then(data => {
                    if(response.status == 201){
                        alert(data.message);  
                        sessionStorage.setItem('seller_email', inp_email.value);
                        window.location.href = 'home_seller.html';
                        return;
                    }
                    alert(data.message);  
                }))
                .catch(error => {
                    console.error('Error:', error);
                });

            })
        } else {
            const error = await response.json();
            alert('error ', error.message)
        }

    form_modal.style.display = 'flex'; 
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
