@echo off
echo ================================================================================
echo Mastra AI Excel VBA Generator - スーパーデバッグモード
echo ================================================================================
echo.

echo このバッチファイルはコマンドプロンプトを強制的に開いたままにし、詳細なデバッグ情報を表示します。
echo アプリケーションがすぐに閉じてしまう場合に使用してください。
echo.

echo Pythonのインストールを確認中...
python --version
if %errorlevel% neq 0 (
    echo [エラー] Pythonがインストールされていないか、PATHに設定されていません。
    echo https://www.python.org/downloads/ からPython 3.8以上をインストールしてください。
    echo インストール時に「Add Python to PATH」にチェックを入れてください。
    pause
    exit /b 1
)

echo 必要なパッケージをインストール中...
pip install PyQt6 PyQt6-WebEngine
pip install -r backend/requirements.txt

echo.
echo ディレクトリ構造を確認中...
dir /s /b backend\app
dir /s /b frontend\dist

echo.
echo 環境変数を設定中...
set PYTHONPATH=%CD%
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set DEBUG_MODE=1

echo.
echo アプリケーションを起動中...
echo エラーが発生した場合は以下に表示されます。
echo.

python -u standalone_app.py

echo.
echo アプリケーションが終了しました。
echo エラーメッセージを確認してください。
echo ログファイル mastra_app_log.txt も確認してください。
echo.
echo 終了するには任意のキーを押してください...
pause > nul
