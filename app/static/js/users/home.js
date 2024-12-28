const btn_user_to_seller = document.getElementById('btn_user_to_seller');
const btn_submit_seller = document.getElementById('btn_submit_seller');
const btn_close_sesion = document.getElementById('btn_close_sesion');

const form_modal = document.getElementById('form_modal');
form_modal.style.display = 'none';
const btn_close_modal = document.getElementById('btn_close_modal');

const div_products = document.getElementById('home_products');

document.addEventListener('DOMContentLoaded', async () => {
await get_products();

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
            inp_name.value = user_data.name.toString();
            inp_email.value = user_data.email.toString();
            inp_number.value = user_data.cell_phone.toString();

            btn_submit_seller.addEventListener('click', () => {
                const data = {
                    name: inp_name.value,
                    email: inp_email.value,
                    password: inp_password.value.toString(),
                    cell_phone: inp_number.value
                }

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
            alert('error ', error.message);
        }

    form_modal.style.display = 'flex'; 
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
btn_close_sesion.addEventListener('click', () => {
    sessionStorage.clear();
    window.location.href = '/'
})
async function get_products(){
    form_modal.style.display = 'none';
    const response = await fetch('/get_all_products',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    const data = await response.json();
    if(response.ok){
        data.forEach(prd => {
            const product_card = document.createElement('div');
            product_card.innerHTML = `
            <h2>Vendido por: ${prd.seller.name}</h2>
            <h3>Nombre: ${prd.product_name}</h3>
            <p>Descripción: ${prd.product_description}</p>
            <p>Precio: $${prd.product_price}</p>
            <p>Stock: ${prd.product_stock}</p>
            <button>AGREGAR AL CARRITO</button>
        `;
            div_products.appendChild(product_card);
        });
    }
}
})