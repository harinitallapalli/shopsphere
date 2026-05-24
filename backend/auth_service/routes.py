import datetime

import jwt
from flask import Blueprint, jsonify, request

from backend.shared.config import JWT_SECRET
from .database import get_db, init_db

auth_bp = Blueprint("auth", __name__)

init_db()


def create_token(username: str) -> str:
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")


def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def get_bearer_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def require_auth():
    token = get_bearer_token()
    if not token:
        return None, (jsonify({"message": "Missing authorization token"}), 401)
    payload = decode_token(token)
    if not payload:
        return None, (jsonify({"message": "Invalid or expired token"}), 401)
    return payload["user"], None


@auth_bp.route("/")
def home():
    return jsonify({"service": "Auth Service Running", "version": "2.0"})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if existing:
        conn.close()
        return jsonify({"message": "User already exists"}), 400

    conn.execute(
        "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
        (username, password, datetime.datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully", "success": True})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    conn = get_db()
    row = conn.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_token(row["username"])
    return jsonify({"token": token, "user_id": row["id"], "username": row["username"]})


@auth_bp.route("/me", methods=["GET"])
@auth_bp.route("/user", methods=["GET"])
def me():
    username, error = require_auth()
    if error:
        return error

    conn = get_db()
    row = conn.execute(
        "SELECT id, username, created_at FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {"user_id": row["id"], "username": row["username"], "created_at": row["created_at"]}
    )
