import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// RAG API
export const ragAPI = {
  query: async (question: string) => {
    const response = await api.post('/rag/query', { question });
    return response.data;
  },
  clear: async () => {
    const response = await api.post('/rag/clear');
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/rag/stats');
    return response.data;
  },
};

// Flashcards API
export const flashcardsAPI = {
  list: async (params?: { subject?: string; tag?: string; limit?: number; offset?: number }) => {
    const response = await api.get('/flashcards', { params });
    return response.data;
  },
  get: async (flashcard_id: string) => {
    const response = await api.get(`/flashcards/${flashcard_id}`);
    return response.data;
  },
  create: async (flashcard: {
    subject: string;
    question: string;
    answer: string;
    difficulty?: number;
    tags?: string[];
  }) => {
    const response = await api.post('/flashcards', flashcard);
    return response.data;
  },
  update: async (flashcard_id: string, data: {
    question?: string;
    answer?: string;
    difficulty?: number;
    tags?: string[];
  }) => {
    const response = await api.put(`/flashcards/${flashcard_id}`, data);
    return response.data;
  },
  delete: async (flashcard_id: string) => {
    const response = await api.delete(`/flashcards/${flashcard_id}`);
    return response.data;
  },
  getNext: async (subject?: string) => {
    const response = await api.get('/flashcards/next/due', { params: { subject } });
    return response.data; // Can be null if no cards due
  },
  recordAnswer: async (flashcard_id: string, correct: boolean, time_spent_seconds?: number) => {
    const response = await api.post('/flashcards/answer', {
      flashcard_id,
      correct,
      time_spent_seconds,
    });
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/flashcards/stats/overview');
    return response.data;
  },
  clearAll: async () => {
    const response = await api.delete('/flashcards/clear-all');
    return response.data;
  },
};

// Documents API
export const documentsAPI = {
  upload: async (file: File, subject?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (subject) formData.append('subject', subject);

    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  list: async () => {
    const response = await api.get('/documents');
    return response.data;
  },
  get: async (document_id: string) => {
    const response = await api.get(`/documents/${document_id}`);
    return response.data;
  },
  delete: async (document_id: string, deleteFromGraph: boolean = true, deleteFlashcards: boolean = true) => {
    const response = await api.delete(`/documents/${document_id}`, {
      params: { delete_from_graph: deleteFromGraph, delete_flashcards: deleteFlashcards },
    });
    return response.data;
  },
};

// Graph API
export const graphAPI = {
  getConcepts: async (subject?: string) => {
    const response = await api.get('/graph/concepts', { params: { subject } });
    return response.data;
  },
  getRelated: async (concept: string, depth: number = 2) => {
    const response = await api.get(`/graph/related/${concept}`, { params: { depth } });
    return response.data;
  },
  findPath: async (start: string, end: string, maxLength: number = 10) => {
    const response = await api.post('/graph/path', null, {
      params: { start, end, max_length: maxLength },
    });
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/graph/stats');
    return response.data;
  },
  clear: async () => {
    const response = await api.delete('/graph/clear');
    return response.data;
  },
};

export default api;
