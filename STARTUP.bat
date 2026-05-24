@echo off
echo ============================================================
echo            ShopSphere - Startup (backend + frontend)
echo ============================================================
echo.
echo BACKEND (Python) - run from project root in 3 terminals:
echo.
echo   cd %~dp0
echo   pip install -r backend\requirements.txt
echo.
echo   Terminal 1: python backend\auth_service\run.py
echo   Terminal 2: python backend\product_service\run.py
echo   Terminal 3: python backend\order_service\run.py
echo.
echo   OR all-in-one: python backend\start_backend.py
echo.
echo FRONTEND:
echo.
echo   cd %~dp0frontend
echo   npm install
echo   npm start
echo.
echo Login: demo / demo123
echo ============================================================
pause
