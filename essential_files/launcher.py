import os
import sys
import webbrowser
import subprocess
import time
import socket
import traceback
from pathlib import Path

def is_port_in_use(port):
    """Check if a port is in use by attempting to connect to it"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_server_running(port, max_attempts=60):
    """Check if server is running by attempting to connect to the port"""
    attempts = 0
    while attempts < max_attempts:
        if is_port_in_use(port):
            return True
        time.sleep(1)
        attempts += 1
        print(f"Waiting for server to start... ({attempts}/{max_attempts})")
    return False

def find_project_root():
    """Find the project root directory containing the backend folder"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(current_dir) == "essential_files":
        parent_dir = os.path.dirname(current_dir)
        if os.path.exists(os.path.join(parent_dir, "backend")):
            return parent_dir
    
    if os.path.exists(os.path.join(current_dir, "backend")):
        return current_dir
    
    if os.path.basename(current_dir) == "backend":
        return os.path.dirname(current_dir)
    
    parent_dir = os.path.dirname(current_dir)
    if os.path.exists(os.path.join(parent_dir, "backend")):
        return parent_dir
    
    return current_dir

def install_requirements(backend_dir):
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    requirements_path = os.path.join(backend_dir, "requirements.txt")
    
    if os.path.exists(requirements_path):
        print(f"Found requirements.txt at {requirements_path}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path],
                check=True
            )
            print("Package installation completed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            print("Installing core packages manually...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", 
                     "python-dotenv", "httpx", "openpyxl", "pandas", "pydantic"],
                    check=True
                )
                print("Core package installation completed.")
                return True
            except Exception as e:
                print(f"Failed to install core packages: {e}")
                return False
    else:
        print(f"Requirements file not found at {requirements_path}")
        print("Creating requirements.txt file...")
        try:
            os.makedirs(os.path.dirname(requirements_path), exist_ok=True)
            with open(requirements_path, 'w') as f:
                f.write("fastapi==0.110.0\n")
                f.write("uvicorn==0.27.1\n")
                f.write("python-multipart==0.0.9\n")
                f.write("python-dotenv==1.0.1\n")
                f.write("httpx==0.27.0\n")
                f.write("openpyxl==3.1.2\n")
                f.write("pandas==2.2.0\n")
                f.write("pydantic==2.6.1\n")
            
            print(f"Created requirements.txt at {requirements_path}")
            return install_requirements(backend_dir)
        except Exception as e:
            print(f"Failed to create requirements.txt: {e}")
            return False

def verify_python_installation():
    """Verify Python installation and version"""
    print("Checking Python installation...")
    try:
        python_version = sys.version_info
        print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("Warning: Python 3.8 or higher is recommended for this application.")
            print(f"Current version: {python_version.major}.{python_version.minor}.{python_version.micro}")
            return False
        return True
    except Exception as e:
        print(f"Error checking Python version: {e}")
        return False

def load_env_variables(backend_dir):
    """Load environment variables from .env file"""
    env_file = os.path.join(backend_dir, ".env")
    env_vars = os.environ.copy()
    
    if os.path.exists(env_file):
        print(f"Loading environment variables from {env_file}")
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            env_vars[key] = value.strip('"').strip("'")
                        except ValueError:
                            print(f"Warning: Could not parse line in .env file: {line}")
            
            api_key = env_vars.get('OPENROUTER_API_KEY', '')
            if api_key:
                print(f"OpenRouter API Key: {api_key[:10]}...")
            else:
                print("Warning: OpenRouter API Key not found in .env file.")
                env_vars['OPENROUTER_API_KEY'] = "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"
                print("Using default API key for testing.")
        except Exception as e:
            print(f"Error loading .env file: {e}")
    else:
        print(f"Warning: .env file not found at {env_file}")
        print("Creating .env file with default API key...")
        try:
            with open(env_file, 'w') as f:
                f.write("# OpenRouter API Key\n")
                f.write("# Real API key provided by user\n")
                f.write('OPENROUTER_API_KEY="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"\n')
            print(f"Created .env file at {env_file}")
            return load_env_variables(backend_dir)
        except Exception as e:
            print(f"Failed to create .env file: {e}")
    
    return env_vars

def main():
    print("\n" + "="*80)
    print("Mastra AI Excel VBA Generator - Launcher")
    print("="*80 + "\n")
    
    project_root = find_project_root()
    print(f"Project root directory: {project_root}")
    
    if not verify_python_installation():
        print("Warning: Continuing with current Python version, but some features may not work correctly.")
    
    backend_dir = os.path.join(project_root, "backend")
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        print("\nCurrent directory structure:")
        for root, dirs, files in os.walk(project_root):
            print(f"Directory: {root}")
            for d in dirs:
                print(f"  - {d}/")
            for f in files:
                print(f"  - {f}")
        print("\nPlease make sure you extracted the entire ZIP file and are running this script from the correct location.")
        input("\nPress Enter to exit...")
        return
    
    app_main_path = os.path.join(backend_dir, "app", "main.py")
    if not os.path.exists(app_main_path):
        print(f"Error: app/main.py not found at {app_main_path}")
        print("\nCurrent app directory structure:")
        app_dir = os.path.join(backend_dir, "app")
        if os.path.exists(app_dir):
            for root, dirs, files in os.walk(app_dir):
                print(f"Directory: {root}")
                for d in dirs:
                    print(f"  - {d}/")
                for f in files:
                    print(f"  - {f}")
        print("\nPlease make sure you extracted the entire ZIP file and are running this script from the correct location.")
        input("\nPress Enter to exit...")
        return
    
    if not install_requirements(backend_dir):
        print("Failed to install required packages. The application may not work correctly.")
        input("\nPress Enter to continue anyway or Ctrl+C to exit...")
    
    if is_port_in_use(8000):
        print("\nWarning: Port 8000 is already in use. The application may not start correctly.")
        print("Please close any other applications using port 8000 and try again.")
        print("Common applications that use port 8000 include:")
        print("- Other instances of this application")
        print("- Web servers (Apache, Nginx, etc.)")
        print("- Development servers (Django, Flask, etc.)")
        choice = input("\nDo you want to continue anyway? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting application.")
            return
    
    env_vars = load_env_variables(backend_dir)
    
    print("\nStarting backend server...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=backend_dir,
            env=env_vars,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("Waiting for backend server to start...")
        if check_server_running(8000, max_attempts=60):
            print("\n✅ Backend server started successfully!")
            print("\nOpening application in browser...")
            
            time.sleep(2)
            
            try:
                webbrowser.open("http://localhost:8000")
                print("\n✅ Application opened in browser.")
            except Exception as e:
                print(f"\nError opening browser: {e}")
                print("Please manually open your browser and navigate to: http://localhost:8000")
            
            print("\n" + "="*80)
            print("Mastra AI Excel VBA Generator is now running!")
            print("="*80)
            print("\nPress Ctrl+C to stop the application.")
            
            while backend_process.poll() is None:
                try:
                    if not is_port_in_use(8000):
                        print("\nWarning: Backend server is no longer responding on port 8000.")
                        print("Attempting to restart the server...")
                        backend_process.terminate()
                        backend_process = subprocess.Popen(
                            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
                            cwd=backend_dir,
                            env=env_vars
                        )
                        if check_server_running(8000):
                            print("Backend server restarted successfully!")
                        else:
                            print("Failed to restart backend server.")
                            break
                    
                    time.sleep(5)
                except KeyboardInterrupt:
                    print("\nStopping application...")
                    backend_process.terminate()
                    print("Application stopped.")
                    return
                except Exception as e:
                    print(f"\nError monitoring server: {e}")
                    break
            
            stdout, stderr = backend_process.communicate()
            print("\nBackend server has stopped.")
            if stdout:
                print("\nServer output:")
                print(stdout)
            if stderr:
                print("\nServer errors:")
                print(stderr)
        else:
            stdout, stderr = backend_process.communicate()
            print("\n❌ Error: Backend server failed to start within the timeout period.")
            print("\nServer output:")
            if stdout:
                print(stdout)
            print("\nServer errors:")
            if stderr:
                print(stderr)
            
            print("\nPlease check the following:")
            print("1. Make sure all required packages are installed")
            print("2. Check if port 8000 is already in use by another application")
            print("3. Check if there are any errors in the backend code")
            
            backend_process.terminate()
    except Exception as e:
        print(f"\n❌ Error starting backend server: {e}")
        print("\nDetailed error information:")
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nDetailed error information:")
        traceback.print_exc()
        input("\nPress Enter to exit...")
