import datetime
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

DEMO_USERS = [
    {"username": "demo", "password": "demo123"},
    {"username": "john", "password": "john123"},
    {"username": "sarah", "password": "sarah123"},
    {"username": "admin", "password": "admin123"},
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    for user in DEMO_USERS:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (username, password, created_at)
            VALUES (?, ?, ?)
            """,
            (user["username"], user["password"], datetime.datetime.utcnow().isoformat()),
        )
    conn.commit()
    conn.close()
