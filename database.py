# database.py
import psycopg2

# Postgres Config
def get_db_connection():
    return psycopg2.connect(
        host="98.84.245.136",
        database="items",
        user="stalin",
        password="stalin"
    )