import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from recommend import df, get_book_image, recommend
from fastapi import Form
from fastapi.responses import RedirectResponse
from database import conn


app = FastAPI(title="Reading Realm AI")

users = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set absolute path to frontend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")

# Mount /images
if os.path.exists(IMAGES_DIR):
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# Home Page
# Home Page
@app.get("/")
def home():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "register.html"),
        headers={"Cache-Control": "no-cache"}
    )
# Browse Books Page
@app.get("/books")
def books():
    return FileResponse(os.path.join(FRONTEND_DIR, "books.html"))

# Recommendation API
@app.get("/recommend/{book_name}")
def get_recommendations(book_name: str):
    return recommend(book_name)

# 1. Full Books Catalog API
@app.get("/api/catalog")
def get_catalog():
    catalog = []
    for idx, row in df.iterrows():
        book_dict = {
            "title": str(row.get("title", "")),
            "author": str(row.get("author", "")),
            "genre": str(row.get("genre", "")),
            "rating": float(row.get("rating", 4.5)),
            "price": int(row.get("price", 299)),
            "image": get_book_image(row)
        }
        catalog.append(book_dict)
    return catalog

# 2. Checkout & Order Placement API
@app.post("/api/checkout")
def checkout(order: dict):
    items = order.get("items", [])
    total_amount = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
    order_id = f"RR-{random.randint(100000, 999999)}"
    
    return {
        "status": "success",
        "order_id": order_id,
        "total_amount": total_amount,
        "item_count": len(items),
        "message": "Order placed successfully!"
    }
@app.get("/book_details")
def book_details():
    return FileResponse(os.path.join(FRONTEND_DIR, "book_details.html"))


# --------------------------
# Pages
# --------------------------

@app.get("/register")
def register_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))


@app.get("/login")
def login_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))


@app.get("/index")
def index_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# --------------------------
# Register API
# --------------------------

@app.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    cur = conn.cursor()

    # Check if email already exists
    cur.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    if cur.fetchone():
        cur.close()
        return {
            "success": False,
            "message": "Email already exists"
        }

    # Insert new user
    cur.execute(
        """
        INSERT INTO users (username, email, password, name, role)
        VALUES (%s, %s, %s, %s, 'user')
        """,
        (username, email, password, username)
    )

    conn.commit()
    cur.close()

    return {
        "success": True,
        "message": "Registration Successful"
    }
#----------------
# Login API
# --------------------------

from fastapi.responses import JSONResponse

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT username, role
        FROM users
        WHERE email=%s AND password=%s
        """,
        (email, password)
    )

    user = cur.fetchone()
    cur.close()

    if not user:
        return JSONResponse(
            {
                "success": False,
                "message": "Invalid email or password"
            },
            status_code=401
        )

    username, role = user

    return {
        "success": True,
        "message": "Login Successful",
        "username": username,
        "role": role,
        "redirect": "/admin" if role == "admin" else "/index"
    }

@app.get("/admin")
def admin_dashboard():
    cur = conn.cursor()

    # Total Books
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    # Total Users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.close()

    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))
@app.get("/api/admin/stats")
def admin_stats():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM books")
    books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.close()

    return {
        "books": books,
        "users": users,
        "orders": 0,
        "revenue": 0
    }
@app.get("/add-book")
def add_book_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "add_book.html"))

@app.post("/api/add-book")
def add_book(
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    description: str = Form(...),
    rating: float = Form(...),
    price: int = Form(...),
    image: str = Form(...)
):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO books
        (title, author, genre, description, rating, price, image)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,
    (title, author, genre, description, rating, price, image))

    conn.commit()
    cur.close()

    return {
        "success": True,
        "message": "Book Added Successfully!"
    }
@app.get("/manage-books")
def manage_books():
    return FileResponse(os.path.join(FRONTEND_DIR, "manage_books.html"))
@app.get("/api/manage-books")
def get_all_books():

    cur = conn.cursor()

    cur.execute("""
        SELECT
        id,
        title,
        author,
        genre,
        rating,
        price,
        image
        FROM books
        ORDER BY id DESC
    """)

    books = cur.fetchall()

    cur.close()

    return [
        {
            "id": b[0],
            "title": b[1],
            "author": b[2],
            "genre": b[3],
            "rating": b[4],
            "price": b[5],
            "image": b[6]
        }
        for b in books
    ]

@app.get("/edit-book/{book_id}")
def edit_book_page(book_id: int):
    return FileResponse(os.path.join(FRONTEND_DIR, "edit_book.html"))

@app.get("/api/book/{book_id}")
def get_book(book_id: int):

    cur = conn.cursor()

    cur.execute("""
        SELECT id,title,author,genre,description,rating,price,image
        FROM books
        WHERE id=%s
    """,(book_id,))

    book = cur.fetchone()

    cur.close()

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
        "image": book[7]
    }

@app.put("/api/update-book/{book_id}")
def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    description: str = Form(...),
    rating: float = Form(...),
    price: int = Form(...),
    image: str = Form(...)
):

    cur = conn.cursor()

    cur.execute("""
        UPDATE books
        SET
            title=%s,
            author=%s,
            genre=%s,
            description=%s,
            rating=%s,
            price=%s,
            image=%s
        WHERE id=%s
    """,
    (title,author,genre,description,rating,price,image,book_id))

    conn.commit()

    cur.close()

    return {
        "success": True,
        "message": "Book Updated Successfully"
    }

@app.get("/manage-users")
def manage_users():
    return FileResponse(os.path.join(FRONTEND_DIR, "manage_users.html"))

@app.get("/api/manage-users")
def get_users():

    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email, role
        FROM users
        ORDER BY id
    """)

    rows = cur.fetchall()

    cur.close()

    return [
        {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "role": row[3]
        }
        for row in rows
    ]


@app.delete("/api/delete-user/{user_id}")
def delete_user(user_id: int):

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )

    conn.commit()

    cur.close()

    return {
        "success": True,
        "message": "User deleted successfully"
    }
@app.post("/api/place-order")
def place_order(
    user_id: int = Form(...),
    book_id: int = Form(...),
    quantity: int = Form(...)
):

    cur = conn.cursor()

    # Get price
    cur.execute(
        "SELECT price FROM books WHERE id=%s",
        (book_id,)
    )

    book = cur.fetchone()

    if not book:
        cur.close()
        return {"success": False, "message": "Book not found"}

    price = book[0]
    total = price * quantity

    cur.execute("""
        INSERT INTO orders(user_id, book_id, quantity, total)
        VALUES (%s, %s, %s, %s)
    """, (user_id, book_id, quantity, total))

    conn.commit()
    cur.close()

    return {
        "success": True,
        "message": "Order Placed Successfully!"
    }

@app.get("/api/orders")
def get_orders():

    cur = conn.cursor()

    cur.execute("""
        SELECT
            o.id,
            u.username,
            b.title,
            o.quantity,
            o.total,
            o.status
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN books b ON o.book_id = b.id
        ORDER BY o.id DESC
    """)

    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id": r[0],
            "username": r[1],
            "book": r[2],
            "quantity": r[3],
            "total": r[4],
            "status": r[5]
        }
        for r in rows
    ]
@app.get("/order_success", response_class=HTMLResponse)
def order_success(request: Request):
    return templates.TemplateResponse(
        "order_success.html",
        {"request": request}
    )
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")