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
    const user_email = sessionStorage.getItem('user_email');
    if (user_email) {
        await get_cart_products(user_email);
    }
});

btn_user_to_seller.addEventListener('click', async () => {
    form_modal.style.display = 'flex';
    const user_email = sessionStorage.getItem('user_email');

    const inp_name = document.getElementById('seller_name');
    const inp_email = document.getElementById('seller_email');
    const inp_number = document.getElementById('seller_phone');
    const inp_password = document.getElementById('seller_password');
    const response = await fetch('/get_user_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_email: user_email }),
    });

    if (response.ok) {
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
            };

            fetch('/user_to_seller', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json().then(data => {
                    if (response.status == 201) {
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

    if (clicked_element.id === 'btn_add_product') {
        const product_id = clicked_element.dataset.id;
        if (product_id) {
            await add_product(product_id, sessionStorage.getItem('user_email'));
        }
    }
});

async function add_product(product_id, user_email) {
    const quantity = prompt('Ingresa la cantidad deseada a comprar: ');
    if((isNaN(Number(quantity))) || (quantity < 0)){
        alert('la cantidad debe ser un numero y mayor que cero.');
        return;
    }
    
    const response = await fetch('/add_product_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            product_id: product_id, 
            user_email: user_email,
            quantity: quantity,
        }),
    });

    if (response.ok) {
        alert('Producto agregado al carrito exitosamente.');
        await update_cart(user_email);
    } else {
        const error_data = await response.json();
        alert(`Error: ${error_data.message}`);
    }
}

async function remove_product(product_id, user_email) {
    const response = await fetch('/delete_product_cart', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: product_id, user_email: user_email}),
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        console.log(data.remaining_items)
        await update_cart(user_email);
    } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
    }
}

async function get_cart_products(user_email) {
    const response = await fetch('/get_products_in_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_email: user_email })
    });

    if (response.ok) {
        return await response.json();
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
        return [];
    }
}

function update_quantity(product_id, delta) {
    const quantityElement = document.getElementById(`quantity_${product_id}`);
    let currentQuantity = parseInt(quantityElement.textContent);

    if (currentQuantity + delta > 0) {
        quantityElement.textContent = currentQuantity + delta;
        console.log(`Cantidad actualizada: ${currentQuantity + delta}`);
    } else {
        alert("La cantidad no puede ser menor a 1.");
    }
}


async function buy_all_products(user_email) {
    div_products.innerHTML = '';
    div_cart.innerHTML = '';
    const response = await fetch('/buy_all_products',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_email: user_email })
    });

    const data = await response.json()
    if(response.ok){
        alert(data.message);
        console.log(data.summary)
        get_products();
    }else{
        alert(`Error: ${data.message}`);
    }
}

async function update_cart(user_email) {
    const cart_products = await get_cart_products(user_email);
    div_cart.innerHTML = ''; 

    if (cart_products.length === 0) {
        div_cart.innerHTML = '<p>No hay ningún producto en el carrito</p>';
        return;
    }

    const aux = cart_products.cart_items.length === 0 ? [] : cart_products.cart_items;

    aux.forEach(product => {
        const product_card = document.createElement('div');
        product_card.className = 'cart-item';
        product_card.dataset.productId = product.product_id;

        product_card.innerHTML = `
            <h3>${product.product_name}</h3>
            <p>Precio: $${product.product_price}</p>
            <p>Cantidad: <span id="quantity_${product.product_id}">${product.quantity}</span></p>
            <button id="btn_increase_${product.product_id}" data-id="${product.product_id}">+</button>
            <button id="btn_decrease_${product.product_id}" data-id="${product.product_id}">-</button>
            <button id="btn_buy_${product.product_id}" data-id="${product.product_id}">COMPRAR</button>
            <button id="btn_remove_${product.product_id}" data-id="${product.product_id}">ELIMINAR</button>
        `;

        div_cart.appendChild(product_card);


        document.getElementById(`btn_increase_${product.product_id}`).addEventListener('click', () => {
            update_quantity(product.product_id, 1);
        });

        document.getElementById(`btn_decrease_${product.product_id}`).addEventListener('click', () => {
            update_quantity(product.product_id, -1);
        });

        document.getElementById(`btn_buy_${product.product_id}`).addEventListener('click', async () => {
            await buy_all_products(user_email);
        });

        document.getElementById(`btn_remove_${product.product_id}`).addEventListener('click', async () => {
            await remove_product(product.product_id, user_email);
        });
    });
}


// get all the products published by the sellers
async function get_products() {
    form_modal.style.display = 'none';
    const response = await fetch('/get_all_products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    const data = await response.json();
    if (response.ok) {
        const aux = data.length === undefined ? [] : data;
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