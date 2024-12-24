from werkzeug.security import check_password_hash
from app.models.Seller import Seller
from flask import request, jsonify
from app.models.User import User


def login_user(email, password):
    user_in_db = User.query.filter_by(email=email).first()
    if user_in_db and check_password_hash(user_in_db.password, password):
        return {
            "email": user_in_db.email,
            "name": user_in_db.name,
            "role": user_in_db.role
        }
    return None

def login_seller(email, password):
    seller_in_db = Seller.query.filter_by(seller_email=email).first()
    if seller_in_db and check_password_hash(seller_in_db.seller_password, password):
        return {
            "email": seller_in_db.seller_email,
            "name": seller_in_db.seller_name,
            "role": seller_in_db.role
        }
    return None

#use in login.js
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    type = data.get('type')
    print(type)

    if not all([email, password]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    if not isinstance(email, str) or '@' not in email:
        return jsonify({"message": "Correo electrónico no válido"}), 400
    
    if type == 0:
        user_data = login_user(email,password)
    elif type == 1:
        user_data = login_seller(email, password)
    else:
        return jsonify({"message": "Tipo de usuario inválido"}), 400

    if user_data:
        return jsonify({"message":"login exitoso", "user":user_data}), 200
    else:
        return jsonify({"message":"email o contraseña incorrectos"}), 401
    