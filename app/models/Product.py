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

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "product_price": self.product_price,
            "product_stock": self.product_stock,
            "product_status": self.product_status,
            "seller": {
                "id": self.seller.id,
                "name": self.seller.seller_name,
                "email": self.seller.seller_email,
                "phone": self.seller.seller_phone,
            } if self.seller else None
        }
