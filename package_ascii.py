import os
import shutil
import argparse
import zipfile
from pathlib import Path
import sys

def create_package(output_filename="mastra_ai_ascii.zip"):
    """Create a package with ASCII-only batch files for the standalone application"""
    print("Creating Mastra AI Excel VBA Generator ASCII package...")
    
    os.makedirs("dist", exist_ok=True)
    
    package_dir = "dist/ascii_package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir, exist_ok=True)
    os.makedirs(f"{package_dir}/backend", exist_ok=True)
    os.makedirs(f"{package_dir}/backend/app", exist_ok=True)
    os.makedirs(f"{package_dir}/frontend", exist_ok=True)
    os.makedirs(f"{package_dir}/frontend/dist", exist_ok=True)
    
    print("Copying backend files...")
    backend_files = [
        "backend/requirements.txt",
        "backend/.env",
        "backend/app/main.py",
        "backend/app/llm_service.py",
        "backend/app/excel_service.py",
        "backend/app/vba_service.py",
        "backend/app/models.py",
        "backend/app/__init__.py"
    ]
    for file in backend_files:
        src = file
        dst = f"{package_dir}/{file}"
        
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
            if file.endswith("__init__.py"):
                with open(dst, "w") as f:
                    f.write("# Auto-generated __init__.py file")
                print(f"Created empty {dst}")
    
    print("Copying frontend files...")
    if os.path.exists("frontend/dist"):
        for root, dirs, files in os.walk("frontend/dist"):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, "frontend/dist")
                dst_path = os.path.join(f"{package_dir}/frontend/dist", rel_path)
                
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"Copied {src_path} to {dst_path}")
    else:
        print("Warning: frontend/dist directory does not exist")
    
    print("Copying standalone application files...")
    standalone_files = [
        "standalone_app.py",
        "README_standalone.md",
        "run_windows_ansi.bat",
        "simple_run.bat"
    ]
    for file in standalone_files:
        src = file
        dst = f"{package_dir}/{file}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
    
    run_bat = f"{package_dir}/run.bat"
    with open(run_bat, "w", encoding="ascii") as f:
        f.write("""@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator
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
""")
    print(f"Created {run_bat}")
    
    debug_bat = f"{package_dir}/debug.bat"
    with open(debug_bat, "w", encoding="ascii") as f:
        f.write("""@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - Debug Mode
echo ================================================================================
echo.

echo This batch file will keep the command prompt window open.
echo Use this if the application closes immediately.
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
echo If errors occur, they will be displayed below.
echo.

python standalone_app.py

echo.
echo Application has exited.
echo Check for error messages above.
echo Also check the log file mastra_app_log.txt for details.
echo.
echo Press any key to exit...
pause > nul
""")
    print(f"Created {debug_bat}")
    
    readme_file = f"{package_dir}/README.txt"
    with open(readme_file, "w", encoding="ascii") as f:
        f.write("""Mastra AI Excel VBA Generator - Standalone Application

How to use:
1. Double-click run.bat to start the application
2. If the application closes immediately, use debug.bat instead
3. Required packages will be installed on first run

Requirements:
- Windows 10/11
- Python 3.8+ (added to PATH)
- Internet connection

If you encounter any issues:
1. Check the error messages in the command prompt window
2. Check the log file mastra_app_log.txt
3. Make sure Python is installed and added to PATH
4. Try running as administrator if needed

For more details, see README_standalone.md
""")
    print(f"Created {readme_file}")
    
    print("Creating ZIP file...")
    output_path = output_filename
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    print(f"ASCII package created at {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Package Mastra AI Excel VBA Generator with ASCII-only batch files')
    parser.add_argument('--output', type=str, default="mastra_ai_ascii.zip",
                        help='Output filename for the package')
    
    args = parser.parse_args()
    
    create_package(args.output)
