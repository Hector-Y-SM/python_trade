const btn_user_to_seller = document.getElementById('btn_user_to_seller');
const btn_submit_seller = document.getElementById('btn_submit_seller');

const form_modal = document.getElementById('form_modal');
form_modal.style.display = 'none';
const btn_close_modal = document.getElementById('btn_close_modal');

btn_user_to_seller.addEventListener('click', async () => {
    try{
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

        if ( response.ok ){
            const user_data = await response.json();
            inp_name.value = user_data.name;
            inp_email.value = user_data.email;
            inp_number.value = user_data.number;

            btn_submit_seller.addEventListener('click', () =>{
                const data = {
                    name: inp_name.value,
                    email: inp_email.value,
                    password: inp_password.value,
                    cell_phone: inp_number.value
                }

                fetch('/user_to_seller', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data),
                })
                .then(response => response.json())  
                .then(data => {
                    console.log(data.message);  
                    window.location.href = 'home_seller.html';
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            })
        } else {
            const error = await response.json();
            console.log('error ',error.message)
        }

    } catch(error){ console.log('error '. error) }
    
    form_modal.style.display = 'flex'; 
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
