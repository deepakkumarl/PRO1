import React, { useState } from 'react';

const QuestionInput = ({ onSubmit, onClear, loading }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;
    onSubmit(question.trim());
    setQuestion('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="question-input-form" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <textarea
          className="question-textarea"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter BMW service procedure or diagnostic question... (Press Enter to submit)"
          rows={2}
          disabled={loading}
        />
        <div className="input-actions">
          {onClear && (
            <button
              type="button"
              className="btn-clear-chat"
              onClick={onClear}
              disabled={loading}
              title="Clear chat thread"
            >
              🗑️ Clear
            </button>
          )}
          <button
            type="submit"
            className="btn-submit-query"
            disabled={!question.trim() || loading}
          >
            {loading ? 'Searching...' : 'Ask Assistant ↵'}
          </button>
        </div>
      </div>
    </form>
  );
};

export default QuestionInput;
