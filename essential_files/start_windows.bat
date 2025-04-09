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

echo Checking directory structure...
if not exist backend (
    echo Error: backend directory not found in current location.
    echo Current directory: %CD%
    echo Directory contents:
    dir
    echo.
    echo Please make sure you extracted the entire ZIP file and are running this script from the correct location.
    pause
    exit /b 1
)

echo Installing required packages...
cd backend
if not exist requirements.txt (
    echo Error: requirements.txt not found in backend directory.
    echo Creating requirements.txt...
    (
        echo fastapi
        echo uvicorn
        echo python-multipart
        echo python-dotenv
        echo httpx
        echo openpyxl
        echo pandas
        echo pydantic
    ) > requirements.txt
    echo requirements.txt created.
)

echo Installing packages from requirements.txt...
pip install -r requirements.txt
cd ..

echo.
echo Starting application...
python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Application failed to start.
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python 3.8 or higher is installed
    echo 2. Make sure all required packages are installed
    echo 3. Try running the application manually:
    echo    - Open Command Prompt
    echo    - Navigate to this directory
    echo    - Run: python launcher.py
    echo.
    echo If the problem persists, please contact support.
)

pause
