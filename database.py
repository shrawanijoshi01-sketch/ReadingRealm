import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Render sometimes sets INTERNAL_DATABASE_URL automatically
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("INTERNAL_DATABASE_URL")

conn = None

if DATABASE_URL:
    # Convert 'postgres://' to 'postgresql://' for SQLAlchemy/psycopg2 compatibility
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        print("✅ Successfully connected to Render Cloud Database")
    except Exception as e:
        print(f"❌ Cloud Database connection failed: {e}")
        conn = None
else:
    print("⚠️ DATABASE_URL not found in environment. Attempting local connection...")
    try:
        LOCAL_URL = "postgresql://postgres:admin%40123@localhost:5432/ReadingRealm"
        conn = psycopg2.connect(LOCAL_URL)
        print("✅ Successfully connected to Local Database")
    except Exception as e:
        print(f"❌ Local Database connection failed: {e}")
        conn = None