@echo off
echo Mastra AI Excel VBA Generator - Windows Launcher
echo ================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing required packages...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo Starting application...
python launcher.py

pause
