# 📚 Studien-RAG-Assistent

**Deine persönliche KI-gestützte Lernplattform** - Lade PDFs hoch, stelle Fragen, lerne mit KI-Karteikarten und visualisiere Konzepte.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🤖 RAG Chat
- **Intelligente Frage-Antwort** basierend auf deinen Dokumenten
- **GPT-4o-mini** für präzise, kontextuelle Antworten
- **Automatische Quellenangaben** (Seite + Dokument)
- **🎤 Voice-Eingabe** - Fragen per Sprache stellen
- **🔊 Text-to-Speech** - Antworten vorlesen lassen
- **ChromaDB Vector Store** für semantische Suche

### 📇 Karteikarten mit Spaced Repetition
- **Automatische Generierung** aus deinen Dokumenten
- **SM-2 Algorithm** für optimale Wiederholungsintervalle
- **Vollständige CRUD-Operationen** - Erstellen, Bearbeiten, Löschen
- **Lernstatistiken** - Genauigkeit, Streak, Fällige Karten

### 🕸️ Knowledge Graph
- **Automatische Konzeptextraktion** mit OpenAI
- **Neo4j Graph Database** für Beziehungen
- **Interaktive Cytoscape.js Visualisierung**
- **Path Finding** - Verbindungen zwischen Konzepten entdecken
- Zoom, Pan, Such- und Filterfunktionen

### 📊 Datenverwaltung
- **Dokumenten-Management** - Upload, Anzeigen, Löschen
- **Karteikarten-Editor** - Inline-Bearbeitung
- **Graph-Verwaltung** - Statistiken und Löschfunktionen

---

## 🚀 Schnellstart (3 Schritte)

### Voraussetzungen
- **Docker** und **Docker Compose**
- **OpenAI API Key** ([hier erhalten](https://platform.openai.com/api-keys))

### 1. Repository klonen
```bash
git clone https://github.com/dein-username/studien-rag-assistent.git
cd studien-rag-assistent
```

### 2. API Key konfigurieren
```bash
# Windows
copy .env.example .env
notepad .env

# macOS/Linux
cp .env.example .env
nano .env
```

Füge deinen OpenAI API Key ein:
```env
OPENAI_API_KEY=sk-...dein-key-hier...
```

### 3. Starten!
```bash
# Windows
start.bat

# macOS/Linux
./start.sh
```

**Fertig!** Die App läuft auf: **http://localhost:3000**

> **Hinweis**: Beim ersten Start dauert es 1-2 Minuten. Deine Daten bleiben persistent gespeichert.

### Stoppen
```bash
# Windows: stop.bat
# macOS/Linux: ./stop.sh
```

---

## 🏗️ Architektur

```
┌──────────────────────────────────────┐
│    React Frontend (Port 3000)        │
│  Dashboard │ RAG │ Cards │ Graph     │
└──────────────┬───────────────────────┘
               │ REST API
               ▼
┌──────────────────────────────────────┐
│   FastAPI Backend (Port 8000)        │
│  Python 3.11 + Async/Await           │
└──┬──────┬──────┬──────────────────────┘
   │      │      │
   ▼      ▼      ▼
┌──────┐ ┌────────┐ ┌─────────┐
│Neo4j │ │ChromaDB│ │ OpenAI  │
│Graph │ │Vector  │ │ GPT-4o  │
│ DB   │ │Store   │ │  mini   │
└──────┘ └────────┘ └─────────┘
```

**Tech Stack:**
- **Frontend**: React 18 + TypeScript + Vite + React Query
- **Backend**: FastAPI + LangChain + Pydantic
- **Databases**: ChromaDB (Vektor), Neo4j (Graph), SQLite (Karteikarten)
- **AI**: OpenAI GPT-4o-mini + text-embedding-3-small

---

## 📖 Benutzung

### 1. Dokumente hochladen 📄
1. Gehe zu **"Datenverwaltung"** → **"Dokumente"**
2. Klicke **"Dokument hochladen"**
3. Wähle PDF-Vorlesungsskripte aus
4. Warte ~30 Sekunden pro Dokument
5. ✅ Daten sind in RAG, Karteikarten & Graph verfügbar

### 2. Fragen stellen 💬
1. Gehe zu **"RAG Chat"**
2. Stelle Fragen: *"Erkläre mir [Konzept]"*
3. **🎤 NEU**: Klicke Mikrofon für Spracheingabe
4. Erhalte Antworten mit **Quellenangaben**
5. **🔊 NEU**: Antwort wird automatisch vorgelesen

### 3. Mit Karteikarten lernen 🎴
1. Gehe zu **"Karteikarten"**
2. Siehe Stats: Gesamt, Fällig, Genauigkeit
3. Klicke Karte zum Umdrehen
4. Bewerte: **"Ja"** = gewusst, **"Nein"** = nicht gewusst
5. System merkt sich automatisch Wiederholungsintervalle

### 4. Knowledge Graph erkunden 🕸️
1. Gehe zu **"Knowledge Graph"**
2. Siehst alle Konzepte visualisiert
3. **Zoom** mit Buttons oder Mausrad
4. **Suche** nach Konzepten
5. **Klicke Nodes** für Details

---

## 🔧 Entwicklung

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
# Frontend E2E Tests (Playwright)
cd frontend
npx playwright test

# Backend Tests
cd backend
pytest
```

---

## ⚙️ Konfiguration

Hauptkonfiguration in `.env`:

```bash
# OpenAI (Erforderlich)
OPENAI_API_KEY=sk-...your-key-here

# LLM Settings
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
TEMPERATURE=0.2
MAX_TOKENS=2000

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4

# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=studyplatform2024
```

---

## 📁 Projektstruktur

```
studien-rag-assistent/
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # React Components
│   │   ├── services/        # API Client
│   │   └── App.tsx          # Main App
│   └── tests/               # Playwright E2E Tests
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/routes/      # API Endpoints
│   │   ├── services/        # Business Logic
│   │   │   ├── rag/         # RAG Chain, Vector Store
│   │   │   ├── flashcards/  # Spaced Repetition
│   │   │   └── graph/       # Neo4j, Entity Extraction
│   │   └── main.py          # FastAPI App
│   └── requirements.txt
├── docker/                  # Docker Configs
│   ├── Dockerfile.backend
│   └── docker-compose-full.yml
└── data/                    # Persistent Data
    ├── chroma_db/           # Vector DB
    └── uploads/             # PDFs
```

---

## 🔧 API Dokumentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Wichtige Endpoints

```
# RAG
GET  /api/rag/stats         # Statistiken
POST /api/rag/query         # Frage stellen

# Flashcards
GET    /api/flashcards                 # Liste
POST   /api/flashcards                 # Erstellen
PUT    /api/flashcards/{id}            # Bearbeiten
DELETE /api/flashcards/{id}            # Löschen
GET    /api/flashcards/next/due        # Nächste fällige
POST   /api/flashcards/answer          # Antwort
GET    /api/flashcards/stats/overview  # Statistiken

# Graph
GET    /api/graph/concepts      # Alle Konzepte
GET    /api/graph/stats         # Statistiken
DELETE /api/graph/clear         # Graph leeren

# Documents
GET    /api/documents           # Liste
POST   /api/documents/upload    # Upload
DELETE /api/documents/{id}      # Löschen
```

---

## 🐛 Troubleshooting

### Docker Container starten nicht
```bash
docker-compose -f docker-compose-full.yml logs
docker-compose -f docker-compose-full.yml down -v
docker-compose -f docker-compose-full.yml up --build -d
```

### Frontend zeigt "Failed to fetch"
- Prüfe Backend: `curl http://localhost:8000/health`
- Prüfe Browser Console für CORS-Fehler
- Stelle sicher: `VITE_API_URL=http://localhost:8000`

### Neo4j Connection Error
- Warte 30s nach `docker-compose up`
- Prüfe Credentials: `neo4j / studyplatform2024`
- Teste: http://localhost:7474

### Karteikarten "404 Not Found"
- Normal wenn keine Karten fällig!
- Prüfe "Gesamt" Statistik

### Graph zeigt nichts
- Lade zuerst Dokumente hoch
- Warte auf Verarbeitung (~30-60s)
- Prüfe `/api/graph/stats`

---

## 🚀 Features & Roadmap

### ✅ Neu in v2.0 (November 2025)
- Vollständiges React Frontend
- Knowledge Graph mit Cytoscape.js
- Spaced Repetition (SM-2 Algorithm)
- Vollständige CRUD für alle Datentypen
- Voice-Features (Eingabe & Ausgabe)
- React Query Caching (5min fresh)
- Playwright E2E Tests
- Persistent Docker Volumes

### 🔄 Geplant
- Automatische Flashcard-Generierung aus RAG-Antworten
- Multi-Tenant Support mit Authentication
- Export/Import (Karteikarten & Graphen)
- OpenAI Realtime API Integration
- Mobile App (React Native)

---

## 🔒 Sicherheit

- ✅ API Keys niemals in Git committen
- ✅ `.env` für alle Secrets
- ✅ Input Validation für Uploads
- ✅ Error Handling ohne Stacktraces
- ⚠️ **Keine Authentifizierung** - nur lokal nutzen!

---

## 📝 Lizenz

MIT License

---

## 🤝 Contributing

Beiträge willkommen!

1. Fork das Repository
2. Erstelle Feature Branch (`git checkout -b feature/amazing`)
3. Committe (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Öffne Pull Request

---

## 🎓 Credits

Entwickelt mit: [React](https://react.dev/) • [FastAPI](https://fastapi.tiangolo.com/) • [LangChain](https://github.com/langchain-ai/langchain) • [Neo4j](https://neo4j.com/) • [ChromaDB](https://github.com/chroma-core/chroma) • [OpenAI](https://openai.com/)

---

**Made with ❤️ for students everywhere**

📧 Fragen? Öffne ein Issue!
