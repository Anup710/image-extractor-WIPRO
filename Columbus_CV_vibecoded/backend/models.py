from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UploadedFile(BaseModel):
    filename: str
    content_type: str
    size: int
    stored: bool
    path: Optional[str] = None
    content: Optional[bytes] = None

class UploadResponse(BaseModel):
    session_id: str
    files: List[UploadedFile]
    stored: bool

class ImageData(BaseModel):
    filename: str
    content: str  # base64 encoded
    content_type: str

class ChatRequest(BaseModel):
    prompt: str
    images: Optional[List[ImageData]] = []
    template: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str]
    timestamp: str

class PromptTemplate(BaseModel):
    name: str
    template: str
    description: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str