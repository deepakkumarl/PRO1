import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatusBadge from './components/StatusBadge';
import ChatWindow from './components/ChatWindow';
import { fetchHealth, fetchDocuments, sendQuery } from './api';
import './App.css';

function App() {
  const [health, setHealth] = useState({
    status: 'checking',
    ollama_connected: false,
    index_ready: false,
    document_count: 0,
    ollama_model: 'llama3.2',
  });
  const [docList, setDocList] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const loadBackendStatus = async () => {
    const healthData = await fetchHealth();
    setHealth(healthData);

    const docData = await fetchDocuments();
    setDocList(docData.documents || []);
  };

  useEffect(() => {
    loadBackendStatus();
    const interval = setInterval(loadBackendStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleQuerySubmit = async (questionText) => {
    setErrorMsg(null);
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userMessage = {
      sender: 'user',
      text: questionText,
      timestamp: now,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await sendQuery(questionText, messages);
      const assistantMessage = {
        sender: 'assistant',
        text: response.answer,
        sources: response.sources || [],
        confidenceMet: response.confidence_met,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setErrorMsg(err.message || 'An error occurred while executing the query.');
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `⚠️ Error: ${err.message || 'Failed to retrieve grounded answer.'}`,
          sources: [],
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setErrorMsg(null);
  };

  return (
    <div className="bmw-app">
      <Header />
      <StatusBadge health={health} onRefresh={loadBackendStatus} />

      {errorMsg && (
        <div className="error-banner">
          <span className="error-icon">❌</span>
          <span>{errorMsg}</span>
          <button className="btn-close-error" onClick={() => setErrorMsg(null)}>
            ✕
          </button>
        </div>
      )}

      <main className="bmw-main-container">
        <div className="bmw-sidebar">
          <div className="sidebar-card">
            <h3 className="sidebar-title">📑 Loaded BMW Service Manuals</h3>
            {docList.length === 0 ? (
              <p className="sidebar-empty">No PDFs loaded in data/documents/</p>
            ) : (
              <ul className="doc-list">
                {docList.map((doc, idx) => (
                  <li key={idx} className="doc-item">
                    <span className="doc-icon">📘</span>
                    <div className="doc-details">
                      <div className="doc-name">{doc.filename}</div>
                      <div className="doc-sub">{doc.pages} Pages</div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="sidebar-card info-card">
            <h4 className="info-title">ℹ️ Technical Grounding Policy</h4>
            <p className="info-text">
              This system strictly relies on retrieved BMW technical service manuals.
              It will not generate or fabricate torque specs, diagnostic steps, or safety warnings.
            </p>
          </div>
        </div>

        <div className="bmw-chat-area">
          <ChatWindow
            messages={messages}
            loading={loading}
            onSubmit={handleQuerySubmit}
            onClear={handleClearChat}
          />
        </div>
      </main>

      <footer className="bmw-footer">
        BMW Service Knowledge Assistant • Grounded RAG Platform for Certified Technicians
      </footer>
    </div>
  );
}

export default App;
