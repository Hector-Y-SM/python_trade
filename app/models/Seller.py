from app.extensions import db
#from app.models.Product import Product

class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_name = db.Column(db.String(80), nullable=False)
    seller_email = db.Column(db.String(120), unique=True, nullable=False)
    seller_phone = db.Column(db.String(15), nullable=False)
    seller_password = db.Column(db.String(200), nullable=False)
    _role = db.Column(db.String(20), default='seller')

    # relación con productos
    all_products = db.relationship('Product', back_populates='seller')

    def __repr__(self):
        return f"<Seller: {self.seller_name}, Email: {self.seller_email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.seller_name,
            "email": self.seller_email,
            "phone_number": self.seller_phone,
            "password": self.seller_password,
            "all_products": [product.to_dict() for product in self.all_products],
            "role": self._role
        }

    def add_product(self, product):
        product.product_status = 'active'
        self.all_products.append(product)
        db.session.add(product)
        db.session.commit()
        print(f"producto añadido: {product}")

    def delete_product(self, product_id):
        for product in self.all_products:
            if product.id == product_id and product.product_status == 'active':
                product.product_status = 'deleted'
                db.session.commit()
                print(f"producto {product_id} eliminado (estado cambiado a eliminado)")
                return
        print(f"producto con ID {product_id} no encontrado o ya no está activo")

    def archive_product(self, product_id):
        for product in self.all_products:
            if product.id == product_id and product.product_status == 'active':
                product.product_status = 'pause'
                db.session.commit()
                print(f"producto {product_id} archivado")
                return
        print(f"producto con ID {product_id} no encontrado o ya no está activo")
