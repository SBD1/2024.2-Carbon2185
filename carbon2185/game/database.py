import psycopg2

def create_connection():
    conn = psycopg2.connect(
        dbname="carbon2185",
        user="carbon_user",
        password="carbon_password",
        host="postgres",
        port="5432"
    )
    return conn