## 🛒 ShopSphere - Modern E-Commerce Platform

A scalable full-stack microservices-based e-commerce application built using **React (Frontend)** and **Flask + FastAPI (Backend Services)**.

---

## ✨ Key Highlights

- 🔐 Secure authentication using JWT (Login/Register system)
- 🛍️ Dynamic product catalog with search functionality
- 🛒 Fully functional shopping cart with persistence
- 📦 Order placement & order history tracking
- ⚙️ Microservices-based backend architecture
- 🎨 Modern, responsive UI with smooth user experience
- 📱 Mobile-first responsive design
- 🧠 Context API for global state management
- 📡 Centralized Axios API layer with token handling
- 🐳 Docker support for containerized deployment

---

## 🏗️ System Architecture

ShopSphere follows a **microservices architecture**:

- 🔐 Auth Service → Flask (Port 5000)
- 🛍️ Product Service → FastAPI (Port 8001)
- 📦 Order Service → FastAPI (Port 8002)
- 🌐 Frontend → React (Port 3000)

---

## 🚀 Getting Started

### 🔧 Prerequisites
- Python 3.8+
- Node.js (v14+)
- npm


## 💻 Run Locally

### 1️⃣ Start Backend Services

From project root:


pip install -r backend/requirements.txt

Run services:


python backend/auth_service/run.py
python backend/product_service/run.py
python backend/order_service/run.py

OR start all at once:

python backend/start_backend.py
### 2️⃣ Start Frontend

cd frontend
npm install
npm start

---

## 🌐 Live Demo

* 🚀 Replit Deployment:
  [https://a2b4e2b1-d567-4afa-9a94-991998d219fd-00-3mbmlf5w1jukv.sisko.replit.dev/login](https://a2b4e2b1-d567-4afa-9a94-991998d219fd-00-3mbmlf5w1jukv.sisko.replit.dev/login)

---

## 🧪 Test Credentials

```text
Username: demo
Password: demo123
```

---

## 📦 Sample Data

* 10 preloaded products (Electronics, Fashion, Accessories, etc.)
* Fully functional cart and checkout flow

---

## 📚 Documentation

* 📘 [Deployment Guide](./DEPLOYMENT_GUIDE.md)
* 🧪 [Test Checklist](./TEST_CHECKLIST.md)
* 🏗️ [System Architecture Details](./ADVANCED_UPGRADE.md)

---

## ⚙️ Core Features

* JWT Authentication with protected routes
* Persistent cart using LocalStorage
* Axios-based API communication layer
* Auto logout on unauthorized access (401 handling)
* Clean and modular microservices design
* Docker support for containerized execution

---
 🐳 Docker Support
docker-compose up
Access at:
http://localhost:3000

## 📱 UI Features

* Modern gradient-based UI
* Smooth transitions and animations
* Fully responsive layout
* Cart badge & dynamic navbar updates
* Clean dashboard experience

---

## 👨‍💻 Author

**Harini Tallapalli**
