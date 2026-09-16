import React, { useState } from 'react';

const SourceCard = ({ source, index }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="source-card">
      <div className="source-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="source-title-group">
          <span className="source-icon">📄</span>
          <div>
            <span className="source-doc-name">{source.document}</span>
            <span className="source-page-badge">Page {source.page}</span>
          </div>
        </div>
        <div className="source-meta">
          <span className="source-score" title="Relevance Score">
            {(source.score * 100).toFixed(0)}% match
          </span>
          <button className="btn-expand">
            {expanded ? '▲ Hide' : '▼ View Excerpt'}
          </button>
        </div>
      </div>

      {expanded && (
        <div className="source-card-body">
          <div className="source-content-header">Extracted Context Chunk:</div>
          <pre className="source-snippet">{source.content}</pre>
        </div>
      )}
    </div>
  );
};

export default SourceCard;
