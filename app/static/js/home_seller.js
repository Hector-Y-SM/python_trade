const btn_add_product = document.getElementById('btn_add_product');
const btn_submit_product = document.getElementById('btn_submit_product'); 
const btn_close_modal = document.getElementById('btn_close_modal');
const btn_close_seller_sesion = document.getElementById('btn_close_seller_sesion');

const form_modal = document.getElementById('form_modal_product');
form_modal.style.display = 'none';
const div_product = document.getElementById('seller_products');
const seller_email = sessionStorage.getItem('seller_email'); // obtener email del vendedor usando lo q se almaceno en la sesion

let cached_seller_data = null; 
let submitProductListenerAdded = false; // controlar eventos

async function update_products() {
        const response_products = await fetch('get_seller_products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ seller_email })
        });

        if (!response_products.ok) {
            alert(response_products.message);
        }

        const data = await response_products.json();
        const products = data.products;

        div_product.innerHTML = '';  
        const productCards = products.map(prd => {
            const product_card = document.createElement('div');
            product_card.id = 'product-card';
            product_card.innerHTML = `
                <h2>Vendido por: ${data.seller_name}</h2>
                <h3>Nombre: ${prd.product_name}</h3>
                <p>Descripción: ${prd.product_description}</p>
                <p>Precio: $${prd.product_price}</p>
                <p>Stock: ${prd.product_stock}</p>
            `;
            return product_card;
        });

        div_product.append(...productCards);
}


async function create(seller_data, product_name, product_description, product_price, product_stock) {
    const product_data = {
        seller: seller_data,
        product_name: product_name.value,
        product_description: product_description.value,
        product_price: parseFloat(product_price.value),
        product_stock: parseInt(product_stock.value)
    };

        const response = await fetch('/create_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(product_data),
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            await update_products();  
            product_name.value = '';
            product_description.value = '';
            product_price.value = '';
            product_stock.value = '';
            form_modal.style.display = 'none';  
        } else {
            alert(data.message);
        }

}

async function load_seller_data() {
    if (!cached_seller_data || cached_seller_data.email !== seller_email) {
        console.log('cargando datos del vendedor desde el servidor...');
        const response = await fetch('/get_seller_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ seller_email })
        });
        if (response.ok) {
            cached_seller_data = await response.json(); 
            console.log('datos del vendedor cargados:', cached_seller_data);
        } else {
            alert('error al obtener los datos del vendedor');
        }
    } else {
        console.log('usando datos del vendedor desde el cache');
    }
}

btn_add_product.addEventListener('click', async (e) => {
    e.preventDefault()
    form_modal.style.display = 'flex';
    const product_name = document.getElementById('product_name');
    const product_description = document.getElementById('product_description');
    const product_price = document.getElementById('product_price');
    const product_stock = document.getElementById('product_stock');

    await load_seller_data();

    if (cached_seller_data) {
        if (!submitProductListenerAdded) {  
            btn_submit_product.addEventListener('click', () => {
                create(cached_seller_data, product_name, product_description, product_price, product_stock);
            });
            submitProductListenerAdded = true;  
        }
    } else {
        alert('no se pudieron cargar los datos del vendedor');
    }
});


btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
btn_close_seller_sesion.addEventListener('click', () => window.location.href = '/')