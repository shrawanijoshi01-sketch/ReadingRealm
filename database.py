import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Readingrealm",
    user="postgres",
    password="admin@123",
    port="5432"
)

cursor = conn.cursor()