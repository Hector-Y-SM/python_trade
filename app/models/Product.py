from app.extensions import db
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(200))
    product_price = db.Column(db.Float, nullable=False)
    product_stock = db.Column(db.Integer, nullable=False)
    product_status = db.Column(db.String(10))

    # foreign key
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)

    # relación con Seller
    seller = db.relationship('Seller', back_populates='all_products')
    
    # relación con CartItem
    cart_items = db.relationship('CartItem', back_populates='product')

    def __repr__(self):
        return f"<Product {self.product_id}: {self._product_name}, Price: {self._product_price}, Stock: {self._product_stock}>"

    def to_dict(self):
        return {
            "ID": self.id,
            "seller": self.seller,
            "name": self.product_name,
            "description": self.product_description,
            "price": self.product_price,
            "stock": self.product_stock,
            "status": self.product_status
        }
