@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - Installation and Run
echo ================================================================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing required packages...
pip install PyQt6 PyQt6-WebEngine
pip install -r backend/requirements.txt

echo.
echo Starting application...
python standalone_app.py

echo.
echo Application has exited. Check for any error messages above.
echo Also check the log file mastra_app_log.txt for details.
pause
