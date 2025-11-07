import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { MessageSquare, CreditCard, Network, Upload, TrendingUp } from 'lucide-react';

import { ragAPI, flashcardsAPI } from '../../services/api';

const Dashboard: React.FC = () => {
  const { data: ragStats } = useQuery({
    queryKey: ['ragStats'],
    queryFn: ragAPI.getStats,
  });

  const { data: flashcardStats } = useQuery({
    queryKey: ['flashcardStats'],
    queryFn: flashcardsAPI.getStats,
  });

  const stats = [
    {
      label: 'Dokumente',
      value: ragStats?.total_documents || 0,
      icon: <Upload />,
      color: '#3498db',
    },
    {
      label: 'Karteikarten',
      value: flashcardStats?.total_flashcards || 0,
      icon: <CreditCard />,
      color: '#2ecc71',
    },
    {
      label: 'Fällig heute',
      value: flashcardStats?.due_today || 0,
      icon: <TrendingUp />,
      color: '#e74c3c',
    },
    {
      label: 'Genauigkeit',
      value: flashcardStats?.accuracy ? `${flashcardStats.accuracy}%` : '0%',
      icon: <TrendingUp />,
      color: '#f39c12',
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
          Willkommen zurück! 👋
        </h1>
        <p style={{ color: '#666', fontSize: '16px' }}>
          Hier ist deine Lernübersicht
        </p>
      </div>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card" style={{ borderLeft: `4px solid ${stat.color}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <div>
                <div className="stat-label">{stat.label}</div>
                <div className="stat-value">{stat.value}</div>
              </div>
              <div style={{ color: stat.color, opacity: 0.3 }}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Schnellzugriff</h2>
          <p className="card-description">Starte deine Lernaktivitäten</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
          <Link to="/rag" style={{ textDecoration: 'none' }}>
            <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
              <MessageSquare size={40} color="#3498db" style={{ marginBottom: '12px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>
                RAG Chat
              </h3>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Frage deine Dokumente alles
              </p>
            </div>
          </Link>

          <Link to="/flashcards" style={{ textDecoration: 'none' }}>
            <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
              <CreditCard size={40} color="#2ecc71" style={{ marginBottom: '12px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>
                Karteikarten
              </h3>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Lerne mit Spaced Repetition
              </p>
            </div>
          </Link>

          <Link to="/graph" style={{ textDecoration: 'none' }}>
            <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
              <Network size={40} color="#9b59b6" style={{ marginBottom: '12px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>
                Knowledge Graph
              </h3>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Visualisiere dein Wissen
              </p>
            </div>
          </Link>
        </div>
      </div>

      {flashcardStats && flashcardStats.study_streak_days > 0 && (
        <div className="card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <h3 style={{ fontSize: '24px', fontWeight: '700', marginBottom: '8px' }}>
            🔥 {flashcardStats.study_streak_days} Tage Streak!
          </h3>
          <p style={{ opacity: 0.9 }}>
            Du bist großartig! Bleib dran!
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
