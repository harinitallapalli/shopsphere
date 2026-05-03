from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# ✅ ADD THIS BLOCK HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("products.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    category TEXT
)
""")
conn.commit()

# 🔹 Sample Products to be added on startup
SAMPLE_PRODUCTS = [
    {"name": "Laptop", "price": 50000, "description": "High-performance laptop", "category": "Electronics"},
    {"name": "iPhone 15", "price": 75000, "description": "Latest Apple smartphone", "category": "Electronics"},
    {"name": "Headphones", "price": 3500, "description": "Wireless noise-cancelling headphones", "category": "Audio"},
    {"name": "Smartwatch", "price": 25000, "description": "Smart wearable device", "category": "Wearables"},
    {"name": "USB-C Cable", "price": 500, "description": "High-speed USB-C charging cable", "category": "Accessories"},
    {"name": "Power Bank", "price": 2000, "description": "20000mAh portable power bank", "category": "Accessories"},
    {"name": "Monitor", "price": 15000, "description": "4K UHD display monitor", "category": "Electronics"},
    {"name": "Keyboard", "price": 5000, "description": "Mechanical gaming keyboard", "category": "Peripherals"},
    {"name": "Mouse", "price": 1500, "description": "Wireless ergonomic mouse", "category": "Peripherals"},
    {"name": "Webcam", "price": 4000, "description": "1080p HD webcam with microphone", "category": "Peripherals"},
]

def init_sample_products():
    """Initialize database with sample products if empty"""
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    if count == 0:
        for product in SAMPLE_PRODUCTS:
            cursor.execute(
                "INSERT INTO products (name, price, description, category) VALUES (?, ?, ?, ?)",
                (product["name"], product["price"], product["description"], product["category"])
            )
        conn.commit()
        print(f"✅ Added {len(SAMPLE_PRODUCTS)} sample products to database")

# Initialize products on startup
init_sample_products()

@app.get("/")
def home():
    return {"service": "Product Service Running", "version": "2.0"}

@app.post("/add-product")
def add_product(product: dict):
    cursor.execute(
        "INSERT INTO products (name, price, description, category) VALUES (?, ?, ?, ?)",
        (product.get("name"), product.get("price"), product.get("description", ""), product.get("category", "Uncategorized"))
    )
    conn.commit()
    return {"message": "Product added successfully"}

@app.get("/products")
def get_products():
    cursor.execute("SELECT id, name, price, description, category FROM products")
    rows = cursor.fetchall()
    
    return [
        {
            "id": r[0],
            "name": r[1],
            "price": r[2],
            "description": r[3],
            "category": r[4]
        }
        for r in rows
    ]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    cursor.execute("SELECT id, name, price, description, category FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "category": row[4]
        }
    return {"error": "Product not found"}