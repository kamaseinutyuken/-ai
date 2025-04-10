import os
import shutil
import argparse
import zipfile
from pathlib import Path
import sys

def create_package(output_filename="mastra_ai_simple.zip"):
    """Create a package with ASCII-only batch files for the standalone application"""
    print("Creating Mastra AI Excel VBA Generator simple package...")
    
    os.makedirs("dist", exist_ok=True)
    
    package_dir = "dist/simple_package"
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
        "backend/app/main.py"
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
        "simple_run.bat",
        "install_and_run.bat"
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
        f.write('@echo off\n')
        f.write('echo ================================================================================\n')
        f.write('echo Mastra AI Excel VBA Generator\n')
        f.write('echo ================================================================================\n')
        f.write('echo.\n\n')
        f.write('echo Checking Python installation...\n')
        f.write('python --version\n')
        f.write('if %errorlevel% neq 0 (\n')
        f.write('    echo [ERROR] Python is not installed or not in PATH.\n')
        f.write('    echo Please install Python 3.8+ from https://www.python.org/downloads/\n')
        f.write('    echo Make sure to check "Add Python to PATH" during installation.\n')
        f.write('    pause\n')
        f.write('    exit /b 1\n')
        f.write(')\n\n')
        f.write('echo Installing required packages...\n')
        f.write('pip install PyQt6 PyQt6-WebEngine\n')
        f.write('pip install -r backend/requirements.txt\n\n')
        f.write('echo.\n')
        f.write('echo Starting application...\n')
        f.write('python standalone_app.py\n\n')
        f.write('echo.\n')
        f.write('echo Application has exited. Check for any error messages above.\n')
        f.write('echo Also check the log file mastra_app_log.txt for details.\n')
        f.write('pause\n')
    print(f"Created {run_bat}")
    
    minimal_bat = f"{package_dir}/start.bat"
    with open(minimal_bat, "w", encoding="ascii") as f:
        f.write('@echo off\n')
        f.write('python standalone_app.py\n')
        f.write('pause\n')
    print(f"Created {minimal_bat}")
    
    readme_file = f"{package_dir}/README.txt"
    with open(readme_file, "w", encoding="ascii") as f:
        f.write('Mastra AI Excel VBA Generator - Standalone Application\n\n')
        f.write('How to use:\n')
        f.write('1. Double-click run.bat to start the application\n')
        f.write('2. If the application closes immediately, use debug.bat instead\n')
        f.write('3. For a minimal startup, use start.bat\n')
        f.write('4. Required packages will be installed on first run\n\n')
        f.write('Requirements:\n')
        f.write('- Windows 10/11\n')
        f.write('- Python 3.8+ (added to PATH)\n')
        f.write('- Internet connection\n\n')
        f.write('If you encounter any issues:\n')
        f.write('1. Check the error messages in the command prompt window\n')
        f.write('2. Check the log file mastra_app_log.txt\n')
        f.write('3. Make sure Python is installed and added to PATH\n')
        f.write('4. Try running as administrator if needed\n\n')
        f.write('For more details, see README_standalone.md\n')
    print(f"Created {readme_file}")
    
    print("Creating ZIP file...")
    output_path = output_filename
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    print(f"Simple package created at {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Package Mastra AI Excel VBA Generator with ASCII-only batch files')
    parser.add_argument('--output', type=str, default="mastra_ai_simple.zip",
                        help='Output filename for the package')
    
    args = parser.parse_args()
    
    create_package(args.output)
