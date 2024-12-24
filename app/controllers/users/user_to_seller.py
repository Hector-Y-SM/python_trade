from werkzeug.security import generate_password_hash
from app.models.Seller import Seller
from flask import request, jsonify
from app.models.User import User
from app.extensions import db
#use in home.js 
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
    if not user_in_db:
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
