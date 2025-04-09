import os
import httpx
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from .models import Message, FormData

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

USE_MOCK_RESPONSE = False

GPT4_TURBO_MODEL = "openai/gpt-4-turbo"
GEMINI_MODEL = "google/gemini-pro"
CLAUDE_MODEL = "anthropic/claude-3-opus"
MIXTRAL_MODEL = "mistralai/mixtral-8x7b"

IS_TEST_MODE = OPENROUTER_API_KEY == "sk-or-v1-test-key"
if IS_TEST_MODE:
    logger.warning("Using test API key. Responses will be mock data. For production, set a real OpenRouter API key.")
else:
    logger.info("Using production OpenRouter API key.")

async def call_openrouter(
    model: str, 
    messages: List[Dict[str, str]], 
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """
    Call the OpenRouter API with the specified model and messages.
    For testing, returns a mock response if using a test API key.
    """
    api_key = OPENROUTER_API_KEY
    if api_key:
        logger.info(f"Using API key starting with: {api_key[:10]}...")
    else:
        logger.error("No API key found!")
        raise ValueError("OpenRouter API key is not set")
    
    if api_key == "sk-or-v1-test-key" or not api_key:
        logger.warning("Using mock response instead of real API call")
        return {
            "choices": [
                {
                    "message": {
                        "content": "これはテスト応答です。実際のAPIキーを使用すると、本物のLLMからの応答が返されます。"
                    }
                }
            ]
        }
    
    if not api_key or len(api_key) < 20:
        api_key = "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"
        logger.warning(f"Using hardcoded API key: {api_key[:10]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mastra-ai-excel-vba-generator.app",
        "OpenAI-Organization": "org-dummy",  # Required by OpenRouter
        "X-Title": "Mastra AI Excel VBA Generator"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Calling OpenRouter API with model: {model}")
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                error_text = response.text
                logger.error(f"OpenRouter API error: {error_text}")
                raise Exception(f"OpenRouter API error: {error_text}")
            
            return response.json()
    except Exception as e:
        logger.error(f"Error in call_openrouter: {str(e)}")
        return {
            "choices": [
                {
                    "message": {
                        "content": f"APIエラーが発生しました。詳細: {str(e)}"
                    }
                }
            ]
        }

async def structure_chat_content(chat_history: List[Message]) -> str:
    """
    Use GPT-4 Turbo to structure chat content logically.
    """
    formatted_messages = [
        {"role": msg.role, "content": msg.content} 
        for msg in chat_history
    ]
    
    formatted_messages.insert(0, {
        "role": "system",
        "content": "あなたはチャット内容を論理的に構造化するアシスタントです。ユーザーとの会話から重要な情報を抽出し、整理してください。"
    })
    
    response = await call_openrouter(
        model=GPT4_TURBO_MODEL,
        messages=formatted_messages,
        temperature=0.3
    )
    
    return response["choices"][0]["message"]["content"]

async def analyze_excel_structure(excel_data: Dict[str, Any]) -> str:
    """
    Use Gemini 2.0 to analyze Excel data structure.
    """
    excel_data_str = str(excel_data)
    
    messages = [
        {
            "role": "system",
            "content": "あなたはExcelデータ構造を分析するアシスタントです。提供されたExcelデータを分析し、その構造と内容を理解してください。"
        },
        {
            "role": "user",
            "content": f"以下のExcelデータを分析してください:\n\n{excel_data_str}"
        }
    ]
    
    response = await call_openrouter(
        model=GEMINI_MODEL,
        messages=messages,
        temperature=0.2
    )
    
    return response["choices"][0]["message"]["content"]

async def clarify_ambiguities(content: str) -> str:
    """
    Use Claude 3 to clarify ambiguous expressions.
    """
    messages = [
        {
            "role": "system",
            "content": "あなたは表現の曖昧さを明確化するアシスタントです。提供されたテキストの曖昧な表現を特定し、より明確にしてください。"
        },
        {
            "role": "user",
            "content": f"以下のテキストの曖昧な表現を明確にしてください:\n\n{content}"
        }
    ]
    
    response = await call_openrouter(
        model=CLAUDE_MODEL,
        messages=messages,
        temperature=0.4
    )
    
    return response["choices"][0]["message"]["content"]

async def handle_edge_cases(content: str) -> str:
    """
    Use Mixtral to handle nuances and edge cases.
    """
    messages = [
        {
            "role": "system",
            "content": "あなたは細かいニュアンスや例外処理を補完するアシスタントです。提供されたテキストの中で、特殊なケースや例外的な状況を特定し、それに対する処理方法を提案してください。"
        },
        {
            "role": "user",
            "content": f"以下のテキストの中の細かいニュアンスや例外的なケースを特定し、対処方法を提案してください:\n\n{content}"
        }
    ]
    
    response = await call_openrouter(
        model=MIXTRAL_MODEL,
        messages=messages,
        temperature=0.5
    )
    
    return response["choices"][0]["message"]["content"]

async def generate_vba_code(
    form_data: FormData,
    excel_data: Optional[Dict[str, Any]],
    chat_history: List[Message]
) -> str:
    """
    Generate VBA code based on form data, Excel data, and chat history.
    Uses all LLMs in sequence to create comprehensive VBA code.
    """
    structured_content = await structure_chat_content(chat_history)
    
    excel_analysis = ""
    if excel_data:
        excel_analysis = await analyze_excel_structure(excel_data)
    
    combined_content = f"構造化されたチャット内容:\n{structured_content}\n\nExcelデータ分析:\n{excel_analysis}"
    clarified_content = await clarify_ambiguities(combined_content)
    
    refined_content = await handle_edge_cases(clarified_content)
    
    vba_prompt = f"""
    以下の情報に基づいて、Excelファイルに入力するためのVBAコードを生成してください。

    - 工事名（セルI9）: {form_data.projectName}
    - 施工場所（セルI11）: {form_data.location}
    - 工期（セルI13）: {form_data.period}
    - 作業者数（セルQ15）: {form_data.workerCount}

    {refined_content}

    1. 準備作業→本作業→後始末作業の順に記述する
    2. 安全施工計画書シート：D, AS, BK列（行34-43, 54-73, 81-100, 108-127）にデータを入力
    3. リスクアセスメントシート：C, O, Y, AI, AS, CC, AV, CF, BE, CL列（行34, 37, 40, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 192, 195, 198, 201, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 240～567）にデータを入力

    VBAコードのみを返してください。コメントは日本語で記述してください。
    """
    
    messages = [
        {
            "role": "system",
            "content": "あなたはExcel VBAコードを生成する専門家です。提供された情報に基づいて、正確で効率的なVBAコードを生成してください。"
        },
        {
            "role": "user",
            "content": vba_prompt
        }
    ]
    
    response = await call_openrouter(
        model=GPT4_TURBO_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=2000
    )
    
    return response["choices"][0]["message"]["content"]

async def generate_follow_up_questions(
    chat_history: List[Message],
    form_data: Optional[FormData] = None,
    question_round: int = 1
) -> str:
    """
    Generate follow-up questions based on chat history and current form data.
    Uses GPT-4 Turbo to identify missing information.
    """
    try:
        formatted_messages = [
            {"role": msg.role, "content": msg.content} 
            for msg in chat_history
        ]
        
        if question_round == 1:
            system_content = """
            あなたは建設プロジェクトの安全計画に関する情報を収集するアシスタントです。
            初回の質問として、以下の情報を収集してください：
            1. 工事名（どのような工事か）
            2. 施工場所（どこで行われるか）
            3. 工期（いつからいつまでか）
            4. 作業者数（何人の作業員が関わるか）
            
            丁寧かつ簡潔に質問してください。
            """
        elif question_round == 2:
            system_content = """
            あなたは建設プロジェクトの安全計画に関する情報を収集するアシスタントです。
            2回目の質問として、以下のような追加情報を収集してください：
            1. 工事の具体的な内容（どのような作業が行われるか）
            2. 使用する主な機械・工具
            3. 特に注意すべき危険要因
            4. 過去に類似工事で発生した事故やヒヤリハット
            
            ユーザーがすでに提供した情報に基づいて、不足している情報を特定し質問してください。
            """
        else:
            system_content = """
            あなたは建設プロジェクトの安全計画に関する情報を収集するアシスタントです。
            最終確認として、これまでに収集した情報を整理し、まだ不足している重要な情報があれば質問してください。
            特に以下の点に注目してください：
            1. 安全対策の具体的な内容
            2. 緊急時の連絡体制
            3. 特殊な作業条件や環境要因
            4. 法令遵守に関する確認事項
            
            最後に、収集した情報に基づいてVBAコードを生成する準備ができていることを伝えてください。
            """
        
        form_data_str = ""
        if form_data:
            form_data_str = f"""
            現在把握している確定情報：
            - 工事名: {form_data.projectName}
            - 施工場所: {form_data.location}
            - 工期: {form_data.period}
            - 作業者数: {form_data.workerCount}
            """
        
        formatted_messages.insert(0, {
            "role": "system",
            "content": system_content + form_data_str
        })
        
        if OPENROUTER_API_KEY == "sk-or-v1-test-key" or not OPENROUTER_API_KEY:
            logger.warning("Using mock response for generate_follow_up_questions")
            if question_round == 1:
                return "工事名、施工場所、工期、作業者数についての情報をありがとうございます。次に以下の情報を教えていただけますか？\n\n1. 工事の具体的な内容（どのような作業が行われるか）\n2. 使用する主な機械・工具\n3. 特に注意すべき危険要因\n4. 過去に類似工事で発生した事故やヒヤリハット"
            elif question_round == 2:
                return "ありがとうございます。最後に以下の点について教えていただけますか？\n\n1. 安全対策の具体的な内容\n2. 緊急時の連絡体制\n3. 特殊な作業条件や環境要因\n4. 法令遵守に関する確認事項"
            else:
                return "これまでに提供していただいた情報をもとに、VBAコードを生成する準備が整いました。フォームに必要事項を入力し、「VBAコード生成」ボタンをクリックしてください。"
        
        try:
            response = await call_openrouter(
                model=GPT4_TURBO_MODEL,
                messages=formatted_messages,
                temperature=0.7
            )
            
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {str(e)}")
            return f"申し訳ありませんが、OpenRouter APIとの通信中にエラーが発生しました。詳細: {str(e)}"
    
    except Exception as e:
        logger.error(f"Error in generate_follow_up_questions: {str(e)}")
        return "申し訳ありませんが、質問生成中にエラーが発生しました。もう一度お試しください。"
