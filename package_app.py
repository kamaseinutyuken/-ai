import os
import shutil
import argparse
import zipfile
from pathlib import Path
import sys

def create_package(output_filename="mastra_ai_excel_vba_generator.zip"):
    """Create a package with all necessary files for the application"""
    print("Creating Mastra AI Excel VBA Generator package...")
    
    os.makedirs("dist", exist_ok=True)
    
    package_dir = "dist/package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir, exist_ok=True)
    os.makedirs(f"{package_dir}/backend", exist_ok=True)
    os.makedirs(f"{package_dir}/backend/app", exist_ok=True)
    os.makedirs(f"{package_dir}/essential_files", exist_ok=True)
    
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
    
    print("Copying essential files...")
    essential_files = [
        "essential_files/start_windows.bat",
        "essential_files/run_simple.bat",
        "essential_files/README_windows.md",
        "essential_files/launcher.py"
    ]
    for file in essential_files:
        src = file
        dst = f"{package_dir}/{file}"
        
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
    
    print("Copying root files...")
    root_files = [
        "README.md",
        "start_windows.bat",  # Copy to root for easier access
        "run_simple.bat"      # Copy to root for easier access
    ]
    for file in root_files:
        if file == "start_windows.bat":
            src = "essential_files/start_windows.bat"
        elif file == "run_simple.bat":
            src = "essential_files/run_simple.bat"
        else:
            src = file
        
        dst = f"{package_dir}/{file}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} does not exist")
    
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
    parser = argparse.ArgumentParser(description='Package Mastra AI Excel VBA Generator')
    parser.add_argument('--output', type=str, default="mastra_ai_excel_vba_generator.zip",
                        help='Output filename for the package')
    
    args = parser.parse_args()
    
    create_package(args.output)
