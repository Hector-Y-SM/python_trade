from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    # product_id es una clave foránea que hace referencia a Product
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    product_stock = db.Column(db.Integer, default=0)
    product_status = db.Column(db.String(8))

    # relacion con product
    product = db.relationship('Product', back_populates='cart_items')
    
    # clave foránea para la relación con user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # relación con User 
    user = db.relationship('User', back_populates='cart_items')

    def __repr__(self):
        return f'<Product: {self.product.product_name} x{self.quantity}: ${self.product.product_price * self.quantity}>'
