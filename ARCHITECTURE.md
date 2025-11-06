# Study Platform - Integrierte Architektur

## Überblick
Eine umfassende Lernplattform, die drei Hauptfunktionen kombiniert:
1. **RAG Assistant** - Dokumenten-Suche und Q&A
2. **Voice Study Buddy** - Interaktive Karteikarten-Abfrage mit Sprache
3. **Knowledge Graph Navigator** - Wissensvisualisierung und Lernpfade

## Systemarchitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌────────────┐ ┌─────────────┐ ┌────────────┐ ┌──────────────┐│
│  │ Dashboard  │ │  RAG Chat   │ │ Voice Buddy│ │ Graph Viewer ││
│  └────────────┘ └─────────────┘ └────────────┘ └──────────────┘│
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST/WebSocket
┌─────────────────────────┴───────────────────────────────────────┐
│                    Backend (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ API Routes                                                    │
│  │  /api/rag       /api/voice      /api/graph    /api/flashcards│
│  ├──────────────────────────────────────────────────────────────┤
│  │ Services                                                      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  │   RAG    │  │  Voice   │  │  Graph   │  │Flashcards│    │
│  │  │ Service  │  │  Buddy   │  │ Builder  │  │  Manager │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│  └───────┼─────────────┼─────────────┼─────────────┼──────────┘
           │             │             │             │
┌──────────┴─────┬───────┴──────┬──────┴─────┬───────┴─────────┐
│   ChromaDB     │  OpenAI API  │   Neo4j    │     SQLite      │
│  (Vectorstore) │  (Realtime)  │  (Graph)   │  (Flashcards)   │
└────────────────┴──────────────┴────────────┴─────────────────┘
```

## Technologie-Stack

### Backend
- **FastAPI** - Haupt-API-Server
- **Python 3.11+**
- **LangChain** - RAG Pipeline
- **OpenAI** - Embeddings, LLM, Realtime API
- **Neo4j Python Driver** - Graph Datenbank
- **SQLite** - Flashcard Datenbank

### Frontend
- **React 18+**
- **TypeScript**
- **Zustand** - State Management
- **D3.js / Cytoscape** - Graph Visualisierung
- **Web Audio API** - Voice Interface

### Datenbanken
- **ChromaDB** - Vektor-Embeddings
- **Neo4j** - Knowledge Graph
- **SQLite** - Karteikarten & Sessions

### DevOps
- **Docker & Docker Compose** - Container Orchestration
- **Nginx** - Reverse Proxy (optional)

## Projektstruktur

```
studien-rag-assistent/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI Entry Point
│   │   ├── config.py                  # Configuration
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── rag.py            # RAG Endpoints
│   │   │   │   ├── voice.py          # Voice WebSocket
│   │   │   │   ├── graph.py          # Graph API
│   │   │   │   ├── flashcards.py     # Flashcard CRUD
│   │   │   │   └── documents.py      # Document Upload
│   │   │   └── dependencies.py       # Shared Dependencies
│   │   ├── services/
│   │   │   ├── rag/
│   │   │   │   ├── rag_chain.py      # RAG Chain Logic
│   │   │   │   ├── vector_store.py   # ChromaDB Wrapper
│   │   │   │   └── document_processor.py
│   │   │   ├── voice/
│   │   │   │   ├── realtime_client.py   # OpenAI Realtime
│   │   │   │   ├── session_manager.py   # Session Handling
│   │   │   │   └── audio_processor.py   # Audio Utils
│   │   │   ├── graph/
│   │   │   │   ├── entity_extractor.py  # LLM Entity Extraction
│   │   │   │   ├── graph_builder.py     # Neo4j Operations
│   │   │   │   ├── path_finder.py       # Learning Paths
│   │   │   │   └── query_engine.py      # Graph Queries
│   │   │   └── flashcards/
│   │   │       ├── flashcard_manager.py # CRUD Operations
│   │   │       ├── generator.py         # Auto-generate from docs
│   │   │       └── spaced_repetition.py # SR Algorithm
│   │   ├── models/
│   │   │   ├── rag_models.py
│   │   │   ├── graph_models.py
│   │   │   ├── flashcard_models.py
│   │   │   └── voice_models.py
│   │   └── db/
│   │       ├── chroma_client.py
│   │       ├── neo4j_client.py
│   │       └── sqlite_client.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   ├── RAG/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── DocumentUpload.tsx
│   │   │   │   └── SourceCitations.tsx
│   │   │   ├── Voice/
│   │   │   │   ├── VoiceInterface.tsx
│   │   │   │   ├── AudioVisualizer.tsx
│   │   │   │   └── FlashcardDisplay.tsx
│   │   │   ├── Graph/
│   │   │   │   ├── GraphVisualization.tsx
│   │   │   │   ├── PathExplorer.tsx
│   │   │   │   └── ConceptSearch.tsx
│   │   │   └── Flashcards/
│   │   │       ├── FlashcardEditor.tsx
│   │   │       └── StudySession.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── RAGPage.tsx
│   │   │   ├── VoicePage.tsx
│   │   │   ├── GraphPage.tsx
│   │   │   └── FlashcardsPage.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useAudioStream.ts
│   │   │   └── useRAGQuery.ts
│   │   └── store/
│   │       ├── ragStore.ts
│   │       ├── voiceStore.ts
│   │       └── graphStore.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf (optional)
├── data/
│   ├── chroma_db/           # Vector store persistence
│   ├── uploads/             # Uploaded PDFs
│   ├── flashcards.db        # SQLite database
│   └── neo4j/               # Neo4j data directory
├── tests/
│   ├── backend/
│   └── frontend/
└── docs/
    ├── API.md
    ├── SETUP.md
    └── USER_GUIDE.md
```

## Datenfluss

### 1. Dokument-Upload Pipeline
```
PDF Upload → FastAPI
    ↓
DocumentProcessor (Chunking)
    ↓
    ├→ ChromaDB (Embeddings)
    ├→ Entity Extraction (LLM)
    │   ↓
    │   Neo4j (Knowledge Graph)
    └→ Flashcard Generator
        ↓
        SQLite (Flashcards)
```

### 2. RAG Query Flow
```
User Question → FastAPI → RAG Service
    ↓
Vector Search (ChromaDB)
    ↓
LLM + Context → Answer + Sources
    ↓
Frontend Display
```

### 3. Voice Study Session
```
User Speech → WebSocket → Voice Service
    ↓
OpenAI Realtime API
    ↓
    ├→ Flashcard Query (SQLite)
    ├→ Concept Explanation (RAG)
    └→ Audio Response → User
```

### 4. Knowledge Graph Navigation
```
User Query → Graph Service
    ↓
    ├→ Cypher Query (Neo4j)
    ├→ Path Finding Algorithm
    └→ Graph Data → Frontend (D3.js/Cytoscape)
```

## API Endpoints

### RAG Endpoints
- `POST /api/rag/query` - RAG Abfrage
- `POST /api/rag/documents` - Dokument hochladen
- `GET /api/rag/documents` - Dokumente auflisten
- `DELETE /api/rag/documents/{id}` - Dokument löschen
- `POST /api/rag/clear` - Konversation löschen

### Voice Endpoints
- `WS /api/voice/session` - WebSocket für Voice Session
- `POST /api/voice/ephemeral-key` - Ephemeral Key für Client
- `GET /api/voice/sessions` - Sessions auflisten

### Graph Endpoints
- `POST /api/graph/extract` - Entities extrahieren
- `GET /api/graph/concepts` - Alle Konzepte
- `GET /api/graph/concept/{name}` - Konzept-Details
- `POST /api/graph/path` - Lernpfad finden
- `GET /api/graph/related/{concept}` - Verwandte Konzepte

### Flashcard Endpoints
- `GET /api/flashcards` - Alle Karteikarten
- `POST /api/flashcards` - Karteikarte erstellen
- `PUT /api/flashcards/{id}` - Karteikarte aktualisieren
- `DELETE /api/flashcards/{id}` - Karteikarte löschen
- `POST /api/flashcards/generate` - Aus Dokumenten generieren
- `GET /api/flashcards/next` - Nächste Karte (SR)
- `POST /api/flashcards/answer` - Antwort speichern

## Integrationspunkte

### 1. Dokument zu Knowledge Graph
- Beim Dokument-Upload: Automatische Entity Extraction
- Entities werden als Nodes in Neo4j gespeichert
- Beziehungen zwischen Konzepten werden erkannt

### 2. Knowledge Graph zu Flashcards
- Wichtige Konzepte (hohe Centrality) → Flashcards
- Prerequisite-Beziehungen → Card Dependencies
- Difficulty basierend auf Graph-Struktur

### 3. RAG zu Voice Buddy
- Voice Buddy nutzt RAG für Erklärungen
- Flashcards werden aus RAG-Dokumenten generiert
- Kontext-bewusste Antworten

### 4. Alle Services zu Dashboard
- Unified Dashboard zeigt alle Metriken
- Cross-Service Recommendations
- Lernfortschritt über alle Features

## Docker Compose Services

```yaml
services:
  backend:
    - FastAPI Application
    - Port 8000
    - Volumes: data/, uploads/

  frontend:
    - React Application
    - Port 3000
    - Depends on: backend

  neo4j:
    - Neo4j Community
    - Ports: 7474 (Browser), 7687 (Bolt)
    - Volumes: data/neo4j/
    - Plugins: APOC, GDS

  nginx: (optional)
    - Reverse Proxy
    - Port 80/443
    - SSL Termination
```

## Development Workflow

1. **Backend Development**: `cd backend && python -m uvicorn app.main:app --reload`
2. **Frontend Development**: `cd frontend && npm run dev`
3. **Full Stack**: `docker-compose up`
4. **Neo4j Browser**: http://localhost:7474
5. **API Docs**: http://localhost:8000/docs

## Sicherheitsüberlegungen

- API Keys über Environment Variables
- Ephemeral Keys für Realtime API (Browser)
- CORS Configuration für Frontend
- Input Validation (Pydantic)
- File Upload Restrictions
- Rate Limiting für API Endpoints

## Skalierbarkeit

- Stateless Backend (horizontal scaling)
- ChromaDB kann durch managed service ersetzt werden
- Neo4j Aura für Production
- Redis für Caching (optional)
- Load Balancer vor Backend

## Nächste Schritte

1. ✅ Architektur definieren
2. ⏳ Backend-Struktur aufsetzen
3. ⏳ Voice Buddy implementieren
4. ⏳ Knowledge Graph integrieren
5. ⏳ Frontend entwickeln
6. ⏳ Docker Compose konfigurieren
7. ⏳ Tests schreiben
8. ⏳ Deployment vorbereiten
