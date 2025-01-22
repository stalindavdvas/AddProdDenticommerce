from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="host.docker.internal",
        database="items",
        user="postgres",
        password="stalin"
    )

@app.route('/productos', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto con una URL de imagen"""
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    stock = data.get('stock')
    categoria_id = data.get('categoria_id')
    imagen_url = data.get('imagen_url')  # Recibir la URL de la imagen

    if not (nombre and precio and categoria_id):
        return jsonify({'error': 'Nombre, precio y categoría son obligatorios'}), 400

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
            'nombre': producto[1],
            'descripcion': producto[2],
            'precio': producto[3],
            'stock': producto[4],
            'categoria_id': producto[5],
            'image_url': producto[6]
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Bloque __main__ para ejecutar el microservicio en el puerto 5001
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
