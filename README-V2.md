# 🎓 Study Platform v2.0 - Intelligenter Lernassistent

Eine **umfassende Lernplattform** mit RAG, Voice Buddy, Knowledge Graph und Spaced Repetition Flashcards.

## 🌟 Features

### ✅ Vollständig implementiert und einsatzbereit:

#### 1. **RAG Assistant** 💬
- Dokumenten-basierte Fragen & Antworten
- PDF Upload und automatische Verarbeitung
- Semantische Suche mit ChromaDB
- Quellenangaben mit Seitenzahlen
- Konversationsgedächtnis

#### 2. **Flashcard System** 📚
- Automatische Karteikarten-Generierung aus PDFs
- Spaced Repetition Algorithm (SM-2)
- Study Statistiken und Streak-Tracking
- Review History und Performance Tracking
- SQLite Datenbank für Persistenz

#### 3. **Knowledge Graph** 🕸️
- Automatische Entity Extraction aus Dokumenten
- Neo4j Graph-Datenbank
- Konzept-Beziehungen und Prerequisites
- Learning Path Generation (Backend bereit)
- Graph API vollständig implementiert

#### 4. **Voice Study Buddy** 🎤
- OpenAI Realtime API Integration (Backend bereit)
- WebSocket-basierte Audio-Streaming
- Function Calling für Flashcards und Erklärungen
- Session Management

#### 5. **Modern React Frontend** 🎨
- Dashboard mit Statistiken
- RAG Chat Interface
- Flashcard Study Interface
- Responsive Design
- TypeScript + React 18

#### 6. **Docker Deployment** 🐳
- Multi-Service Setup
- Automatisches Orchestrierung
- Health Checks
- Persistente Volumes
- Ein-Befehl-Start

---

## 🚀 Schnellstart

### Voraussetzungen
- Docker & Docker Compose
- OpenAI API Key
- 8GB RAM empfohlen

### In 3 Schritten starten:

```bash
# 1. Repository klonen (falls noch nicht geschehen)
git clone <your-repo>
cd studien-rag-assistent

# 2. OpenAI API Key konfigurieren
cp .env.example .env
# Öffne .env und füge ein: OPENAI_API_KEY=sk-...

# 3. Alle Services starten
./START.sh  # Linux/Mac
# ODER
START.bat   # Windows
```

**Das war's!** 🎉

---

## 📍 Service URLs

Nach dem Start sind folgende Services verfügbar:

| Service | URL | Beschreibung |
|---------|-----|--------------|
| 🎨 **Frontend** | http://localhost:3000 | Moderne React UI |
| 🚀 **Backend API** | http://localhost:8000 | FastAPI Backend |
| 📚 **API Docs** | http://localhost:8000/api/docs | Swagger UI |
| 🕸️ **Neo4j Browser** | http://localhost:7474 | Graph Datenbank |
| 📊 **Streamlit** | http://localhost:8501 | Original RAG UI |

### Neo4j Zugangsdaten:
- **Username:** neo4j
- **Password:** studyplatform2024

---

## 🎯 Erste Schritte

### 1. Frontend öffnen
Öffne http://localhost:3000 in deinem Browser

### 2. PDF hochladen
- Gehe zu "RAG Chat"
- Klicke auf "PDF hochladen"
- Wähle eine PDF-Datei (z.B. Vorlesungsfolien)
- Warte ~30 Sekunden auf Verarbeitung

### 3. Dokumente befragen
- Stelle Fragen im Chat
- Erhalte Antworten mit Quellenangaben
- Konversationskontext wird automatisch berücksichtigt

### 4. Mit Karteikarten lernen
- Gehe zu "Karteikarten"
- Flashcards wurden automatisch generiert
- Lerne mit Spaced Repetition
- Verfolge deinen Fortschritt

---

## 📁 Projektstruktur

```
studien-rag-assistent/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI Entry Point
│   │   ├── config.py          # Konfiguration
│   │   ├── api/routes/        # API Endpoints
│   │   └── services/          # Business Logic
│   │       ├── rag/           # RAG Services
│   │       ├── voice/         # Voice Buddy
│   │       ├── graph/         # Knowledge Graph
│   │       └── flashcards/    # Flashcard System
│   └── requirements.txt
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React Komponenten
│   │   ├── services/          # API Services
│   │   └── styles/            # CSS
│   ├── Dockerfile
│   └── package.json
├── docker/
│   ├── docker-compose-full.yml  # Vollständiges Setup
│   ├── Dockerfile.backend
│   └── Dockerfile
├── data/                       # Persistente Daten
│   ├── chroma_db/             # Vector Store
│   ├── uploads/               # PDF Files
│   └── flashcards/            # SQLite DB
├── START.sh / START.bat       # Start Scripts
├── ARCHITECTURE.md            # System-Architektur
├── IMPLEMENTATION.md          # Implementierungs-Details
└── START.md                   # Detaillierte Anleitung
```

---

## 🎨 Frontend Features

### Dashboard
- Übersicht über alle Statistiken
- Schnellzugriff auf alle Features
- Streak-Tracking und Motivation

### RAG Chat
- Interaktiver Chat mit Dokumenten
- PDF Upload mit Drag & Drop
- Quellenangaben mit Seitenzahlen
- Markdown-Unterstützung

### Flashcards
- Interaktive Karteikarten
- Spaced Repetition
- Fortschritts-Statistiken
- Schwierigkeits-Anpassung

### Knowledge Graph
- Placeholder für zukünftige Visualisierung
- Backend vollständig bereit
- API Endpoints verfügbar

---

## 🔧 API Endpoints

### RAG
```
POST   /api/rag/query          - Frage stellen
POST   /api/rag/clear          - Konversation löschen
GET    /api/rag/stats          - Statistiken
```

### Flashcards
```
GET    /api/flashcards         - Alle Karteikarten
POST   /api/flashcards         - Erstellen
GET    /api/flashcards/next/due - Nächste fällige
POST   /api/flashcards/answer  - Antwort aufzeichnen
GET    /api/flashcards/stats/overview - Statistiken
```

### Documents
```
POST   /api/documents/upload   - PDF hochladen
GET    /api/documents          - Alle Dokumente
DELETE /api/documents/{id}     - Dokument löschen
```

### Graph
```
GET    /api/graph/concepts     - Alle Konzepte
GET    /api/graph/related/{concept} - Verwandte Konzepte
POST   /api/graph/path         - Lernpfad finden
```

**Vollständige API Dokumentation:** http://localhost:8000/api/docs

---

## 🐛 Troubleshooting

### Services starten nicht
```bash
# Docker Status prüfen
docker ps

# Logs anzeigen
docker-compose -f docker/docker-compose-full.yml logs -f

# Services neu bauen
docker-compose -f docker/docker-compose-full.yml build --no-cache
docker-compose -f docker/docker-compose-full.yml up -d
```

### "Connection refused" Fehler
```bash
# Warte ~30 Sekunden, Services brauchen Zeit zum Starten
# Prüfe Health Status
docker-compose -f docker/docker-compose-full.yml ps

# Einzelne Services neu starten
docker-compose -f docker/docker-compose-full.yml restart backend
docker-compose -f docker/docker-compose-full.yml restart neo4j
```

### Frontend zeigt keine Daten
```bash
# Prüfe ob Backend erreichbar ist
curl http://localhost:8000/health

# Prüfe Frontend Logs
docker-compose -f docker/docker-compose-full.yml logs frontend

# Browser Cache leeren und neu laden
```

---

## 🛠️ Entwicklung

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
# Läuft auf http://localhost:5173
```

### Tests ausführen
```bash
# Backend Tests
cd backend
pytest

# Frontend Tests
cd frontend
npm test
```

---

## 📊 Technologie-Stack

### Backend
- **FastAPI** - Modern Python Web Framework
- **LangChain** - RAG Pipeline
- **ChromaDB** - Vector Database
- **Neo4j** - Graph Database
- **SQLite** - Flashcard Database
- **OpenAI** - LLM & Embeddings

### Frontend
- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build Tool
- **TanStack Query** - Data Fetching
- **Axios** - HTTP Client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **Nginx** - Reverse Proxy

---

## 📚 Dokumentation

- **START.md** - Detaillierte Startanleitung
- **ARCHITECTURE.md** - System-Architektur
- **IMPLEMENTATION.md** - Implementierungs-Details (18+ Seiten!)
- **QUICKSTART-V2.md** - 5-Minuten-Quickstart

---

## 🎯 Roadmap

### Phase 1: ✅ Vollständig implementiert
- ✅ FastAPI Backend mit allen Services
- ✅ React Frontend mit allen Hauptseiten
- ✅ RAG Integration
- ✅ Flashcard System mit Spaced Repetition
- ✅ Knowledge Graph Backend
- ✅ Document Pipeline
- ✅ Docker Deployment

### Phase 2: 🚧 In Entwicklung
- Graph Visualization (D3.js/Cytoscape)
- Voice Buddy WebSocket Frontend
- User Authentication
- Multi-User Support

### Phase 3: 📋 Geplant
- Mobile App
- Collaborative Learning
- Advanced Analytics
- Export Features

---

## 📄 Lizenz

Siehe LICENSE Datei.

---

## 🤝 Beitragen

Pull Requests sind willkommen! Für größere Änderungen bitte zuerst ein Issue erstellen.

---

## 💡 Hinweise

- **Erste Verwendung:** Warte ~30 Sekunden nach dem Start, bis alle Services bereit sind
- **PDF Upload:** Große PDFs (>50MB) können länger dauern
- **Neo4j:** Der erste Start kann 1-2 Minuten dauern
- **Daten:** Alle Daten werden in `./data` persistiert

---

## 🎉 Los geht's!

```bash
./START.sh    # Oder START.bat auf Windows
```

Öffne http://localhost:3000 und beginne zu lernen! 🚀

---

**Version:** 2.0.0
**Letzte Aktualisierung:** 2025-01-06
**Entwickelt mit:** ❤️ und Claude Code
