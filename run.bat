@echo off
echo ========================================
echo    Stocks AI - NEPSE Market Prediction
echo ========================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Using Python version: %pyver%

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Run the application
echo.
echo Starting the application...
python run.py

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause 