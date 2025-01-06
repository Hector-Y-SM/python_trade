from flask import request, jsonify
from app.models.Product import Product
from app.models.CartItem import CartItem
from app.models.User import User
from app.extensions import db

def delete_product_cart():
    data = request.get_json()

    product_id = data.get('product_id')
    print(product_id)
    user_email = data.get('user_email')

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    remaining_items = user.delete_product(product_id)

    return jsonify({
        "message": "Producto eliminado del carrito",
        "remaining_items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in remaining_items
        ]
    }), 200
