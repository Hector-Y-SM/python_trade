from app import create_app
from flask import render_template, request, jsonify
from app.models.User import User

app = create_app()
usuarios = []
vendedores= []

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    cell_phone = data.get('cell_phone')

    usr = User(name, email, password, cell_phone)
    usuarios.append(usr)
    return jsonify({"message":"usuario creado exitosamente"}), 201


@app.route('/login_usr', methods=['POST'])
def login_usr():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    usuario = False
    name = ''

    for x in usuarios:
        if x.email == email and x.password == password:
            name = x.name
            usuario = True

    if usuario:
        return jsonify({
            "message":"Login exitoso",
            "user":{
                "name": name,
                "email": email
            }
        }), 200
    else:
        return jsonify({"message":"credenciales invalidas"}), 401

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    flag = False
    user = {}

    for x in usuarios:
        if x.email == email:
            user = x
            flag = True

    if flag:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "number": user.number,
            "password": user.password
        }), 200
    else:
        return jsonify({"message":"usuario no encontrado"}), 401


if __name__ == '__main__':
    app.run(debug=True)
