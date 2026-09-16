import React, { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';

const MessageList = ({ messages, loading }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="message-list-container">
      {messages.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">🏎️</div>
          <h3>BMW Service Knowledge Assistant Ready</h3>
          <p>
            Ask questions regarding EV battery thermal management, cooling loop diagnostics,
            high-voltage safety procedures, torque specifications, or ISTA fault codes.
          </p>
        </div>
      ) : (
        messages.map((msg, idx) => <MessageItem key={idx} message={msg} />)
      )}

      {loading && (
        <div className="message-row assistant-row loading-row">
          <div className="avatar-col">
            <div className="avatar assistant-avatar pulsating">⚡</div>
          </div>
          <div className="message-content-col">
            <div className="message-bubble assistant-bubble loading-bubble">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="loading-text">
                Retrieving relevant BMW service documents & generating grounded response...
              </span>
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};

export default MessageList;
