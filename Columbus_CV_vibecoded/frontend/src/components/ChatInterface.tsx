import React, { useState } from 'react';

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
  images?: string[]; // image URLs for display
}

interface ChatInterfaceProps {
  onSendMessage: (message: string) => void;
  messages: ChatMessage[];
  isLoading?: boolean;
  disabled?: boolean;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSendMessage,
  messages,
  isLoading = false,
  disabled = false
}) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">💬</div>
            <h3>Ready for CV Analysis</h3>
            <p>Upload images and ask questions about the CV content, or request specific analysis.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-header">
                <span className="message-sender">
                  {message.type === 'user' ? '👤 You' : '🤖 AI Assistant'}
                </span>
                <span className="message-time">
                  {formatTimestamp(message.timestamp)}
                </span>
              </div>

              {message.images && message.images.length > 0 && (
                <div className="message-images">
                  {message.images.map((imageUrl, index) => (
                    <img
                      key={index}
                      src={imageUrl}
                      alt={`Attached image ${index + 1}`}
                      className="message-image"
                    />
                  ))}
                </div>
              )}

              <div className="message-content">
                {message.content.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="message assistant loading">
            <div className="message-header">
              <span className="message-sender">🤖 AI Assistant</span>
              <span className="message-time">Thinking...</span>
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              disabled
                ? "Please upload images first..."
                : "Ask about the CV content, request analysis, or provide specific instructions..."
            }
            disabled={disabled || isLoading}
            rows={3}
            maxLength={2000}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading || disabled}
            className="send-button"
            title="Send message (Enter)"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
        <div className="input-footer">
          <small>
            Press Enter to send, Shift+Enter for new line
            {input.length > 0 && ` • ${input.length}/2000 characters`}
          </small>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
export type { ChatMessage };