from app import create_app
from app.controllers.auth.create_user import create_user
from app.controllers.auth.login import login
from app.controllers.sellers.create_product import create_product
from app.controllers.sellers.get_seller_data import get_seller_data
from app.controllers.sellers.get_seller_products import get_seller_products
from app.controllers.users.get_user_data import get_user_data
from app.controllers.users.user_to_seller import user_to_seller
from app.controllers.sellers.delete_product import delete_product
from app.controllers.sellers.upgrade_product import upgrade_product

app = create_app()

# controladores
@app.route('/create_user', methods=['POST'])
def route_create_user():
    return create_user()

@app.route('/login', methods=['POST'])
def route_login():
    return login()

@app.route('/create_product', methods=['POST'])
def route_create_product():
    return create_product()

@app.route('/get_seller_data', methods=['POST'])
def route_get_seller_data():
    return get_seller_data()

@app.route('/get_seller_products', methods=['POST'])
def route_get_seller_products():
    return get_seller_products()

@app.route('/get_user_data', methods=['POST'])
def route_get_user_data():
    return get_user_data()

@app.route('/user_to_seller', methods=['POST'])
def route_user_to_seller():
    return user_to_seller()

@app.route('/delete_product', methods=['POST'])
def route_delete_product():
    return delete_product()

@app.route('/upgrade_product', methods=['POST'])
def route_upgrade_product():
    return upgrade_product()