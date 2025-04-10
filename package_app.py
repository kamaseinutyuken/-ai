import os
import shutil
import argparse
import zipfile
from pathlib import Path
import sys

def create_package(output_filename="mastra_ai_standalone.zip"):
    """Create a package with all necessary files for the standalone application"""
    print("Creating Mastra AI Excel VBA Generator standalone package...")
    
    os.makedirs("dist", exist_ok=True)
    
    package_dir = "dist/package"
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
        "README_standalone.md"
    ]
    for file in standalone_files:
        src = file
        dst = f"{package_dir}/{file}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
    
    windows_bat = f"{package_dir}/run_standalone.bat"
    with open(windows_bat, "w") as f:
        f.write("""@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - スタンドアロンアプリケーション
echo ================================================================================
echo.

echo Pythonのインストールを確認中...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] Pythonがインストールされていないか、PATHに設定されていません。
    echo https://www.python.org/downloads/ からPython 3.8以上をインストールしてください。
    echo インストール時に「Add Python to PATH」にチェックを入れてください。
    pause
    exit /b 1
)

echo 必要なパッケージをインストール中...
pip install PyQt6 PyQt6-WebEngine
pip install -r backend/requirements.txt

echo.
echo アプリケーションを起動中...
python standalone_app.py

echo.
echo アプリケーションが終了しました。
pause
""")
    print(f"Created {windows_bat}")
    
    readme_file = f"{package_dir}/README.txt"
    with open(readme_file, "w") as f:
        f.write("""Mastra AI Excel VBA Generator - スタンドアロンアプリケーション

使用方法:
1. run_standalone.bat をダブルクリックして実行
2. 初回実行時は必要なパッケージがインストールされます
3. アプリケーションが自動的に起動します

必要環境:
- Windows 10/11
- Python 3.8以上（PATHに追加されていること）
- インターネット接続

詳細については README_standalone.md をご覧ください。
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
    
    print(f"Package created at {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Package Mastra AI Excel VBA Generator Standalone Application')
    parser.add_argument('--output', type=str, default="mastra_ai_standalone.zip",
                        help='Output filename for the package')
    
    args = parser.parse_args()
    
    create_package(args.output)
