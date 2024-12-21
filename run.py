from app import create_app
from flask import render_template, request, jsonify
from app.models.User import User
from app.models.Seller import Seller
from app.models.Product import Product

app = create_app()
usuarios = []
vendedores = []
productos = []

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    cell_phone = data.get('cell_phone')

    if not all([name, email, cell_phone, password]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    
    usr = User(name, email, password, cell_phone)
    usuarios.append(usr)
    return jsonify({"message":"usuario creado exitosamente"}), 201


@app.route('/login_usr', methods=['POST'])
def login_usr():
    print(usuarios)
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    usuario = False
    name = ''

    for x in usuarios:
        if x.email == email and x.password == password:
            name = x.name
            usuario = True

    if usuario:
        return jsonify({
            "message":"Login exitoso",
            "user":{
                "name": name,
                "email": email
            }
        }), 200
    else:
        return jsonify({"message":"credenciales invalidas"}), 401


@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('user_email')
    flag = False
    user = {}

    for x in usuarios:
        if x.email == email:
            user = x
            flag = True

    if flag:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "number": user.number
            #"password": user.password
        }), 200
    else:
        return jsonify({"message":"usuario no encontrado"}), 401


@app.route('/get_seller_data', methods=['POST'])
def get_seller_data():
    data = request.get_json()

    email = data.get('seller_email')
    if not email:
        return jsonify({"message": "El campo 'seller_email' es obligatorio"}), 400

    seller = next((x for x in vendedores if x.seller_email == email), None)
    if not seller:
        return jsonify({"message":"el vendedor no existe"}), 404
    
    return jsonify({
        "name": seller.seller_name,
        "email": seller.seller_email,
        "phone_number": seller.seller_phone,
        "password": seller.seller_password,
        "available": seller.available,
        "archive": seller.archive,
        "all_products": seller.all_products,
        "role": seller._role
    }), 200;


@app.route('/user_to_seller', methods=['POST'])
def user_to_seller():
    data = request.get_json()

    email = data.get('email')
    user = next((x for x in usuarios if x.email == email), None)
    name = data.get('name', user.name)
    cell_phone = data.get('cell_phone', user.number)
    password = data.get('password', user.password)

    if not all([name, email, cell_phone, password]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    
    if user.email == email:
        usuarios.remove(user)

    seller = Seller(name, email, cell_phone, password)
    vendedores.append(seller)
    return jsonify({"message":"te has convertido en vendedor exitosamente"}), 201


@app.route('/create_product', methods=['POST'])
def create_product():
    data = request.get_json()
    print('esto llega ', data)

    seller_data = data.get('seller')
    seller_email = seller_data['email']  

    product_name = data.get('product_name')
    product_description = data.get('product_description')
    product_price = data.get('product_price')
    product_stock = data.get('product_stock')

    if not all([seller_data, product_name, product_description, product_price, product_stock]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    try:
        product_price = float(product_price)
        product_stock = int(product_stock)
        if product_price <= 0 or product_stock < 0:
            raise ValueError
    except ValueError:
        return jsonify({"message":"el precio y la cantidad disponible de unidades debe ser mayor a 0"}), 404

    seller_object = next((x for x in vendedores if x.seller_email == seller_email), None)
    if not seller_object:
        return jsonify({"message":"el vendedor no existe"}), 404
    
    prd = Product(seller_object, product_name, product_description, product_price, product_stock)
    seller_object.add_product(prd)
    productos.append(prd)

    return jsonify({"message":"Producto publicado exitosamente"}), 201


@app.route('/get_seller_products', methods=['POST'])
def get_seller_products():
    data = request.get_json()

    email = data.get('seller_email')
    if not email:
        return jsonify({"message": "El campo 'seller_email' es obligatorio"}), 400

    seller = next((v for v in vendedores if v.seller_email == email), None)
    seller_products = [prd for prd in productos if prd.seller.seller_email == email]
    if not seller_products:
        return jsonify({"message": "No se encontraron productos para este vendedor"}), 404


    response = {
        "seller_name": seller.seller_name,
        "seller_email": seller.seller_email,
        "products": [
            {
                "product_name": prd.product_name,
                "product_description": prd.product_description,
                "product_price": prd.product_price,
                "product_stock": prd.product_stock
            }
            for prd in seller_products
        ]
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)