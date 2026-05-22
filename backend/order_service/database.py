import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

from .tracking import (
    STATUS_LABELS,
    delivery_progress,
    generate_tracking_number,
    estimated_delivery_date,
    status_event_copy,
    target_status_after_payment,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "orders.db")


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _add_column_if_missing(conn, table: str, column: str, definition: str):
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


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
            status TEXT NOT NULL DEFAULT 'placed',
            payment_status TEXT NOT NULL DEFAULT 'pending',
            tracking_number TEXT,
            carrier TEXT DEFAULT 'ShopSphere Express',
            estimated_delivery TEXT,
            shipping_address TEXT,
            payment_method TEXT,
            payment_id TEXT,
            paid_at TEXT,
            shipped_at TEXT,
            delivered_at TEXT,
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
        CREATE TABLE IF NOT EXISTS order_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            location TEXT,
            event_at TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );
        """
    )
    for col, typedef in [
        ("payment_status", "TEXT NOT NULL DEFAULT 'pending'"),
        ("tracking_number", "TEXT"),
        ("carrier", "TEXT DEFAULT 'ShopSphere Express'"),
        ("estimated_delivery", "TEXT"),
        ("shipping_address", "TEXT"),
        ("payment_method", "TEXT"),
        ("payment_id", "TEXT"),
        ("paid_at", "TEXT"),
        ("shipped_at", "TEXT"),
        ("delivered_at", "TEXT"),
        ("delivery_partner_name", "TEXT"),
        ("delivery_partner_phone", "TEXT"),
        ("delivery_vehicle", "TEXT"),
        ("emi_months", "INTEGER"),
        ("wallet_provider", "TEXT"),
        ("upi_id", "TEXT"),
        ("card_last4", "TEXT"),
    ]:
        _add_column_if_missing(conn, "orders", col, typedef)

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


def fetch_cart_rows(conn, username: str):
    return conn.execute(
        "SELECT * FROM cart_items WHERE username = ? ORDER BY id", (username,)
    ).fetchall()


def calculate_total(rows) -> float:
    return sum((row["price"] or 0) * (row["quantity"] or 1) for row in rows)


def get_order_events(conn, order_id: int):
    return conn.execute(
        "SELECT * FROM order_events WHERE order_id = ? ORDER BY event_at ASC",
        (order_id,),
    ).fetchall()


def ensure_placed_event(conn, order_id: int, created_at: str):
    exists = conn.execute(
        "SELECT id FROM order_events WHERE order_id = ? AND status = 'placed'",
        (order_id,),
    ).fetchone()
    if exists:
        return
    msg, loc = status_event_copy("placed")
    conn.execute(
        """
        INSERT INTO order_events (order_id, status, title, message, location, event_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (order_id, "placed", STATUS_LABELS["placed"], msg, loc, created_at),
    )


def append_event_if_new(conn, order_id: int, status: str, event_at: str):
    exists = conn.execute(
        "SELECT id FROM order_events WHERE order_id = ? AND status = ?",
        (order_id, status),
    ).fetchone()
    if exists:
        return
    msg, loc = status_event_copy(status)
    conn.execute(
        """
        INSERT INTO order_events (order_id, status, title, message, location, event_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (order_id, status, STATUS_LABELS.get(status, status), msg, loc, event_at),
    )


def sync_delivery_status(conn, order: sqlite3.Row) -> str:
    """Auto-advance paid orders through shipping pipeline (demo)."""
    if order["payment_status"] != "paid":
        return order["status"]

    new_status = target_status_after_payment(order["paid_at"])
    now = datetime.utcnow().isoformat()

    if new_status != order["status"]:
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order["id"]))
        append_event_if_new(conn, order["id"], new_status, now)
        if new_status == "shipped" and not order["shipped_at"]:
            conn.execute("UPDATE orders SET shipped_at = ? WHERE id = ?", (now, order["id"]))
        if new_status == "delivered" and not order["delivered_at"]:
            conn.execute(
                "UPDATE orders SET delivered_at = ?, estimated_delivery = ? WHERE id = ?",
                (now, now, order["id"]),
            )

    return new_status


def order_to_detail(conn, order: sqlite3.Row) -> dict[str, Any]:
    status = sync_delivery_status(conn, order)
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order["id"],)).fetchone()

    items = conn.execute(
        "SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order["id"],)
    ).fetchall()
    events = get_order_events(conn, order["id"])

    timeline = [
        {
            "status": e["status"],
            "title": e["title"],
            "message": e["message"],
            "location": e["location"],
            "event_at": e["event_at"],
            "completed": True,
        }
        for e in events
    ]

    prog = delivery_progress(status) if order["payment_status"] == "paid" else 0
    detail = {
        "order_id": order["id"],
        "total": order["total"],
        "status": status,
        "status_label": STATUS_LABELS.get(status, status),
        "payment_status": order["payment_status"],
        "payment_method": order["payment_method"],
        "payment_id": order["payment_id"],
        "tracking_number": order["tracking_number"],
        "carrier": order["carrier"] or "ShopSphere Express",
        "estimated_delivery": order["estimated_delivery"],
        "shipping_address": order["shipping_address"] or "Default delivery address",
        "delivery_progress": prog,
        "created_at": order["created_at"],
        "paid_at": order["paid_at"],
        "shipped_at": order["shipped_at"],
        "delivered_at": order["delivered_at"],
        "items": [row_to_item(i) for i in items],
        "timeline": timeline,
        "can_pay": order["payment_status"] == "pending",
        "is_delivered": status == "delivered",
        "delivery_partner": {
            "name": order["delivery_partner_name"],
            "phone": order["delivery_partner_phone"],
            "vehicle": order["delivery_vehicle"],
        }
        if order["delivery_partner_name"]
        else None,
        "emi_months": order["emi_months"],
        "wallet_provider": order["wallet_provider"],
    }
    return detail


def get_latest_pending_order(conn, username: str):
    return conn.execute(
        """
        SELECT * FROM orders
        WHERE username = ? AND payment_status = 'pending'
        ORDER BY id DESC LIMIT 1
        """,
        (username,),
    ).fetchone()


def create_order_from_cart(conn, username: str, rows, shipping_address: Optional[str] = None) -> dict:
    total = calculate_total(rows)
    created_at = datetime.utcnow().isoformat()
    tracking = generate_tracking_number()
    eta = estimated_delivery_date()
    address = shipping_address or "ShopSphere Customer, India"

    cursor = conn.execute(
        """
        INSERT INTO orders (
            username, total, status, payment_status, tracking_number, carrier,
            estimated_delivery, shipping_address, created_at
        ) VALUES (?, ?, 'placed', 'pending', ?, 'ShopSphere Express', ?, ?, ?)
        """,
        (username, total, tracking, eta, address, created_at),
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
                order_id, row["product_id"], row["name"], row["price"], row["description"],
                row["category"], row["image_url"], row["rating"], row["reviews"],
                row["discount"], row["stock"], row["quantity"],
            ),
        )

    ensure_placed_event(conn, order_id, created_at)
    conn.execute("DELETE FROM cart_items WHERE username = ?", (username,))
    conn.commit()

    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return order_to_detail(conn, order)
