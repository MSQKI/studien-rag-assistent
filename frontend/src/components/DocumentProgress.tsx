import React from 'react';
import { Loader2, CheckCircle, XCircle, Upload } from 'lucide-react';
import { useDocumentProgress } from '../hooks/useDocumentProgress';

interface DocumentProgressProps {
  documentId: string | null;
  onComplete?: (results: any) => void;
  onError?: (error: string) => void;
}

const DocumentProgress: React.FC<DocumentProgressProps> = ({ documentId, onComplete, onError }) => {
  const { progress, isConnected } = useDocumentProgress(documentId);

  React.useEffect(() => {
    if (progress?.status === 'completed' && onComplete) {
      onComplete(progress.results);
    }
    if (progress?.status === 'error' && onError) {
      onError(progress.error || 'Unknown error');
    }
  }, [progress?.status, progress?.results, progress?.error, onComplete, onError]);

  if (!documentId || !progress) {
    return null;
  }

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'started':
      case 'processing':
        return <Loader2 size={20} className="animate-spin" style={{ color: '#3498db' }} />;
      case 'completed':
        return <CheckCircle size={20} style={{ color: '#2ecc71' }} />;
      case 'error':
        return <XCircle size={20} style={{ color: '#e74c3c' }} />;
      default:
        return <Upload size={20} />;
    }
  };

  const getStatusColor = () => {
    switch (progress.status) {
      case 'completed':
        return '#2ecc71';
      case 'error':
        return '#e74c3c';
      default:
        return '#3498db';
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '400px',
        maxWidth: 'calc(100vw - 40px)',
        backgroundColor: 'white',
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        padding: '16px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        zIndex: 1000,
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ marginRight: '12px' }}>{getStatusIcon()}</div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: '600', fontSize: '14px', marginBottom: '2px' }}>
            {progress.filename}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {progress.step}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {progress.status !== 'error' && (
        <div
          style={{
            width: '100%',
            height: '6px',
            backgroundColor: '#f0f0f0',
            borderRadius: '3px',
            overflow: 'hidden',
            marginBottom: '8px',
          }}
        >
          <div
            style={{
              width: `${progress.progress}%`,
              height: '100%',
              backgroundColor: getStatusColor(),
              transition: 'width 0.3s ease',
            }}
          />
        </div>
      )}

      {/* Details */}
      {progress.details && (
        <div
          style={{
            fontSize: '11px',
            color: '#999',
            marginTop: '4px',
          }}
        >
          {progress.details}
        </div>
      )}

      {/* Error Message */}
      {progress.error && (
        <div
          style={{
            fontSize: '12px',
            color: '#e74c3c',
            marginTop: '8px',
            padding: '8px',
            backgroundColor: '#ffebee',
            borderRadius: '4px',
          }}
        >
          {progress.error}
        </div>
      )}

      {/* Results Summary */}
      {progress.status === 'completed' && progress.results && (
        <div
          style={{
            fontSize: '12px',
            marginTop: '12px',
            padding: '8px',
            backgroundColor: '#e8f5e9',
            borderRadius: '4px',
          }}
        >
          <div style={{ fontWeight: '600', marginBottom: '4px', color: '#2e7d32' }}>
            Verarbeitung abgeschlossen!
          </div>
          <div style={{ fontSize: '11px', color: '#666' }}>
            {progress.results.chunks_created} Abschnitte • {progress.results.flashcards_generated} Karteikarten •{' '}
            {progress.results.entities_extracted} Konzepte
          </div>
        </div>
      )}

      {/* Connection Status */}
      {!isConnected && progress.status === 'processing' && (
        <div
          style={{
            fontSize: '10px',
            color: '#ff9800',
            marginTop: '4px',
            textAlign: 'center',
          }}
        >
          Verbindung wird wiederhergestellt...
        </div>
      )}
    </div>
  );
};

export default DocumentProgress;
