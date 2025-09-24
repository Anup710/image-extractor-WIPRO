const API_BASE_URL = 'http://localhost:8000/api';

export interface UploadedFile {
  filename: string;
  content_type: string;
  size: number;
  stored: boolean;
  path?: string;
  content?: ArrayBuffer;
}

export interface UploadResponse {
  session_id: string;
  files: UploadedFile[];
  stored: boolean;
}

export interface ImageData {
  filename: string;
  content: string; // base64 encoded
  content_type: string;
}

export interface ChatRequest {
  prompt: string;
  images?: ImageData[];
  template?: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  session_id?: string;
  timestamp: string;
}

class ApiService {
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  }

  async uploadFiles(files: FileList, storeFiles: boolean = false): Promise<UploadResponse> {
    const formData = new FormData();

    Array.from(files).forEach(file => {
      formData.append('files', file);
    });
    formData.append('store_files', storeFiles.toString());

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return await response.json();
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Chat request failed');
    }

    return await response.json();
  }

  // Helper function to convert File to base64 ImageData
  async fileToImageData(file: File): Promise<ImageData> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        const base64 = result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
        resolve({
          filename: file.name,
          content: base64,
          content_type: file.type,
        });
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
}

export const apiService = new ApiService();