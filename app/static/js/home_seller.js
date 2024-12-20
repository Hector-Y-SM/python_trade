const btn_add_product = document.getElementById('btn_add_product');
const btn_submit_product = document.getElementById('btn_submit_product'); 
const btn_close_modal = document.getElementById('btn_close_modal');

const form_modal = document.getElementById('form_modal_product');
form_modal.style.display = 'none';
const div_product = document.getElementById('seller_products');

async function update_products(){
    const seller_email = sessionStorage.getItem('seller_email');
    const response = await fetch('get_seller_products',{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({seller_email}),  
    });

    if(response.ok){
        const data = await response.json();
        const products = data.products;

        div_product.innerHTML = '';
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

btn_add_product.addEventListener('click', async () => {
    form_modal.style.display = 'flex';
    const product_name = document.getElementById('product_name');
    const product_description = document.getElementById('product_description');
    const product_price = document.getElementById('product_price');
    const product_stock = document.getElementById('product_stock');
    const seller_email = sessionStorage.getItem('seller_email'); //get seller object

    const response = await fetch('/get_seller_data',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({seller_email}),  
      });

    if(response.ok){
        const seller_data = await response.json()
        btn_submit_product.addEventListener('click', () => {
            const product_data = {
                seller: seller_data,
                product_name: product_name.value,
                product_description: product_description.value,
                product_price: product_price.value,
                product_stock: product_stock.value
            }
            console.log(product_data)
            fetch('/create_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(product_data),
            })
            .then(response => response.json())  
            .then(data => {
                console.log(data.message);  
                alert('producto publicado');
                update_products();
                form_modal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

btn_close_modal.addEventListener('click', () => { form_modal.style.display = 'none'; });