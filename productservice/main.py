from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Database setup
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "products.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ✅ Sample products
SAMPLE_PRODUCTS = [
    {
        "name": "Laptop",
        "price": 50000,
        "description": "High-performance laptop",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
    },
    {
        "name": "iPhone 15",
        "price": 75000,
        "description": "Latest flagship smartphone",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500",
    },
    {
        "name": "Headphones",
        "price": 3500,
        "description": "Wireless noise-cancelling headphones",
        "category": "Audio",
        "image_url": "https://images.unsplash.com/photo-1510070009289-b5bc34383727?w=500",
    },
    {
        "name": "Smartwatch",
        "price": 25000,
        "description": "Smart wearable device",
        "category": "Wearables",
        "image_url": "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=500",
    },
    {
        "name": "USB-C Cable",
        "price": 500,
        "description": "High-speed USB-C charging cable",
        "category": "Accessories",
        "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500",
    },
    {
        "name": "Power Bank",
        "price": 2000,
        "description": "20000mAh portable power bank",
        "category": "Accessories",
        "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500",
    },
    {
        "name": "Monitor",
        "price": 15000,
        "description": "4K UHD display monitor",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
    },
    {
        "name": "Keyboard",
        "price": 5000,
        "description": "Mechanical gaming keyboard",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500",
    },
    {
        "name": "Mouse",
        "price": 1500,
        "description": "Wireless ergonomic mouse",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500",
    },
    {
        "name": "Webcam",
        "price": 4000,
        "description": "1080p HD webcam with microphone",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=500",
    },
]

# ✅ Create table
def ensure_schema():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            category TEXT,
            image_url TEXT
        )
    """)
    conn.commit()

# ✅ Insert sample products
def init_sample_products():
    ensure_schema()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        for product in SAMPLE_PRODUCTS:
            cursor.execute("""
                INSERT INTO products
                (name, price, description, category, image_url)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product["name"],
                product["price"],
                product["description"],
                product["category"],
                product["image_url"]
            ))

        conn.commit()
        print(f"✅ Added {len(SAMPLE_PRODUCTS)} sample products")

# ✅ Initialize database
init_sample_products()

# ✅ Home route
@app.get("/")
def home():
    return {
        "service": "Product Service Running",
        "version": "2.0"
    }

# ✅ Add product
@app.post("/add-product")
def add_product(product: dict):

    cursor.execute("""
        INSERT INTO products
        (name, price, description, category, image_url)
        VALUES (?, ?, ?, ?, ?)
    """, (
        product.get("name"),
        product.get("price"),
        product.get("description", ""),
        product.get("category", "Uncategorized"),
        product.get("image_url", "")
    ))

    conn.commit()

    return {"message": "Product added successfully"}

# ✅ Get all products
@app.get("/products")
def get_products():

    cursor.execute("""
        SELECT id, name, price, description, category, image_url
        FROM products
    """)

    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "category": row[4],
            "image_url": row[5],
        }
        for row in rows
    ]

# ✅ Get single product
@app.get("/products/{product_id}")
def get_product(product_id: int):

    cursor.execute("""
        SELECT id, name, price, description, category, image_url
        FROM products
        WHERE id = ?
    """, (product_id,))

    row = cursor.fetchone()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "category": row[4],
            "image_url": row[5],
        }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )