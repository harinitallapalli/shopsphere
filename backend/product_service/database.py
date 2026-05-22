import os
import sqlite3

from .seed_data import SAMPLE_PRODUCTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "products.db")

PRODUCT_COLUMNS = """
    id, name, price, description, category, image_url, rating, reviews, discount, stock
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_product(row) -> dict:
    if isinstance(row, sqlite3.Row):
        keys = ["id", "name", "price", "description", "category", "image_url", "rating", "reviews", "discount", "stock"]
        return {k: row[k] for k in keys}
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


def init_db():
    conn = get_connection()
    conn.execute(
        """
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
        """
    )
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        for product in SAMPLE_PRODUCTS:
            conn.execute(
                """
                INSERT INTO products (
                    name, price, description, category, image_url,
                    rating, reviews, discount, stock
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    product["name"],
                    product["price"],
                    product["description"],
                    product["category"],
                    product["image_url"],
                    product["rating"],
                    product["reviews"],
                    product["discount"],
                    product["stock"],
                ),
            )
        conn.commit()
        print(f"Seeded {len(SAMPLE_PRODUCTS)} products")

    sunscreen_url = (
        "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&q=80"
    )
    conn.execute(
        "UPDATE products SET image_url = ? WHERE name = 'Sunscreen SPF50'",
        (sunscreen_url,),
    )
    conn.commit()
    conn.close()
