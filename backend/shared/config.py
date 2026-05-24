import os

JWT_SECRET = os.environ.get("JWT_SECRET", "secret123")

AUTH_HOST = os.environ.get("AUTH_HOST", "127.0.0.1")
AUTH_PORT = int(os.environ.get("AUTH_PORT", "5001"))

PRODUCT_HOST = os.environ.get("PRODUCT_HOST", "127.0.0.1")
PRODUCT_PORT = int(os.environ.get("PRODUCT_PORT", "8001"))

ORDER_HOST = os.environ.get("ORDER_HOST", "127.0.0.1")
ORDER_PORT = int(os.environ.get("ORDER_PORT", "8002"))
