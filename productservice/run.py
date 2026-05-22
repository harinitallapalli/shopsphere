"""Legacy entry point — runs the new backend product service."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    import uvicorn
    from backend.shared.config import PRODUCT_HOST, PRODUCT_PORT

    uvicorn.run("backend.product_service.app:app", host=PRODUCT_HOST, port=PRODUCT_PORT, reload=False)
