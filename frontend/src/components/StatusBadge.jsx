import React, { useState } from 'react';
import { triggerIngest } from '../api';

const StatusBadge = ({ health, onRefresh }) => {
  const [ingesting, setIngesting] = useState(false);
  const [message, setMessage] = useState('');

  const handleIngest = async () => {
    setIngesting(true);
    setMessage('Ingesting documents into FAISS...');
    try {
      const res = await triggerIngest();
      setMessage(`Ingested ${res.documents_processed} PDFs (${res.chunks_created} chunks)`);
      if (onRefresh) onRefresh();
    } catch (err) {
      setMessage('Ingestion failed: ' + err.message);
    } finally {
      setIngesting(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const isOnline = health.status === 'healthy';
  const indexReady = health.index_ready;
  const ollamaReady = health.ollama_connected;

  return (
    <div className="status-bar">
      <div className="status-items">
        <div className={`status-tag ${isOnline ? 'online' : 'offline'}`}>
          <span className="status-indicator-dot"></span>
          Backend: {isOnline ? 'Connected' : 'Offline'}
        </div>

        <div className={`status-tag ${indexReady ? 'ready' : 'warning'}`}>
          <span className="status-icon">{indexReady ? '📚' : '⚠️'}</span>
          FAISS Index: {indexReady ? `${health.document_count} PDFs Loaded` : 'Not Ingested'}
        </div>

        <div className={`status-tag ${ollamaReady ? 'ready' : 'notice'}`}>
          <span className="status-icon">{ollamaReady ? '⚡' : '⚙️'}</span>
          LLM: {ollamaReady ? `Ollama (${health.ollama_model})` : 'Offline / Standby'}
        </div>
      </div>

      <div className="status-actions">
        {message && <span className="status-feedback">{message}</span>}
        <button
          className="btn-reingest"
          onClick={handleIngest}
          disabled={ingesting}
          title="Re-scan documents directory and rebuild FAISS index"
        >
          {ingesting ? 'Indexing...' : '🔄 Re-ingest Documents'}
        </button>
      </div>
    </div>
  );
};

export default StatusBadge;
