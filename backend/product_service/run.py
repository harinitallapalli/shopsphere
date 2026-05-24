import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import uvicorn
from backend.shared.config import PRODUCT_HOST, PRODUCT_PORT

if __name__ == "__main__":
    uvicorn.run("backend.product_service.app:app", host=PRODUCT_HOST, port=PRODUCT_PORT, reload=False)
