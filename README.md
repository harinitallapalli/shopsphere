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

**Terminal 1: Auth Service**
```bash
cd authservice
pip install flask flask-cors pyjwt
python run.py
```

**Terminal 2: Product Service**
```bash
cd productservice
pip install fastapi uvicorn
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

**Terminal 3: Order Service**
```bash
cd orderservice
pip install fastapi uvicorn
python -m uvicorn main:app --host 127.0.0.1 --port 8002
```

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

## **👤 Demo Users**

| Username | Password | 
|----------|----------|
| demo | demo123 |
| john | john123 |
| sarah | sarah123 |
| admin | admin123 |

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

---

**Version**: 2.0 - Advanced Edition  
**Status**: ✅ Production Ready
