# productos/__init__.py
from flask import Blueprint

# Crear un Blueprint para las rutas de productos
productos_bp = Blueprint('productos', __name__)

# Importar las rutas
from . import routes