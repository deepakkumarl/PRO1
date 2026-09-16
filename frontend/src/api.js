import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60s timeout for local LLM responses
});

export const fetchHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('API Health check failed:', error);
    return {
      status: 'offline',
      ollama_connected: false,
      index_ready: false,
      document_count: 0,
      ollama_model: 'llama3.2',
    };
  }
};

export const fetchDocuments = async () => {
  try {
    const response = await api.get('/documents');
    return response.data;
  } catch (error) {
    console.error('Fetch documents failed:', error);
    return { documents: [], total_documents: 0, total_chunks: 0, index_ready: false };
  }
};

export const triggerIngest = async () => {
  try {
    const response = await api.post('/ingest');
    return response.data;
  } catch (error) {
    console.error('Document ingestion failed:', error);
    throw error;
  }
};

export const sendQuery = async (question, chatHistory = []) => {
  try {
    const formattedHistory = chatHistory.map((msg) => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text,
    }));

    const response = await api.post('/query', {
      question: question.trim(),
      chat_history: formattedHistory,
    });
    return response.data;
  } catch (error) {
    console.error('RAG Query failed:', error);
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to connect to BMW Service Assistant backend.');
  }
};
