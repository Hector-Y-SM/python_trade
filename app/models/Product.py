from app.extensions import db
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(200))
    product_price = db.Column(db.Float, nullable=False)
    product_stock = db.Column(db.Integer, nullable=False)
    product_status = db.Column(db.String(10))

    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)

    # Relación con Seller
    seller = db.relationship('Seller', back_populates='all_products')
    
    # Relación con CartItem
    cart_items = db.relationship('CartItem', back_populates='product')

    def __repr__(self):
        return f"<Product {self.product_id}: {self._product_name}, Price: {self._product_price}, Stock: {self._product_stock}>"

    def to_dict(self):
        return {
            "ID": self.product_id,
            "seller": self.seller,
            "name": self._product_name,
            "description": self._product_description,
            "price": self._product_price,
            "stock": self._product_stock,
            "status": self._product_status
        }
