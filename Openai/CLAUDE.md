# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Columbus_CV_vibecoded is a full-stack application that provides a GPT wrapper API with image analysis capabilities. The application consists of a FastAPI backend and a React+TypeScript frontend.

## Architecture

### Backend (FastAPI)
- **Location**: `backend/`
- **Main entry**: `backend/main.py`
- **Framework**: FastAPI with CORS middleware configured for localhost:3000
- **Services**:
  - `GPTService`: Handles OpenAI API integration (currently using gpt-4o model)
  - `StorageService`: Manages file uploads with user consent and session-based storage
- **Models**: Pydantic models in `backend/models.py` for request/response validation
- **Key Features**:
  - Health check endpoint (`/api/health`)
  - File upload with optional storage (`/api/upload`)
  - Chat completion with image support (`/api/chat`)
  - Session-based file management
  - Template system for prompt customization

### Frontend (React + Vite)
- **Location**: `frontend/`
- **Framework**: React 19 with TypeScript, built with Vite
- **Components**:
  - `ImageUpload`: Drag & drop file upload with preview and management
  - `ChatInterface`: Real-time chat with AI including typing indicators
  - `TemplateSelector`: Choose analysis mode (default, analyze, describe, technical)
  - `App`: Main application with sidebar layout and state management
- **Features**: Responsive design, file management, session tracking, error handling

## Development Commands

### Frontend
```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start development server (localhost:3000)
npm run build        # Build for production (runs tsc -b && vite build)
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

### Backend
```bash
cd backend
pip install -r requirements.txt  # Install Python dependencies
cp .env.template .env            # Copy environment template
# Edit .env file and add your OPENAI_API_KEY
python main.py                   # Start FastAPI server on port 8000
```

## Environment Setup

### Backend Dependencies
All dependencies are now listed in `requirements.txt`:
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- openai==1.3.8
- pydantic==2.5.0
- python-multipart==0.0.6
- python-dotenv==1.0.0

### Environment Variables
Create `.env` file in backend directory (copy from `.env.template`):
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (optional, defaults to gpt-4o)
- `HOST`: Server host (optional, defaults to 0.0.0.0)
- `PORT`: Server port (optional, defaults to 8000)
- `FRONTEND_URL`: Frontend URL for CORS (optional, defaults to localhost:3000)

### Frontend Dependencies
- React 19
- TypeScript
- Vite
- ESLint with React hooks and refresh plugins

## API Endpoints

- `GET /api/health`: Health check
- `POST /api/upload`: Upload images with optional storage
- `POST /api/chat`: Process chat requests with optional image analysis

## File Storage

The backend includes a storage service that:
- Stores files only with user consent
- Organizes uploads by session ID
- Supports file cleanup and session management
- Uses `backend/uploads/` directory structure

## Development Notes

- Frontend uses standard React + TypeScript + Vite setup
- Backend implements proper CORS for local development
- Image processing requires base64 encoding for OpenAI API
- Session-based architecture allows for stateful interactions
- Template system supports different analysis modes (analyze, describe, technical)