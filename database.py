import os
import psycopg2
from dotenv import load_dotenv

# Load .env file (for local development)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    if DATABASE_URL:
        print("✅ Connecting to Render PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
    else:
        print("✅ Connecting to Local PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="Readingrealm",
            user="postgres",
            password="admin@123"  # Replace with your local password
        )

    cursor = conn.cursor()
    print("✅ Database connected successfully!")

except Exception as e:
    print("❌ Database connection failed:")
    print(e)
    conn = None
    cursor = None