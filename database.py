import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render
    conn = psycopg2.connect(DATABASE_URL)
else:
    # Local PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Readingrealm",
        user="postgres",
        password="admin@123"   # <-- Replace with your password
    )

cursor = conn.cursor()