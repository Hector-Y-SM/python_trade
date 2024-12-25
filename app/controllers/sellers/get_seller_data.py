from app.models.Seller import Seller
from flask import request, jsonify

#use in home_seller.js
def get_seller_data():
    data = request.get_json()
    email = data.get('seller_email')

    if not email:
        return jsonify({"message": "El campo 'seller_email' es obligatorio"}), 400

    seller_in_db = Seller.query.filter_by(seller_email=email).first()
    if not seller_in_db:
        return jsonify({"message":"el vendedor no existe"}), 404
    
    # se tienen que serializar, para evitar errores, no es capaz de procesar objetos
    serialized_products = [
        {
            "product_name": product.product_name,
            "product_description": product.product_description,
            "product_price": product.product_price,
            "product_stock": product.product_stock
        }
        for product in seller_in_db.all_products
    ]
        
    return jsonify({
        "name": seller_in_db.seller_name,
        "email": seller_in_db.seller_email,
        "phone_number": seller_in_db.seller_phone,
        "password": seller_in_db.seller_password,
        "role": seller_in_db.role,
        "all_products": serialized_products
    }), 200;