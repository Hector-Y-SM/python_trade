from app.models.CartItem import CartItem
from app.models.Product import Product
from app.extensions import db
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cell_phone = db.Column(db.String(15), nullable=False)
    pay = db.Column(db.Float, default = 0)
    role = db.Column(db.String(20), default = 'user')

    #relacionar con la tabla del carrito
    cart_items = db.relationship('CartItem', back_populates='user', lazy='joined')
    
    def __repr__(self):
        return f'<User: {self.name}, Email: {self.email}>'

    def buy_all_products(self):
        purchased_items = []
        failed_items = []

        for prd in self.cart_items:
            product = prd.product
            if product.product_stock <= 0:
                failed_items.append({'product_id': product.id, 'reason': 'Sin stock disponible'})
                continue
            if prd.quantity > product.product_stock:
                failed_items.append({'product_id': product.id, 'reason': 'Cantidad excede el stock disponible'})
                continue

       
            product.product_stock -= prd.quantity
            purchased_items.append({'product_id': product.id, 'quantity': prd.quantity, 'price': product.product_price})
            db.session.delete(prd)  


        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al procesar la compra: {str(e)}")

        return {'purchased': purchased_items, 'failed': failed_items}


    #TODO LA CANTIDAD APARECE UNDEFINED
    def add_product(self, product, quantity): 
        if product.product_stock > 0 and int(quantity) <= product.product_stock and product.product_status != 'archive':
            for prd in self.cart_items:
                if prd.product == product:
                    prd.quantity += int(quantity)
                    print(f'aumentaste la cantidad de {prd.product_name} a {prd.quantity}')
                    break
            else:
                cart_item = CartItem(product=product, quantity=quantity, user_id=self.id)
                db.session.add(cart_item)
                db.session.commit()
                print(f'agregaste: {product.product_name} x{quantity}')

            self.pay += product.product_price * int(quantity)
        else:
            print(f'{product.product_name} está fuera de stock o no hay suficiente inventario.')


    def delete_product(self, product_id):
        for prd in self.cart_items:
            if prd.product_id == product_id:
                product = Product.query.get(prd.product_id) 
                if product:
                    self.pay -= product.product_price * prd.quantity
                    db.session.delete(prd)
                    db.session.commit()
                    print(f'eliminaste: {product.product_name} del carrito.')
                    break
        else:
            print(f'producto con ID {product_id} no encontrado en el carrito.')
        return self.cart_items
