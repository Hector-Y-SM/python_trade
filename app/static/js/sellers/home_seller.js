const btn_add_product = document.getElementById('btn_add_product');
const btn_submit_product = document.getElementById('btn_submit_product'); 
const btn_close_modal = document.getElementById('btn_close_modal');
const btn_close_seller_sesion = document.getElementById('btn_close_seller_sesion');

const form_modal = document.getElementById('form_modal_product');
form_modal.style.display = 'none';
const product_name = document.getElementById('product_name');
const product_description = document.getElementById('product_description');
const product_price = document.getElementById('product_price');
const product_stock = document.getElementById('product_stock');

const div_product = document.getElementById('seller_products');
const seller_email = sessionStorage.getItem('seller_email'); // obtener email del vendedor usando lo q se almaceno en la sesion

let cached_seller_data = null; 
let submitProductListenerAdded = false; // controlar eventos
let aux_update = false;

async function update_products() {
    const response_products = await fetch('/get_seller_products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ seller_email })
    });

    if (!response_products.ok) {
        alert(response_products.message);
        return;
    }

    const data = await response_products.json();
    const products = data.products;

    div_product.innerHTML = '';  
    if (products.length === 0) {
        div_product.innerHTML = '<p>No hay productos publicados por este vendedor.</p>';
        return;
    }

    products.forEach(prd => {
        const product_card = document.createElement('div');
        product_card.className = 'product-card';
        product_card.dataset.productId = prd.product_id;
        product_card.innerHTML = `
            <h2>Vendido por: ${data.seller_name}</h2>
            <h3>Nombre: ${prd.product_name}</h3>
            <p>Descripción: ${prd.product_description}</p>
            <p>Precio: $${prd.product_price}</p>
            <p>Stock: ${prd.product_stock}</p>
            <button id="btn_delete_product" data-id="${prd.id}">Eliminar</button>
            <button id="btn_upgrade_product" data-id=${prd.id}>Editar</button>
        `;
        div_product.appendChild(product_card);
    });
}
await update_products();

div_product.addEventListener('click', async (e)=>{
    const clicked_element = e.target;

    if(clicked_element.id === 'btn_delete_product'){
        const product_id = clicked_element.dataset.id;
        if(product_id){
            const confirmed = confirm('estas seguro de elimnar este producto?')
            if(confirmed){
                await delete_product(product_id);
            }
        }else{
            console.log('no exits')
        }
    } else if(clicked_element.id === 'btn_upgrade_product'){
        const product_id = clicked_element.dataset.id;
        if(product_id){
            form_modal.style.display = 'flex';
            console.log(aux_update)
            aux_update = true;
            console.log(aux_update)
            btn_submit_product.onclick = async () => {
                const name = product_name.value;
                const description = product_description.value;
                const price = product_price.value;
                const stock = product_stock.value;

                if (name && description && price && stock) {
                    await upgrade_product(product_id, name, description, price, stock);

                    product_name.value = '';
                    product_description.value = '';
                    product_price.value = '';
                    product_stock.value = '';
                    form_modal.style.display = 'none';
                } else {
                    alert('Por favor completa todos los campos antes de actualizar.');
                }
            };
        }
    }
})

async function upgrade_product(product_id, name, description, price, stock){
    const product_data = {
        id: product_id,
        product_name: name,
        product_description: description,
        product_price: price,
        product_stock: stock
    }

    const response = await fetch('/upgrade_product',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product_data)
    });    

    const data = await response.json()
    if(response.ok) {
        alert(data.message);
        update_products();
    } else {
        alert('error al actualizar este producto ', data.message)
    }
}

async function delete_product(product_id) {
    const response = await fetch('/delete_product',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({product_id: product_id})
    });    
 
    const data = await response.json();
    if(response.ok){
        alert(data.message);
        await update_products()
    } else {
        alert('error al eliminar el producto', data.message)
    }
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
            console.log(cached_seller_data)
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

    await load_seller_data();
    if (cached_seller_data) {
        if (!submitProductListenerAdded) {  
            console.log('estadooo ', aux_update)
                btn_submit_product.addEventListener('click', () => {
                    if(aux_update == false){
                    create(cached_seller_data, product_name, product_description, product_price, product_stock);
                    }
                });
            submitProductListenerAdded = true;  
        }
    } else {
        alert('no se pudieron cargar los datos del vendedor');
        return;
    }
});


btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });
btn_close_seller_sesion.addEventListener('click', () => {
    cached_seller_data = null;
    sessionStorage.clear()    
    window.location.href = '/'
});
