import { useState, useCallback } from 'react'
import ImageUpload from './components/ImageUpload'
import TemplateSelector from './components/TemplateSelector'
import ChatInterface, { type ChatMessage } from './components/ChatInterface'
import { apiService, type ImageData } from './services/api'
import './App.css'

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState('default');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [storeFiles, setStoreFiles] = useState(false);

  const handleFilesSelected = useCallback((newFiles: File[]) => {
    setSelectedFiles(prev => [...prev, ...newFiles]);
  }, []);

  const handleRemoveFile = useCallback((index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  }, []);

  const handleTemplateChange = useCallback((template: string) => {
    setSelectedTemplate(template);
  }, []);

  const convertFilesToImageData = async (files: File[]): Promise<ImageData[]> => {
    const imageDataPromises = files.map(file => apiService.fileToImageData(file));
    return Promise.all(imageDataPromises);
  };

  const handleSendMessage = useCallback(async (message: string) => {
    if (selectedFiles.length === 0) {
      alert('Please upload at least one image first.');
      return;
    }

    try {
      setIsChatLoading(true);

      // Add user message to chat
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'user',
        content: message,
        timestamp: new Date().toISOString(),
        images: selectedFiles.map(file => URL.createObjectURL(file))
      };
      setMessages(prev => [...prev, userMessage]);

      // Convert files to ImageData for API
      const imageData = await convertFilesToImageData(selectedFiles);

      // Send chat request
      const response = await apiService.chat({
        prompt: message,
        images: imageData,
        template: selectedTemplate === 'default' ? undefined : selectedTemplate,
        session_id: sessionId || undefined
      });

      // Update session ID if we got a new one
      if (response.session_id && response.session_id !== sessionId) {
        setSessionId(response.session_id);
      }

      // Add AI response to chat
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.response,
        timestamp: response.timestamp
      };
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Chat error:', error);

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsChatLoading(false);
    }
  }, [selectedFiles, selectedTemplate, sessionId]);

  const handleClearChat = () => {
    setMessages([]);
    setSessionId('');
  };

  const handleClearFiles = () => {
    setSelectedFiles([]);
    setMessages([]);
    setSessionId('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📄 Columbus CV Analyzer</h1>
          <p>Professional CV Analysis powered by Advanced AI Technology</p>
        </div>
      </header>

      <main className="app-main">
        <div className="content-grid">
          <div className="left-panel">
            <section className="upload-section">
              <h2>📁 Document Upload</h2>
              <ImageUpload
                onFilesSelected={handleFilesSelected}
                selectedFiles={selectedFiles}
                onRemoveFile={handleRemoveFile}
                isUploading={false}
              />

              <div className="file-controls">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={storeFiles}
                    onChange={(e) => setStoreFiles(e.target.checked)}
                  />
                  Store files on server (optional)
                </label>

                {selectedFiles.length > 0 && (
                  <button
                    className="clear-files-btn"
                    onClick={handleClearFiles}
                    type="button"
                  >
                    Clear All Files
                  </button>
                )}
              </div>
            </section>
          </div>

          <div className="center-panel">
            <section className="chat-section">
              <h2>🤖 AI Analysis Assistant</h2>
              <ChatInterface
                onSendMessage={handleSendMessage}
                messages={messages}
                isLoading={isChatLoading}
                disabled={selectedFiles.length === 0}
              />
            </section>
          </div>

          <div className="right-panel">
            <section className="template-section">
              <TemplateSelector
                selectedTemplate={selectedTemplate}
                onTemplateChange={handleTemplateChange}
              />
            </section>

            {messages.length > 0 && (
              <section className="chat-controls">
                <button
                  className="clear-chat-btn"
                  onClick={handleClearChat}
                  type="button"
                >
                  Clear Chat History
                </button>
              </section>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>
          Powered by OpenAI GPT-4o •
          {selectedFiles.length > 0 && ` ${selectedFiles.length} document(s) uploaded • `}
          {sessionId && ` Session: ${sessionId.slice(0, 8)}... • `}
          Columbus CV Analyzer Professional Edition
        </p>
      </footer>
    </div>
  );
}

export default App
