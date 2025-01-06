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

    def buy_product(self):
        print('ACABAS DE COMPRAR:')
        for prd in self.cart_items:
            product = prd.product
            if product.product_stock > 0 and prd.quantity <= product.product_stock and product.product_status == 'active':
                product.product_stock -= prd.quantity
                db.session.delete(prd)  # Elimina el ítem del carrito
                print(f'{product.product_name}: {product.product_price}, stock: {product.product_stock}, cantidad: {prd.quantity}')
            else:
                self.pay -= prd.product.product_price * prd.quantity
                print('out of stock')
                continue

        db.session.commit()
        print(f'PAGASTE: {self.pay}')
        self.pay = 0

    
    def add_product(self, product, quantity): 
        if product.product_stock > 0 and quantity <= product.product_stock and product.product_status != 'archive':
            for prd in self.cart_items:
                if prd.product == product:
                    prd.quantity += quantity
                    print(f'aumentaste la cantidad de {prd.product_name} a {prd.quantity}')
                    break
            else:
                cart_item = CartItem(product=product, quantity=quantity, user_id=self.id)
                db.session.add(cart_item)
                db.session.commit()
                print(f'agregaste: {product.product_name} x{quantity}')

            self.pay += product.product_price * quantity
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
