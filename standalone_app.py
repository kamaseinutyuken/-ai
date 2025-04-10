import sys
import os
import threading
import webbrowser
import traceback
import logging
import time
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QCoreApplication, QTimer

log_file = "mastra_app_log.txt"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MastraAI")

def global_exception_handler(exctype, value, tb):
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    logger.error(f"未処理の例外: {error_msg}")
    try:
        QMessageBox.critical(None, "エラー", f"アプリケーションでエラーが発生しました:\n{str(value)}\n\n詳細はログファイルを確認してください: {log_file}")
    except:
        pass
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler

try:
    from backend.app.main import app as fastapi_app
    import uvicorn
except Exception as e:
    logger.error(f"バックエンドのインポートエラー: {str(e)}\n{traceback.format_exc()}")
    QMessageBox.critical(None, "起動エラー", f"バックエンドモジュールの読み込みに失敗しました:\n{str(e)}")
    sys.exit(1)

class MastraAIApp(QMainWindow):
    def __init__(self):
        try:
            logger.info("アプリケーション初期化開始")
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
            
            logger.info(f"バックエンドサーバーを起動: {self.host}:{self.port}")
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
            
            QTimer.singleShot(2000, self.load_application)
            logger.info("アプリケーション初期化完了")
        except Exception as e:
            logger.error(f"アプリケーション初期化エラー: {str(e)}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "初期化エラー", f"アプリケーションの初期化に失敗しました:\n{str(e)}")
            raise
    
    def run_server(self):
        """バックエンドサーバーをアプリケーション内部で実行"""
        try:
            logger.info("バックエンドサーバー起動中...")
            uvicorn.run(fastapi_app, host=self.host, port=self.port)
        except Exception as e:
            logger.error(f"サーバー起動エラー: {str(e)}\n{traceback.format_exc()}")
            error = str(e)
            QTimer.singleShot(0, lambda: QMessageBox.critical(None, "サーバーエラー", 
                                                           f"バックエンドサーバーの起動に失敗しました:\n{error}"))
    
    def load_application(self):
        """フロントエンドをWebViewにロード"""
        try:
            logger.info("フロントエンドをロード中...")
            url = f"http://{self.host}:{self.port}"
            self.web_view.load(QUrl(url))
            logger.info(f"URL {url} をロードしました")
        except Exception as e:
            logger.error(f"フロントエンドロードエラー: {str(e)}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "ロードエラー", f"フロントエンドのロードに失敗しました:\n{str(e)}")

def main():
    try:
        logger.info("アプリケーション起動開始")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ["PYTHONPATH"] = base_dir
        logger.info(f"PYTHONPATH: {base_dir}")
        
        if os.path.exists(os.path.join(base_dir, ".env")):
            logger.info(".envファイルが存在します")
        else:
            logger.warning(".envファイルが見つかりません")
            
        if os.path.exists(os.path.join(base_dir, "backend", ".env")):
            logger.info("backend/.envファイルが存在します")
        else:
            logger.warning("backend/.envファイルが見つかりません")
        
        frontend_dist = os.path.join(base_dir, "frontend", "dist")
        if os.path.exists(frontend_dist):
            logger.info(f"フロントエンドディレクトリが存在します: {frontend_dist}")
        else:
            logger.error(f"フロントエンドディレクトリが見つかりません: {frontend_dist}")
            QMessageBox.critical(None, "起動エラー", f"フロントエンドファイルが見つかりません:\n{frontend_dist}")
        
        app = QApplication(sys.argv)
        window = MastraAIApp()
        window.show()
        logger.info("アプリケーションウィンドウを表示")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"アプリケーション起動エラー: {str(e)}\n{traceback.format_exc()}")
        QMessageBox.critical(None, "致命的エラー", f"アプリケーションの起動に失敗しました:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"メイン関数エラー: {str(e)}\n{traceback.format_exc()}")
        print(f"致命的エラー: {str(e)}")
        input("Enterキーを押して終了...")
        sys.exit(1)
