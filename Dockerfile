# Usamos una imagen base de Python 3.9 slim
FROM python:3.9-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto a la carpeta /app dentro del contenedor
COPY . /app

# Instalar las dependencias del sistema que necesitamos para psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde se ejecutará tu aplicación (5001 para Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
