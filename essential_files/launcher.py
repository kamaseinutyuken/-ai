import os
import sys
import webbrowser
import subprocess
import time
import socket
from pathlib import Path

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_server_running(port, max_attempts=30):
    """Check if server is running by attempting to connect to the port"""
    attempts = 0
    while attempts < max_attempts:
        if is_port_in_use(port):
            return True
        time.sleep(1)
        attempts += 1
        print(f"Waiting for server to start... ({attempts}/{max_attempts})")
    return False

def main():
    print("Mastra AI Excel VBA Generator - Launcher")
    print("========================================")
    print()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Checking Python installation...")
    try:
        import uvicorn
        import fastapi
        import dotenv
        import openpyxl
        import pandas
        print("All required packages are installed.")
    except ImportError as e:
        print(f"Missing package: {e}")
        print("Installing required packages...")
        backend_req_path = os.path.join(script_dir, "backend", "requirements.txt")
        if os.path.exists(backend_req_path):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", backend_req_path])
        else:
            print(f"Error: requirements.txt not found at {backend_req_path}")
            print("Installing core packages manually...")
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-dotenv", "openpyxl", "pandas", "python-multipart"])
    
    backend_dir = os.path.join(script_dir, "backend")
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        print("Current directory structure:")
        for root, dirs, files in os.walk(script_dir):
            print(f"Directory: {root}")
            for d in dirs:
                print(f"  - {d}/")
            for f in files:
                print(f"  - {f}")
        input("Press Enter to exit...")
        return
    
    app_main_path = os.path.join(backend_dir, "app", "main.py")
    if not os.path.exists(app_main_path):
        print(f"Error: app/main.py not found at {app_main_path}")
        print("Current app directory structure:")
        app_dir = os.path.join(backend_dir, "app")
        if os.path.exists(app_dir):
            for root, dirs, files in os.walk(app_dir):
                print(f"Directory: {root}")
                for d in dirs:
                    print(f"  - {d}/")
                for f in files:
                    print(f"  - {f}")
        input("Press Enter to exit...")
        return
    
    if is_port_in_use(8000):
        print("Warning: Port 8000 is already in use. The application may not start correctly.")
        print("Please close any other applications using port 8000 and try again.")
        input("Press Enter to continue anyway...")
    
    print("Starting backend server...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=backend_dir
        )
        
        print("Waiting for backend to start...")
        if check_server_running(8000):
            print("Backend server started successfully!")
            print("Opening application in browser...")
            webbrowser.open("http://localhost:8000")
            
            print()
            print("Mastra AI Excel VBA Generator is now running!")
            print("Press Ctrl+C to stop the application.")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Stopping application...")
                backend_process.terminate()
                print("Application stopped.")
        else:
            print("Error: Backend server failed to start within the timeout period.")
            print("Please check the following:")
            print("1. Make sure all required packages are installed")
            print("2. Check if port 8000 is already in use by another application")
            print("3. Check if there are any errors in the backend code")
            backend_process.terminate()
            input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting backend server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
