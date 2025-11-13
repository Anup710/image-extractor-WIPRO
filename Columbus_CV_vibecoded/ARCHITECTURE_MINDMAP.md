# Columbus CV Analyzer - Architecture Mind Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COLUMBUS CV ANALYZER APPLICATION                        │
│                    GPT-Powered Image Analysis Platform                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┴─────────────────────┐
                │                                           │
        ┌───────▼───────┐                          ┌────────▼────────┐
        │   FRONTEND    │                          │    BACKEND      │
        │  React + TS   │◄─────────────────────────┤    FastAPI      │
        │  Port: 3000   │       REST API           │   Port: 8000    │
        └───────────────┘                          └─────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              FRONTEND ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                            ROOT COMPONENT (App.tsx)                          │
│                          State Management Hub                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────▼────────┐           ┌────────▼────────┐          ┌────────▼────────┐
│  IMAGE UPLOAD  │           │ CHAT INTERFACE  │          │    TEMPLATE     │
│   Component    │           │    Component    │          │    SELECTOR     │
└────────────────┘           └─────────────────┘          └─────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          STATE MANAGEMENT (App.tsx)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │  selectedFiles      │  │  selectedTemplate    │  │  messages        │  │
│  │  Type: File[]       │  │  Type: string        │  │  Type: Chat[]    │  │
│  └─────────────────────┘  └──────────────────────┘  └──────────────────┘  │
│                                                                              │
│  ┌─────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │  sessionId          │  │  isChatLoading       │  │  storeFiles      │  │
│  │  Type: string       │  │  Type: boolean       │  │  Type: boolean   │  │
│  └─────────────────────┘  └──────────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT: ImageUpload.tsx                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Features:                                  Props:                           │
│  ├─ Drag & Drop Support                     ├─ onFilesSelected()            │
│  ├─ Multiple File Selection                 ├─ selectedFiles                │
│  ├─ Image Preview (thumbnails)              ├─ onRemoveFile()               │
│  ├─ File Size Display                       └─ isUploading                  │
│  ├─ Remove Individual Files                                                 │
│  └─ Type Filtering (image/*)                                                │
│                                                                              │
│  Utilities:                                                                  │
│  └─ formatFileSize() → Bytes to KB/MB/GB                                    │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                       COMPONENT: ChatInterface.tsx                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Features:                                  Props:                           │
│  ├─ Message History Display                 ├─ onSendMessage()              │
│  ├─ User/Assistant Bubbles                  ├─ messages[]                   │
│  ├─ Typing Indicator Animation              ├─ isLoading                    │
│  ├─ Image Attachments Display               └─ disabled                     │
│  ├─ Timestamp Formatting                                                    │
│  ├─ Character Counter (max 2000)                                            │
│  ├─ Keyboard Support (Enter/Shift+Enter)                                    │
│  └─ Empty State Placeholder                                                 │
│                                                                              │
│  Message Type:                                                               │
│  └─ { id, type, content, timestamp, images? }                               │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                      COMPONENT: TemplateSelector.tsx                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Templates Available:                       Props:                           │
│  ├─ Default Analysis                        ├─ selectedTemplate             │
│  ├─ Detailed Analysis                       └─ onTemplateChange()           │
│  ├─ Description Mode                                                         │
│  └─ Technical Analysis                                                       │
│                                                                              │
│  UI Pattern: Radio Button Group                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         API SERVICE LAYER (api.ts)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Base URL: http://localhost:8000/api                                        │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  healthCheck()                                                        │  │
│  │  GET /api/health                                                      │  │
│  │  Returns: { status, timestamp }                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  uploadFiles(files, storeFiles)                                      │  │
│  │  POST /api/upload                                                     │  │
│  │  Returns: UploadResponse { session_id, files[], stored }            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  chat(request: ChatRequest)                                          │  │
│  │  POST /api/chat                                                       │  │
│  │  Body: { prompt, images?, template?, session_id? }                  │  │
│  │  Returns: ChatResponse { response, session_id?, timestamp }         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  fileToImageData(file: File)                                         │  │
│  │  Utility: Converts File → base64 ImageData                          │  │
│  │  Uses FileReader API                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                             STYLING ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CSS Files:                        Color System (CSS Variables):            │
│  ├─ App.css (843 lines)            ├─ --wipro-primary-blue                  │
│  └─ index.css (69 lines)           ├─ --wipro-secondary-blue                │
│                                     ├─ --wipro-accent-green                  │
│  Layout System:                     ├─ --wipro-accent-purple                 │
│  └─ CSS Grid (3 panels)            └─ --wipro-text/bg/border colors         │
│     1fr | 1.2fr | 1fr                                                        │
│                                                                              │
│  Responsive Breakpoints:            Animations:                              │
│  ├─ Desktop: 1200px+                ├─ @keyframes spin (loading)            │
│  ├─ Tablet: 768px-1200px            └─ @keyframes typing (dots)             │
│  └─ Mobile: <768px                                                           │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              BACKEND ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION (main.py)                        │
│                             Entry Point & Routing                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
        ┌───────▼────────┐   ┌────────▼────────┐   ┌──────▼──────┐
        │  GPT SERVICE   │   │ STORAGE SERVICE │   │   MODELS    │
        │  OpenAI API    │   │  File Manager   │   │  Pydantic   │
        └────────────────┘   └─────────────────┘   └─────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          API ENDPOINTS (main.py)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  GET /api/health                                                      │  │
│  │  ├─ Handler: health_check()                                          │  │
│  │  └─ Returns: { status: "healthy", timestamp }                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  POST /api/upload                                                     │  │
│  │  ├─ Handler: upload_files()                                          │  │
│  │  ├─ Params: files (multipart), store_files (bool)                   │  │
│  │  ├─ Validation: Image files only                                     │  │
│  │  ├─ Process:                                                         │  │
│  │  │   1. Generate session_id (UUID)                                  │  │
│  │  │   2. Read file contents                                          │  │
│  │  │   3. Optionally store via StorageService                         │  │
│  │  └─ Returns: UploadResponse                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  POST /api/chat                                                       │  │
│  │  ├─ Handler: chat_with_gpt()                                         │  │
│  │  ├─ Request: ChatRequest (prompt, images?, template?, session_id?)  │  │
│  │  ├─ Process:                                                         │  │
│  │  │   1. Extract request data                                        │  │
│  │  │   2. Call gpt_service.process_chat()                            │  │
│  │  │   3. Add metadata (session_id, timestamp)                       │  │
│  │  └─ Returns: ChatResponse                                           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                       SERVICE: GPTService (gpt_service.py)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Configuration:                                                              │
│  ├─ Model: gpt-4o (from env or default)                                     │
│  ├─ API Key: From OPENAI_API_KEY env                                        │
│  ├─ Max Tokens: 4000                                                         │
│  └─ Temperature: 0.7                                                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  process_chat(prompt, images?, template?) → string                   │  │
│  │  ├─ Apply template via _apply_template()                            │  │
│  │  ├─ Build message content via _build_message_content()              │  │
│  │  ├─ Call OpenAI Chat Completion API                                 │  │
│  │  └─ Return AI response text                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  _apply_template(prompt, template?) → string                        │  │
│  │  ├─ Templates: analyze, describe, technical, default                │  │
│  │  └─ Wraps prompt with template text                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  _build_message_content(prompt, images?) → content[]                │  │
│  │  ├─ Creates array with text + image_url objects                     │  │
│  │  └─ Images as data URLs (base64)                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                   SERVICE: StorageService (storage_service.py)               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Upload Directory: backend/uploads/                                          │
│  Organization: {session_id}/{timestamp}_{filename}                           │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  store_file(file, session_id) → string                               │  │
│  │  ├─ Create session directory                                        │  │
│  │  ├─ Generate timestamped filename                                   │  │
│  │  ├─ Save file to disk                                               │  │
│  │  └─ Return file path                                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  get_stored_files(session_id) → list                                │  │
│  │  └─ Returns file metadata for session                               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  delete_session_files(session_id) → bool                            │  │
│  │  └─ Removes all files for session                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  cleanup_old_files(days_old) → void                                 │  │
│  │  └─ Placeholder for future cleanup                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                       DATA MODELS (models.py - Pydantic)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  UploadedFile                       ChatRequest                              │
│  ├─ filename: str                   ├─ prompt: str                           │
│  ├─ content_type: str               ├─ images: List[ImageData]?             │
│  ├─ size: int                       ├─ template: str?                        │
│  ├─ stored: bool                    └─ session_id: str?                      │
│  ├─ path: str?                                                               │
│  └─ content: bytes?                 ChatResponse                             │
│                                     ├─ response: str                         │
│  UploadResponse                     ├─ session_id: str?                      │
│  ├─ session_id: str                 └─ timestamp: str                        │
│  ├─ files: List[UploadedFile]                                               │
│  └─ stored: bool                    ErrorResponse                            │
│                                     ├─ error: str                            │
│  ImageData                          ├─ detail: str?                          │
│  ├─ filename: str                   └─ timestamp: str                        │
│  ├─ content: str (base64)                                                    │
│  └─ content_type: str               PromptTemplate                           │
│                                     ├─ name: str                             │
│                                     ├─ template: str                         │
│                                     └─ description: str                      │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                      CONFIGURATION & ENVIRONMENT                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Environment Variables (.env):                                               │
│  ├─ OPENAI_API_KEY (required)                                               │
│  ├─ OPENAI_MODEL (default: gpt-4o)                                          │
│  ├─ HOST (default: 0.0.0.0)                                                 │
│  ├─ PORT (default: 8000)                                                    │
│  └─ FRONTEND_URL (default: localhost:3000)                                  │
│                                                                              │
│  Dependencies (requirements.txt):                                            │
│  ├─ fastapi >= 0.104.1                                                      │
│  ├─ uvicorn[standard] >= 0.24.0                                             │
│  ├─ openai >= 1.3.8                                                         │
│  ├─ pydantic >= 2.5.0                                                       │
│  ├─ python-multipart >= 0.0.6                                               │
│  └─ python-dotenv >= 1.0.0                                                  │
│                                                                              │
│  CORS Configuration:                                                         │
│  ├─ Allowed Origins:                                                         │
│  │   ├─ http://localhost:3000                                               │
│  │   ├─ http://127.0.0.1:3000                                               │
│  │   ├─ http://localhost:5173                                               │
│  │   └─ http://127.0.0.1:5173                                               │
│  ├─ Allow Credentials: True                                                 │
│  ├─ Allow Methods: All                                                      │
│  └─ Allow Headers: All                                                      │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                            DATA FLOW ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE USER FLOW DIAGRAM                           │
└─────────────────────────────────────────────────────────────────────────────┘

    USER INTERACTION
          │
    ┌─────▼─────┐
    │   1. User │
    │   Uploads │
    │   Images  │
    └─────┬─────┘
          │
    ┌─────▼──────────┐
    │ 2. ImageUpload │
    │   Component    │
    │   Stores Files │
    │   in State     │
    └─────┬──────────┘
          │
    ┌─────▼──────────┐
    │ 3. User Selects│
    │    Template    │
    │   (Optional)   │
    └─────┬──────────┘
          │
    ┌─────▼──────────┐
    │ 4. User Types  │
    │   Message in   │
    │ ChatInterface  │
    └─────┬──────────┘
          │
    ┌─────▼──────────┐
    │ 5. User Clicks │
    │   Send Button  │
    └─────┬──────────┘
          │
    ┌─────▼──────────────────┐
    │ 6. handleSendMessage() │
    │    ├─ Get prompt       │
    │    ├─ Convert files    │
    │    │   to base64       │
    │    └─ Get template     │
    └─────┬──────────────────┘
          │
    ┌─────▼─────────────┐
    │ 7. apiService     │
    │    .chat()        │
    │    POST /api/chat │
    └─────┬─────────────┘
          │
          │ HTTP Request
          │ { prompt, images, template, session_id }
          │
    ┌─────▼─────────────┐
    │ 8. FastAPI        │
    │    chat_with_gpt()│
    │    Endpoint       │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 9. GPTService     │
    │    .process_chat()│
    │    ├─ Apply       │
    │    │   template   │
    │    ├─ Build       │
    │    │   message    │
    │    └─ Call OpenAI │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 10. OpenAI API    │
    │     GPT-4o Model  │
    │     Processes     │
    │     with Vision   │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 11. AI Response   │
    │     Returned      │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 12. ChatResponse  │
    │     with metadata │
    │     (session_id,  │
    │      timestamp)   │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 13. Frontend      │
    │     Updates State │
    │     ├─ Add message│
    │     ├─ Update     │
    │     │   sessionId │
    │     └─ Re-render  │
    └─────┬─────────────┘
          │
    ┌─────▼─────────────┐
    │ 14. User Sees     │
    │     AI Response   │
    │     in Chat       │
    └───────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                          KEY ARCHITECTURAL PATTERNS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                          DESIGN PATTERNS EMPLOYED                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FRONTEND:                              BACKEND:                             │
│  ├─ Component Composition               ├─ Service-Oriented Architecture    │
│  ├─ Props Drilling (unidirectional)     ├─ Dependency Injection (services)  │
│  ├─ Controlled Components               ├─ Request/Response Pattern         │
│  ├─ Custom Event Handlers               ├─ Data Validation (Pydantic)       │
│  ├─ Callback Props Pattern              ├─ Error Handling Middleware        │
│  └─ Functional Components + Hooks       └─ Async/Await Pattern              │
│                                                                              │
│  COMMUNICATION:                                                              │
│  ├─ RESTful API                                                              │
│  ├─ JSON Serialization                                                       │
│  ├─ Base64 Encoding for Images                                              │
│  └─ Session-based State Management                                          │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                            TECHNOLOGY STACK                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FRONTEND:                              BACKEND:                             │
│  ├─ React 19.1.1                        ├─ Python 3.x                        │
│  ├─ TypeScript 5.8.3                    ├─ FastAPI 0.104.1                  │
│  ├─ Vite 7.1.2                          ├─ Uvicorn 0.24.0                   │
│  ├─ ESLint + TypeScript ESLint          ├─ Pydantic 2.5.0                   │
│  └─ Custom CSS (no framework)           ├─ OpenAI SDK 1.3.8                 │
│                                         └─ Python-dotenv 1.0.0               │
│                                                                              │
│  EXTERNAL SERVICES:                                                          │
│  └─ OpenAI GPT-4o (Vision Model)                                            │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECURITY CONSIDERATIONS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Implemented:                           Not Implemented:                     │
│  ├─ CORS Configuration                  ├─ Authentication                    │
│  ├─ File Type Validation                ├─ Authorization                     │
│  ├─ Environment Variables               ├─ Rate Limiting                     │
│  ├─ Session-based Isolation             ├─ Request Logging                   │
│  └─ Error Message Sanitization         ├─ File Size Limits                  │
│                                         ├─ API Key Rotation                  │
│                                         └─ HTTPS Enforcement                 │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                            FEATURE CAPABILITIES
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                            CORE FEATURES                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  IMAGE ANALYSIS:                        CHAT FUNCTIONALITY:                  │
│  ├─ Multiple Image Upload               ├─ Conversational Interface         │
│  ├─ Drag & Drop Support                 ├─ Message History                  │
│  ├─ Image Preview                       ├─ Typing Indicators                │
│  ├─ Vision-enabled AI (GPT-4o)          ├─ Timestamps                       │
│  └─ Base64 Processing                   └─ Session Persistence              │
│                                                                              │
│  TEMPLATE SYSTEM:                       FILE MANAGEMENT:                     │
│  ├─ Default Analysis                    ├─ Optional Storage                  │
│  ├─ Detailed Analysis                   ├─ Session Organization             │
│  ├─ Description Mode                    ├─ Timestamp Naming                 │
│  └─ Technical Analysis                  └─ Metadata Tracking                │
│                                                                              │
│  USER EXPERIENCE:                                                            │
│  ├─ Responsive Design (mobile/tablet/desktop)                               │
│  ├─ Loading States & Indicators                                             │
│  ├─ Error Handling with User Feedback                                       │
│  ├─ Clear/Reset Functionality                                               │
│  └─ Character Limits & Validation                                           │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                          DEVELOPMENT INFORMATION
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                          SETUP & COMMANDS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FRONTEND SETUP:                        BACKEND SETUP:                       │
│  $ cd frontend                          $ cd backend                         │
│  $ npm install                          $ pip install -r requirements.txt    │
│  $ npm run dev         (port 3000)      $ cp .env.template .env              │
│  $ npm run build                        $ python main.py    (port 8000)      │
│  $ npm run lint                                                              │
│  $ npm run preview                                                           │
│                                                                              │
│  PROJECT STRUCTURE:                                                          │
│  Columbus_CV_vibecoded/                                                      │
│  ├── frontend/                  (React + TypeScript app)                    │
│  │   ├── src/                                                                │
│  │   │   ├── components/        (UI components)                             │
│  │   │   ├── services/          (API layer)                                 │
│  │   │   ├── App.tsx            (Root component)                            │
│  │   │   └── main.tsx           (Entry point)                               │
│  │   └── package.json                                                        │
│  │                                                                            │
│  ├── backend/                   (FastAPI server)                            │
│  │   ├── services/               (Business logic)                           │
│  │   │   ├── gpt_service.py                                                 │
│  │   │   └── storage_service.py                                             │
│  │   ├── uploads/               (File storage)                              │
│  │   ├── main.py                (FastAPI app)                               │
│  │   ├── models.py              (Data models)                               │
│  │   ├── requirements.txt                                                    │
│  │   └── .env                   (Configuration)                             │
│  │                                                                            │
│  └── CLAUDE.md                  (Project documentation)                     │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                          EXTENSION OPPORTUNITIES
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                        POTENTIAL ENHANCEMENTS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FEATURES:                              INFRASTRUCTURE:                      │
│  ├─ Multi-user Authentication           ├─ Database Integration (sessions)  │
│  ├─ Conversation Export (PDF/JSON)      ├─ Redis Caching                    │
│  ├─ Custom Template Creation            ├─ Message Queue (async tasks)      │
│  ├─ Image Annotation Tools              ├─ Docker Containerization          │
│  ├─ Batch Image Processing              ├─ Kubernetes Deployment            │
│  └─ Advanced Filtering Options          └─ Load Balancing                   │
│                                                                              │
│  IMPROVEMENTS:                          MONITORING:                          │
│  ├─ Implement cleanup_old_files()       ├─ Application Logging              │
│  ├─ File Size Validation                ├─ Error Tracking (Sentry)          │
│  ├─ Request Cancellation                ├─ Analytics Integration            │
│  ├─ Progressive Image Upload            ├─ Performance Metrics              │
│  ├─ LocalStorage Persistence            └─ Health Check Dashboard           │
│  └─ Internationalization (i18n)                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              FILE REFERENCE MAP
═══════════════════════════════════════════════════════════════════════════════

FRONTEND FILES (frontend/):
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx       (141 lines) - Chat UI with message display
│   │   ├── ImageUpload.tsx         (134 lines) - File upload with drag-drop
│   │   └── TemplateSelector.tsx     (69 lines) - Analysis mode selector
│   ├── services/
│   │   └── api.ts                  (103 lines) - API service layer
│   ├── App.tsx                     (195 lines) - Main application component
│   ├── App.css                     (843 lines) - Application styles
│   ├── main.tsx                             - React entry point
│   └── index.css                    (69 lines) - Global base styles
├── index.html                               - HTML entry point
├── vite.config.ts                           - Vite build configuration
├── tsconfig.json                            - TypeScript configuration
└── package.json                             - Dependencies & scripts

BACKEND FILES (backend/):
├── services/
│   ├── gpt_service.py               (74 lines) - OpenAI API integration
│   └── storage_service.py           (75 lines) - File storage management
├── main.py                          (98 lines) - FastAPI application & routes
├── models.py                        (42 lines) - Pydantic data models
├── requirements.txt                         - Python dependencies
├── .env                                     - Environment configuration
└── .env.template                            - Environment template

TOTAL SOURCE CODE: ~1,843 lines

═══════════════════════════════════════════════════════════════════════════════
```

---

## Summary

**Columbus CV Analyzer** is a full-stack GPT-powered image analysis platform that enables users to upload images, select analysis templates, and interact with OpenAI's GPT-4o model through a conversational interface. The application features:

- **Frontend**: React 19 + TypeScript with custom CSS, built with Vite
- **Backend**: FastAPI with service-oriented architecture
- **AI Integration**: OpenAI GPT-4o with vision capabilities
- **Architecture**: RESTful API with session-based state management
- **Key Features**: Drag-drop upload, multiple analysis modes, real-time chat, file storage

The codebase is well-organized with clear separation of concerns, type safety, and modern development practices.
