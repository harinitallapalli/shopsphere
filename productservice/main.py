from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
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
        "rating": 4.8,
"reviews": 2450,
"discount": "15% OFF",
"stock": 8
    },
    {
        "name": "iPhone 15",
        "price": 75000,
        "description": "Latest flagship smartphone",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500",
        "rating": 4.9,
"reviews": 5321,
"discount": "10% OFF",
"stock": 5

    },
    {
        "name": "Headphones",
        "price": 3500,
        "description": "Wireless noise-cancelling headphones",
        "category": "Audio",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "rating": 4.4,
"reviews": 1150,
"discount": "25% OFF",
"stock": 23
    },
    {
        "name": "Smartwatch",
        "price": 25000,
        "description": "Smart wearable device",
        "category": "Wearables",
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500",
        "rating": 4.6,
"reviews": 1870,
"discount": "18% OFF",
"stock": 10
    },
    {
        "name": "Monitor",
        "price": 15000,
        "description": "4K UHD display monitor",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
       "rating": 4.7,
"reviews": 920,
"discount": "12% OFF",
"stock": 11
    },
    {
        "name": "Keyboard",
        "price": 5000,
        "description": "Mechanical gaming keyboard",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500",
        "rating": 4.6,
"reviews": 980,
"discount": "20% OFF",
"stock": 17
    },
    {
        "name": "Mouse",
        "price": 1500,
        "description": "Wireless ergonomic mouse",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500",
        "rating": 4.5,
"reviews": 850,
"discount": "20% OFF",
"stock": 15
    },
    {
        "name": "Webcam",
        "price": 4000,
        "description": "1080p HD webcam with microphone",
        "category": "Peripherals",
        "image_url": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=500",
        "rating": 4.3,
"reviews": 600,"discount": "15% OFF",
"stock": 20
    },
     {
         "name": "Gaming Headphones",
    "price": 3500,
    "description": "Wireless noise-cancelling headphones",
    "category": "Audio",
    "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
    "rating": 4.8,
    "reviews": 2250,
    "discount": "22% OFF",
    "stock": 14
    },

    {
        "name": "Nike Shoes",
        "price": 4500,
        "description": "Comfortable running shoes",
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
        "rating": 4.7,
"reviews": 3110,
"discount": "45% OFF",
"stock": 7
    },

    {
        "name": "Denim Jacket",
        "price": 2200,
        "description": "Trendy blue denim jacket",
        "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
        "rating": 4.5,
"reviews": 980,
"discount": "35% OFF",
"stock": 16
    },

    {
        "name": "Face Wash",
        "price": 299,
        "description": "Deep cleansing face wash",
        "category": "Skincare",
        "image_url": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500",
       "rating": 4.2,
"reviews": 500,
"discount": "20% OFF",
"stock": 35
    },

    {
        "name": "Vitamin C Serum",
        "price": 799,
        "description": "Brightening skincare serum",
        "category": "Skincare",
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500",
        "rating": 4.8,
"reviews": 2760,
"discount": "25% OFF",
"stock": 13
    },

    {
        "name": "Lipstick Set",
        "price": 999,
        "description": "Long-lasting matte shades",
        "category": "Makeup",
        "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500",
        "rating": 4.6,
"reviews": 1490,
"discount": "30% OFF",
"stock": 18
    },

    {
        "name": "Perfume",
        "price": 1499,
        "description": "Luxury fragrance collection",
        "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500",
        "rating": 4.9,
"reviews": 4021,
"discount": "15% OFF",
"stock": 6

    },

    {
        "name": "Hand Sanitizer",
        "price": 149,
        "description": "Kills 99.9% germs",
        "category": "Healthcare",
        "image_url": "https://images.unsplash.com/photo-1584744982491-665216d95f8b?w=500",
       "rating": 4.1,
"reviews": 245,
"discount": "50% OFF",
"stock": 48
    },

    {
        "name": "Protein Powder",
        "price": 2499,
        "description": "Muscle recovery supplement",
        "category": "Healthcare",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=500",
        "rating": 4.7,
"reviews": 1680,
"discount": "18% OFF",
"stock": 20
    },

    {
        "name": "Smartwatch",
        "price": 25000,
        "description": "Smart wearable device",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500",
        "rating": 4.4,
"reviews": 640,
"discount": "35% OFF",
"stock": 12
    },

    {
        "name": "Power Bank",
        "price": 2000,
        "description": "20000mAh portable charger",
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500",
        "rating": 4.5,
"reviews": 850,
"discount": "20% OFF",
"stock": 15
    },
    {
    "name": "Adidas Hoodie",
    "price": 1999,
    "description": "Winter special hoodie | 40% OFF",
    "category": "Clothing",
    "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
    "rating": 4.8,
"reviews": 2210,
"discount": "40% OFF",
"stock": 9
},

{
    "name": "Maybelline Makeup Kit",
    "price": 1299,
    "description": "Best seller | Limited Deal",
    "category": "Makeup",
    "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
   "rating": 4.6,
"reviews": 1840,
"discount": "28% OFF",
"stock": 12
},

{
    "name": "Sunscreen SPF50",
    "price": 599,
    "description": "Dermatologist recommended",
    "category": "Skincare",
    "image_url": "https://images.unsplash.com/photo-1612817288484-6f916006741a?w=500",
   "rating": 4.7,
"reviews": 1160,
"discount": "20% OFF",
"stock": 30
},

{
    "name": "Yoga Mat",
    "price": 899,
    "description": "Fitness essentials",
    "category": "Healthcare",
    "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500",
    "rating": 4.3,
"reviews": 440,
"discount": "25% OFF",
"stock": 22
},

{
    "name": "Casual T-Shirt",
    "price": 699,
    "description": "Trending fashion item",
    "category": "Fashion",
    "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",
    "rating": 4.4,
"reviews": 840,
"discount": "35% OFF",
"stock": 27
},

{
    "name": "Wireless Earbuds",
    "price": 2999,
    "description": "New arrival | Noise cancellation",
    "category": "Electronics",
    "image_url": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=500",
    "rating": 4.8,
"reviews": 9200,
"discount": "50% OFF",
"stock": 11
},

{
    "name": "Deal of the Day Laptop Bag",
    "price": 999,
    "description": "🔥 60% OFF today only",
    "category": "Deals",
    "image_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500",
    "rating": 4.5,
"reviews": 970,
"discount": "60% OFF",
"stock": 4
}
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
            image_url TEXT,
            rating REAL,
            reviews INTEGER,
            discount TEXT,
            stock INTEGER
        )
    """)
    conn.commit()

# ✅ Insert sample products
# ✅ Insert sample products
def init_sample_products():
    ensure_schema()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        for product in SAMPLE_PRODUCTS:
            cursor.execute("""
                INSERT INTO products
                (
                    name,
                    price,
                    description,
                    category,
                    image_url,
                    rating,
                    reviews,
                    discount,
                    stock
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product["name"],
                product["price"],
                product["description"],
                product["category"],
                product["image_url"],
                product["rating"],
                product["reviews"],
                product["discount"],
                product["stock"]
            ))

        conn.commit()
        print(f"✅ Added {len(SAMPLE_PRODUCTS)} sample products")
# ✅ Initialize database
init_sample_products()


class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = "Uncategorized"
    image_url: Optional[str] = ""
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 100
    discount: Optional[str] = "10% OFF"
    stock: Optional[int] = 20


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    discount: Optional[str] = None
    stock: Optional[int] = None


def row_to_product(row) -> dict:
    return {
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "description": row[3],
        "category": row[4],
        "image_url": row[5],
        "rating": row[6],
        "reviews": row[7],
        "discount": row[8],
        "stock": row[9],
    }


PRODUCT_COLUMNS = """
    id, name, price, description, category, image_url, rating, reviews, discount, stock
"""


# ✅ Home route
@app.get("/")
def home():
    return {
        "service": "Product Service Running",
        "version": "2.0"
    }


# ✅ Search products
@app.get("/search")
def search_products(q: str = Query("", min_length=0)):
    query = q.strip().lower()
    cursor.execute(f"""
        SELECT {PRODUCT_COLUMNS}
        FROM products
        WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(category) LIKE ?
        ORDER BY id
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    return [row_to_product(row) for row in rows]


# ✅ Add product
@app.post("/add-product")
@app.post("/products")
def add_product(product: ProductCreate):

    cursor.execute("""
        INSERT INTO products
        (
            name,
            price,
            description,
            category,
            image_url,
            rating,
            reviews,
            discount,
            stock
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product.name,
        product.price,
        product.description,
        product.category,
        product.image_url,
        product.rating,
        product.reviews,
        product.discount,
        product.stock,
    ))

    conn.commit()
    product_id = cursor.lastrowid

    return {"message": "Product added successfully", "id": product_id}


# ✅ Get all products
@app.get("/products")
def get_products(category: Optional[str] = Query(None)):
    if category and category.lower() != "all":
        cursor.execute(f"""
            SELECT {PRODUCT_COLUMNS}
            FROM products
            WHERE category = ?
            ORDER BY id
        """, (category,))
    else:
        cursor.execute(f"""
            SELECT {PRODUCT_COLUMNS}
            FROM products
            ORDER BY id
        """)

    rows = cursor.fetchall()
    return [row_to_product(row) for row in rows]


# ✅ Get single product
@app.get("/products/{product_id}")
def get_product(product_id: int):
    cursor.execute(f"""
        SELECT {PRODUCT_COLUMNS}
        FROM products
        WHERE id = ?
    """, (product_id,))

    row = cursor.fetchone()
    if row:
        return row_to_product(row)

    raise HTTPException(status_code=404, detail="Product not found")


# ✅ Update product
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    cursor.execute(f"SELECT {PRODUCT_COLUMNS} FROM products WHERE id = ?", (product_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    current = row_to_product(existing)
    updates = product.model_dump(exclude_unset=True)
    for key, value in updates.items():
        current[key] = value

    cursor.execute("""
        UPDATE products
        SET name = ?, price = ?, description = ?, category = ?,
            image_url = ?, rating = ?, reviews = ?, discount = ?, stock = ?
        WHERE id = ?
    """, (
        current["name"],
        current["price"],
        current["description"],
        current["category"],
        current["image_url"],
        current["rating"],
        current["reviews"],
        current["discount"],
        current["stock"],
        product_id,
    ))
    conn.commit()
    return {"message": "Product updated successfully", "product": current}


# ✅ Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Product not found")

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    return {"message": "Product deleted successfully"}