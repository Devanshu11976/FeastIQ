@echo off
echo Starting FeastIQ Servers...
echo.

echo Starting Backend Server (Flask)...
cd backend
start "FeastIQ Backend" cmd /k "venv\Scripts\python.exe run.py"
cd ..

echo Starting Frontend Server...
cd frontend
start "FeastIQ Frontend" cmd /k "python -m http.server 8000"
cd ..

echo.
echo ========================================
echo Servers Started Successfully!
echo ========================================
echo Backend API: http://localhost:5000
echo Frontend:   http://localhost:8000
echo.
echo Customer Landing: http://localhost:8000/customer/index.html
echo Admin Login:      http://localhost:8000/admin/login.html
echo.
echo Opening browser...
start http://localhost:8000/landing.html
echo.
echo Press any key to close this window (servers will continue running)...
pause >nul
