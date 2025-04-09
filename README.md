# Mastra AI Excel VBA Generator

複数のLLM（GPT-4 Turbo、Gemini 2.0、Claude 3、Mixtral）を連携させ、自動的にExcelファイルへの入力を行うVBAコードを生成するWindows11用アプリケーション

## 概要

このアプリケーションは、チャットとExcelファイルをもとに、複数のLLMを連携させて安全施工計画書とリスクアセスメントのためのVBAコードを自動生成します。

### 主な機能

1. **UI機能**
   - チャット送信可能なUI（React）
   - Excelファイル(.xlsm)のアップロード
   - 確定事項入力フォーム（工事名、施工場所、工期、作業者数）

2. **LLM連携機能（OpenRouter API）**
   - GPT-4 Turbo：チャット内容の論理的構造化
   - Gemini 2.0：Excelデータ構造の分析
   - Claude 3：表現の曖昧さを明確化
   - Mixtral：細かいニュアンスや例外処理の補完

3. **インタラクティブ質問プロセス**
   - 初回：工事名、施工場所、工期、作業員数など確定情報を聞く
   - 2回目以降：LLMが不足と判断した情報を追加で質問
   - 最終確認：入力項目を整理してユーザーに最終確認

4. **ナレッジベース自動構築**
   - Excelファイルの指定されたセル範囲を自動解析してナレッジ化

5. **VBAコード生成**
   - 準備作業→本作業→後始末作業の順に、Excelファイルに入力するためのVBAコードを作成

## インストール方法

### 開発環境

#### フロントエンド（React）

```bash
cd frontend
npm install
npm run dev
```

#### バックエンド（FastAPI）

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### 本番環境（Windows 11用アプリケーション）

1. リリースページから最新のインストーラーをダウンロード
2. インストーラーを実行し、画面の指示に従ってインストール
3. デスクトップに作成されたショートカットからアプリケーションを起動

## 設定

### OpenRouter APIキーの設定

1. [OpenRouter](https://openrouter.ai/)でアカウントを作成し、APIキーを取得
2. `backend/.env`ファイルを作成または編集し、以下の内容を追加：

```
OPENROUTER_API_KEY="あなたのAPIキー"
```

## 使用方法

1. アプリケーションを起動
2. Excelファイル(.xlsm)をアップロード
3. 確定事項（工事名、施工場所、工期、作業者数）を入力
4. AIアシスタントとチャットして、工事の詳細情報を提供
5. 「VBAコードを生成」ボタンをクリックしてVBAコードを生成
6. 生成されたVBAコードをコピーしてExcelファイルのVBAエディタに貼り付け

## 開発者向け情報

### パッケージング方法

Windows 11用のexe形式アプリケーションを作成するには：

```bash
python package_app.py
```

生成されたアプリケーションは`dist`ディレクトリに保存されます。

### テスト

APIワークフローのテストを実行するには：

```bash
python test_api_workflow.py
```

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
