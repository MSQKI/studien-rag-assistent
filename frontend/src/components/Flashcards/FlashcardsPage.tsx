import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { RefreshCw, CheckCircle, XCircle, SkipForward } from 'lucide-react';

import { flashcardsAPI } from '../../services/api';

const FlashcardsPage: React.FC = () => {
  const [showAnswer, setShowAnswer] = useState(false);
  const [startTime, setStartTime] = useState<number>(Date.now());
  const queryClient = useQueryClient();

  const { data: stats } = useQuery({
    queryKey: ['flashcardStats'],
    queryFn: flashcardsAPI.getStats,
  });

  const { data: currentCard, refetch, isLoading } = useQuery({
    queryKey: ['nextFlashcard'],
    queryFn: () => flashcardsAPI.getNext(),
  });

  const answerMutation = useMutation({
    mutationFn: ({ correct }: { correct: boolean }) => {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000);
      return flashcardsAPI.recordAnswer(currentCard.id, correct, timeSpent);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flashcardStats'] });
      setShowAnswer(false);
      setStartTime(Date.now());
      refetch();
    },
  });

  const handleAnswer = (correct: boolean) => {
    answerMutation.mutate({ correct });
  };

  const handleFlip = () => {
    setShowAnswer(!showAnswer);
  };

  const handleSkip = () => {
    setShowAnswer(false);
    setStartTime(Date.now());
    refetch();
  };

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '4px' }}>
          Karteikarten
        </h1>
        <p style={{ color: '#666' }}>Lerne mit Spaced Repetition</p>
      </div>

      {stats && (
        <div className="stats-grid" style={{ marginBottom: '30px' }}>
          <div className="stat-card">
            <div className="stat-label">Gesamt</div>
            <div className="stat-value">{stats.total_flashcards}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Fällig heute</div>
            <div className="stat-value">{stats.due_today}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Genauigkeit</div>
            <div className="stat-value">{stats.accuracy}%</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Streak</div>
            <div className="stat-value">{stats.study_streak_days} Tage</div>
          </div>
        </div>
      )}

      {!currentCard ? (
        <div className="card" style={{ textAlign: 'center', padding: '60px' }}>
          <CheckCircle size={64} color="#27ae60" style={{ margin: '0 auto 20px' }} />
          <h2 style={{ fontSize: '24px', marginBottom: '12px' }}>Alles erledigt!</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>
            Keine Karteikarten fällig. Komm später wieder!
          </p>
          <button className="btn btn-primary" onClick={() => refetch()}>
            <RefreshCw size={18} />
            Erneut prüfen
          </button>
        </div>
      ) : (
        <>
          <div className="flashcard" onClick={handleFlip}>
            {!showAnswer ? (
              <>
                <div style={{ fontSize: '14px', color: '#999', marginBottom: '20px' }}>
                  FRAGE
                </div>
                <div className="flashcard-question">{currentCard.question}</div>
                <div style={{ marginTop: '20px', color: '#999', fontSize: '14px' }}>
                  Klicke um Antwort zu sehen
                </div>
              </>
            ) : (
              <>
                <div style={{ fontSize: '14px', color: '#999', marginBottom: '12px' }}>
                  FRAGE
                </div>
                <div style={{ fontSize: '18px', marginBottom: '24px', color: '#666' }}>
                  {currentCard.question}
                </div>
                <div style={{ fontSize: '14px', color: '#27ae60', marginBottom: '12px' }}>
                  ANTWORT
                </div>
                <div className="flashcard-answer">{currentCard.answer}</div>
              </>
            )}

            <div className="flashcard-difficulty">
              Level {currentCard.difficulty}
            </div>
          </div>

          {showAnswer && (
            <div className="card" style={{ marginTop: '20px' }}>
              <div style={{ textAlign: 'center', marginBottom: '16px', fontWeight: '600' }}>
                Wusstest du die Antwort?
              </div>
              <div className="flashcard-actions" style={{ justifyContent: 'center' }}>
                <button
                  className="btn btn-danger"
                  onClick={() => handleAnswer(false)}
                  disabled={answerMutation.isPending}
                >
                  <XCircle size={18} />
                  Nein
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={handleSkip}
                >
                  <SkipForward size={18} />
                  Überspringen
                </button>
                <button
                  className="btn btn-primary"
                  onClick={() => handleAnswer(true)}
                  disabled={answerMutation.isPending}
                >
                  <CheckCircle size={18} />
                  Ja
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default FlashcardsPage;
