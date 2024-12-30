from flask import request, jsonify
from app.models.Product import Product


def get_product():
    data = request.get_json()

    product_id = data.get('product_id')
    product_in_db = Product.query.get(product_id)

    data_product = product_in_db.to_dict()
    return jsonify(data_product), 200
