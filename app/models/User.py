from app.models.Interfaces import Buy, Add, Delete
from app.models.CartItem import CartItem

class User(Buy, Add, Delete):
    def __init__(self, name, email, password, number):
        self.name = name
        self.email = email
        self.password = password
        self.number = number
        self.pay = 0
        self.cart = []
    

    def buy_product(self):
        print('ACABAS DE COMPRAR:')
        for prd in self.cart:
            product = prd.product
            if product.product_stock > 0 and prd.quantity <= product.product_stock and product.product_status == 'active':
                product.product_stock -= prd.quantity
                print(f'{product.product_name}: {product.product_price}, stock: {product.product_stock}, cantidad: {prd.quantity}')
            else:
                self.pay -= prd.product.product_price * prd.quantity
                print('out of stock')
                continue

        print(f'PAGASTE: {self.pay}')
        self.pay = 0
        self.cart = []

    
    def add_product(self, product, quantity): 
        if product.product_stock > 0 and quantity <= product.product_stock and product.product_status == 'active':
            for prd in self.cart:
                if prd.product == product:
                    prd.quantity += quantity
                    print(f'aumentaste la cantidad de {prd.product_name} a {prd.quantity}')
                    break
            else:
                self.cart.append(CartItem(product, quantity, product.product_id, product.product_stock, product.product_status))
                print(f'agregaste: {product.product_name} x{quantity}')
            
            self.pay += product.product_price * quantity
        else:
            print(f'{product.product_name} está fuera de stock o no hay suficiente inventario.')


    def delete_product(self, product_id):
        for prd in self.cart:
            if prd.product_id == product_id:
                self.cart.remove(prd)
                self.pay -= prd.product.product_price * prd.quantity
                print(f'eliminaste: {prd.product.product_name} del carrito.')
                break
        else:
            print(f'producto con ID {product_id} \nno encontrado en el carrito.')
        return self.cart