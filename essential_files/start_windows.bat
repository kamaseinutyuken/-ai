@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - Windows Launcher
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

echo Checking directory structure...
if exist launcher.py (
    echo Found launcher.py in current directory.
) else if exist essential_files\launcher.py (
    echo Found launcher.py in essential_files directory.
    copy essential_files\launcher.py . >nul
    echo Copied launcher.py to current directory.
) else (
    echo [ERROR] launcher.py not found in current location or essential_files directory.
    echo Current directory: %CD%
    echo Directory contents:
    dir
    echo.
    echo Please make sure you extracted the entire ZIP file and are running this script from the correct location.
    pause
    exit /b 1
)

echo Checking for backend directory...
if not exist backend (
    echo [ERROR] Backend directory not found in current location.
    echo Current directory: %CD%
    echo Directory contents:
    dir
    echo.
    echo Please make sure you extracted the entire ZIP file and are running this script from the correct location.
    pause
    exit /b 1
)

echo Checking for .env file...
if not exist backend\.env (
    echo Creating .env file with default API key...
    (
        echo # OpenRouter API Key
        echo # Real API key provided by user
        echo OPENROUTER_API_KEY="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"
    ) > backend\.env
    echo .env file created.
)

echo Checking for requirements.txt...
if not exist backend\requirements.txt (
    echo Creating requirements.txt file...
    (
        echo fastapi==0.110.0
        echo uvicorn==0.27.1
        echo python-multipart==0.0.9
        echo python-dotenv==1.0.1
        echo httpx==0.27.0
        echo openpyxl==3.1.2
        echo pandas==2.2.0
        echo pydantic==2.6.1
    ) > backend\requirements.txt
    echo requirements.txt created.
)

echo Installing required packages...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install from requirements.txt
    echo Installing core packages directly...
    pip install fastapi uvicorn python-multipart python-dotenv httpx openpyxl pandas pydantic
)
cd ..

echo.
echo ================================================================================
echo Starting Mastra AI Excel VBA Generator...
echo ================================================================================
echo.
echo The application will open in your default web browser.
echo If the browser doesn't open automatically, please navigate to:
echo http://localhost:1337
echo.
echo Please wait while the application starts...
echo.

echo Starting backend server...
start cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 1337 --log-level debug"

echo Waiting for backend to start...
timeout /t 10 /nobreak >nul

echo.
echo Opening application in browser...
start http://localhost:1337

echo.
echo Mastra AI Excel VBA Generator is now running!
echo Close this window to stop the application.
echo.
echo If the application doesn't open automatically, please navigate to:
echo http://localhost:1337
echo.
echo If you encounter any issues, please check the command prompt window
echo that was opened for the backend server for error messages.

pause
