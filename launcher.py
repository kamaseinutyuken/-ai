
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
