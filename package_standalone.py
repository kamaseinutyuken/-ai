import os
import subprocess
import sys
import shutil
from pathlib import Path

def check_requirements():
    """必要なツールがインストールされているか確認"""
    print("要件を確認中...")
    
    try:
        subprocess.check_output(["pyinstaller", "--version"])
    except:
        print("PyInstallerをインストール中...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import PyQt6
    except ImportError:
        print("PyQt6をインストール中...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6", "PyQt6-WebEngine"])
    
    return True

def build_frontend():
    """Reactフロントエンドをビルド"""
    print("\nフロントエンドをビルド中...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print(f"エラー: フロントエンドディレクトリが {frontend_dir.absolute()} に見つかりません")
        return False
    
    if os.path.exists(os.path.join(frontend_dir, "dist")):
        print("フロントエンドのビルドは既に存在します。ビルドステップをスキップします。")
        return True
    
    if not os.path.exists(os.path.join(frontend_dir, "package.json")):
        print("警告: package.jsonが見つかりません。フロントエンドのビルドをスキップします。")
        return True
    
    os.chdir(frontend_dir)
    
    print("フロントエンド依存関係をインストール中...")
    subprocess.check_call(["npm", "install"])
    
    print("フロントエンドをビルド中...")
    subprocess.check_call(["npm", "run", "build"])
    
    os.chdir("..")
    return True

def package_application():
    """PyInstallerを使用してアプリケーションをパッケージング"""
    print("\nアプリケーションをパッケージング中...")
    
    print("バックエンド依存関係をインストール中...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    
    if not os.path.exists(".env") and os.path.exists("backend/.env"):
        shutil.copy("backend/.env", ".env")
        print(".envファイルをコピーしました")
    
    subprocess.check_call(["pyinstaller", "standalone.spec", "--clean"])
    
    output_dir = "dist/Mastra AI Excel VBA Generator"
    if os.path.exists(output_dir):
        output_zip = "mastra_ai_standalone.zip"
        shutil.make_archive("mastra_ai_standalone", 'zip', "dist", "Mastra AI Excel VBA Generator")
        print(f"\nパッケージが {output_zip} として作成されました")
    
    return True

def main():
    print("=== Mastra AI Excel VBA Generator スタンドアロンパッケージングツール ===")
    
    if not check_requirements():
        print("要件を満たせませんでした。終了します。")
        return
    
    if not build_frontend():
        print("フロントエンドのビルドに失敗しました。終了します。")
        return
    
    if not package_application():
        print("アプリケーションのパッケージングに失敗しました。終了します。")
        return
    
    print("\n=== パッケージング完了 ===")
    print("パッケージングされたアプリケーションは 'mastra_ai_standalone.zip' で利用可能です。")
    print("これはサーバーなしで実行できるスタンドアロンアプリケーションです。")

if __name__ == "__main__":
    main()
