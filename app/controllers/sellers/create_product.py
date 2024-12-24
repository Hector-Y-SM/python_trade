from app.models.Product import Product
from app.models.Seller import Seller
from flask import request, jsonify
from app.extensions import db

#use in home_seller.js
def create_product():
    data = request.get_json()
    print('esto llega ', data)

    seller_data = data.get('seller')
    seller_email = seller_data['email']  

    product_name = data.get('product_name')
    product_description = data.get('product_description')
    product_price = data.get('product_price')
    product_stock = data.get('product_stock')

    if not all([seller_data, product_name, product_description, product_price, product_stock]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    try:
        product_price = float(product_price)
        product_stock = int(product_stock)
        if product_price <= 0 or product_stock < 0:
            raise ValueError
    except ValueError:
        return jsonify({"message":"el precio y la cantidad disponible de unidades debe ser mayor a 0"}), 404

    seller_in_db = Seller.query.filter_by(seller_email=seller_email).first()
    if not seller_in_db:
        return jsonify({"message":"el usuario no existe"}), 404
    
    try:
        prd = Product(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_stock=product_stock,
            seller_id=seller_in_db.id
        )
        db.session.add(prd)
        db.session.commit()
        return jsonify({"message":"Producto publicado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al publicar el producto: {str(e)}"}), 500
