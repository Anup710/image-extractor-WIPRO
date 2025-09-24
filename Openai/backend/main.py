from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import shutil
from datetime import datetime
import uuid

from models import ChatRequest, ChatResponse, UploadResponse
from services.gpt_service import GPTService
from services.storage_service import StorageService

app = FastAPI(title="GPT-5 Wrapper API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gpt_service = GPTService()
storage_service = StorageService()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/upload", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    store_files: bool = Form(False)
):
    try:
        uploaded_files = []
        session_id = str(uuid.uuid4())

        for file in files:
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not an image")

            # Read file content
            content = await file.read()

            # Store file if user consents
            file_path = None
            if store_files:
                file_path = await storage_service.store_file(file, session_id)

            uploaded_files.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "stored": store_files,
                "path": file_path,
                "content": content  # For immediate processing
            })

        return UploadResponse(
            session_id=session_id,
            files=uploaded_files,
            stored=store_files
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_gpt(request: ChatRequest):
    try:
        # Process the chat request with GPT-5
        response = await gpt_service.process_chat(
            prompt=request.prompt,
            images=request.images,
            template=request.template
        )

        return ChatResponse(
            response=response,
            session_id=request.session_id,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)