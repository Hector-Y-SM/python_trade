# quantity in cart
class CartItem:
    def __init__(self, product, quantity, id, stock, status):
        self.product = product
        self.quantity = quantity
        self.product_id = id
        self.product_stock = stock
        self.product_status = status
    
    def __str__(self):
        return f'{self.product.product_name} x{self.quantity}: ${self.product.product_price * self.quantity}'