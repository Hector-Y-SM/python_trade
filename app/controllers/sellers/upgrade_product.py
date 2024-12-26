from app.models.Product import Product
from flask import request, jsonify
from app.extensions import db

# use in home_seller.js 
def upgrade_product():
    print('si entrrrr')
    data = request.get_json()
    print('me enviii ', data)
    id = data.get('id')
    name = data.get('product_name')
    description = data.get('product_description')
    price = data.get('product_price')
    stock = data.get('product_stock')

    if not all([name, description, price, stock]):
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    try:
        price = float(price)
        stock = int(stock)
        if price <= 0 or stock < 0:
            raise ValueError
    except ValueError:
        return jsonify({"message":"el precio y la cantidad disponible de unidades debe ser mayor a 0"}), 404


    product_data = Product.query.get(id)
    if not product_data:
        return jsonify({"message":"producto no encontrado"}), 404
    
    product_data.product_name = name
    product_data.product_description = description
    product_data.product_price = price
    product_data.product_stock = stock

    try:
        db.session.commit()
        return jsonify({"message":"producto actualizado con exito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"error al actualizar: {str(e)}"}), 500

