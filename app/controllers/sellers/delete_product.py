from app.models.Product import Product
from flask import request, jsonify
from app.extensions import db

#use in home_seller.js
def delete_product():
    data = request.get_json()

    id = data.get('product_id')
    product_in_db = Product.query.filter_by(id=id).first()
    if not product_in_db:
        return jsonify({"message":"producto no encontrado"}), 404
    
    try:
        db.session.delete(product_in_db)
        db.session.commit()
        return jsonify({"message":"producto eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"error al eliminar el producto {str(e)}"}), 404