from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import logging
import traceback

from .models import (
    Message, 
    FormData, 
    FileUploadResponse, 
    ChatRequest, 
    LLMResponse,
    VBACodeRequest,
    VBACodeResponse
)
from .llm_service import generate_follow_up_questions
from .excel_service import save_uploaded_file, combine_excel_analysis
from .vba_service import generate_vba_from_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backend_errors.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mastra AI Excel VBA Generator")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

chat_histories = {}  # session_id -> List[Message]
form_data_store = {}  # session_id -> FormData
excel_data_store = {}  # session_id -> Dict
question_rounds = {}  # session_id -> int

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/session")
async def create_session():
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    chat_histories[session_id] = []
    question_rounds[session_id] = 1
    
    welcome_message = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content="こんにちは！Mastra AIへようこそ。安全施工計画書とリスクアセスメントのためのVBAコード生成をお手伝いします。まずは工事名、施工場所、工期、作業者数などの基本情報を教えていただけますか？",
        timestamp=datetime.now()
    )
    chat_histories[session_id].append(welcome_message)
    
    return {"session_id": session_id, "message": welcome_message}

@app.post("/api/chat/{session_id}", response_model=LLMResponse)
async def chat(
    session_id: str,
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    """Process a chat message and generate a response"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_message = Message(
        id=str(uuid.uuid4()),
        role="user",
        content=request.message,
        timestamp=datetime.now()
    )
    chat_histories[session_id].append(user_message)
    
    current_round = question_rounds.get(session_id, 1)
    
    current_form_data = form_data_store.get(session_id)
    
    response_content = await generate_follow_up_questions(
        chat_histories[session_id],
        current_form_data,
        current_round
    )
    
    assistant_message = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content=response_content,
        timestamp=datetime.now()
    )
    chat_histories[session_id].append(assistant_message)
    
    if current_round < 3:
        question_rounds[session_id] = current_round + 1
    
    return LLMResponse(content=response_content)

@app.post("/api/upload/{session_id}", response_model=FileUploadResponse)
async def upload_file(
    session_id: str,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Upload and process an Excel file"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xlsm')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only .xlsx and .xlsm files are supported."
        )
    
    try:
        file_content = await file.read()
        
        file_path = save_uploaded_file(file_content, file.filename)
        
        if background_tasks:
            background_tasks.add_task(process_excel_file, session_id, file_path)
            return FileUploadResponse(
                filename=file.filename,
                status="processing",
                message="ファイルをアップロードしました。処理中です..."
            )
        else:
            await process_excel_file(session_id, file_path)
            return FileUploadResponse(
                filename=file.filename,
                status="completed",
                message="ファイルの処理が完了しました。"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

async def process_excel_file(session_id: str, file_path: str):
    """Process the uploaded Excel file and store the extracted data"""
    try:
        excel_data = combine_excel_analysis(file_path)
        
        excel_data_store[session_id] = excel_data
        
        system_message = Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Excelファイルの解析が完了しました。安全施工計画書とリスクアセスメントの情報を抽出しました。引き続き、必要な情報をお聞かせください。",
            timestamp=datetime.now()
        )
        chat_histories[session_id].append(system_message)
        
    except Exception as e:
        error_message = Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content=f"Excelファイルの処理中にエラーが発生しました: {str(e)}",
            timestamp=datetime.now()
        )
        chat_histories[session_id].append(error_message)

@app.post("/api/form/{session_id}")
async def submit_form(session_id: str, form_data: FormData):
    """Submit form data with confirmed project information"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    form_data_store[session_id] = form_data
    
    confirmation_message = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content=f"以下の情報を確認しました：\n\n"
                f"- 工事名: {form_data.projectName}\n"
                f"- 施工場所: {form_data.location}\n"
                f"- 工期: {form_data.period}\n"
                f"- 作業者数: {form_data.workerCount}\n\n"
                f"これらの情報はExcelファイルの指定されたセルに入力されます。他に必要な情報があればお知らせください。",
        timestamp=datetime.now()
    )
    chat_histories[session_id].append(confirmation_message)
    
    return {"status": "success", "message": "フォームデータを保存しました"}

@app.post("/api/generate-vba/{session_id}", response_model=VBACodeResponse)
async def generate_vba(session_id: str):
    """Generate VBA code based on form data, Excel data, and chat history"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_id not in form_data_store:
        raise HTTPException(
            status_code=400, 
            detail="Form data not found. Please submit the form first."
        )
    
    try:
        form_data = form_data_store[session_id]
        chat_history = chat_histories[session_id]
        
        excel_data = excel_data_store.get(session_id)
        
        vba_code = await generate_vba_from_data(form_data, excel_data, chat_history)
        
        vba_message = Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="VBAコードの生成が完了しました。このコードをExcelファイルのVBAエディタに貼り付けて実行してください。",
            timestamp=datetime.now()
        )
        chat_histories[session_id].append(vba_message)
        
        return VBACodeResponse(vba_code=vba_code)
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"VBA code generation failed: {str(e)}"
        )

@app.get("/api/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    """Get the chat history for a session"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"chat_history": chat_histories[session_id]}

@app.get("/api/form-data/{session_id}")
async def get_form_data(session_id: str):
    """Get the stored form data for a session"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_id not in form_data_store:
        return {"form_data": None}
    
    return {"form_data": form_data_store[session_id]}
