class Product:
    next_id = 1

    def __init__(self, seller, product_name, product_description, product_price, product_stock):
        self.product_id = Product.next_id
        Product.next_id += 1
        self.seller = seller
        self._product_name = product_name
        self._product_description = product_description
        self._product_price = product_price
        self._product_stock = product_stock
        self._product_status = ''

    def __str__(self):
        return f"""
                ID: {self.product_id}
                seller: {self.seller}
                name: {self._product_name}
                description: {self._product_description}
                price: {self._product_price}
                stock: {self._product_stock}
                status: {self._product_status}
                """
    
    @property
    def product_name(self):
        return self._product_name  
    
    @product_name.setter
    def product_name(self, new_name):
        self._product_name = new_name  

    @property
    def product_description(self):
        return self._product_description  
    
    @product_description.setter
    def product_description(self, new_description):
        self._product_description = new_description  

    @property
    def product_price(self):
        return self._product_price  
    
    @product_price.setter
    def product_price(self, new_price):
        self._product_price = new_price  

    @property
    def product_stock(self):
        return self._product_stock  
    
    @product_stock.setter
    def product_stock(self, new_stock):
        self._product_stock = new_stock  

    @property
    def product_status(self):
        return self._product_status  
    
    @product_status.setter
    def product_status(self, new_status):
        self._product_status = new_status  