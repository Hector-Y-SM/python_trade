from flask import request, jsonify
from app.models.Product import Product
from app.models.CartItem import CartItem
from app.models.User import User

#use in home.js
def add_product_cart():
    data = request.get_json()

    product_id = data.get('product_id')
    user_email = data.get('user_email')
    quantity = data.get('quantity', 1)  #default 1

    product_in_db = Product.query.get(product_id)
    user_in_db = User.query.filter_by(email=user_email).first()

    if not product_in_db:
        return jsonify({"message": "Producto no encontrado"}), 404

    if not user_in_db:
        return jsonify({"message": "Usuario no encontrado"}), 404


    try:
        data_in_db = product_in_db.to_dict()
        user_in_db.add_product(product_in_db, quantity)
        return jsonify(data_in_db), 200
    except Exception as e:
        return jsonify({"message": f"Error al agregar producto: {str(e)}"}), 500