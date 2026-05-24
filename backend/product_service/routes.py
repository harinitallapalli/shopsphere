from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from .database import PRODUCT_COLUMNS, get_connection, init_db, row_to_product
from .models import ProductCreate, ProductUpdate

router = APIRouter()
init_db()


@router.get("/")
def home():
    return {"service": "Product Service Running", "version": "2.0"}


@router.get("/search")
def search_products(q: str = Query("", min_length=0)):
    query = q.strip().lower()
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT {PRODUCT_COLUMNS} FROM products
        WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(category) LIKE ?
        ORDER BY id
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%"),
    ).fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]


@router.get("/products")
def get_products(category: Optional[str] = Query(None)):
    conn = get_connection()
    if category and category.lower() != "all":
        rows = conn.execute(
            f"SELECT {PRODUCT_COLUMNS} FROM products WHERE category = ? ORDER BY id",
            (category,),
        ).fetchall()
    else:
        rows = conn.execute(f"SELECT {PRODUCT_COLUMNS} FROM products ORDER BY id").fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]


@router.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    row = conn.execute(
        f"SELECT {PRODUCT_COLUMNS} FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return row_to_product(row)


@router.post("/add-product")
@router.post("/products")
def add_product(product: ProductCreate):
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO products (name, price, description, category, image_url, rating, reviews, discount, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product.name, product.price, product.description, product.category,
            product.image_url, product.rating, product.reviews, product.discount, product.stock,
        ),
    )
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return {"message": "Product added successfully", "id": product_id}


@router.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    conn = get_connection()
    existing = conn.execute(
        f"SELECT {PRODUCT_COLUMNS} FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    current = row_to_product(existing)
    for key, value in product.model_dump(exclude_unset=True).items():
        current[key] = value

    conn.execute(
        """
        UPDATE products SET name=?, price=?, description=?, category=?,
        image_url=?, rating=?, reviews=?, discount=?, stock=? WHERE id=?
        """,
        (
            current["name"], current["price"], current["description"], current["category"],
            current["image_url"], current["rating"], current["reviews"], current["discount"],
            current["stock"], product_id,
        ),
    )
    conn.commit()
    conn.close()
    return {"message": "Product updated successfully", "product": current}


@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()
    if not conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"message": "Product deleted successfully"}
