"""Legacy entry point — runs the new backend order service."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    import uvicorn
    from backend.shared.config import ORDER_HOST, ORDER_PORT

    uvicorn.run("backend.order_service.app:app", host=ORDER_HOST, port=ORDER_PORT, reload=False)
