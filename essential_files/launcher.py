import os
import sys
import webbrowser
import subprocess
import time
from pathlib import Path

def main():
    print("Mastra AI Excel VBA Generator - Launcher")
    print("========================================")
    print()
    
    print("Checking Python installation...")
    try:
        import uvicorn
        import fastapi
        import dotenv
        import openpyxl
        import pandas
    except ImportError:
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    )
    
    print("Waiting for backend to start...")
    time.sleep(5)
    
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

if __name__ == "__main__":
    main()
