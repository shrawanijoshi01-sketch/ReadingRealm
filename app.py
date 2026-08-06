import os
import random
from pathlib import Path
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Reading Realm AI")

# ----------------------------------------------------
# 1. Absolute Paths & Directory Setup
# ----------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()

if CURRENT_FILE.parent.name == "backend":
    BACKEND_DIR = CURRENT_FILE.parent
    PROJECT_ROOT = BACKEND_DIR.parent
else:
    PROJECT_ROOT = CURRENT_FILE.parent
    BACKEND_DIR = PROJECT_ROOT

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")

print("=" * 60)
print(f"DEBUG: PROJECT_ROOT -> {PROJECT_ROOT}")
print(f"DEBUG: FRONTEND_DIR -> {FRONTEND_DIR}")
print(
    f"DEBUG: register.html exists -> {os.path.exists(os.path.join(FRONTEND_DIR, 'register.html'))}"
)
print("=" * 60)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safe folder creation and static assets mounting
os.makedirs(IMAGES_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ----------------------------------------------------
# 2. Safe Database & Recommendation Imports
# ----------------------------------------------------
df = None
get_book_image = None
recommend = None
conn = None

try:
    from backend.recommend import df, get_book_image, recommend
    print("✅ Successfully imported backend.recommend")
except Exception:
    try:
        from recommend import df, get_book_image, recommend
        print("✅ Successfully imported recommend")
    except Exception as e:
        print(f"❌ ERROR importing recommend: {e}")

try:
    from backend.database import conn
    print("✅ Successfully connected to Database")
except Exception:
    try:
        from database import conn
        print("✅ Successfully connected to Database")
    except Exception as e:
        print(f"❌ ERROR importing database connection: {e}")


# Helper function to safely serve frontend pages
def serve_html(filename: str):
    file_path = os.path.join(FRONTEND_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={
                "error": f"File '{filename}' NOT FOUND!",
                "looking_at": file_path,
                "project_root": str(PROJECT_ROOT),
                "frontend_dir_exists": os.path.exists(FRONTEND_DIR),
            },
        )
    return FileResponse(file_path, headers={"Cache-Control": "no-cache"})


# ----------------------------------------------------
# 3. Frontend HTML Page Serving Routes
# ----------------------------------------------------
@app.get("/")
def home():
    return serve_html("register.html")

@app.get("/books")
def books():
    return serve_html("books.html")

@app.get("/book_details")
def book_details():
    return serve_html("book_details.html")

@app.get("/register")
def register_page():
    return serve_html("register.html")

@app.get("/login")
def login_page():
    return serve_html("login.html")

@app.get("/index")
def index_page():
    return serve_html("index.html")

@app.get("/admin")
def admin_dashboard():
    return serve_html("admin.html")

@app.get("/add-book")
def add_book_page():
    return serve_html("add_book.html")

@app.get("/manage-books")
def manage_books():
    return serve_html("manage_books.html")

@app.get("/edit-book/{book_id}")
def edit_book_page(book_id: int):
    return serve_html("edit_book.html")

@app.get("/manage-users")
def manage_users():
    return serve_html("manage_users.html")

@app.get("/order_success")
def order_success():
    return serve_html("order_success.html")


# ----------------------------------------------------
# 4. REST APIs
# ----------------------------------------------------
@app.get("/recommend/{book_name}")
def get_recommendations(book_name: str):
    if not recommend:
        raise HTTPException(
            status_code=503, detail="Recommendation engine unavailable"
        )
    return recommend(book_name)

@app.get("/api/catalog")
def get_catalog():
    if df is None:
        return []

    catalog = []
    for idx, row in df.iterrows():
        book_dict = {
            "title": str(row.get("title", "")),
            "author": str(row.get("author", "")),
            "genre": str(row.get("genre", "")),
            "rating": float(row.get("rating", 4.5)),
            "price": int(row.get("price", 299)),
            "image": (
                get_book_image(row)
                if get_book_image
                else "/images/default.jpg"
            ),
        }
        catalog.append(book_dict)
    return catalog

@app.post("/api/checkout")
def checkout(order: dict):
    items = order.get("items", [])
    total_amount = sum(
        item.get("price", 0) * item.get("quantity", 1) for item in items
    )
    order_id = f"RR-{random.randint(100000, 999999)}"

    return {
        "status": "success",
        "order_id": order_id,
        "total_amount": total_amount,
        "item_count": len(items),
        "message": "Order placed successfully!",
    }

@app.post("/register")
def register(
    username: str = Form(...), email: str = Form(...), password: str = Form(...)
):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            return {"success": False, "message": "Email already exists"}

        cur.execute(
            """
            INSERT INTO users (username, email, password, name, role)
            VALUES (%s, %s, %s, %s, 'user')
            """,
            (username, email, password, username),
        )
        conn.commit()
        return {"success": True, "message": "Registration Successful"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT username, role
            FROM users
            WHERE email=%s AND password=%s
            """,
            (email, password),
        )
        user = cur.fetchone()

        if not user:
            return JSONResponse(
                {"success": False, "message": "Invalid email or password"},
                status_code=401,
            )

        username, role = user
        return {
            "success": True,
            "message": "Login Successful",
            "username": username,
            "role": role,
            "redirect": "/admin" if role == "admin" else "/index",
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.get("/api/admin/stats")
def admin_stats():
    if not conn:
        return {"books": 0, "users": 0, "orders": 0, "revenue": 0}

    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM books")
        books_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM users")
        users_count = cur.fetchone()[0]

        return {
            "books": books_count,
            "users": users_count,
            "orders": 0,
            "revenue": 0,
        }
    except Exception as e:
        conn.rollback()
        return {"books": 0, "users": 0, "orders": 0, "revenue": 0}
    finally:
        cur.close()

@app.post("/api/add-book")
def add_book(
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    description: str = Form(...),
    rating: float = Form(...),
    price: int = Form(...),
    image: str = Form(...),
):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO books (title, author, genre, description, rating, price, image)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (title, author, genre, description, rating, price, image),
        )
        conn.commit()
        return {"success": True, "message": "Book Added Successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.get("/api/manage-books")
def get_all_books():
    if not conn:
        return []

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, title, author, genre, rating, price, image
            FROM books
            ORDER BY id DESC
        """)
        books = cur.fetchall()
        return [
            {
                "id": b[0],
                "title": b[1],
                "author": b[2],
                "genre": b[3],
                "rating": b[4],
                "price": b[5],
                "image": b[6],
            }
            for b in books
        ]
    except Exception:
        conn.rollback()
        return []
    finally:
        cur.close()

@app.get("/api/book/{book_id}")
def get_book(book_id: int):
    if not conn:
        return {"success": False}

    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, title, author, genre, description, rating, price, image
            FROM books
            WHERE id=%s
            """,
            (book_id,),
        )
        book = cur.fetchone()
        if not book:
            return {"success": False}

        return {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "genre": book[3],
            "description": book[4],
            "rating": book[5],
            "price": book[6],
            "image": book[7],
        }
    except Exception:
        conn.rollback()
        return {"success": False}
    finally:
        cur.close()

@app.put("/api/update-book/{book_id}")
def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    description: str = Form(...),
    rating: float = Form(...),
    price: int = Form(...),
    image: str = Form(...),
):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE books
            SET title=%s, author=%s, genre=%s, description=%s, rating=%s, price=%s, image=%s
            WHERE id=%s
            """,
            (title, author, genre, description, rating, price, image, book_id),
        )
        conn.commit()
        return {"success": True, "message": "Book Updated Successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.get("/api/manage-users")
def get_users():
    if not conn:
        return []

    cur = conn.cursor()
    try:
        cur.execute("SELECT id, username, email, role FROM users ORDER BY id")
        rows = cur.fetchall()
        return [
            {"id": row[0], "username": row[1], "email": row[2], "role": row[3]}
            for row in rows
        ]
    except Exception:
        conn.rollback()
        return []
    finally:
        cur.close()

@app.delete("/api/delete-user/{user_id}")
def delete_user(user_id: int):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        return {"success": True, "message": "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.post("/api/place-order")
def place_order(
    user_id: int = Form(...),
    book_id: int = Form(...),
    quantity: int = Form(...),
):
    if not conn:
        raise HTTPException(
            status_code=500, detail="Database connection unavailable"
        )

    cur = conn.cursor()
    try:
        cur.execute("SELECT price FROM books WHERE id=%s", (book_id,))
        book = cur.fetchone()

        if not book:
            return {"success": False, "message": "Book not found"}

        price = book[0]
        total = price * quantity

        cur.execute(
            """
            INSERT INTO orders(user_id, book_id, quantity, total)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, book_id, quantity, total),
        )

        conn.commit()
        return {"success": True, "message": "Order Placed Successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()

@app.get("/api/orders")
def get_orders():
    if not conn:
        return []

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT o.id, u.username, b.title, o.quantity, o.total, o.status
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN books b ON o.book_id = b.id
            ORDER BY o.id DESC
        """)
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "username": r[1],
                "book": r[2],
                "quantity": r[3],
                "total": r[4],
                "status": r[5],
            }
            for r in rows
        ]
    except Exception:
        conn.rollback()
        return []
    finally:
        cur.close()

@app.get("/logout")
def logout(request: Request):
    return RedirectResponse("/login")