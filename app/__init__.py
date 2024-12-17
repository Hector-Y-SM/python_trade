from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

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
    
    return app
