from fastapi import FastAPI

app = FastAPI()

products = []

@app.get("/")
def home():
    return {"service": "Product Service Running"}

@app.post("/add-product")
def add_product(product: dict):
    products.append(product)
    return {"message": "Product added"}

@app.get("/products")
def get_products():
    return products