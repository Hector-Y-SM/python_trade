from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.models.User import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError

# use in register.js
def create_user():
    print('si entrooo')
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
