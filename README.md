# 🛒 ShopSphere - Modern E-Commerce Platform

A full-stack microservices e-commerce application built with React, Flask, and FastAPI.

## **✨ Features**

- 🔐 **JWT Authentication** - Secure login/register with demo accounts
- 🛍️ **Product Catalog** - Browse 10 sample products with search
- 🛒 **Shopping Cart** - Add/remove items with persistent storage
- 📦 **Order Management** - Place orders and view order history
- 🎨 **Modern UI** - Gradient design with smooth animations
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🏗️ **Microservices** - Scalable architecture with 3 backend services
- ⚙️ **Context API** - Lightweight state management
- 📡 **Axios API Layer** - Centralized API communication
- 🐳 **Docker Support** - One-command deployment

## **🚀 Quick Start**

### **Option 1: Local Development (Recommended)**

**Terminal 1–3: Backend (from project root)**
```bash
pip install -r backend/requirements.txt

python backend/auth_service/run.py      # port 5000
python backend/product_service/run.py   # port 8001
python backend/order_service/run.py     # port 8002
```

Or start all backend services at once:
```bash
python backend/start_backend.py
```

See [backend/README.md](./backend/README.md) for API details.

**Terminal 4: Frontend**
```bash
cd frontend
npm install
npm start
```

Visit **http://127.0.0.1:3000** and login with demo/demo123

### **Option 2: Docker Compose**
```bash
docker-compose up
```

Visit **http://localhost:3000**

## **🛍️ Sample Products**

10 products pre-loaded including Laptop, iPhone 15, Headphones, and more!

## **📚 Documentation**

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Setup & deployment
- **[TEST_CHECKLIST.md](./TEST_CHECKLIST.md)** - 30 test scenarios
- **[ADVANCED_UPGRADE.md](./ADVANCED_UPGRADE.md)** - Architecture details

## **🏗️ Architecture**

Microservices with React + Context API + Axios
- Auth Service (Flask, Port 5000)
- Product Service (FastAPI, Port 8001)
- Order Service (FastAPI, Port 8002)
- Frontend (React, Port 3000)

## **✅ Key Features**

✅ Context API for state management
✅ Axios API layer with JWT handling
✅ Protected routes
✅ Cart badge in navbar
✅ Auto-logout on 401 errors
✅ LocalStorage persistence
✅ Docker support
✅ 30 test scenarios

## **🚀 Ready to Launch?**

1. Follow the Quick Start section
2. Login with demo/demo123
3. Browse products and add to cart
4. Place an order
5. Run TEST_CHECKLIST.md

**Your ShopSphere is production ready!** 🎉

## Recent Improvements
- Added better product UI
- Improved authentication flow
