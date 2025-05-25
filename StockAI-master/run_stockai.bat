@echo off
echo 🚀 StockAI - NEPSE Market Prediction Platform
echo ================================================
echo Starting secure authentication and AI dashboard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🔐 Starting Authentication System...
start "StockAI Auth" cmd /c "python auth_app.py"

echo 📊 Waiting for auth system to start...
timeout /t 3 /nobreak >nul

echo 📈 Starting Main Dashboard...
start "StockAI Dashboard" cmd /c "python app.py"

echo.
echo 🎉 StockAI is starting!
echo =============================================
echo 📋 Application URLs:
echo 🔑 Authentication: http://127.0.0.1:8060
echo 📈 Main Dashboard: http://127.0.0.1:8050
echo.
echo 📖 How to use:
echo 1. First, login or create account at the authentication page
echo 2. After successful login, access the main dashboard
echo 3. Upload your NEPSE stock data (Excel format)
echo 4. Configure model parameters and train AI model
echo 5. View predictions and technical analysis
echo.
echo ⚠️  Close the terminal windows to stop the applications
echo =============================================

REM Open authentication page
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8060

REM Open main dashboard
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8050

echo ✅ Both applications are starting...
echo ✅ Browser tabs should open automatically
echo.
pause 