import os
import shutil
import argparse
import zipfile
from pathlib import Path
import sys

def create_package(output_filename="mastra_ai_debug.zip"):
    """Create a debug package with all necessary files for the standalone application"""
    print("Creating Mastra AI Excel VBA Generator debug package...")
    
    os.makedirs("dist", exist_ok=True)
    
    package_dir = "dist/debug_package"
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
        "run_debug.bat"
    ]
    for file in standalone_files:
        src = file
        dst = f"{package_dir}/{file}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
    
    readme_file = f"{package_dir}/README_DEBUG.txt"
    with open(readme_file, "w") as f:
        f.write("""Mastra AI Excel VBA Generator - デバッグバージョン

使用方法:
1. run_debug.bat をダブルクリックして実行
2. 必要なパッケージがインストールされます
3. アプリケーションが起動します
4. エラーが発生した場合は、コマンドプロンプトのメッセージとmastra_app_log.txtを確認してください

必要環境:
- Windows 10/11
- Python 3.8以上（PATHに追加されていること）
- インターネット接続

このデバッグバージョンは、エラーメッセージを表示し、ログファイルを生成します。
問題が発生した場合は、これらの情報を開発者に提供してください。
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
    
    print(f"Debug package created at {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Package Mastra AI Excel VBA Generator Debug Version')
    parser.add_argument('--output', type=str, default="mastra_ai_debug.zip",
                        help='Output filename for the package')
    
    args = parser.parse_args()
    
    create_package(args.output)
