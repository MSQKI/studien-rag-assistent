import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Trash2, Edit2, FileText, Brain, Database } from 'lucide-react';

import { documentsAPI, flashcardsAPI, graphAPI } from '../../services/api';

type TabType = 'documents' | 'flashcards' | 'graph';

const DataManagementPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('documents');
  const [editingFlashcard, setEditingFlashcard] = useState<any>(null);
  const queryClient = useQueryClient();

  // Documents Query
  const { data: documentsData, isLoading: documentsLoading } = useQuery({
    queryKey: ['documents'],
    queryFn: () => documentsAPI.list(),
  });

  // Flashcards Query
  const { data: flashcardsData, isLoading: flashcardsLoading } = useQuery({
    queryKey: ['flashcards'],
    queryFn: () => flashcardsAPI.list({ limit: 100 }),
  });

  // Graph Stats Query
  const { data: graphStats, isLoading: graphLoading } = useQuery({
    queryKey: ['graph-stats'],
    queryFn: () => graphAPI.getStats(),
  });

  // Delete Document Mutation
  const deleteDocumentMutation = useMutation({
    mutationFn: (document_id: string) => documentsAPI.delete(document_id, true, true),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      alert('Dokument erfolgreich gelöscht');
    },
    onError: (error) => {
      alert(`Fehler beim Löschen: ${error}`);
    },
  });

  // Delete Flashcard Mutation
  const deleteFlashcardMutation = useMutation({
    mutationFn: (flashcard_id: string) => flashcardsAPI.delete(flashcard_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flashcards'] });
      alert('Karteikarte erfolgreich gelöscht');
    },
    onError: (error) => {
      alert(`Fehler beim Löschen: ${error}`);
    },
  });

  // Update Flashcard Mutation
  const updateFlashcardMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) => flashcardsAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flashcards'] });
      setEditingFlashcard(null);
      alert('Karteikarte erfolgreich aktualisiert');
    },
    onError: (error) => {
      alert(`Fehler beim Aktualisieren: ${error}`);
    },
  });

  // Clear Graph Mutation
  const clearGraphMutation = useMutation({
    mutationFn: () => graphAPI.clear(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['graph-stats'] });
      alert('Knowledge Graph erfolgreich geleert');
    },
    onError: (error) => {
      alert(`Fehler beim Leeren: ${error}`);
    },
  });

  const handleDeleteDocument = (doc_id: string, filename: string) => {
    if (confirm(`Dokument "${filename}" wirklich löschen?`)) {
      deleteDocumentMutation.mutate(doc_id);
    }
  };

  const handleDeleteFlashcard = (card_id: string, question: string) => {
    if (confirm(`Karteikarte "${question}" wirklich löschen?`)) {
      deleteFlashcardMutation.mutate(card_id);
    }
  };

  const handleUpdateFlashcard = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingFlashcard) return;

    updateFlashcardMutation.mutate({
      id: editingFlashcard.id,
      data: {
        question: editingFlashcard.question,
        answer: editingFlashcard.answer,
        difficulty: editingFlashcard.difficulty,
        tags: editingFlashcard.tags,
      },
    });
  };

  const handleClearGraph = () => {
    if (confirm('ACHTUNG: Alle Graph-Daten werden gelöscht. Fortfahren?')) {
      clearGraphMutation.mutate();
    }
  };

  return (
    <div>
      <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '20px' }}>
        Datenverwaltung
      </h1>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button
          className={`btn ${activeTab === 'documents' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('documents')}
        >
          <FileText size={18} />
          Dokumente
        </button>
        <button
          className={`btn ${activeTab === 'flashcards' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('flashcards')}
        >
          <Brain size={18} />
          Karteikarten
        </button>
        <button
          className={`btn ${activeTab === 'graph' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('graph')}
        >
          <Database size={18} />
          Knowledge Graph
        </button>
      </div>

      {/* Documents Tab */}
      {activeTab === 'documents' && (
        <div className="card">
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>Dokumente</h2>
          {documentsLoading ? (
            <p>Lade...</p>
          ) : documentsData?.documents?.length === 0 ? (
            <p style={{ color: '#999' }}>Keine Dokumente vorhanden</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                    <th style={{ padding: '12px', textAlign: 'left' }}>Dateiname</th>
                    <th style={{ padding: '12px', textAlign: 'left' }}>Chunks</th>
                    <th style={{ padding: '12px', textAlign: 'left' }}>Größe</th>
                    <th style={{ padding: '12px', textAlign: 'left' }}>Status</th>
                    <th style={{ padding: '12px', textAlign: 'left' }}>Aktionen</th>
                  </tr>
                </thead>
                <tbody>
                  {documentsData?.documents?.map((doc: any) => (
                    <tr key={doc.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                      <td style={{ padding: '12px' }}>{doc.filename}</td>
                      <td style={{ padding: '12px' }}>{doc.chunk_count}</td>
                      <td style={{ padding: '12px' }}>
                        {(doc.file_size_bytes / 1024 / 1024).toFixed(2)} MB
                      </td>
                      <td style={{ padding: '12px' }}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          backgroundColor: doc.processed ? '#e8f5e9' : '#fff3e0',
                          color: doc.processed ? '#2e7d32' : '#e65100',
                          fontSize: '12px'
                        }}>
                          {doc.processed ? 'Verarbeitet' : 'Ausstehend'}
                        </span>
                      </td>
                      <td style={{ padding: '12px' }}>
                        <button
                          className="btn btn-danger"
                          onClick={() => handleDeleteDocument(doc.id, doc.filename)}
                          disabled={deleteDocumentMutation.isPending}
                          style={{ padding: '6px 12px', fontSize: '14px' }}
                        >
                          <Trash2 size={14} />
                          Löschen
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Flashcards Tab */}
      {activeTab === 'flashcards' && (
        <div className="card">
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>Karteikarten</h2>
          {flashcardsLoading ? (
            <p>Lade...</p>
          ) : flashcardsData?.length === 0 ? (
            <p style={{ color: '#999' }}>Keine Karteikarten vorhanden</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {flashcardsData?.map((card: any) => (
                <div
                  key={card.id}
                  style={{
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                    padding: '16px',
                    backgroundColor: editingFlashcard?.id === card.id ? '#f5f5f5' : 'white'
                  }}
                >
                  {editingFlashcard?.id === card.id ? (
                    <form onSubmit={handleUpdateFlashcard}>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                          Frage:
                        </label>
                        <input
                          type="text"
                          className="input"
                          value={editingFlashcard.question}
                          onChange={(e) => setEditingFlashcard({ ...editingFlashcard, question: e.target.value })}
                          style={{ width: '100%' }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                          Antwort:
                        </label>
                        <textarea
                          className="input"
                          value={editingFlashcard.answer}
                          onChange={(e) => setEditingFlashcard({ ...editingFlashcard, answer: e.target.value })}
                          rows={3}
                          style={{ width: '100%' }}
                        />
                      </div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button type="submit" className="btn btn-primary" disabled={updateFlashcardMutation.isPending}>
                          Speichern
                        </button>
                        <button
                          type="button"
                          className="btn btn-secondary"
                          onClick={() => setEditingFlashcard(null)}
                        >
                          Abbrechen
                        </button>
                      </div>
                    </form>
                  ) : (
                    <>
                      <div style={{ marginBottom: '8px' }}>
                        <strong>Frage:</strong> {card.question}
                      </div>
                      <div style={{ marginBottom: '8px', color: '#666' }}>
                        <strong>Antwort:</strong> {card.answer}
                      </div>
                      <div style={{ marginBottom: '12px', fontSize: '12px', color: '#999' }}>
                        Schwierigkeit: {card.difficulty} | Korrekt: {card.correct_count} | Falsch: {card.incorrect_count}
                      </div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          className="btn btn-secondary"
                          onClick={() => setEditingFlashcard(card)}
                          style={{ padding: '6px 12px', fontSize: '14px' }}
                        >
                          <Edit2 size={14} />
                          Bearbeiten
                        </button>
                        <button
                          className="btn btn-danger"
                          onClick={() => handleDeleteFlashcard(card.id, card.question)}
                          disabled={deleteFlashcardMutation.isPending}
                          style={{ padding: '6px 12px', fontSize: '14px' }}
                        >
                          <Trash2 size={14} />
                          Löschen
                        </button>
                      </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Graph Tab */}
      {activeTab === 'graph' && (
        <div className="card">
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>Knowledge Graph</h2>
          {graphLoading ? (
            <p>Lade...</p>
          ) : (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
                <div style={{ padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Gesamt Knoten</div>
                  <div style={{ fontSize: '24px', fontWeight: '700' }}>{graphStats?.total_nodes || 0}</div>
                </div>
                <div style={{ padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Konzepte</div>
                  <div style={{ fontSize: '24px', fontWeight: '700' }}>{graphStats?.concepts || 0}</div>
                </div>
                <div style={{ padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Themen</div>
                  <div style={{ fontSize: '24px', fontWeight: '700' }}>{graphStats?.topics || 0}</div>
                </div>
                <div style={{ padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Verbindungen</div>
                  <div style={{ fontSize: '24px', fontWeight: '700' }}>{graphStats?.total_relationships || 0}</div>
                </div>
              </div>

              <div style={{ padding: '16px', backgroundColor: '#fff3e0', borderRadius: '8px', marginBottom: '16px' }}>
                <p style={{ marginBottom: '8px' }}>
                  <strong>Warnung:</strong> Das Leeren des Knowledge Graphs kann nicht rückgängig gemacht werden!
                </p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                  Alle Konzepte, Themen und Verbindungen werden permanent gelöscht.
                </p>
              </div>

              <button
                className="btn btn-danger"
                onClick={handleClearGraph}
                disabled={clearGraphMutation.isPending}
              >
                <Trash2 size={18} />
                {clearGraphMutation.isPending ? 'Wird geleert...' : 'Knowledge Graph leeren'}
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default DataManagementPage;
