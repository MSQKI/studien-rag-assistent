# 📚 Studien-RAG-Assistent v2.0

**Deine persönliche KI-gestützte Lernplattform**

Lade deine Vorlesungsskripte hoch und:
- 🤖 Stelle Fragen zu deinen Dokumenten (RAG Chat)
- 📇 Lerne mit intelligenten Karteikarten (Spaced Repetition)
- 🕸️ Visualisiere Konzepte im Knowledge Graph
- 📊 Verwalte all deine Lerndaten

## ✨ Hauptfeatures

### 🤖 RAG Chat
- Intelligentes Frage-Antwort-System basierend auf hochgeladenen Dokumenten
- **OpenAI GPT-4o-mini** für präzise Antworten
- Kontextuelle Antworten mit **automatischen Quellenangaben**
- **ChromaDB Vector Store** für semantische Suche
- Persistente Speicherung aller Dokumente
- **🎤 Voice-Eingabe**: Fragen per Sprache stellen (Web Speech API)
- **🔊 Text-to-Speech**: Antworten automatisch vorlesen lassen

### 📇 Karteikarten mit Spaced Repetition
- **Automatische Karteikartenerstellung** aus Dokumenten
- **SM-2 Algorithm** für optimale Wiederholungsintervalle
- Schwierigkeitsanpassung basierend auf Lernfortschritt
- **Vollständige CRUD-Operationen**: Erstellen, Bearbeiten, Löschen
- **Alle Karteikarten löschen**: Mit Bestätigungsdialog
- Detaillierte Statistiken: Genauigkeit, Streak, Fällige Karten

### 🕸️ Knowledge Graph
- **Automatische Konzeptextraktion** mit OpenAI aus Dokumenten
- **Neo4j Graph Database** für Beziehungen zwischen Konzepten
- **Interaktive Cytoscape.js Visualisierung** mit allen extrahierten Konzepten
- Zoom, Pan, Such- und Filterfunktionen
- Konzept-Details beim Klicken auf Nodes
- **Visualisierungstool**: Zeigt "big picture" Zusammenhänge (nicht direkt in RAG-Queries genutzt)
- **Path Finding**: Entdecke Verbindungen zwischen Konzepten

### 📊 Datenverwaltung
- **Dokumenten-Management**: Upload, Anzeigen, Löschen
- **Karteikarten-Editor**: Inline-Bearbeitung aller Karten
- **Graph-Verwaltung**: Statistiken und Löschfunktionen
- Vollständige **CRUD für alle Datentypen**

### ⚡ Performance & UX
- **React Query Caching**: 5 min fresh, 10 min GC
- **Optimierte API-Aufrufe** mit intelligentem Retry
- **Persistente Docker Volumes** für Neo4j, ChromaDB
- **Responsive Design** für Desktop & Tablet
- **Playwright E2E Tests** für Qualitätssicherung

## 🏗️ Architektur

```
┌──────────────────────────────────────────────────────────┐
│              React Frontend (Port 3000)                   │
│     React 18 + TypeScript + Vite + React Query          │
│  Dashboard │ RAG │ Flashcards │ Graph │ Data Mgmt       │
└──────────────────┬───────────────────────────────────────┘
                   │ REST API (axios)
                   ▼
┌──────────────────────────────────────────────────────────┐
│            FastAPI Backend (Port 8000)                   │
│        Python 3.11 + Pydantic + Async/Await             │
│  /rag │ /flashcards │ /graph │ /documents               │
└──┬──────────┬──────────┬──────────────────────────────────┘
   │          │          │
   │          │          │
   ▼          ▼          ▼
┌─────┐   ┌────────┐   ┌──────────┐   ┌─────────┐
│Neo4j│   │ChromaDB│   │PostgreSQL│   │ OpenAI  │
│Graph│   │ Vector │   │Flashcards│   │   API   │
│ DB  │   │ Store  │   │    DB    │   │         │
│7687 │   │ Local  │   │   5432   │   │GPT-4o   │
│7474 │   │Persist │   │          │   │  mini   │
└─────┘   └────────┘   └──────────┘   └─────────┘
```

### Legacy Support
- **Streamlit UI (Port 8501)**: Original RAG-Interface für Kompatibilität

## 📦 Installation & Start

### Voraussetzungen
- **Docker** und **Docker Compose** installiert
- **OpenAI API Key** ([hier erhalten](https://platform.openai.com/api-keys))
- Windows, macOS oder Linux

### 🚀 Schnellstart (3 Schritte - 5 Minuten)

#### Schritt 1: Repository herunterladen
```bash
git clone <repository-url>
cd studien-rag-assistent
```

#### Schritt 2: OpenAI API Key konfigurieren
1. Hol dir einen API Key von https://platform.openai.com/api-keys
2. Erstelle eine `.env` Datei im Hauptverzeichnis:
   ```bash
   # Windows
   copy .env.example .env
   notepad .env

   # macOS/Linux
   cp .env.example .env
   nano .env
   ```
3. Füge deinen API Key ein:
   ```
   OPENAI_API_KEY=sk-...dein-key-hier...
   ```

#### Schritt 3: Starten!
```bash
# Windows
start.bat

# macOS/Linux
./start.sh
```

**Das war's!** Die Plattform läuft jetzt auf http://localhost:3000

#### Stoppen
```bash
# Windows
stop.bat

# macOS/Linux
./stop.sh
```

> **Hinweis**: Beim ersten Start dauert es 1-2 Minuten bis alle Services bereit sind. Deine Daten bleiben auch nach dem Stoppen erhalten.

### Lokale Entwicklung

#### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📖 Wie benutze ich die Plattform?

### 1. Dokumente hochladen 📄
- Gehe zu **"Datenverwaltung"** → Tab **"Dokumente"**
- Klicke auf **"Dokument hochladen"**
- Wähle deine PDF-Vorlesungsskripte aus
- Warte ~30 Sekunden pro Dokument (automatische Verarbeitung)
- ✅ Fertig! Daten sind jetzt in RAG, Karteikarten & Graph verfügbar

### 2. Fragen stellen 💬
- Gehe zu **"RAG Chat"**
- Stelle Fragen wie: *"Erkläre mir [Konzept]"* oder *"Was steht über [Thema]?"*
- **🎤 NEU: Spracheingabe!** Klicke das Mikrofon-Symbol und sprich deine Frage
- Erhalte Antworten mit **Quellenangaben** (Seite + Dokument)
- **🔊 NEU: Antwort anhören!** Die Antwort wird automatisch vorgelesen
- Chatte natürlich - die KI versteht Kontext!

### 3. Mit Karteikarten lernen 🎴
- Gehe zu **"Karteikarten"**
- Siehe deine Stats: Gesamt, Fällig heute, Genauigkeit
- Klicke Karte zum Umdrehen
- Bewerte dich ehrlich: **"Ja"** = gewusst, **"Nein"** = nicht gewusst
- Das System merkt sich automatisch wann du wiederholen solltest!

### 4. Knowledge Graph erkunden 🕸️
- Gehe zu **"Knowledge Graph"**
- Siehst alle Konzepte aus deinen Dokumenten visualisiert
- **Zoom**: Buttons oder Mausrad
- **Suche**: Suchfeld oben rechts
- **Klicke Nodes**: Für Details und Beschreibung
- **Verbindungen**: Zeigen Beziehungen zwischen Konzepten

### 5. Daten bearbeiten ✏️
- Gehe zu **"Datenverwaltung"**
- **Dokumente**: Alle Docs anzeigen & löschen
- **Karteikarten**: Inline bearbeiten (Frage/Antwort ändern), einzeln löschen, **alle löschen**
- **Graph**: Statistiken sehen, kompletten Graph leeren

> **Tipp**: Alle Änderungen werden automatisch gespeichert und bleiben auch nach Neustart erhalten!

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

# PostgreSQL
DATABASE_URL=postgresql://user:password@postgres:5432/studydb

# Paths
CHROMA_PERSIST_DIR=./data/chroma_db
UPLOAD_DIR=./data/uploads
```

## 📁 Projektstruktur

```
studien-rag-assistent/
├── frontend/                 # React Frontend
│   ├── src/
│   │   ├── components/       # React Components
│   │   │   ├── Dashboard/    # Dashboard Page
│   │   │   ├── RAG/          # RAG Chat Page
│   │   │   ├── Flashcards/   # Flashcards Page
│   │   │   ├── Graph/        # Knowledge Graph Page
│   │   │   └── DataManagement/ # Data Mgmt Page
│   │   ├── services/         # API Client (axios)
│   │   └── App.tsx           # Main App with Routing
│   ├── tests/                # Playwright E2E Tests
│   ├── package.json
│   └── Dockerfile
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/routes/       # API Endpoints
│   │   │   ├── rag.py
│   │   │   ├── flashcards.py
│   │   │   ├── graph.py
│   │   │   └── documents.py
│   │   ├── services/         # Business Logic
│   │   │   ├── rag/          # RAG Chain, Vector Store
│   │   │   ├── flashcards/   # Spaced Repetition
│   │   │   └── graph/        # Neo4j, Entity Extraction
│   │   ├── models/           # Pydantic Models
│   │   └── main.py           # FastAPI App
│   └── requirements.txt
├── docker/                   # Docker Configs
│   ├── Dockerfile.backend
│   ├── Dockerfile
│   ├── docker-compose.yml     # Streamlit only
│   └── docker-compose-full.yml # Full stack
├── data/                     # Persistent Data
│   ├── chroma_db/            # Vector DB (mounted)
│   └── uploads/              # Uploaded PDFs
└── .env                      # Environment Variables
```

## 🧪 Tests

### Playwright E2E Tests
```bash
cd frontend
npm install
npx playwright test                    # Run all tests
npx playwright test --headed          # With browser
npx playwright test graph.spec.ts     # Specific test
npx playwright show-report            # Show HTML report
```

### Backend Tests
```bash
cd backend
pytest                                # All tests
pytest --cov=app --cov-report=html    # With coverage
```

## 🔧 API Dokumentation

Backend API Docs (automatisch generiert):
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Wichtige Endpoints

#### RAG
```
GET  /api/rag/stats         # RAG Statistiken
POST /api/rag/query         # Frage stellen
POST /api/rag/clear         # RAG Cache leeren
```

#### Flashcards
```
GET    /api/flashcards                 # Liste alle Karten
POST   /api/flashcards                 # Neue Karte erstellen
GET    /api/flashcards/{id}            # Eine Karte abrufen
PUT    /api/flashcards/{id}            # Karte bearbeiten
DELETE /api/flashcards/{id}            # Karte löschen
GET    /api/flashcards/next/due        # Nächste fällige Karte
POST   /api/flashcards/answer          # Antwort aufzeichnen
GET    /api/flashcards/stats/overview  # Statistiken
```

#### Graph
```
GET    /api/graph/concepts      # Alle Konzepte
GET    /api/graph/stats         # Graph Statistiken
DELETE /api/graph/clear         # Graph leeren
```

#### Documents
```
GET    /api/documents           # Liste alle Dokumente
POST   /api/documents/upload    # Dokument hochladen
DELETE /api/documents/{id}      # Dokument löschen
```

## 🐛 Troubleshooting

### Docker Container starten nicht
```bash
docker-compose -f docker-compose-full.yml logs
docker-compose -f docker-compose-full.yml down -v
docker-compose -f docker-compose-full.yml up --build -d
```

### Frontend zeigt "Failed to fetch"
- Prüfe ob Backend läuft: `curl http://localhost:8000/health`
- Prüfe Browser Console für CORS-Fehler
- Stelle sicher, dass `VITE_API_URL` korrekt ist

### Neo4j Connection Error
- Warte 30s nach `docker-compose up` (Neo4j braucht Zeit zum Starten)
- Prüfe Credentials: neo4j / studyplatform2024
- Öffne http://localhost:7474 um Verbindung zu testen

### Karteikarten zeigen "404 Not Found"
- Normal wenn keine Karten fällig sind!
- Prüfe "Gesamt" Statistik - wenn 0, erstelle zuerst Karten

### Graph zeigt nichts
- Lade zuerst Dokumente hoch (automatische Konzeptextraktion)
- Warte auf Verarbeitung (kann 30-60s dauern)
- Prüfe `/api/graph/stats` - sollte `concepts > 0` zeigen

## 🚀 Features & Improvements

### Neu in v2.0 (Aktuell - November 2025)
- ✅ **Vollständiges React Frontend** statt nur Streamlit
- ✅ **Knowledge Graph Visualisierung** mit Cytoscape.js (inkl. Beziehungen)
- ✅ **Spaced Repetition System** für Karteikarten (SM-2 Algorithm)
- ✅ **Vollständige CRUD-Operationen** für alle Datentypen
- ✅ **Alle Karteikarten löschen** mit Bestätigungsdialog ⚠️
- ✅ **React Query Caching** für Performance (5min fresh)
- ✅ **Playwright E2E Tests** für Qualitätssicherung
- ✅ **Modern UI/UX** mit Lucide Icons
- ✅ **Persistent Docker Volumes** (Daten bleiben erhalten!)
- ✅ **🎤 Voice im RAG Chat**: Spracheingabe & Text-to-Speech
- ✅ **Lokale Installation**: Alles läuft auf deinem PC
- ✅ **Ausführliche Tests**: Alle Features getestet und funktionsfähig

### Geplante Features
- 🔄 Automatische Flashcard-Generierung aus RAG-Antworten
- 🔄 Multi-Tenant Support mit User Authentication
- 🔄 Export/Import von Karteikarten & Graphen
- 🔄 Erweiterte Voice-Features mit OpenAI Realtime API
- 🔄 Mobile App (React Native)

## 🔒 Sicherheit

- ✅ API Keys niemals in Git committen
- ✅ `.env` für alle Secrets verwenden
- ✅ Input Validation für alle Uploads
- ✅ Error Handling ohne Stacktrace-Leaks
- ⚠️ **Aktuell keine Authentifizierung** - nur für lokale Nutzung!

## 📝 Lizenz

MIT License - siehe LICENSE Datei.

## 🤝 Contributing

Beiträge sind willkommen!

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Committe Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

## 🎓 Credits

Entwickelt mit:
- [React 18](https://react.dev/) + [Vite](https://vitejs.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Neo4j](https://neo4j.com/)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [OpenAI API](https://openai.com/)
- [Cytoscape.js](https://js.cytoscape.org/)
- [React Query](https://tanstack.com/query/latest)
- [Playwright](https://playwright.dev/)

---

**Made with ❤️ by Claude & Eric for students everywhere**

📧 Bei Fragen: Issue im Repository öffnen
