from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    # La columna product_id debe ser una clave foránea que hace referencia a Product
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    product_stock = db.Column(db.Integer, default=0)
    product_status = db.Column(db.String(8))

    # Relación con Product usando backref para simplificar
    product = db.relationship('Product', back_populates='cart_items')
    
    # Clave foránea para la relación con User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relación con User usando back_populates
    user = db.relationship('User', back_populates='cart_items')

    def __repr__(self):
        return f'<Product: {self.product.product_name} x{self.quantity}: ${self.product.product_price * self.quantity}>'
