from flask import request, jsonify
from app.models.Product import Product

#use in home.js
def get_all_products():
    try:
        products_in_db = Product.query.all()
        print(products_in_db)
        if not products_in_db:
            return jsonify({"message":"nadie ha publicado nada aun"})

        products_list = [product.to_dict() for product in products_in_db]
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"message":f"error, {str(e)}"})
