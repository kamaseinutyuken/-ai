from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime


class FormData(BaseModel):
    projectName: str
    location: str
    period: str
    workerCount: int


class FileUploadResponse(BaseModel):
    filename: str
    status: str
    message: str


class ChatRequest(BaseModel):
    message: str


class LLMResponse(BaseModel):
    content: str
    vba_code: Optional[str] = None


class VBACodeRequest(BaseModel):
    form_data: FormData
    excel_data: Optional[Dict[str, Any]] = None
    chat_history: List[Message]


class VBACodeResponse(BaseModel):
    vba_code: str
