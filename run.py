from app import create_app
from flask import render_template, request, jsonify
from app.models.User import User

app = create_app()
usuarios = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    telefono = data.get('telefono')

    usr = User(nombre, email, password, telefono)
    usuarios.append(usr)
    return jsonify({"message":"usuario creado exitosamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)
