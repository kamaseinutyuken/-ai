@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - Simple Launcher
echo ================================================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Checking for port conflicts...
netstat -ano | findstr :1337 >nul
if %errorlevel% equ 0 (
    echo [WARNING] Port 1337 is already in use.
    echo Attempting to free the port...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :1337') do (
        echo Terminating process with PID: %%a
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

echo Creating .env file with API key...
if not exist backend\.env (
    mkdir backend 2>nul
    (
        echo # OpenRouter API Key
        echo # Real API key provided by user
        echo OPENROUTER_API_KEY="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"
    ) > backend\.env
)

echo Installing required packages...
cd backend
pip install fastapi uvicorn python-multipart python-dotenv httpx openpyxl pandas pydantic
cd ..

echo.
echo Starting backend server...
start cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 1337 --log-level debug"

echo Waiting for backend to start...
timeout /t 10 /nobreak >nul

echo.
echo Opening application in browser...
start http://localhost:1337

echo.
echo Application started! If browser doesn't open, go to: http://localhost:1337
pause
