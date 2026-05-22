import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.auth_service.app import app
from backend.shared.config import AUTH_HOST, AUTH_PORT

if __name__ == "__main__":
    app.run(host=AUTH_HOST, port=AUTH_PORT, debug=True, use_reloader=False)
