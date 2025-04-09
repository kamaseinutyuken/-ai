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

python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start.
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python 3.8 or higher is installed
    echo 2. Make sure all required packages are installed
    echo 3. Check if port 1337 is already in use by another application
    echo 4. Try running the application manually:
    echo    - Open Command Prompt
    echo    - Navigate to this directory
    echo    - Run: python launcher.py
    echo.
    echo If the problem persists, please contact support.
)

pause
