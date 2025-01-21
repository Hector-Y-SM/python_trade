from flask import request, jsonify
from app.models.User import User
from app.models.CartItem import CartItem
from app.extensions import db

def update_product_quantity():
    data = request.get_json()
    product_id = data.get('product_id')
    user_email = data.get('user_email')
    quantity = data.get('quantity')

    user_in_db = User.query.filter_by(email=user_email).first()
    if not user_in_db:
        return jsonify({"message": "Usuario no encontrado"}), 404

    cart_item = CartItem.query.filter_by(user_id=user_in_db.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"message": "Producto no encontrado en el carrito"}), 404

    try:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({"message": "Cantidad actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"message": f"Error al actualizar la cantidad: {str(e)}"}), 500