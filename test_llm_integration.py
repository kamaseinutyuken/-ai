import asyncio
import os
import logging
from dotenv import load_dotenv
from backend.app.llm_service import (
    structure_chat_content,
    analyze_excel_structure,
    clarify_ambiguities,
    handle_edge_cases,
    generate_vba_code
)
from backend.app.models import Message, FormData

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("llm_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

async def test_gpt4_turbo():
    """GPT-4 Turboを使用したチャット内容の構造化をテスト"""
    logger.info("=== GPT-4 Turboテスト開始 ===")
    test_messages = [
        Message(id="1", role="user", content="このプロジェクトは横浜市内の商業ビル改修工事です。", timestamp=None),
        Message(id="2", role="assistant", content="了解しました。詳細を教えていただけますか？", timestamp=None),
        Message(id="3", role="user", content="工期は2023年6月から2023年9月までの3ヶ月間です。", timestamp=None)
    ]
    
    try:
        result = await structure_chat_content(test_messages)
        logger.info(f"GPT-4 Turbo結果: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"GPT-4 Turboテストエラー: {str(e)}")
        return False

async def test_gemini():
    """Gemini 2.0を使用したExcelデータ構造の分析をテスト"""
    logger.info("=== Gemini 2.0テスト開始 ===")
    test_excel_data = {
        "safety_plan": {
            "fixed_cells": {
                "工事名": "横浜市商業ビル改修工事",
                "施工場所": "横浜市西区みなとみらい",
                "工期": "2023年6月～2023年9月",
                "作業者数": "15"
            }
        }
    }
    
    try:
        result = await analyze_excel_structure(test_excel_data)
        logger.info(f"Gemini 2.0結果: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"Gemini 2.0テストエラー: {str(e)}")
        return False

async def test_claude():
    """Claude 3を使用した曖昧さの明確化をテスト"""
    logger.info("=== Claude 3テスト開始 ===")
    test_content = "工事の際に気をつけるべき点は足場からの転落と電気関連です。"
    
    try:
        result = await clarify_ambiguities(test_content)
        logger.info(f"Claude 3結果: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"Claude 3テストエラー: {str(e)}")
        return False

async def test_mixtral():
    """Mixtralを使用した例外処理の補完をテスト"""
    logger.info("=== Mixtralテスト開始 ===")
    test_content = "雨天時の作業は原則として中止するが、軽微な室内作業は継続可能。"
    
    try:
        result = await handle_edge_cases(test_content)
        logger.info(f"Mixtral結果: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"Mixtralテストエラー: {str(e)}")
        return False

async def test_vba_generation():
    """VBAコード生成機能をテスト"""
    logger.info("=== VBAコード生成テスト開始 ===")
    form_data = FormData(
        projectName="横浜市商業ビル改修工事",
        location="横浜市西区みなとみらい",
        period="2023年6月～2023年9月",
        workerCount=15
    )
    
    test_messages = [
        Message(id="1", role="user", content="このプロジェクトは横浜市内の商業ビル改修工事です。", timestamp=None),
        Message(id="2", role="assistant", content="了解しました。詳細を教えていただけますか？", timestamp=None),
        Message(id="3", role="user", content="工期は2023年6月から2023年9月までの3ヶ月間です。作業内容は内装解体、電気配線工事、壁面塗装、床材交換です。", timestamp=None)
    ]
    
    try:
        result = await generate_vba_code(form_data, None, test_messages)
        logger.info(f"VBAコード生成結果: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"VBAコード生成テストエラー: {str(e)}")
        return False

async def run_all_tests():
    """すべてのLLM統合テストを実行"""
    logger.info("LLM統合テスト開始")
    
    test_results = {
        "GPT-4 Turbo": await test_gpt4_turbo(),
        "Gemini 2.0": await test_gemini(),
        "Claude 3": await test_claude(),
        "Mixtral": await test_mixtral(),
        "VBA生成": await test_vba_generation()
    }
    
    logger.info("===== テスト結果 =====")
    all_passed = True
    for model, result in test_results.items():
        status = "成功" if result else "失敗"
        logger.info(f"{model}: {status}")
        if not result:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("Mastra AI LLM統合テストを実行しています...")
    result = asyncio.run(run_all_tests())
    status = "すべてのテストが成功しました！" if result else "一部のテストが失敗しました。詳細はllm_test.logを確認してください。"
    print(status)
