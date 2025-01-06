from flask import request, jsonify
from app.models.User import User

def get_products_in_cart():
    data = request.get_json() 
    email = data.get('user_email')

    user_in_db = User.query.filter_by(email=email).first()
    if not user_in_db:
        return jsonify({"message":"usuario no existe"}), 404

    serialized_products = [
        {
            "product_id": product.product.id,
            "product_name": product.product.product_name,
            "product_description": product.product.product_description,
            "product_price": product.product.product_price,
            "product_stock": product.product.product_stock
        }
        for product in user_in_db.cart_items
    ]

    return jsonify({"cart_items": serialized_products}), 200