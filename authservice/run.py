"""Legacy entry point — runs the new backend auth service."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    from backend.auth_service.app import app
    from backend.shared.config import AUTH_HOST, AUTH_PORT

    app.run(host=AUTH_HOST, port=AUTH_PORT, debug=True, use_reloader=False)
