@echo off
REM ShopSphere Startup Script for Windows
REM This script helps you understand how to start all services

echo.
echo ============================================================
echo            ShopSphere v2.0 - Startup Instructions
echo ============================================================
echo.
echo You need to open 4 SEPARATE command prompt/terminal windows
echo and run each command in its own window.
echo.
echo ============================================================
echo.
echo STEP 1: Open Terminal 1 for Auth Service
echo ============================================================
echo.
echo Copy and paste this:
echo.
echo cd c:\Users\vinug\OneDrive\Desktop\HARINI\shopsphere\authservice
echo pip install flask flask-cors pyjwt
echo python run.py
echo.
echo Expected: "Running on http://127.0.0.1:5000"
echo.
echo ============================================================
echo.
echo STEP 2: Open Terminal 2 for Product Service
echo ============================================================
echo.
echo Copy and paste this:
echo.
echo cd c:\Users\vinug\OneDrive\Desktop\HARINI\shopsphere\productservice
echo pip install fastapi uvicorn
echo python -m uvicorn main:app --host 127.0.0.1 --port 8001
echo.
echo Expected: "Uvicorn running on http://127.0.0.1:8001"
echo.
echo ============================================================
echo.
echo STEP 3: Open Terminal 3 for Order Service
echo ============================================================
echo.
echo Copy and paste this:
echo.
echo cd c:\Users\vinug\OneDrive\Desktop\HARINI\shopsphere\orderservice
echo pip install fastapi uvicorn
echo python -m uvicorn main:app --host 127.0.0.1 --port 8002
echo.
echo Expected: "Uvicorn running on http://127.0.0.1:8002"
echo.
echo ============================================================
echo.
echo STEP 4: Open Terminal 4 for Frontend
echo ============================================================
echo.
echo Copy and paste this:
echo.
echo cd c:\Users\vinug\OneDrive\Desktop\HARINI\shopsphere\frontend
echo npm install
echo npm start
echo.
echo Expected: Opens http://127.0.0.1:3000 automatically
echo.
echo ============================================================
echo.
echo Login with: demo / demo123
echo.
echo ============================================================
echo.
pause
