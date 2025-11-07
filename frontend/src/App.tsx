import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import Layout from './components/Layout';
import Dashboard from './components/Dashboard/Dashboard';
import RAGPage from './components/RAG/RAGPage';
import FlashcardsPage from './components/Flashcards/FlashcardsPage';
import GraphPage from './components/Graph/GraphPage';
import DataManagementPage from './components/DataManagement/DataManagementPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes - data stays fresh for 5 min
      gcTime: 10 * 60 * 1000, // 10 minutes - unused cache garbage collected after 10 min
      refetchInterval: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="rag" element={<RAGPage />} />
            <Route path="flashcards" element={<FlashcardsPage />} />
            <Route path="graph" element={<GraphPage />} />
            <Route path="data" element={<DataManagementPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
