from flask import request, jsonify
from app.models.Product import Product
from app.models.CartItem import CartItem

#use in home.js
def add_product_cart():
    data = request.get_json()

    product_id = data.get('product_id')
    product_in_db = Product.query.get(product_id)

    product_data = product_in_db.to_dict()
    print('iddddddddddd ', product_data)
    return jsonify(product_data), 200