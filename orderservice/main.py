from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# ✅ ADD THIS BLOCK HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orders = []
cart = []

PRODUCT_SERVICE_URL = "http://127.0.0.1:8001/products"

@app.get("/")
def home():
    return {"service": "Order Service Running"}

@app.post("/add-to-cart")
def add_to_cart(item: dict):
    if not item:
        return {"message": "Invalid item"}
    
    cart.append(item)
    return {"message": "Item added to cart"}

@app.get("/cart")
def get_cart():
    return cart

@app.post("/place-order")
def place_order():
    if not cart:
        return {"message": "Cart is empty"}

    orders.append(cart.copy())
    cart.clear()

    return {"message": "Order placed"}

@app.get("/orders")
def get_orders():
    return orders

@app.post("/pay")
def pay():
    return {"message": "Payment successful ✅"}