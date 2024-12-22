from flask import Flask, render_template
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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
    
    with app.app_context():
        db.drop_all()
        db.create_all()  # Crea las tablas si no existen
        
    return app
