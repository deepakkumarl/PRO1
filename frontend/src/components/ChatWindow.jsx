import React from 'react';
import MessageList from './MessageList';
import QuestionInput from './QuestionInput';
import ExampleQuestions from './ExampleQuestions';

const ChatWindow = ({ messages, loading, onSubmit, onClear }) => {
  return (
    <div className="chat-window-panel">
      <MessageList messages={messages} loading={loading} />

      {messages.length === 0 && (
        <ExampleQuestions onSelectQuestion={(q) => onSubmit(q)} />
      )}

      <QuestionInput onSubmit={onSubmit} onClear={onClear} loading={loading} />
    </div>
  );
};

export default ChatWindow;
