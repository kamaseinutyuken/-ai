import os
import subprocess
import shutil
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        return False
    
    try:
        node_version = subprocess.check_output(["node", "--version"]).decode().strip()
        print(f"Node.js version: {node_version}")
    except:
        print("Error: Node.js is not installed")
        return False
    
    try:
        subprocess.check_output(["pyinstaller", "--version"])
    except:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    return True

def build_frontend():
    """Build the React frontend"""
    print("\nBuilding frontend...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print(f"Error: Frontend directory not found at {frontend_dir.absolute()}")
        return False
    
    os.chdir(frontend_dir)
    
    print("Installing frontend dependencies...")
    subprocess.check_call(["npm", "install"])
    
    print("Building frontend...")
    subprocess.check_call(["npm", "run", "build"])
    
    os.chdir("..")
    return True

def build_backend():
    """Build the FastAPI backend"""
    print("\nBuilding backend...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print(f"Error: Backend directory not found at {backend_dir.absolute()}")
        return False
    
    os.chdir(backend_dir)
    
    print("Installing backend dependencies...")
    subprocess.check_call(["poetry", "install"])
    
    os.chdir("..")
    return True

def create_launcher():
    """Create a launcher script that starts both frontend and backend"""
    print("\nCreating launcher script...")
    
    launcher_content = """
import os
import sys
import subprocess
import threading
import webbrowser
import time
from pathlib import Path

def run_backend():
    os.chdir(Path(__file__).parent / "backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"])

def run_frontend():
    os.chdir(Path(__file__).parent / "frontend" / "dist")
    import http.server
    import socketserver
    
    PORT = 5173
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving frontend at http://localhost:{PORT}")
        httpd.serve_forever()

def main():
    print("Starting Mastra AI Excel VBA Generator...")
    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    print("Starting backend server...")
    time.sleep(2)
    
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    print("Opening application in browser...")
    webbrowser.open("http://localhost:5173")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
"""
    
    with open("launcher.py", "w") as f:
        f.write(launcher_content)
    
    return True

def package_application():
    """Package the application using PyInstaller"""
    print("\nPackaging application...")
    
    spec_content = """

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend/dist'),
        ('backend', 'backend'),
    ],
    hiddenimports=['uvicorn.logging', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Mastra AI Excel VBA Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Mastra AI Excel VBA Generator',
)
"""
    
    with open("mastra_ai.spec", "w") as f:
        f.write(spec_content)
    
    subprocess.check_call(["pyinstaller", "mastra_ai.spec", "--clean"])
    
    return True

def main():
    print("=== Mastra AI Excel VBA Generator Packaging Tool ===")
    
    if not check_requirements():
        print("Failed to meet requirements. Exiting.")
        return
    
    if not build_frontend():
        print("Failed to build frontend. Exiting.")
        return
    
    if not build_backend():
        print("Failed to build backend. Exiting.")
        return
    
    if not create_launcher():
        print("Failed to create launcher script. Exiting.")
        return
    
    if not package_application():
        print("Failed to package application. Exiting.")
        return
    
    print("\n=== Packaging Complete ===")
    print("The packaged application is available in the 'dist' directory.")
    print("To run the application, execute 'dist/Mastra AI Excel VBA Generator/Mastra AI Excel VBA Generator.exe'")

if __name__ == "__main__":
    main()
