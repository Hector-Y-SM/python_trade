from flask import request, jsonify
from app.models.User import User

def buy_all_products():
    data = request.get_json()
    email = data.get('user_email')

    user_in_db = User.query.filter_by(email=email).first()
    if not user_in_db:
        return jsonify({"message": "Usuario no existe"}), 404

    try:
        result = user_in_db.buy_all_products()
        return jsonify({
            "message": "Compra realizada con éxito",
            "summary": result
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error al procesar la compra: {str(e)}"}), 500
