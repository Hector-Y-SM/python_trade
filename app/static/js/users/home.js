const btn_user_to_seller = document.getElementById('btn_user_to_seller');
const btn_submit_seller = document.getElementById('btn_submit_seller');
const btn_close_sesion = document.getElementById('btn_close_sesion');

const form_modal = document.getElementById('form_modal');
form_modal.style.display = 'none';
const btn_close_modal = document.getElementById('btn_close_modal');

const div_products = document.getElementById('home_products');
const div_cart = document.getElementById('cart_items');

document.addEventListener('DOMContentLoaded', async () => {
    await get_products();
});

btn_user_to_seller.addEventListener('click', async () => {
    form_modal.style.display = 'flex'; 
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
            });
        } else {
            const error = await response.json();
            alert('error ', error.message);
        }

    form_modal.style.display = 'flex'; 
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
btn_close_sesion.addEventListener('click', () => {
    sessionStorage.clear();
    window.location.href = '/';
});

div_products.addEventListener('click', async (e) => {
    const clicked_element = e.target;


    if(clicked_element.id === 'btn_add_product'){
        const product_id = clicked_element.dataset.id;
        if(product_id){
            await add_product(product_id, sessionStorage.getItem('user_email'));
        }
    }
})

async function add_product(product_id, user) {
    const response = await fetch('/get_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: product_id }),
    });

    const data = [await response.json()];
    console.log(data);

    if (response.ok) {
        data.forEach(prd => {
            const product_card = document.createElement('div');
            product_card.className = 'product-card';
            product_card.dataset.productId = prd.product_id;
            product_card.innerHTML = `
                <h2>Vendido por: ${prd.seller.name}</h2>
                <h3>${prd.product_name}</h3>
                <p>Precio: $${prd.product_price}</p>
                <button id="btn_show_form" data-id=${prd.id}>COMPRAR</button>
                <div id="form_container_${prd.id}" class="hidden">
                    <label>Cantidad:</label>
                    <div>
                        <button id="btn_decrease_${prd.id}">-</button>
                        <span id="quantity_${prd.id}">1</span>
                        <button id="btn_increase_${prd.id}">+</button>
                    </div>
                    <button id="btn_confirm_${prd.id}" data-id=${prd.id}>Confirmar</button>
                </div>
            `;
            div_cart.appendChild(product_card);

            document.getElementById(`btn_show_form`).addEventListener('click', () => {
                document.getElementById(`form_container_${prd.id}`).classList.toggle('hidden');
            });

            let quantity = 1;
            document.getElementById(`btn_decrease_${prd.id}`).addEventListener('click', () => {
                if (quantity > 1) {
                    quantity--;
                    document.getElementById(`quantity_${prd.id}`).textContent = quantity;
                }
            });

            document.getElementById(`btn_increase_${prd.id}`).addEventListener('click', () => {
                quantity++;
                document.getElementById(`quantity_${prd.id}`).textContent = quantity;
            });

            document.getElementById(`btn_confirm_${prd.id}`).addEventListener('click', async () => {
                const confirm_response = await fetch('/add_product_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        product_id: prd.id, 
                        user_email: user, 
                        quantity: quantity 
                    }),
                });

                if (confirm_response.ok) {
                    alert('Producto agregado al carrito exitosamente.');
                    document.getElementById(`form_container_${prd.id}`).classList.add('hidden');
                } else {
                    const error_data = await confirm_response.json();
                    alert(`Error: ${error_data.message}`);
                }
            });
        });
    }
}


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
        const aux = data.length == undefined? [] : data;
        aux.forEach(prd => {
            const product_card = document.createElement('div');
            product_card.className = 'product-card';
            product_card.dataset.productId = prd.product_id;
            product_card.innerHTML = `
            <h2>Vendido por: ${prd.seller.name}</h2>
            <h3>Nombre: ${prd.product_name}</h3>
            <p>Descripción: ${prd.product_description}</p>
            <p>Precio: $${prd.product_price}</p>
            <p>Stock: ${prd.product_stock}</p>
            <button id="btn_add_product" data-id=${prd.id}>AGREGAR AL CARRITO</button>
        `;
        div_products.appendChild(product_card);
        });
    }
}