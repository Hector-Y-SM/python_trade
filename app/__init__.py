from app.routes import app
from app.extensions import db

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all() 
        
    return app
