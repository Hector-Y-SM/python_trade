from flask import Flask, render_template

app = Flask(__name__)

# vistas
@app.route('/')
def init():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/home_seller.html')
def home_seller():
    return render_template('home_seller.html')
