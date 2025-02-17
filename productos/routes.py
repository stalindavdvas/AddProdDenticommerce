# productos/routes.py
from . import productos_bp  # Importar el Blueprint desde el módulo productos
from flask import request, jsonify
from database import get_db_connection

# Registrar la ruta POST /productos en el Blueprint
@productos_bp.route('', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto con una URL de imagen"""
    data = request.get_json()
    nombre = data.get('name')
    descripcion = data.get('description')
    precio = data.get('price')
    stock = data.get('stock')
    categoria_id = data.get('category_id')
    imagen_url = data.get('image_url')

    if not (nombre and precio and categoria_id):
        return jsonify({'error': 'Name, price and category are Required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO products (name, description, price, stock, category_id, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, name, description, price, stock, category_id, image_url;
        """
        cursor.execute(query, (nombre, descripcion, precio, stock, categoria_id, imagen_url))
        producto = cursor.fetchone()
        conn.commit()

        return jsonify({
            'id': producto[0],
            'name': producto[1],
            'description': producto[2],
            'price': producto[3],
            'stock': producto[4],
            'category_id': producto[5],
            'image_url': producto[6]
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()