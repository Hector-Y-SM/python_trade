from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.User import User
from app.models.Seller import Seller
from app.models.Product import Product
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app import create_app

app = create_app()

usuarios = []
vendedores = []
productos = []

# use in register.js
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    cell_phone = data.get('cell_phone')

    if not all([name, email, cell_phone, password]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    
    if not isinstance(email, str) or '@' not in email:
        return jsonify({"message": "Correo electrónico no válido"}), 400
    
    hashed_password = generate_password_hash(password)
    usr = User(name=name, email=email, password=hashed_password, cell_phone=cell_phone)
    try:
        db.session.add(usr)
        db.session.commit()

        user_in_db = User.query.filter_by(email=email).first()
        return jsonify({"message":f"usuario creado exitosamente: {user_in_db}"}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message":"el correo ya fue registrado anteriormente"}), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"error al crear el usuario: {str(e)}"}), 500

#use in login.js
@app.route('/login_usr', methods=['POST'])
def login_usr():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    if not isinstance(email, str) or '@' not in email:
        return jsonify({"message": "Correo electrónico no válido"}), 400
    
    user_in_db = User.query.filter_by(email=email).first()
    if user_in_db and check_password_hash(user_in_db.password, password):
        return jsonify({
            "message": "login exitoso",
            "user": {
                "email": user_in_db.email,
                "name": user_in_db.name,  
                "role": user_in_db.role  
            }
        }), 200
    else:
        return jsonify({"message":"email o contraseña incorrecta"}), 401

#use in home.js
@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('user_email')
    user_in_db = User.query.filter_by(email=email).first()
    
    if user_in_db:
        return jsonify({
            "name": user_in_db.name,
            "email": user_in_db.email,
            "cell_phone": user_in_db.cell_phone
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

#use in home.js 
@app.route('/user_to_seller', methods=['POST'])
def user_to_seller():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    cell_phone = data.get('cell_phone')    

    if not all([name, email, password, cell_phone]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    
    user_in_db = User.query.filter_by(email=email).first()
    if user_in_db == None:
        return jsonify({"message":"el usuario no existe"}), 404
    
    try:
        db.session.delete(user_in_db)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"error al eliminar el usuario: {str(e)}"}), 500
    
    try:
        seller = Seller(seller_name=name, seller_email=email, seller_phone=cell_phone, seller_password=hashed_password)
        db.session.add(seller)
        db.session.commit()
        return jsonify({"message":"te has convertido en vendedor"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"error al convertirte en vendedor {str(e)}"}), 500


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