import React, { useState, useRef, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Send, Loader2, Upload, Trash2, MessageSquare, Mic, Volume2, VolumeX } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import toast from 'react-hot-toast';

import { ragAPI, documentsAPI } from '../../services/api';
import { useVoiceInput } from '../../hooks/useVoiceInput';
import { useTextToSpeech } from '../../hooks/useTextToSpeech';
import DocumentProgress from '../DocumentProgress';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

const RAGPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadingDocumentId, setUploadingDocumentId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();

  // Voice functionality
  const { isListening, transcript, startListening, stopListening, resetTranscript, isSupported: voiceSupported } = useVoiceInput();
  const { speak, stop, isSpeaking } = useTextToSpeech();

  const queryMutation = useMutation({
    mutationFn: (question: string) => ragAPI.query(question),
    onSuccess: (data) => {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
        },
      ]);
      // Auto-speak the response
      if (isSpeaking) stop(); // Stop any previous speech
      speak(data.answer);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || queryMutation.isPending) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    queryMutation.mutate(input);
    setInput('');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const response = await documentsAPI.upload(file);
      setUploadingDocumentId(response.document_id);
      toast.success(`${file.name} erfolgreich hochgeladen! Verarbeitung läuft im Hintergrund...`);
    } catch (error) {
      toast.error(`Fehler beim Hochladen: ${error}`);
    } finally {
      setIsUploading(false);
      // Reset file input
      e.target.value = '';
    }
  };

  const handleUploadComplete = () => {
    // Invalidate queries to refresh data
    queryClient.invalidateQueries({ queryKey: ['documents'] });
    queryClient.invalidateQueries({ queryKey: ['ragStats'] });
    queryClient.invalidateQueries({ queryKey: ['flashcards'] });
    queryClient.invalidateQueries({ queryKey: ['graph-stats'] });

    // Clear the uploading state after a delay
    setTimeout(() => {
      setUploadingDocumentId(null);
    }, 3000);
  };

  const handleUploadError = (error: string) => {
    toast.error(`Verarbeitungsfehler: ${error}`);
    setTimeout(() => {
      setUploadingDocumentId(null);
    }, 5000);
  };

  const handleClear = async () => {
    if (confirm('Konversation löschen?')) {
      await ragAPI.clear();
      setMessages([]);
    }
  };

  // Update input when voice transcript changes
  useEffect(() => {
    if (transcript) {
      setInput(transcript);
      resetTranscript();
    }
  }, [transcript, resetTranscript]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleVoiceToggle = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const toggleSpeech = (text: string) => {
    if (isSpeaking) {
      stop();
    } else {
      speak(text);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '4px' }}>
            RAG Chat
          </h1>
          <p style={{ color: '#666' }}>Befrage deine Dokumente</p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <label className="btn btn-secondary" style={{ cursor: 'pointer' }}>
            <Upload size={18} />
            {isUploading ? 'Lädt hoch...' : 'PDF hochladen'}
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              disabled={isUploading}
            />
          </label>

          <button className="btn btn-danger" onClick={handleClear}>
            <Trash2 size={18} />
            Löschen
          </button>
        </div>
      </div>

      <div className="card">
        <div className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                <MessageSquare size={48} style={{ margin: '0 auto 16px' }} />
                <p>Stelle eine Frage zu deinen Dokumenten</p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`chat-message ${msg.role}`}>
                  <div className="message-content">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div style={{ flex: 1 }}>
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                      {msg.role === 'assistant' && (
                        <button
                          onClick={() => toggleSpeech(msg.content)}
                          className="btn btn-secondary"
                          style={{
                            padding: '8px',
                            minWidth: 'auto',
                            marginLeft: '12px',
                            opacity: 0.7,
                          }}
                          title={isSpeaking ? "Vorlesen stoppen" : "Antwort vorlesen"}
                        >
                          {isSpeaking ? <VolumeX size={16} /> : <Volume2 size={16} />}
                        </button>
                      )}
                    </div>

                    {msg.sources && msg.sources.length > 0 && (
                      <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #eee' }}>
                        <div style={{ fontSize: '12px', fontWeight: '600', marginBottom: '8px', opacity: 0.7 }}>
                          QUELLEN:
                        </div>
                        {msg.sources.map((src, i) => (
                          <div key={i} style={{ fontSize: '12px', marginBottom: '4px', opacity: 0.8 }}>
                            📄 {src.file}, Seite {src.page}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {queryMutation.isPending && (
              <div className="chat-message assistant">
                <div className="message-content">
                  <Loader2 className="spinner" size={20} />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-container">
            <input
              type="text"
              className="input chat-input"
              placeholder={isListening ? "Sprechen Sie jetzt..." : "Frage eingeben..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={queryMutation.isPending}
            />
            {voiceSupported && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleVoiceToggle}
                disabled={queryMutation.isPending}
                style={{
                  backgroundColor: isListening ? '#ef4444' : '#6b7280',
                  animation: isListening ? 'pulse 1.5s infinite' : 'none',
                }}
                title={isListening ? "Aufnahme stoppen" : "Spracheingabe starten"}
              >
                <Mic size={18} />
              </button>
            )}
            <button
              type="submit"
              className="btn btn-primary"
              disabled={queryMutation.isPending || !input.trim()}
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>

      {/* Real-time Progress Tracking */}
      <DocumentProgress
        documentId={uploadingDocumentId}
        onComplete={handleUploadComplete}
        onError={handleUploadError}
      />
    </div>
  );
};

export default RAGPage;
