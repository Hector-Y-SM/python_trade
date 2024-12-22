const btn_add_product = document.getElementById('btn_add_product');
const btn_submit_product = document.getElementById('btn_submit_product'); 
const btn_close_modal = document.getElementById('btn_close_modal');
const btn_close_seller_sesion = document.getElementById('btn_close_seller_sesion');

const form_modal = document.getElementById('form_modal_product');
form_modal.style.display = 'none';
const div_product = document.getElementById('seller_products');
const seller_email = sessionStorage.getItem('seller_email'); // obtener email del vendedor

async function update_products(){
    const response_products = await fetch('get_seller_products',{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({seller_email}),  
    });

    if(response_products.ok){
        const data = await response_products.json();
        const products = data.products;

        div_product.innerHTML = '';
        console.log('estooo ', products)
        products.forEach(prd => {
            const product_card = document.createElement('div');
            product_card.id = 'product-card';
            product_card.innerHTML = `
                <h2>Vendido por:${data.seller_name}</h2>
                <h3>Nombre: ${prd.product_name}</h3>
                <p>Description: ${prd.product_description}</p>
                <p>Precio: $${prd.product_price}</p>
                <p>Stock: ${prd.product_stock}</p>
            `;
            div_product.appendChild(product_card);
        });
    } else {
        console.error('Error al obtener los productos del vendedor');
    }
}

function create(cached_seller_data, product_name, product_description, product_price, product_stock, seller_email){
    const seller_data = cached_seller_data;

    const product_data = {
        seller: seller_data,
        product_name: product_name.value,
        product_description: product_description.value,
        product_price: product_price.value,
        product_stock: product_stock.value
    };

    console.log('esto enviare ',product_data);
    fetch('/create_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product_data),
    })
    .then(response => response.json())
    .then(data => {
        update_products(seller_email); 
        product_name.value = '';
        product_description.value = '';
        product_price.value = '';
        product_stock.value = '';
        console.log(data.message);
        form_modal.style.display = 'none'; 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


let cached_seller_data = null; // auxiliar para almacenar los datos del vendedor en memoria
btn_add_product.addEventListener('click', async () => {
    form_modal.style.display = 'flex';
    const product_name = document.getElementById('product_name');
    const product_description = document.getElementById('product_description');
    const product_price = document.getElementById('product_price');
    const product_stock = document.getElementById('product_stock');

    // verificar si los datos ya estan guardados en cache y ver si correspoden al vendedor actual
    if (!cached_seller_data || cached_seller_data.email !== seller_email) {
        console.log('Cargando datos del vendedor desde el servidor...');
        const response = await fetch('/get_seller_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ seller_email }),
        });

        if (response.ok) {
            cached_seller_data = await response.json(); // actualizar cache con datos del vendedor
            
            btn_submit_product.removeEventListener('click', create);

            btn_submit_product.addEventListener('click', () => 
                create(cached_seller_data, product_name, product_description, product_price, product_stock, seller_email)
            );
            
        } else {
            console.error('error al obtener los datos del vendedor');
            return;
        }
    } else {
        console.log('usando cache');
    }
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
btn_close_seller_sesion.addEventListener('click', () => window.location.href = '/')