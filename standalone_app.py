import sys
import os
import threading
import webbrowser
import traceback
import logging
import time
import importlib.util
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QCoreApplication, QTimer

log_file = "mastra_app_log.txt"
if os.path.exists(log_file):
    backup_log = f"{log_file}.bak"
    try:
        shutil.copy2(log_file, backup_log)
        print(f"前回のログファイルをバックアップしました: {backup_log}")
    except Exception as e:
        print(f"ログファイルのバックアップに失敗しました: {str(e)}")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),  # 上書きモード
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MastraAI")

logger.info("=" * 80)
logger.info("Mastra AI Excel VBA Generator 起動")
logger.info(f"Python バージョン: {sys.version}")
logger.info(f"実行パス: {os.path.abspath(__file__)}")
logger.info(f"作業ディレクトリ: {os.getcwd()}")
logger.info(f"環境変数: {dict(os.environ)}")
logger.info("=" * 80)

def global_exception_handler(exctype, value, tb):
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    logger.error(f"未処理の例外: {error_msg}")
    try:
        print(f"\n致命的エラー: {str(value)}\n")
        print(f"詳細なエラー情報:\n{error_msg}")
        print(f"ログファイル: {os.path.abspath(log_file)}")
        
        QMessageBox.critical(None, "エラー", 
                            f"アプリケーションでエラーが発生しました:\n{str(value)}\n\n"
                            f"詳細はログファイルを確認してください: {log_file}\n\n"
                            f"エラータイプ: {exctype.__name__}")
    except Exception as e:
        print(f"エラーメッセージの表示に失敗: {str(e)}")
    
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler

def check_module_exists(module_name):
    """モジュールが存在するか確認する"""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except ModuleNotFoundError:
        return False

required_modules = ["uvicorn", "fastapi", "PyQt6", "PyQt6.QtWebEngineWidgets"]
missing_modules = []

for module in required_modules:
    if not check_module_exists(module):
        missing_modules.append(module)
        logger.error(f"必要なモジュール {module} が見つかりません")

if missing_modules:
    error_msg = f"以下の必要なモジュールがインストールされていません:\n{', '.join(missing_modules)}\n\npip install {' '.join(missing_modules)} を実行してください。"
    logger.error(error_msg)
    print(error_msg)
    try:
        QMessageBox.critical(None, "モジュールエラー", error_msg)
    except:
        pass
    input("Enterキーを押して終了...")
    sys.exit(1)

try:
    logger.info("バックエンドモジュールをインポート中...")
    from backend.app.main import app as fastapi_app
    import uvicorn
    logger.info("バックエンドモジュールのインポートに成功しました")
except Exception as e:
    error_msg = f"バックエンドのインポートエラー: {str(e)}\n{traceback.format_exc()}"
    logger.error(error_msg)
    print(f"\n{error_msg}\n")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    backend_app_dir = os.path.join(backend_dir, "app")
    
    logger.info(f"バックエンドディレクトリ確認: {backend_dir} 存在={os.path.exists(backend_dir)}")
    logger.info(f"バックエンドアプリディレクトリ確認: {backend_app_dir} 存在={os.path.exists(backend_app_dir)}")
    
    if os.path.exists(backend_app_dir):
        logger.info(f"バックエンドアプリディレクトリの内容: {os.listdir(backend_app_dir)}")
    
    try:
        QMessageBox.critical(None, "起動エラー", 
                           f"バックエンドモジュールの読み込みに失敗しました:\n{str(e)}\n\n"
                           f"詳細はログファイル {log_file} を確認してください。")
    except:
        pass
    
    input("Enterキーを押して終了...")
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
            
            logger.info("WebViewを初期化中...")
            try:
                self.web_view = QWebEngineView()
                layout.addWidget(self.web_view)
                logger.info("WebViewの初期化に成功しました")
            except Exception as e:
                logger.error(f"WebView初期化エラー: {str(e)}\n{traceback.format_exc()}")
                QMessageBox.critical(self, "WebViewエラー", f"WebViewの初期化に失敗しました:\n{str(e)}")
                raise
            
            self.host = "127.0.0.1"
            self.port = 1337
            self.server_started = False
            
            logger.info(f"バックエンドサーバーを起動: {self.host}:{self.port}")
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
            
            logger.info("サーバー起動を待機中...")
            wait_time = 0
            max_wait = 10  # 最大10秒待機
            while not self.server_started and wait_time < max_wait:
                time.sleep(0.5)
                wait_time += 0.5
                QCoreApplication.processEvents()  # UIの応答性を維持
            
            if not self.server_started and wait_time >= max_wait:
                logger.warning(f"サーバー起動タイムアウト（{max_wait}秒）")
            
            QTimer.singleShot(2000, self.load_application)
            logger.info("アプリケーション初期化完了")
        except Exception as e:
            logger.error(f"アプリケーション初期化エラー: {str(e)}\n{traceback.format_exc()}")
            print(f"\nアプリケーション初期化エラー: {str(e)}")
            try:
                QMessageBox.critical(self, "初期化エラー", 
                                   f"アプリケーションの初期化に失敗しました:\n{str(e)}\n\n"
                                   f"詳細はログファイル {log_file} を確認してください。")
            except:
                pass
            input("Enterキーを押して終了...")
            raise
    
    def run_server(self):
        """バックエンドサーバーをアプリケーション内部で実行"""
        try:
            logger.info("バックエンドサーバー起動中...")
            self.server_started = True  # サーバー起動フラグを設定
            uvicorn.run(fastapi_app, host=self.host, port=self.port)
        except Exception as e:
            self.server_started = False
            error_msg = f"サーバー起動エラー: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            print(f"\n{error_msg}\n")
            
            error_str = str(e)  # エラー文字列を保存
            try:
                QTimer.singleShot(0, lambda: QMessageBox.critical(None, "サーバーエラー", 
                                                               f"バックエンドサーバーの起動に失敗しました:\n{error_str}\n\n"
                                                               f"詳細はログファイル {log_file} を確認してください。"))
            except:
                pass
    
    def load_application(self):
        """フロントエンドをWebViewにロード"""
        try:
            logger.info("フロントエンドをロード中...")
            url = f"http://{self.host}:{self.port}"
            self.web_view.load(QUrl(url))
            logger.info(f"URL {url} をロードしました")
        except Exception as e:
            error_msg = f"フロントエンドロードエラー: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            print(f"\n{error_msg}\n")
            
            try:
                QMessageBox.critical(self, "ロードエラー", 
                                   f"フロントエンドのロードに失敗しました:\n{str(e)}\n\n"
                                   f"詳細はログファイル {log_file} を確認してください。")
            except:
                pass

def main():
    try:
        logger.info("アプリケーション起動開始")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ["PYTHONPATH"] = base_dir
        logger.info(f"PYTHONPATH: {base_dir}")
        
        missing_files = []
        
        if os.path.exists(os.path.join(base_dir, ".env")):
            logger.info(".envファイルが存在します")
        else:
            logger.warning(".envファイルが見つかりません")
            missing_files.append(".env")
            
        if os.path.exists(os.path.join(base_dir, "backend", ".env")):
            logger.info("backend/.envファイルが存在します")
        else:
            logger.warning("backend/.envファイルが見つかりません")
            missing_files.append("backend/.env")
        
        frontend_dist = os.path.join(base_dir, "frontend", "dist")
        if os.path.exists(frontend_dist):
            logger.info(f"フロントエンドディレクトリが存在します: {frontend_dist}")
            frontend_files = os.listdir(frontend_dist)
            logger.info(f"フロントエンドファイル: {frontend_files}")
        else:
            logger.error(f"フロントエンドディレクトリが見つかりません: {frontend_dist}")
            missing_files.append("frontend/dist")
        
        backend_app_dir = os.path.join(base_dir, "backend", "app")
        if os.path.exists(backend_app_dir):
            logger.info(f"バックエンドアプリディレクトリが存在します: {backend_app_dir}")
            backend_files = os.listdir(backend_app_dir)
            logger.info(f"バックエンドファイル: {backend_files}")
        else:
            logger.error(f"バックエンドアプリディレクトリが見つかりません: {backend_app_dir}")
            missing_files.append("backend/app")
        
        if missing_files:
            warning_msg = f"以下の必要なファイル/ディレクトリが見つかりません:\n{', '.join(missing_files)}"
            logger.warning(warning_msg)
            print(f"\n警告: {warning_msg}\n")
            
            try:
                QMessageBox.warning(None, "ファイル不足", warning_msg)
            except:
                pass
        
        logger.info("QApplicationを初期化中...")
        app = QApplication(sys.argv)
        
        logger.info("MastraAIAppを初期化中...")
        window = MastraAIApp()
        
        logger.info("ウィンドウを表示中...")
        window.show()
        
        logger.info("アプリケーションウィンドウを表示")
        return_code = app.exec()
        logger.info(f"アプリケーション終了（コード: {return_code}）")
        sys.exit(return_code)
    except Exception as e:
        error_msg = f"アプリケーション起動エラー: {str(e)}\n{traceback.format_exc()}"
        logger.critical(error_msg)
        print(f"\n致命的エラー: {error_msg}\n")
        
        try:
            QMessageBox.critical(None, "致命的エラー", 
                               f"アプリケーションの起動に失敗しました:\n{str(e)}\n\n"
                               f"詳細はログファイル {log_file} を確認してください。")
        except:
            pass
        
        input("Enterキーを押して終了...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        print("Mastra AI Excel VBA Generator を起動中...")
        print(f"ログファイル: {os.path.abspath(log_file)}")
        main()
    except Exception as e:
        error_msg = f"メイン関数エラー: {str(e)}\n{traceback.format_exc()}"
        logger.critical(error_msg)
        print(f"\n致命的エラー: {error_msg}\n")
        print(f"詳細はログファイル {os.path.abspath(log_file)} を確認してください。")
        input("Enterキーを押して終了...")
        sys.exit(1)
