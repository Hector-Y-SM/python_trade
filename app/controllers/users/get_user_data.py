from flask import request, jsonify
from app.models.User import User

#use in home.js
def get_user_data():
    data = request.get_json()
    email = data.get('user_email')
    user_in_db = User.query.filter_by(email=email).first()
    
    if user_in_db:
        return jsonify({
            "name": user_in_db.name,
            "email": user_in_db.email,
            "cell_phone": user_in_db.cell_phone
        }), 200
    else:
        return jsonify({"message":"usuario no encontrado"}), 401