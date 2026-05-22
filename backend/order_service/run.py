import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import uvicorn
from backend.shared.config import ORDER_HOST, ORDER_PORT

if __name__ == "__main__":
    uvicorn.run("backend.order_service.app:app", host=ORDER_HOST, port=ORDER_PORT, reload=False)
