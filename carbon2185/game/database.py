import psycopg2
from psycopg2 import sql

def create_connection():
    conn = psycopg2.connect(
        dbname="carbon2185",
        user="carbon_user",
        password="carbon_password",
        host="0.0.0.0",
        port="5432"
    )
    return conn
