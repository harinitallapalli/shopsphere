from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
CART_FILE = os.path.join(BASE_DIR, "cart.json")


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_orders():
    return load_json(ORDERS_FILE, [])


def save_orders(orders):
    save_json(ORDERS_FILE, orders)


def load_cart():
    return load_json(CART_FILE, [])


def save_cart(cart):
    save_json(CART_FILE, cart)


PRODUCT_SERVICE_URL = "http://127.0.0.1:8001/products"


@app.get("/")
def home():
    return {"service": "Order Service Running"}


@app.post("/add-to-cart")
def add_to_cart(item: dict):
    if not item:
        return {"message": "Invalid item"}

    cart = load_cart()
    cart.append(item)
    save_cart(cart)
    return {"message": "Item added to cart"}


@app.get("/cart")
def get_cart():
    return load_cart()


@app.delete("/cart/{index}")
def remove_from_cart(index: int):
    cart = load_cart()
    if 0 <= index < len(cart):
        removed = cart.pop(index)
        save_cart(cart)
        return {"message": f"Removed {removed.get('name', 'item')} from cart"}
    return {"message": "Invalid index"}


@app.post("/place-order")
def place_order():
    cart = load_cart()
    if not cart:
        return {"message": "Cart is empty"}

    orders = load_orders()
    orders.append(cart)
    save_orders(orders)
    save_cart([])

    return {"message": "Order placed"}


@app.get("/orders")
def get_orders():
    return load_orders()


@app.post("/pay")
def pay():
    return {"message": "Payment successful"}
