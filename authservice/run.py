from flask import Flask, request
from flask_cors import CORS
import jwt
import datetime

# 🔹 App setup
app = Flask(__name__)
CORS(app)

SECRET_KEY = "secret123"

# 🔹 Pre-populated demo users
users = [
    {"username": "demo", "password": "demo123"},
    {"username": "john", "password": "john123"},
    {"username": "sarah", "password": "sarah123"},
    {"username": "admin", "password": "admin123"},
]

# 🔹 Home route
@app.route("/")
def home():
    return {"service": "Auth Service Running"}

# 🔹 Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    
    # Check if user already exists
    for user in users:
        if user["username"] == data["username"]:
            return {"message": "User already exists"}, 400
    
    users.append(data)
    return {"message": "User registered successfully"}

# 🔹 Login (JWT)
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    for user in users:
        if user["username"] == data["username"] and user["password"] == data["password"]:
            
            # 🔐 Create token
            token = jwt.encode({
                "user": user["username"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            return {"token": token}

    return {"message": "Invalid credentials"}


# 🔥 START SERVER (VERY IMPORTANT)
if __name__ == "__main__":
    print("🚀 Auth Service Starting on port 5000...")
    print("📝 Demo Users Available:")
    print("   • Username: demo    | Password: demo123")
    print("   • Username: john    | Password: john123")
    print("   • Username: sarah   | Password: sarah123")
    print("   • Username: admin   | Password: admin123")
    print()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)