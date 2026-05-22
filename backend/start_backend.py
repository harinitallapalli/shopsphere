"""
Start all ShopSphere backend services.

From project root (shopsphere/):
    python backend/start_backend.py

From backend folder:
    python start_backend.py
"""
import os
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT = BACKEND_DIR.parent
PYTHON = sys.executable

SERVICES = [
    ("Auth", [PYTHON, str(BACKEND_DIR / "auth_service" / "run.py")]),
    ("Product", [PYTHON, str(BACKEND_DIR / "product_service" / "run.py")]),
    ("Order", [PYTHON, str(BACKEND_DIR / "order_service" / "run.py")]),
]


def main():
    print("Starting ShopSphere backend services...")
    print(f"Project root: {ROOT}\n")
    processes = []
    for name, cmd in SERVICES:
        print(f"  -> {name}: {' '.join(cmd)}")
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        processes.append(subprocess.Popen(cmd, cwd=str(ROOT), env=env))
    print("\nAll services launched. Press Ctrl+C to stop.\n")
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()


if __name__ == "__main__":
    main()
