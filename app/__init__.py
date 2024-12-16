from flask import Flask

def create_app():
    app = Flask(__name__)

    # Aquí puedes agregar configuraciones, como rutas, bases de datos, etc.
    #from . import routes  # Importa las rutas de la aplicación

    return app
