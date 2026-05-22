import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi import Header
from datetime import datetime

from auth_utils import get_current_user, get_current_user_optional

app = FastAPI(title="ShopSphere Order Service", version="2.0")
print("LIVE TRACKING VERSION LOADED")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "orders.db")


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            category TEXT,
            image_url TEXT,
            rating REAL,
            reviews INTEGER,
            discount TEXT,
            stock INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'completed',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            category TEXT,
            image_url TEXT,
            rating REAL,
            reviews INTEGER,
            discount TEXT,
            stock INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );
        """
    )
    conn.commit()
    conn.close()


def row_to_item(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["product_id"] or row["id"],
        "product_id": row["product_id"],
        "name": row["name"],
        "price": row["price"],
        "description": row["description"],
        "category": row["category"],
        "image_url": row["image_url"],
        "rating": row["rating"],
        "reviews": row["reviews"],
        "discount": row["discount"],
        "stock": row["stock"],
        "quantity": row["quantity"],
    }


class CartItemPayload(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = "Uncategorized"
    image_url: Optional[str] = ""
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 100
    discount: Optional[str] = "10% OFF"
    stock: Optional[int] = 20
    quantity: int = Field(default=1, ge=1)


class RemoveCartPayload(BaseModel):
    index: int = Field(ge=0)


class PayPayload(BaseModel):
    order_id: Optional[int] = None


init_db()


@app.get("/")
def home():
    return {"service": "Order Service Running", "version": "2.0"}


@app.post("/add-to-cart")
@app.post("/cart/add")
def add_to_cart(
    item: CartItemPayload,
    username: str = Depends(get_current_user),
):
    product_id = item.product_id or item.id
    conn = get_db()
    existing = conn.execute(
        """
        SELECT id, quantity FROM cart_items
        WHERE username = ? AND product_id = ? AND name = ?
        """,
        (username, product_id, item.name),
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE cart_items SET quantity = quantity + ? WHERE id = ?",
            (item.quantity, existing["id"]),
        )
    else:
        conn.execute(
            """
            INSERT INTO cart_items (
                username, product_id, name, price, description, category,
                image_url, rating, reviews, discount, stock, quantity, added_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                product_id,
                item.name,
                item.price,
                item.description,
                item.category,
                item.image_url,
                item.rating,
                item.reviews,
                item.discount,
                item.stock,
                item.quantity,
                datetime.utcnow().isoformat(),
            ),
        )

    conn.commit()
    cart = _fetch_cart_rows(conn, username)
    conn.close()
    return {
        "message": "Item added to cart",
        "success": True,
        "items": [row_to_item(row) for row in cart],
        "total": _calculate_total(cart),
    }


@app.get("/cart")
def get_cart(username: Optional[str] = Depends(get_current_user_optional)):
    conn = get_db()
    if username:
        rows = _fetch_cart_rows(conn, username)
    else:
        rows = conn.execute(
            "SELECT * FROM cart_items ORDER BY id"
        ).fetchall()
    conn.close()
    return [row_to_item(row) for row in rows]


@app.delete("/cart/{item_index}")
@app.post("/remove-from-cart")
def remove_from_cart(
    item_index: Optional[int] = None,
    payload: Optional[RemoveCartPayload] = None,
    username: str = Depends(get_current_user),
):
    index = item_index if item_index is not None else (payload.index if payload else None)
    if index is None:
        raise HTTPException(status_code=400, detail="Item index is required")

    conn = get_db()
    rows = _fetch_cart_rows(conn, username)
    if index < 0 or index >= len(rows):
        conn.close()
        raise HTTPException(status_code=404, detail="Cart item not found")

    conn.execute("DELETE FROM cart_items WHERE id = ?", (rows[index]["id"],))
    conn.commit()
    updated = _fetch_cart_rows(conn, username)
    conn.close()
    return {
        "message": "Item removed from cart",
        "items": [row_to_item(row) for row in updated],
        "total": _calculate_total(updated),
    }


@app.post("/clear-cart")
def clear_cart(username: str = Depends(get_current_user)):
    conn = get_db()
    conn.execute("DELETE FROM cart_items WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return {"message": "Cart cleared", "success": True}


@app.post("/place-order")
def place_order(username: Optional[str] = Depends(get_current_user_optional)):
    conn = get_db()
    if username:
        rows = _fetch_cart_rows(conn, username)
        clear_sql = ("DELETE FROM cart_items WHERE username = ?", (username,))
    else:
        rows = conn.execute("SELECT * FROM cart_items ORDER BY id").fetchall()
        clear_sql = ("DELETE FROM cart_items", ())

    if not rows:
        conn.close()
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_user = username or "guest"
    total = _calculate_total(rows)
    created_at = datetime.utcnow().isoformat()

    cursor = conn.execute(
        """
        INSERT INTO orders (username, total, status, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (order_user, total, "completed", created_at),
    )
    order_id = cursor.lastrowid

    for row in rows:
        conn.execute(
            """
            INSERT INTO order_items (
                order_id, product_id, name, price, description, category,
                image_url, rating, reviews, discount, stock, quantity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order_id,
                row["product_id"],
                row["name"],
                row["price"],
                row["description"],
                row["category"],
                row["image_url"],
                row["rating"],
                row["reviews"],
                row["discount"],
                row["stock"],
                row["quantity"],
            ),
        )

    conn.execute(clear_sql[0], clear_sql[1])
    conn.commit()
    conn.close()

    return {
        "message": "Order placed",
        "success": True,
        "order_id": order_id,
        "total": total,
        "status": "completed",
        "created_at": created_at,
    }

@app.get("/orders")
def get_orders(username: Optional[str] = Depends(get_current_user_optional)):
    conn = get_db()

    if username:
        order_rows = conn.execute(
            """
            SELECT id,total,status,created_at
            FROM orders
            WHERE username = ?
            ORDER BY id DESC
            """,
            (username,),
        ).fetchall()
    else:
        order_rows = conn.execute(
            """
            SELECT id,total,status,created_at
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

    detailed_orders = []

    for order in order_rows:
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id",
            (order["id"],),
        ).fetchall()

        item_list = [row_to_item(item) for item in items]

        detailed_orders.append(
    {
        "order_id": order["id"],
        "total": order["total"],
        "status": "paid",
        "status_label": "Order Shipped",
        "tracking_number": f"TRK{order['id']}123",
        "delivery_progress": 65,
        "is_delivered": False,
        "estimated_delivery": datetime.utcnow().isoformat(),
        "created_at": order["created_at"],
        "items": item_list,
    }
)

    conn.close()

    return detailed_orders


@app.get("/orders/detail")
def get_orders_detail(username: str = Depends(get_current_user)):
    conn = get_db()

    order_rows = conn.execute(
        """
        SELECT id,total,status,created_at
        FROM orders
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,),
    ).fetchall()

    result = []

    for order in order_rows:
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id",
            (order["id"],),
        ).fetchall()

        result.append(
            {
                "order_id": order["id"],
                "total": order["total"],
                "status": order["status"],
                "created_at": order["created_at"],
                "items": [row_to_item(item) for item in items],
            }
        )

    conn.close()

    return result


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_db()

    order = conn.execute(
        """
        SELECT id,total,status,created_at
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    if not order:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    items = conn.execute(
        """
        SELECT * FROM order_items
        WHERE order_id = ?
        ORDER BY id
        """,
        (order_id,)
    ).fetchall()

    conn.close()

    return {
        "order_id": order["id"],
        "total": order["total"],
        "status": "paid",
        "status_label": "Order Shipped",
        "tracking_number": f"TRK{order_id}123",
        "delivery_progress": 65,
        "is_delivered": False,
        "estimated_delivery": datetime.utcnow().isoformat(),

        "delivery_partner": {
            "name": "Rahul Kumar",
            "phone": "9876543210",
            "vehicle": "Bike"
        },

        "timeline": [
            {
                "title": "Order Placed",
                "message": "Your order has been placed",
                "location": "Warehouse",
                "event_at": datetime.utcnow().isoformat()
            },
            {
                "title": "Shipped",
                "message": "Package left facility",
                "location": "Hyderabad",
                "event_at": datetime.utcnow().isoformat()
            }
        ],

        "items": [row_to_item(item) for item in items],
    }
@app.get("/orders/{order_id}/live-tracking")
def get_live_tracking(
    order_id: int,
    authorization: str = Header(None)
):
    return {
        "order_id": order_id,

        "delivery_partner": {
            "name": "Rahul Kumar",
            "phone": "9876543210",
            "vehicle": "Bike"
        },

        "current_location": {
            "lat": 17.3850,
            "lng": 78.4867
        },

        "destination": {
            "lat": 17.4435,
            "lng": 78.3772
        },

        "progress": 65,

        "updated_at": datetime.utcnow().isoformat()
    }

@app.post("/pay")
def pay(
    payload: Optional[PayPayload] = None,
    username: str = Depends(get_current_user),
):
    conn = get_db()
    if payload and payload.order_id:
        order = conn.execute(
            "SELECT id FROM orders WHERE id = ? AND username = ?",
            (payload.order_id, username),
        ).fetchone()
        if not order:
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
        conn.execute(
            "UPDATE orders SET status = 'paid' WHERE id = ?",
            (payload.order_id,),
        )
    conn.commit()
    conn.close()
    return {"message": "Payment successful", "success": True}


def _fetch_cart_rows(conn: sqlite3.Connection, username: str):
    return conn.execute(
        """
        SELECT * FROM cart_items
        WHERE username = ?
        ORDER BY id
        """,
        (username,),
    ).fetchall()


def _calculate_total(rows) -> float:
    return sum((row["price"] or 0) * (row["quantity"] or 1) for row in rows)
