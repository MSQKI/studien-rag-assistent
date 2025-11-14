import { useState, useEffect, useRef } from 'react';

export interface ProgressData {
  document_id: string;
  filename: string;
  status: 'started' | 'processing' | 'completed' | 'error';
  step: string;
  progress: number;
  total_steps: number;
  current_step: number;
  details?: string;
  error?: string;
  results?: any;
}

export function useDocumentProgress(documentId: string | null) {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!documentId) {
      setProgress(null);
      setIsConnected(false);
      return;
    }

    // Connect to SSE endpoint
    const eventSource = new EventSource(`http://localhost:8000/api/progress/stream/${documentId}`);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
      console.log('SSE connection established for document:', documentId);
    };

    eventSource.onmessage = (event) => {
      try {
        const data: ProgressData = JSON.parse(event.data);
        setProgress(data);

        // Auto-close connection when done
        if (data.status === 'completed' || data.status === 'error') {
          setTimeout(() => {
            eventSource.close();
            setIsConnected(false);
          }, 1000);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      setIsConnected(false);
      eventSource.close();
    };

    // Cleanup on unmount
    return () => {
      if (eventSource.readyState !== EventSource.CLOSED) {
        eventSource.close();
      }
    };
  }, [documentId]);

  return { progress, isConnected };
}
