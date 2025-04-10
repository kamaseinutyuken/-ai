import sys
import os
import threading
import webbrowser
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QCoreApplication

from backend.app.main import app as fastapi_app
import uvicorn

class MastraAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mastra AI Excel VBA Generator")
        self.setGeometry(100, 100, 1200, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        self.host = "127.0.0.1"
        self.port = 1337
        
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()
        
        self.load_application()
    
    def run_server(self):
        """バックエンドサーバーをアプリケーション内部で実行"""
        uvicorn.run(fastapi_app, host=self.host, port=self.port)
    
    def load_application(self):
        """フロントエンドをWebViewにロード"""
        import time
        time.sleep(1.5)
        url = f"http://{self.host}:{self.port}"
        self.web_view.load(QUrl(url))

def main():
    os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
    
    app = QApplication(sys.argv)
    window = MastraAIApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
