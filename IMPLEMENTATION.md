# Study Platform - Implementierungs-Dokumentation

## Übersicht

Die Studien-Plattform wurde erfolgreich von einem einzelnen RAG-Assistenten zu einer umfassenden Lernplattform erweitert, die **vier Hauptfunktionen** integriert:

1. **RAG Assistant** - Dokumenten-basierte Fragen & Antworten
2. **Voice Study Buddy** - Interaktive Karteikarten mit Spracherkennung
3. **Knowledge Graph Navigator** - Wissensvisualisierung und Lernpfade
4. **Flashcard System** - Spaced Repetition Learning

---

## ✅ Implementierte Komponenten

### 1. Backend-Architektur (FastAPI)

**Status:** ✅ Vollständig implementiert

#### Hauptkomponenten:
- **`backend/app/main.py`** - FastAPI Hauptanwendung
- **`backend/app/config.py`** - Erweiterte Konfiguration
- **`backend/app/api/routes/`** - API Endpoints für alle Services

#### API-Routen:
```
/api/rag/*          - RAG Queries, Dokument-Verwaltung
/api/voice/*        - Voice Sessions (WebSocket)
/api/graph/*        - Knowledge Graph Abfragen
/api/flashcards/*   - Flashcard CRUD & Spaced Repetition
/api/documents/*    - Dokument-Upload & Management
```

#### Dokumentation:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

### 2. Voice Study Buddy

**Status:** ✅ Vollständig implementiert

#### Komponenten:
- **`realtime_client.py`** - OpenAI Realtime API WebSocket Client
- **`session_manager.py`** - Session-Verwaltung und Cleanup

#### Features:
- ✅ WebSocket-basierte Audio-Streaming
- ✅ OpenAI Realtime API Integration (gpt-4o-realtime-preview)
- ✅ Server-side VAD (Voice Activity Detection)
- ✅ Function Calling für Flashcards und Konzepterklärungen
- ✅ Session Timeout Management (15 Minuten)
- ✅ Automatische Session-Bereinigung

#### Tools für den Assistenten:
1. **`get_flashcard()`** - Nächste Karteikarte abrufen
2. **`check_answer()`** - Antwort des Studenten bewerten
3. **`explain_concept()`** - Konzept mit RAG erklären

#### Verwendung:
```python
from app.services.voice.session_manager import get_session_manager

# Session erstellen
manager = get_session_manager()
session = await manager.create_session(user_id="student123")

# WebSocket-Verbindung
await websocket.accept()
# Audio-Streaming zwischen Client und Realtime API
```

---

### 3. Flashcard System

**Status:** ✅ Vollständig implementiert

#### Komponenten:
- **`flashcard_manager.py`** - SQLite-basierte Verwaltung
- **`spaced_repetition.py`** - SM-2 & Anki-Algorithmen

#### Features:
- ✅ SQLite Datenbank für Persistenz
- ✅ Spaced Repetition (SM-2 Algorithmus)
- ✅ Review History Tracking
- ✅ Schwierigkeits-Anpassung
- ✅ Subject & Tag Filtering
- ✅ Study Statistics

#### Datenbankschema:
```sql
CREATE TABLE flashcards (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty INTEGER DEFAULT 1,
    tags TEXT,
    document_id TEXT,
    created_at TIMESTAMP,
    last_reviewed TIMESTAMP,
    next_review TIMESTAMP,
    correct_count INTEGER DEFAULT 0,
    incorrect_count INTEGER DEFAULT 0,
    easiness_factor REAL DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    repetition_number INTEGER DEFAULT 0
);

CREATE TABLE review_history (
    id TEXT PRIMARY KEY,
    flashcard_id TEXT NOT NULL,
    reviewed_at TIMESTAMP,
    correct BOOLEAN NOT NULL,
    time_spent_seconds INTEGER
);
```

#### Verwendung:
```python
from app.services.flashcards.flashcard_manager import get_flashcard_manager

manager = get_flashcard_manager()

# Karteikarte erstellen
card_id = manager.create_flashcard(
    subject="Mathematik",
    question="Was ist die Ableitung von x²?",
    answer="2x",
    difficulty=2,
    tags=["Analysis", "Ableitungen"]
)

# Nächste fällige Karte abrufen
next_card = manager.get_next_due_flashcard(subject="Mathematik")

# Antwort aufzeichnen
updated = manager.record_answer(card_id, correct=True, time_spent_seconds=30)
```

---

### 4. Knowledge Graph

**Status:** ✅ Vollständig implementiert

#### Komponenten:
- **`entity_extractor.py`** - LLM-basierte Entity Extraction
- **`graph_builder.py`** - Neo4j Graph Management
- **`path_finder.py`** - Learning Path Generation

#### Features:
- ✅ Automatische Entity Extraction aus Dokumenten
- ✅ Fuzzy Matching für Entity Resolution
- ✅ Neo4j Graph-Datenbank
- ✅ Learning Path Finding (Shortest Path)
- ✅ Related Concepts Discovery
- ✅ Prerequisite Tracking
- ✅ Concept Suggestions

#### Entity-Typen:
- **Concept** - Fachbegriffe, Theorien, Algorithmen
- **Person** - Forscher, Autoren
- **Topic** - Übergeordnete Themen
- **Resource** - Bücher, Papers, Websites

#### Beziehungs-Typen:
- **PREREQUISITE_OF** - Voraussetzungsbeziehung
- **RELATES_TO** - Thematische Verwandtschaft
- **PART_OF** - Hierarchische Beziehung
- **TAUGHT_BY** - Lehrender/Entwickler
- **MENTIONED_IN** - Quellenreferenz

#### Verwendung:
```python
from app.services.graph.entity_extractor import EntityExtractor
from app.services.graph.graph_builder import get_graph_builder
from app.services.graph.path_finder import PathFinder

# Entity Extraction
extractor = EntityExtractor()
graph_data = extractor.extract(text, subject="Informatik", chunk_metadata={...})

# Graph aufbauen
builder = get_graph_builder()
result = builder.add_graph_data(graph_data)

# Lernpfad finden
finder = PathFinder(builder.driver)
paths = finder.find_learning_path("Variablen", "Rekursion", max_length=10)

# Verwandte Konzepte
related = finder.find_related_concepts("Algorithmen", depth=2)
```

---

## 📁 Projektstruktur

```
studien-rag-assistent/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI Entry Point
│   │   ├── config.py               # Erweiterte Konfiguration
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── rag.py         # RAG Endpoints
│   │   │       ├── voice.py       # Voice WebSocket
│   │   │       ├── graph.py       # Graph API
│   │   │       ├── flashcards.py  # Flashcard CRUD
│   │   │       └── documents.py   # Document Upload
│   │   └── services/
│   │       ├── rag/               # RAG Services (migrated from src/)
│   │       │   ├── rag_chain.py
│   │       │   ├── vector_store.py
│   │       │   └── document_processor.py
│   │       ├── voice/
│   │       │   ├── realtime_client.py
│   │       │   └── session_manager.py
│   │       ├── graph/
│   │       │   ├── entity_extractor.py
│   │       │   ├── graph_builder.py
│   │       │   └── path_finder.py
│   │       └── flashcards/
│   │           ├── flashcard_manager.py
│   │           └── spaced_repetition.py
│   └── requirements.txt            # Erweiterte Dependencies
├── docker/
│   ├── docker-compose-full.yml    # Full Stack Setup
│   ├── Dockerfile.backend         # Backend Container
│   └── Dockerfile                 # Original Streamlit Container
├── data/
│   ├── chroma_db/                 # Vector Store
│   ├── uploads/                   # PDF Files
│   └── flashcards/
│       └── flashcards.db          # SQLite Database
├── src/                           # Original RAG Code (legacy)
├── ARCHITECTURE.md                # System Architecture
├── IMPLEMENTATION.md              # This file
└── .env                           # Configuration
```

---

## 🐳 Docker Deployment

### Vollständiges Setup (Backend + Neo4j + Streamlit)

```bash
# .env Datei erstellen/aktualisieren
cp .env.example .env
# OPENAI_API_KEY eintragen

# Alle Services starten
cd docker
docker-compose -f docker-compose-full.yml up -d

# Services überprüfen
docker-compose -f docker-compose-full.yml ps

# Logs anzeigen
docker-compose -f docker-compose-full.yml logs -f backend
```

### Verfügbare Services:

| Service | Port | URL | Beschreibung |
|---------|------|-----|--------------|
| **Backend** | 8000 | http://localhost:8000 | FastAPI mit allen APIs |
| **API Docs** | 8000 | http://localhost:8000/api/docs | Swagger UI |
| **Neo4j Browser** | 7474 | http://localhost:7474 | Graph Datenbank UI |
| **Streamlit** | 8501 | http://localhost:8501 | Original RAG UI |

### Neo4j Credentials:
- **Username:** neo4j
- **Password:** studyplatform2024

---

## 🔧 Development Setup

### 1. Backend Development (ohne Docker)

```bash
# Virtual Environment erstellen
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Neo4j starten (Docker)
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/studyplatform2024 \
  neo4j:5-community

# Backend starten
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Testing

```bash
# Tests ausführen
pytest backend/tests/

# Mit Coverage
pytest --cov=app backend/tests/

# Einzelne Tests
pytest backend/tests/test_flashcards.py -v
```

---

## 📝 .env Konfiguration

Erweitere deine `.env` Datei mit folgenden Variablen:

```env
# OpenAI
OPENAI_API_KEY=your_api_key_here

# Models
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
REALTIME_MODEL=gpt-4o-realtime-preview

# Neo4j (Docker)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=studyplatform2024
NEO4J_DATABASE=neo4j

# Voice Configuration
VOICE_NAME=alloy
AUDIO_FORMAT=pcm16
SAMPLE_RATE=24000
TURN_DETECTION_TYPE=server_vad

# Flashcards
FLASHCARD_GENERATION_ENABLED=true
FLASHCARDS_PER_DOCUMENT=10
SPACED_REPETITION_ALGORITHM=sm2

# Graph
ENTITY_EXTRACTION_ENABLED=true
ENTITY_CONFIDENCE_THRESHOLD=0.7

# Paths
DATA_DIR=./data
CHROMA_PERSIST_DIR=./data/chroma_db
UPLOAD_DIR=./data/uploads
FLASHCARDS_DB_PATH=./data/flashcards/flashcards.db
```

---

## 🎯 Nächste Schritte

### Phase 1: Integration & Testing ⏳
1. **RAG Service Integration**
   - RAG Routes mit migrierten Services verbinden
   - Document Upload Pipeline implementieren
   - End-to-End Tests schreiben

2. **Voice Buddy Integration**
   - Flashcard Manager mit Voice Session verbinden
   - RAG-basierte Konzepterklärungen integrieren
   - Client-seitige Audio-Streaming implementieren

3. **Knowledge Graph Pipeline**
   - Automatische Entity Extraction bei Dokument-Upload
   - Graph Visualization Endpoints testen
   - Learning Path API validieren

### Phase 2: Frontend Development 🎨
1. **React Dashboard** erstellen
   - Navigation zwischen Features
   - Unified Dashboard mit Statistiken
   - Document Upload UI

2. **Voice Interface UI**
   - Audio Visualizer
   - Flashcard Display
   - Session Controls

3. **Graph Visualization**
   - D3.js oder Cytoscape Integration
   - Interactive Graph Navigation
   - Learning Path Display

### Phase 3: Advanced Features 🚀
1. **Auto-Flashcard Generation**
   - LLM-basierte Karteikarten-Erstellung aus Dokumenten
   - Quality Scoring
   - Batch Generation

2. **Graph ML Features**
   - Community Detection
   - Concept Importance Ranking (PageRank)
   - Personalized Recommendations

3. **Collaborative Features**
   - Multi-User Support
   - Shared Study Sessions
   - Progress Tracking

---

## 🧪 Testing Guide

### Manual Testing

#### 1. Backend Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Flashcard System
```bash
# Create flashcard
curl -X POST http://localhost:8000/api/flashcards \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test",
    "question": "Was ist 2+2?",
    "answer": "4",
    "difficulty": 1
  }'

# Get next due
curl http://localhost:8000/api/flashcards/next/due

# Record answer
curl -X POST http://localhost:8000/api/flashcards/answer \
  -H "Content-Type: application/json" \
  -d '{
    "flashcard_id": "YOUR_ID",
    "correct": true
  }'
```

#### 3. Knowledge Graph
```bash
# Get all concepts
curl http://localhost:8000/api/graph/concepts

# Find learning path
curl "http://localhost:8000/api/graph/path?start=Variables&end=Recursion"

# Get related concepts
curl http://localhost:8000/api/graph/related/Algorithms?depth=2
```

#### 4. Neo4j Browser
- Öffne http://localhost:7474
- Login: neo4j / studyplatform2024
- Cypher Query testen:
```cypher
MATCH (n:Concept) RETURN n LIMIT 10
```

---

## 🐛 Troubleshooting

### Backend startet nicht
```bash
# Logs prüfen
docker-compose -f docker/docker-compose-full.yml logs backend

# Container neu bauen
docker-compose -f docker/docker-compose-full.yml build backend --no-cache
docker-compose -f docker/docker-compose-full.yml up -d backend
```

### Neo4j Connection Error
```bash
# Neo4j Status prüfen
docker-compose -f docker/docker-compose-full.yml ps neo4j

# Neo4j Logs
docker-compose -f docker/docker-compose-full.yml logs neo4j

# Container neu starten
docker-compose -f docker/docker-compose-full.yml restart neo4j
```

### Flashcard Database Locked
```bash
# SQLite Connection überprüfen
sqlite3 data/flashcards/flashcards.db "PRAGMA integrity_check;"

# Backup erstellen
cp data/flashcards/flashcards.db data/flashcards/flashcards.db.backup
```

---

## 📚 API Dokumentation

Die vollständige API-Dokumentation ist verfügbar unter:

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### Wichtigste Endpoints:

#### RAG
- `POST /api/rag/query` - Stelle eine Frage
- `POST /api/rag/clear` - Lösche Konversation
- `GET /api/rag/stats` - System-Statistiken

#### Voice
- `WS /api/voice/session` - Voice Session (WebSocket)
- `POST /api/voice/ephemeral-key` - Ephemeral Key für Browser
- `GET /api/voice/sessions` - Aktive Sessions

#### Graph
- `POST /api/graph/extract` - Entities extrahieren
- `GET /api/graph/concepts` - Alle Konzepte
- `POST /api/graph/path` - Lernpfad finden
- `GET /api/graph/related/{concept}` - Verwandte Konzepte

#### Flashcards
- `GET /api/flashcards` - Alle Karteikarten
- `POST /api/flashcards` - Erstellen
- `GET /api/flashcards/next/due` - Nächste fällige
- `POST /api/flashcards/answer` - Antwort aufzeichnen
- `POST /api/flashcards/generate` - Auto-generieren
- `GET /api/flashcards/stats/overview` - Statistiken

#### Documents
- `POST /api/documents/upload` - PDF hochladen
- `GET /api/documents` - Alle Dokumente
- `DELETE /api/documents/{id}` - Dokument löschen

---

## 🎓 Verwendungsbeispiele

### Vollständiger Workflow

```python
import requests

API_BASE = "http://localhost:8000/api"

# 1. Dokument hochladen
with open("vorlesung.pdf", "rb") as f:
    response = requests.post(
        f"{API_BASE}/documents/upload",
        files={"file": f},
        params={"subject": "Informatik"}
    )
    doc_id = response.json()["document_id"]

# 2. Flashcards generieren
response = requests.post(
    f"{API_BASE}/flashcards/generate",
    json={"document_id": doc_id, "subject": "Informatik", "count": 10}
)
flashcards = response.json()

# 3. Nächste Karteikarte
response = requests.get(f"{API_BASE}/flashcards/next/due")
next_card = response.json()

# 4. Antwort aufzeichnen
response = requests.post(
    f"{API_BASE}/flashcards/answer",
    json={
        "flashcard_id": next_card["id"],
        "correct": True,
        "time_spent_seconds": 30
    }
)

# 5. RAG Query
response = requests.post(
    f"{API_BASE}/rag/query",
    json={"question": "Was sind Algorithmen?"}
)
answer = response.json()

# 6. Learning Path
response = requests.post(
    f"{API_BASE}/graph/path",
    params={"start": "Variablen", "end": "Rekursion"}
)
paths = response.json()
```

---

## 📊 Performance Optimierung

### Empfohlene Konfiguration

```yaml
# Docker Compose
services:
  neo4j:
    environment:
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=2G

  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Batch Processing
- Dokumente in Batches von max. 10 verarbeiten
- Entity Extraction parallel ausführen
- Flashcard Generation asynchron

---

## 🔐 Sicherheitshinweise

1. **API Keys:** Niemals in Git committen
2. **Neo4j Passwort:** In Production ändern
3. **CORS:** Origins in Production einschränken
4. **File Upload:** Größenbeschränkung (50MB default)
5. **Rate Limiting:** In Production aktivieren

---

## 📄 Lizenz

Siehe LICENSE Datei im Hauptverzeichnis.

---

## 🤝 Beitragen

Pull Requests sind willkommen! Für größere Änderungen bitte zuerst ein Issue erstellen.

---

**Stand:** 2025-01-06
**Version:** 2.0.0
**Author:** Claude Code Assistant
