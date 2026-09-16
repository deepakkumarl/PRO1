import React, { useState } from 'react';
import SourceCard from './SourceCard';

const MessageItem = ({ message }) => {
  const isUser = message.sender === 'user';
  const [showSources, setShowSources] = useState(true);

  // Helper to format response text paragraphs and safety warnings
  const renderFormattedText = (text) => {
    if (!text) return null;
    
    // Split into paragraphs
    const paragraphs = text.split('\n\n');
    return paragraphs.map((para, idx) => {
      if (para.startsWith('[Note:') || para.includes('CRITICAL SAFETY WARNING')) {
        return (
          <div key={idx} className="warning-callout">
            <span className="warning-icon">⚠️</span>
            <div>{para}</div>
          </div>
        );
      }
      return <p key={idx}>{para}</p>;
    });
  };

  return (
    <div className={`message-row ${isUser ? 'user-row' : 'assistant-row'}`}>
      <div className="avatar-col">
        <div className={`avatar ${isUser ? 'user-avatar' : 'assistant-avatar'}`}>
          {isUser ? '🔧' : '⚡'}
        </div>
      </div>

      <div className="message-content-col">
        <div className="message-sender-name">
          {isUser ? 'Technician' : 'BMW RAG Assistant'}
          <span className="message-time">{message.timestamp}</span>
        </div>

        <div className={`message-bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
          {isUser ? (
            <div className="user-text">{message.text}</div>
          ) : (
            <div className="assistant-text">
              {renderFormattedText(message.text)}
            </div>
          )}

          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="sources-section">
              <div
                className="sources-toggle-header"
                onClick={() => setShowSources(!showSources)}
              >
                <span className="sources-title">
                  📚 Cited BMW Service Documentation ({message.sources.length}):
                </span>
                <span className="sources-arrow">{showSources ? '▼' : '▶'}</span>
              </div>

              {showSources && (
                <div className="sources-list">
                  {message.sources.map((src, sIdx) => (
                    <SourceCard key={sIdx} source={src} index={sIdx} />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageItem;
