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

echo.
echo Starting backend server...
start cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 1337"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Opening application in browser...
start http://localhost:1337

echo.
echo Mastra AI Excel VBA Generator is now running!
echo Close this window to stop the application.
pause
