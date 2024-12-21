from app.models.Interfaces import Add, Delete, Archive

class Seller(Add, Delete, Archive):
    def __init__(self, seller_name, seller_email, seller_phone, seller_password, all_products=None, archive=None, available=None):
        self.seller_name = seller_name
        self.seller_email = seller_email
        self.seller_phone = seller_phone
        self.seller_password = seller_password
        self.all_products = all_products or []
        self.archive = archive or []
        self.available = available or []
        self._role = 'seller'

    def __str__(self):
        return f"""
                name: {self.seller_name}
                email: {self.seller_email}
                phone: {self.seller_phone}
                password: {self.seller_password}
                all_products: {[product.to_dict() for product in self.all_products]}  
                archive: {[product.to_dict() for product in self.archive]}  
                available: {[product.to_dict() for product in self.available]}
                """
    # metodo para serializar las instacias en las propiedades para guardar productos
    def to_dict(self):
        return {
            "name": self.seller_name,
            "email": self.seller_email,
            "phone_number": self.seller_phone,
            "password": self.seller_password,
            "all_products": [product.to_dict() for product in self.all_products],  # Serializar productos
            "archive": [product.to_dict() for product in self.archive],  # Serializar productos archivados
            "available": [product.to_dict() for product in self.available],  # Serializar productos disponibles
            "role": self._role
        }

    def add_product(self, product):
        product.product_status = 'active'
        self.available.append(product)
        self.all_products.append(product)
        print(product)


    def delete_product(self, product_id):
        for prd in self.available:
            if prd.product_id == product_id:
                prd.product_status = 'deleted'
                self.available.remove(prd)
                self.all_products = [p for p in self.all_products if p.product_id != product_id]
                print(f'producto {product_id} eliminado (estado cambiado a eliminado)')
                return
        print(f'producto con ID {product_id} no encontrado')

    def archive_product(self, product_id):
        for prd in self.available:
            if prd.product_id == product_id:
                prd.product_status = 'pause'
                self.available.remove(prd)
                self.archive.append(prd)
                print(f'producto {prd.product_id} archivado')
                print(prd)
                return
            
            print('no existe esto')

    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, newRole):
        self._role = newRole