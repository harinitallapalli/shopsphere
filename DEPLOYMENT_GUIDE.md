# 🚀 ShopSphere - Deployment & Setup Guide

## **Quick Start (2 minutes)**

### **1. Local Development Mode**

```bash
# Clone/Navigate to project
cd shopsphere

# Open 4 terminals
```

**Terminal 1: Auth Service**
```bash
cd authservice
pip install flask flask-cors pyjwt
python run.py
# Expected: Running on http://127.0.0.1:5000
```

**Terminal 2: Product Service**
```bash
cd productservice
pip install fastapi uvicorn
python -m uvicorn main:app --host 127.0.0.1 --port 8001
# Expected: Uvicorn running on http://127.0.0.1:8001
```

**Terminal 3: Order Service**
```bash
cd orderservice
pip install fastapi uvicorn
python -m uvicorn main:app --host 127.0.0.1 --port 8002
# Expected: Uvicorn running on http://127.0.0.1:8002
```

**Terminal 4: Frontend**
```bash
cd frontend
npm install
npm start
# Expected: Opens http://localhost:3000 automatically
```

✅ **App is running!** Login with demo/demo123

---

## **Docker Deployment (Advanced)**

### **Prerequisites**
- Docker installed
- Docker Compose installed
- No services running on ports 3000, 5000, 8001, 8002

### **Commands**

```bash
# Start all services
docker-compose up

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild images
docker-compose up --build

# View running containers
docker-compose ps
```

### **Service Health Checks**
```bash
# Auth Service
curl http://localhost:5000/

# Product Service
curl http://localhost:8001/

# Order Service
curl http://localhost:8002/

# Frontend
curl http://localhost:3000
```

---

## **Environment Variables**

Create `.env` file in frontend folder:

```env
REACT_APP_AUTH_URL=http://127.0.0.1:5000
REACT_APP_PRODUCT_URL=http://127.0.0.1:8001
REACT_APP_ORDER_URL=http://127.0.0.1:8002
```

---

## **Port Configuration**

| Service | Port | URL | Status |
|---------|------|-----|--------|
| Auth Service | 5000 | http://127.0.0.1:5000 | Running ✅ |
| Product Service | 8001 | http://127.0.0.1:8001 | Running ✅ |
| Order Service | 8002 | http://127.0.0.1:8002 | Running ✅ |
| Frontend | 3000 | http://localhost:3000 | Running ✅ |

---

## **Database Setup**

### **Auth Service**
- Uses in-memory user list (see `run.py`)
- Default demo users:
  - demo / demo123
  - john / john123
  - sarah / sarah123
  - admin / admin123

### **Product Service**
- SQLite database: `products.db`
- Auto-loads 10 sample products on first run
- Location: `productservice/products.db`

### **Reset Database**
```bash
# Delete product database to reload samples
rm productservice/products.db

# Restart product service
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

---

## **Frontend Setup**

### **Install Dependencies**
```bash
cd frontend
npm install
```

### **Available Scripts**

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject configuration (NOT RECOMMENDED)
npm eject
```

---

## **API Endpoints Reference**

### **Auth Service (Port 5000)**
```
POST /register
  { username, password }
  → { success, message }

POST /login
  { username, password }
  → { token, user_id }

GET /user (requires token)
  → { username, created_at }
```

### **Product Service (Port 8001)**
```
GET /products
  → [ { id, name, description, price, category, stock } ]

GET /products/{id}
  → { id, name, description, price, category, stock }

POST /products (admin only)
  { name, price, description, category, stock }
  → { id, name, ... }

GET /search?q=laptop
  → [ filtered products ]
```

### **Order Service (Port 8002)**
```
GET /cart (requires token)
  → { items: [ { product_id, quantity, price } ], total }

POST /cart/add (requires token)
  { product_id, quantity }
  → { success, cart_total }

POST /orders (requires token)
  { items: [ { product_id, quantity } ] }
  → { order_id, total, status }

GET /orders (requires token)
  → [ { order_id, total, status, created_at } ]
```

---

## **JWT Token Usage**

All requests to protected endpoints need:
```
Authorization: Bearer <token>
```

**Axios Instance** (Frontend)
```javascript
import { authService } from './axiosInstance';

// Token is automatically attached
const products = await authService.get('/products');
```

---

## **Troubleshooting**

### **Port Already in Use**
```bash
# Find process using port
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### **ModuleNotFoundError**
```bash
# Install missing module
pip install <module_name>

# Or upgrade pip
pip install --upgrade pip
```

### **CORS Errors**
- Check frontend origin matches backend CORS config
- Backends have CORS enabled by default
- See `axiosInstance.js` for CORS configuration

### **Blank Login Page**
- Clear browser cache: `Ctrl+Shift+Delete`
- Check console for errors: `F12`
- Verify Auth Service is running

### **404 on Product Load**
- Verify Product Service is running on 8001
- Check product database exists: `productservice/products.db`
- Restart Product Service

### **Cart Items Not Saving**
- Check localStorage in browser DevTools
- Verify CartContext is wrapping the app
- Clear localStorage and refresh

---

## **Performance Tips**

1. **Caching**: Axios instances support caching
2. **Lazy Loading**: Use React.lazy for pages
3. **Compression**: Enable gzip in production
4. **CDN**: Use CDN for static assets
5. **Pagination**: Implement for large product lists

---

## **Production Deployment**

### **Build Frontend**
```bash
cd frontend
npm run build
```

### **Serve with Node**
```bash
npm install -g serve
serve -s build -l 3000
```

### **Deploy Backend Services**
```bash
# Using Gunicorn (Flask)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# FastAPI already uses Uvicorn in production
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### **Docker Production**
```bash
# Build and push to registry
docker-compose build
docker tag shopsphere-frontend:latest your-registry/shopsphere:latest
docker push your-registry/shopsphere:latest

# Deploy to cloud
docker pull your-registry/shopsphere:latest
docker-compose up
```

---

## **Monitoring & Logs**

### **View Logs**
```bash
# Docker Compose logs
docker-compose logs -f auth-service

# Service-specific logs
docker-compose logs -f --tail=100 product-service
```

### **Health Checks**
```bash
# All services
docker-compose ps

# Individual service
docker-compose exec auth-service curl http://localhost:5000/
```

---

## **Security Checklist**

- [ ] Change demo user passwords in production
- [ ] Use HTTPS/SSL certificates
- [ ] Implement rate limiting
- [ ] Add API key validation
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Add authentication timeout
- [ ] Implement refresh token rotation
- [ ] Enable logging and monitoring

---

## **Getting Help**

Check these files for more info:
- `README.md` - Project overview
- `ADVANCED_UPGRADE.md` - Architecture details
- `FRONTEND_UPDATES.md` - UI/UX changes
- `PRODUCTS_ADDED.md` - Sample product list

---

**Happy Deploying! 🚀**

For issues, check the troubleshooting section or verify service health.
