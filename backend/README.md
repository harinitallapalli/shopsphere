# ShopSphere Backend (Python)

Modular Python microservices for ShopSphere.

## Structure

```
backend/
  shared/           # JWT + config
  auth_service/     # Flask — port 5000
    app.py
    routes.py
    database.py
    run.py
  product_service/  # FastAPI — port 8001
    app.py
    routes.py
    database.py
    models.py
    seed_data.py
    run.py
  order_service/    # FastAPI — port 8002
    app.py
    routes.py
    database.py
    models.py
    run.py
  start_backend.py  # Run all 3 services
```

## Install

From project root (`shopsphere/`):

```bash
pip install -r backend/requirements.txt
```

## Run (3 terminals or one script)

**Option A — all at once:**

```bash
# from shopsphere/ (project root)
python backend/start_backend.py

# OR if you are already inside backend/
python start_backend.py
```

**Option B — separate terminals (from project root):**

```bash
python backend/auth_service/run.py
python backend/product_service/run.py
python backend/order_service/run.py
```

## API URLs

| Service | URL |
|---------|-----|
| Auth | http://127.0.0.1:5000 |
| Products | http://127.0.0.1:8001 |
| Orders | http://127.0.0.1:8002 |

Demo login: `demo` / `demo123`

## Order service (v3) — payments & tracking

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/place-order` | Creates order (`placed`, payment `pending`), tracking number |
| POST | `/pay` | Pay latest pending order or `{ order_id, payment_method }` |
| GET | `/orders/detail` | Full order cards + timeline + delivery % |
| GET | `/orders/overview` | Account summary (Amazon-style) |
| GET | `/orders/{id}/track` | Tracking timeline |
| POST | `/orders/{id}/cancel` | Cancel before ship |

**Payment methods:** `upi`, `card`, `netbanking`, `wallet`, `cod`

**Delivery pipeline (auto-advances after payment):**  
`placed` → `confirmed` → `packed` → `shipped` → `out_for_delivery` → `delivered`

Refresh `/orders/detail` to see status move forward (demo timings: ~10 min to delivered).

## Frontend connection

The React app uses `frontend/src/axiosInstance.js` pointing to these URLs.
Start backend first, then `cd frontend && npm start`.
