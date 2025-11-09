# Studien-RAG-Assistent - Vollständige Projektdokumentation

> **Version:** 2.0.0
> **Stand:** November 2025
> **Status:** Produktionsbereit

---

## Inhaltsverzeichnis

1. [Projekt-Übersicht](#projekt-übersicht)
2. [Architektur](#architektur)
3. [Technologie-Stack](#technologie-stack)
4. [Komponenten im Detail](#komponenten-im-detail)
5. [Datenfluss](#datenfluss)
6. [API-Referenz](#api-referenz)
7. [Datenspeicherung](#datenspeicherung)
8. [Deployment](#deployment)
9. [Entwicklung](#entwicklung)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)

---

## Projekt-Übersicht

### Was ist der Studien-RAG-Assistent?

Der Studien-RAG-Assistent ist eine vollständige Lernplattform für Studierende, die Retrieval-Augmented Generation (RAG) nutzt, um Vorlesungsunterlagen durchsuchbar und befragbar zu machen. Die Plattform kombiniert mehrere moderne KI-Technologien:

- **RAG-Chat**: Intelligente Befragung von PDF-Dokumenten
- **Knowledge Graph**: Visualisierung von Konzepten und deren Beziehungen
- **Flashcards**: Spaced Repetition Lernsystem mit SM-2 Algorithmus
- **Voice Interface**: Spracheingabe und Text-to-Speech

### Hauptmerkmale

- ✅ **Vollständig lokal lauffähig** - Keine Cloud-Abhängigkeiten außer OpenAI API
- ✅ **Moderne React-Frontend** - Professionelle Benutzeroberfläche
- ✅ **FastAPI Backend** - Schnelle, asynchrone REST API
- ✅ **Docker-basiert** - Einfaches Deployment mit einem Befehl
- ✅ **Persistente Daten** - Alle Daten bleiben erhalten (Vector Store, Graph, Flashcards)
- ✅ **Vollständig getestet** - E2E Tests mit Playwright

---

## Architektur

### System-Architektur Diagramm

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     (http://localhost:3000)                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTP REST API
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + TypeScript)               │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────────┐ │
│  │Dashboard │ RAG Chat │Flashcards│  Graph   │Data Management │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────────┘ │
│                  React Router | React Query                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Axios API Calls
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Routes                             │   │
│  │  /api/rag  |  /api/flashcards  |  /api/graph  |  /api/docs│  │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Service Layer                           │   │
│  │  ┌────────────┬──────────────┬─────────────┬──────────┐  │   │
│  │  │RAG Service │Graph Service │Flash Service│Doc Service│ │   │
│  │  └────────────┴──────────────┴─────────────┴──────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└────┬─────────────────┬─────────────────┬────────────────────────┘
     │                 │                 │
     ▼                 ▼                 ▼
┌─────────┐      ┌──────────┐     ┌───────────┐
│ChromaDB │      │  Neo4j   │     │  SQLite   │
│ Vector  │      │  Graph   │     │Flashcards │
│  Store  │      │ Database │     │  Database │
└─────────┘      └──────────┘     └───────────┘
     │
     │ Embeddings & LLM Calls
     ▼
┌─────────────────────────────────┐
│       OpenAI API                │
│  - GPT-4o-mini (Chat)           │
│  - text-embedding-3-small       │
└─────────────────────────────────┘
```

### Komponenten-Übersicht

| Komponente | Technologie | Port | Zweck |
|------------|-------------|------|-------|
| Frontend | React 18 + TypeScript | 3000 | Benutzeroberfläche |
| Backend | FastAPI + Python 3.11 | 8000 | REST API |
| Neo4j | Neo4j 5 Community | 7474, 7687 | Knowledge Graph |
| Streamlit (Legacy) | Streamlit + Python | 8501 | Alte UI (optional) |
| ChromaDB | ChromaDB (embedded) | - | Vector Store |
| SQLite | SQLite3 | - | Flashcards DB |

---

## Technologie-Stack

### Backend (Python)

```python
# Core Framework
fastapi==0.115.13          # Moderne Web-Framework
uvicorn[standard]==0.34.0  # ASGI Server
pydantic==2.10.3           # Data Validation
python-dotenv==1.0.1       # Environment Variables

# RAG & LLM
langchain==0.3.10          # RAG Framework
langchain-openai==0.2.12   # OpenAI Integration
langchain-chroma==0.1.4    # ChromaDB Integration
chromadb==0.5.23           # Vector Store
openai==1.55.3             # OpenAI API Client

# Graph Database
neo4j==5.26.0              # Neo4j Python Driver

# Document Processing
pypdf==5.1.0               # PDF Parsing
tiktoken==0.8.0            # Token Counting

# Database
aiosqlite==0.20.0          # Async SQLite für Flashcards

# Utilities
loguru==0.7.3              # Logging
```

### Frontend (TypeScript/JavaScript)

```json
{
  "core": {
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "react-router-dom": "6.20.0",
    "typescript": "5.3.3",
    "vite": "5.0.7"
  },
  "state_api": {
    "@tanstack/react-query": "5.13.0",
    "axios": "1.6.2",
    "zustand": "4.4.7"
  },
  "visualization": {
    "cytoscape": "3.28.1",
    "react-cytoscapejs": "2.0.0"
  },
  "ui": {
    "lucide-react": "0.294.0",
    "react-markdown": "9.0.1"
  },
  "testing": {
    "@playwright/test": "1.56.1"
  }
}
```

### Infrastructure

- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Node.js**: 18+ (für Frontend Build)
- **Python**: 3.11+

---

## Komponenten im Detail

### 1. Backend API (FastAPI)

**Hauptdatei:** `backend/app/main.py`

#### API-Routen

##### RAG Routes (`/api/rag`)

```python
POST   /api/rag/query        # RAG-Query ausführen
GET    /api/rag/stats        # Statistiken abrufen
DELETE /api/rag/clear        # Conversation History löschen
```

**Beispiel Request:**
```bash
curl -X POST http://localhost:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Was ist eine Hashmap?",
    "stream": false
  }'
```

**Beispiel Response:**
```json
{
  "answer": "Eine Hashmap ist eine Datenstruktur...",
  "sources": [
    {
      "page": 42,
      "document": "datenstrukturen.pdf",
      "content": "Hashmaps verwenden..."
    }
  ]
}
```

##### Flashcard Routes (`/api/flashcards`)

```python
GET    /api/flashcards/           # Alle Flashcards
POST   /api/flashcards/           # Neue Flashcard erstellen
PUT    /api/flashcards/{id}       # Flashcard bearbeiten
DELETE /api/flashcards/{id}       # Flashcard löschen
POST   /api/flashcards/{id}/review # Flashcard bewerten (SM-2)
GET    /api/flashcards/stats      # Statistiken
DELETE /api/flashcards/           # Alle löschen
```

##### Graph Routes (`/api/graph`)

```python
GET    /api/graph/concepts        # Alle Konzepte + Beziehungen
POST   /api/graph/path            # Kürzesten Pfad finden
GET    /api/graph/stats           # Graph-Statistiken
DELETE /api/graph/clear           # Graph löschen
```

##### Document Routes (`/api/documents`)

```python
POST   /api/documents/upload      # PDF hochladen
GET    /api/documents/             # Alle Dokumente
DELETE /api/documents/{doc_id}    # Dokument löschen
```

#### Service Layer

##### RAG Service (`backend/app/services/rag/`)

**Datei-Struktur:**
```
services/rag/
├── rag_chain.py           # LangChain ConversationalRetrievalChain
├── vector_store.py        # ChromaDB Integration
└── document_processor.py  # PDF → Chunks Pipeline
```

**Wichtigste Klassen:**

```python
class RAGChain:
    """Wrapper für LangChain RAG Chain"""

    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.chain = ConversationalRetrievalChain(...)

    async def query(self, question: str) -> dict:
        """RAG Query ausführen"""
        ...

class VectorStore:
    """ChromaDB Vector Store Manager"""

    def add_documents(self, docs: List[Document]):
        """Dokumente zu ChromaDB hinzufügen"""
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.collection.add(...)

class DocumentProcessor:
    """PDF → Text → Chunks Pipeline"""

    def process_pdf(self, file_path: str) -> List[Document]:
        """PDF verarbeiten"""
        # 1. PDF lesen (pypdf)
        # 2. Text extrahieren
        # 3. Chunking (RecursiveCharacterTextSplitter)
        # 4. Metadata hinzufügen
        ...
```

**Chunk-Konfiguration:**
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Max 1000 Zeichen pro Chunk
    chunk_overlap=200,      # 200 Zeichen Überlappung
    separators=["\n\n", "\n", ". ", " ", ""]  # Semantische Grenzen
)
```

##### Graph Service (`backend/app/services/graph/`)

**Datei-Struktur:**
```
services/graph/
├── entity_extractor.py    # OpenAI-basierte Konzeptextraktion
├── graph_builder.py       # Neo4j Graph Operations
└── path_finder.py         # Shortest Path Finding
```

**Entity Extraction:**
```python
class EntityExtractor:
    """Extrahiert Konzepte aus Text mit OpenAI"""

    async def extract_entities(self, text: str) -> List[Entity]:
        response = await openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "Extract key concepts and relationships from this text..."
            }]
        )
        # Parse JSON Response → Entities + Relations
        ...
```

**Graph Operations:**
```python
class GraphBuilder:
    """Neo4j Graph Builder"""

    def add_concept(self, name: str, properties: dict):
        query = """
        MERGE (c:Concept {name: $name})
        SET c += $properties
        """
        self.session.run(query, name=name, properties=properties)

    def add_relationship(self, from_concept: str, to_concept: str, rel_type: str):
        query = """
        MATCH (a:Concept {name: $from}), (b:Concept {name: $to})
        MERGE (a)-[r:RELATES_TO {type: $type}]->(b)
        """
        ...
```

##### Flashcard Service (`backend/app/services/flashcards/`)

**SM-2 Spaced Repetition Algorithmus:**

```python
class SpacedRepetition:
    """SM-2 Algorithm Implementation"""

    def calculate_next_review(
        self,
        quality: int,      # 0-5 (0=complete blackout, 5=perfect recall)
        easiness: float,   # Difficulty factor (default 2.5)
        interval: int,     # Days since last review
        repetitions: int   # Number of consecutive correct reviews
    ) -> dict:
        """
        SM-2 Formel:
        - EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        - Interval:
            - If q < 3: start over (interval = 1)
            - First repetition: 1 day
            - Second repetition: 6 days
            - Subsequent: interval * EF
        """

        if quality < 3:
            repetitions = 0
            interval = 1
        else:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = round(interval * easiness)
            repetitions += 1

        easiness = max(1.3, easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        return {
            "next_review": datetime.now() + timedelta(days=interval),
            "interval": interval,
            "easiness": easiness,
            "repetitions": repetitions
        }
```

### 2. Frontend (React)

**Hauptdatei:** `frontend/src/App.tsx`

#### Routing

```typescript
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/rag" element={<RAGInterface />} />
  <Route path="/flashcards" element={<FlashcardsInterface />} />
  <Route path="/graph" element={<GraphVisualization />} />
  <Route path="/data" element={<DataManagement />} />
</Routes>
```

#### State Management

**React Query für Server State:**

```typescript
// Beispiel: RAG Stats fetchen
const { data: stats } = useQuery({
  queryKey: ['rag-stats'],
  queryFn: () => api.get('/api/rag/stats'),
  refetchInterval: 30000,  // Alle 30 Sekunden
  staleTime: 5 * 60 * 1000  // 5 Minuten fresh
});
```

**Zustand für Client State:**

```typescript
interface AppState {
  darkMode: boolean;
  voiceEnabled: boolean;
  setDarkMode: (enabled: boolean) => void;
  setVoiceEnabled: (enabled: boolean) => void;
}

const useAppStore = create<AppState>((set) => ({
  darkMode: false,
  voiceEnabled: true,
  setDarkMode: (enabled) => set({ darkMode: enabled }),
  setVoiceEnabled: (enabled) => set({ voiceEnabled: enabled })
}));
```

#### Knowledge Graph Visualisierung

**Cytoscape.js Konfiguration:**

```typescript
const cytoscapeConfig = {
  elements: {
    nodes: concepts.map(c => ({
      data: { id: c.id, label: c.name }
    })),
    edges: relationships.map(r => ({
      data: { source: r.from, target: r.to }
    }))
  },
  style: [
    {
      selector: 'node',
      style: {
        'background-color': '#4F46E5',
        'label': 'data(label)',
        'width': 60,
        'height': 60,
        'font-size': 12
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#94A3B8',
        'target-arrow-color': '#94A3B8',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier'
      }
    }
  ],
  layout: {
    name: 'cose',  // Force-directed layout
    animate: true,
    animationDuration: 500
  }
};
```

#### Voice Interface

**Web Speech API Integration:**

```typescript
const useVoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const recognition = useRef<SpeechRecognition>();

  useEffect(() => {
    recognition.current = new webkitSpeechRecognition();
    recognition.current.continuous = false;
    recognition.current.lang = 'de-DE';

    recognition.current.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
    };
  }, []);

  const startListening = () => {
    recognition.current?.start();
    setIsListening(true);
  };

  return { isListening, startListening };
};
```

**Text-to-Speech:**

```typescript
const useTextToSpeech = () => {
  const speak = (text: string) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'de-DE';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  return { speak };
};
```

### 3. Legacy Streamlit UI

**Hauptdatei:** `src/ui.py`

Einfachere RAG-Chat-Oberfläche ohne Graph/Flashcards. Läuft parallel auf Port 8501 als Backup.

---

## Datenfluss

### Dokument-Upload bis RAG-Query

```
1. USER UPLOAD
   ↓
2. BACKEND: /api/documents/upload
   ↓
3. DocumentProcessor.process_pdf()
   - PDF → Text (pypdf)
   - Text → Chunks (RecursiveCharacterTextSplitter)
   - Add Metadata (page, source)
   ↓
4. VectorStore.add_documents()
   - Generate Embeddings (OpenAI text-embedding-3-small)
   - Store in ChromaDB
   ↓
5. EntityExtractor.extract_entities()
   - Send chunks to GPT-4o-mini
   - Parse JSON response
   ↓
6. GraphBuilder.build_graph()
   - Create Concept nodes in Neo4j
   - Create Relationships
   ↓
7. FlashcardGenerator.generate()
   - Generate flashcards from entities
   - Store in SQLite
   ↓
8. RESPONSE: {document_id, num_chunks, num_concepts, num_flashcards}
   ↓
9. USER QUERY
   ↓
10. BACKEND: /api/rag/query
    ↓
11. RAGChain.query()
    - Generate Query Embedding
    - ChromaDB Similarity Search (k=4)
    - Retrieve top chunks
    ↓
12. LLM Generation
    - Combine query + context chunks
    - GPT-4o-mini generates answer
    - Include sources (page + document)
    ↓
13. RESPONSE: {answer, sources: [{page, document, content}]}
```

---

## API-Referenz

### Environment Variables

```bash
# ERFORDERLICH
OPENAI_API_KEY=sk-...        # OpenAI API Key

# OPTIONAL (Defaults sind gesetzt)
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
TEMPERATURE=0.2
MAX_TOKENS=2000

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4

NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=studyplatform2024

CHROMA_PERSIST_DIR=./data/chroma_db
UPLOAD_DIR=./data/uploads

LOG_LEVEL=INFO
```

### OpenAI Konfiguration

**LLM für Chat:**
```python
ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,        # Faktisch, wenig Kreativität
    max_tokens=2000,        # Max Response Length
    streaming=False
)
```

**Embeddings:**
```python
OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536  # Vektorgröße
)
```

**Kosten (Stand Nov 2024):**
- GPT-4o-mini: ~$0.15 / 1M input tokens, ~$0.60 / 1M output tokens
- text-embedding-3-small: ~$0.02 / 1M tokens

---

## Datenspeicherung

### 1. ChromaDB (Vector Store)

**Pfad:** `data/chroma_db/`

**Schema:**
```python
Collection: "rag_documents"
Vectors: 1536-dimensional (text-embedding-3-small)
Metadata per Document:
  - source: str (filename)
  - page: int
  - chunk_id: str
  - timestamp: str
```

**Persistenz:** Lokales Dateisystem (SQLite + Parquet)

### 2. Neo4j (Knowledge Graph)

**Docker Volume:** `neo4j_data`

**Schema:**
```cypher
# Nodes
(:Concept {
  name: String,
  description: String,
  created_at: DateTime
})

# Relationships
(:Concept)-[:RELATES_TO {
  type: String,
  strength: Float
}]->(:Concept)
```

**Zugriff:**
- Browser UI: http://localhost:7474
- Bolt Protocol: bolt://localhost:7687
- Credentials: neo4j / studyplatform2024

### 3. SQLite (Flashcards)

**Pfad:** `data/flashcards/flashcards.db`

**Schema:**
```sql
CREATE TABLE flashcards (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- SM-2 Fields
    easiness REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review DATETIME,
    last_reviewed DATETIME,

    -- Stats
    total_reviews INTEGER DEFAULT 0,
    correct_reviews INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0
);
```

---

## Deployment

### Docker Compose Setup

**Full Stack starten:**
```bash
# Linux/Mac
./START.sh

# Windows
START.bat
```

**Services:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs
- Neo4j Browser: http://localhost:7474
- Streamlit (Legacy): http://localhost:8501

**Stoppen:**
```bash
# Linux/Mac
./stop.sh

# Windows
stop.bat
```

### Health Checks

Alle Services haben Health Checks:

```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3

neo4j:
  healthcheck:
    test: ["CMD-SHELL", "cypher-shell -u neo4j -p studyplatform2024 'RETURN 1'"]
    interval: 10s
```

### Volumes & Persistenz

```yaml
volumes:
  # Neo4j
  neo4j_data:      # Graph Database
  neo4j_logs:      # Logs
  neo4j_plugins:   # APOC + GDS Plugins

  # Lokale Mounts
  ../data/chroma_db    # ChromaDB Vector Store
  ../data/uploads      # PDF Files
  ../data/flashcards   # SQLite Database
```

---

## Entwicklung

### Lokale Entwicklung (ohne Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env Datei erstellen
cp ../.env.example ../.env
# OPENAI_API_KEY eintragen

uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Startet auf Port 3000
```

**Neo4j:**
```bash
docker run -d \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/studyplatform2024 \
  neo4j:5-community
```

### Code-Struktur Best Practices

**Backend:**
- Type Hints überall: `def process_pdf(file_path: str) -> List[Document]:`
- Async wo möglich: `async def query(question: str) -> dict:`
- Proper Error Handling: `try/except` mit Logging
- Pydantic Models für Validation
- Docstrings für alle Funktionen

**Frontend:**
- TypeScript strict mode
- Komponenten-basiert (Atomic Design)
- React Query für Server State
- Zustand für Client State
- Error Boundaries

### Testing

**Backend Tests (pytest):**
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

**Frontend Tests (Playwright):**
```bash
cd frontend
npm run test        # Run all tests
npm run test:ui     # UI mode
npm run test:debug  # Debug mode
```

**Test Coverage:**
- Backend: 75%+
- Frontend: E2E Tests für alle Hauptfeatures

---

## Testing

### Playwright E2E Tests

**Test-Dateien:**
```
frontend/tests/
├── comprehensive-test.spec.ts    # Full User Journey
├── rag.spec.ts                   # RAG Chat Tests
├── flashcards.spec.ts            # Flashcard Tests
├── graph.spec.ts                 # Graph Tests
└── data-management.spec.ts       # CRUD Tests
```

**Beispiel Test:**
```typescript
test('RAG Query with Sources', async ({ page }) => {
  await page.goto('http://localhost:3000/rag');

  // Upload document
  await page.setInputFiles('input[type="file"]', './test-data/sample.pdf');
  await expect(page.locator('.success-message')).toBeVisible();

  // Query
  await page.fill('textarea[name="query"]', 'Was ist eine Hashmap?');
  await page.click('button:has-text("Senden")');

  // Verify response
  await expect(page.locator('.answer')).toContainText('Hashmap');
  await expect(page.locator('.source')).toContainText('sample.pdf');
});
```

**Test-Ergebnisse (Stand 07.11.2025):**
- ✅ 2/2 Comprehensive Tests (26.5s)
- ✅ 5/5 Core Functionality Tests (9.6s)
- ✅ 2/2 Dashboard Tests (5.9s)

---

## Troubleshooting

### Häufige Probleme

#### 1. "OpenAI API Key not found"

**Lösung:**
```bash
# .env Datei erstellen
cp .env.example .env

# API Key eintragen
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

#### 2. "ChromaDB Permission Denied"

**Lösung:**
```bash
# Rechte setzen (Linux/Mac)
chmod -R 777 data/chroma_db/

# Docker-Container neustarten
cd docker
docker-compose -f docker-compose-full.yml restart backend
```

#### 3. "Neo4j Connection Failed"

**Lösung:**
```bash
# Prüfen ob Neo4j läuft
docker ps | grep neo4j

# Logs prüfen
docker logs study-platform-neo4j

# Health Check
docker exec study-platform-neo4j \
  cypher-shell -u neo4j -p studyplatform2024 "RETURN 1"
```

#### 4. "Frontend shows 'Network Error'"

**Lösung:**
```bash
# Backend erreichbar?
curl http://localhost:8000/health

# CORS-Problem?
# Prüfe backend/app/config.py → CORS_ORIGINS

# Docker Network prüfen
docker network inspect study-network
```

#### 5. "Flashcards not saving"

**Lösung:**
```bash
# SQLite DB erstellen
mkdir -p data/flashcards
touch data/flashcards/flashcards.db

# Rechte setzen
chmod 777 data/flashcards/flashcards.db

# Container neu starten
docker-compose -f docker-compose-full.yml restart backend
```

### Logs anschauen

```bash
# Alle Services
cd docker
docker-compose -f docker-compose-full.yml logs -f

# Nur Backend
docker logs study-platform-backend -f

# Nur Neo4j
docker logs study-platform-neo4j -f
```

### Performance-Optimierung

**ChromaDB:**
- Batch Processing für große PDFs
- Regelmäßiges Cleanup alter Dokumente

**Neo4j:**
- Indexes erstellen: `CREATE INDEX ON :Concept(name)`
- Memory anpassen in docker-compose-full.yml

**React Query:**
- Cache-Zeiten anpassen
- Aggressive Invalidation für Realtime-Updates

---

## Weiterführende Ressourcen

### Dokumentation

- [README.md](./README.md) - Schnellstart-Guide
- [SETUP.md](./SETUP.md) - Detaillierte Setup-Anleitung
- [INSTALLATION.md](./INSTALLATION.md) - Workshop-Anleitung für Studierende
- [TEST_REPORT.md](./TEST_REPORT.md) - Test-Ergebnisse
- [KNOWLEDGE_GRAPH_ANALYSIS.md](./KNOWLEDGE_GRAPH_ANALYSIS.md) - Graph-Architektur

### Externe Links

- [LangChain Docs](https://python.langchain.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Query Docs](https://tanstack.com/query/latest)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [ChromaDB Docs](https://docs.trychroma.com/)

---

## Lizenz

MIT License - Siehe [LICENSE](./LICENSE)

---

## Support & Kontakt

Bei Fragen oder Problemen:
1. Issue auf GitHub erstellen
2. Logs prüfen (siehe Troubleshooting)
3. Dokumentation durchsuchen

**Version:** 2.0.0
**Letzte Aktualisierung:** November 2025
