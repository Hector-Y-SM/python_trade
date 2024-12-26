from app.models.Product import Product
from app.models.Seller import Seller
from flask import request, jsonify
#use in home_seller.js
def get_seller_products():
    data = request.get_json()

    email = data.get('seller_email')
    seller_in_db = Seller.query.filter_by(seller_email=email).first()
    if not seller_in_db:
        return jsonify({"message": "vendedor no registrado en bd"}), 400

    products_in_db = Product.query.filter_by(seller_id=seller_in_db.id).all()

    response = {
        "seller_name": seller_in_db.seller_name,
        "seller_email": seller_in_db.seller_email,
        "products":[
            {
                "id": product.id,
                "product_name": product.product_name,
                "product_description": product.product_description,
                "product_price": product.product_price,
                "product_stock": product.product_stock
            }
            for product in products_in_db
        ] if products_in_db else []
    }

    if not products_in_db:
        response["message"] = "no se encontraron productos para este vendedor"

    return jsonify(response), 200
