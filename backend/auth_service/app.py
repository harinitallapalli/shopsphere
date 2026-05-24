import sys
from pathlib import Path

# Allow imports from project root (shopsphere/)
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask
from flask_cors import CORS

from backend.auth_service.routes import auth_bp
from backend.shared.config import AUTH_HOST, AUTH_PORT

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    print(f"Auth Service: http://{AUTH_HOST}:{AUTH_PORT}")
    print("Demo: demo/demo123 | john/john123 | sarah/sarah123 | admin/admin123")
    app.run(host=AUTH_HOST, port=AUTH_PORT, debug=True, use_reloader=False)
