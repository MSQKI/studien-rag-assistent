# 📚 Studien-RAG-Assistent

Ein state-of-the-art RAG (Retrieval-Augmented Generation) System für Studierende zum intelligenten Durchsuchen und Befragen von Vorlesungsunterlagen mit automatischen Quellenangaben.

## 🎯 Features

- **PDF-Verarbeitung**: Automatische Verarbeitung von Vorlesungs-PDFs mit intelligenter Chunking-Strategie
- **Intelligente Suche**: Semantische Suche über alle hochgeladenen Dokumente mit ChromaDB
- **Chat-Interface**: Konversationsbasierte Interaktion mit Kontext-Verständnis
- **Quellenangaben**: Automatische Quellenangaben mit Seitenzahlen für jede Antwort
- **Batch Processing**: Effiziente Verarbeitung mehrerer Dokumente gleichzeitig
- **Docker Support**: Einfaches Deployment mit Docker und docker-compose
- **Persistente Speicherung**: Alle Dokumente werden persistent in ChromaDB gespeichert

## 🏗️ Technischer Stack

- **Python 3.11+**
- **LangChain**: RAG-Pipeline und Conversation Management
- **ChromaDB**: Lokale, persistente Vektordatenbank
- **OpenAI API**:
  - `gpt-4o-mini` für Chat-Antworten
  - `text-embedding-3-small` für Embeddings
- **Streamlit**: Modernes Web-Interface
- **Docker**: Containerisierung für einfaches Deployment

## 📦 Installation

### Voraussetzungen

- Python 3.11 oder höher
- OpenAI API Key ([hier erhalten](https://platform.openai.com/api-keys))
- Optional: Docker und docker-compose für Container-Deployment

### Lokale Installation

1. **Repository klonen:**
   ```bash
   git clone <repository-url>
   cd studien-rag-assistent
   ```

2. **Virtuelle Umgebung erstellen:**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Dependencies installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren:**
   ```bash
   # .env Datei aus Vorlage erstellen
   cp .env.example .env

   # .env Datei bearbeiten und OpenAI API Key eintragen
   ```

5. **Anwendung starten:**
   ```bash
   python run.py
   ```

   Die Anwendung ist dann unter http://localhost:8501 verfügbar.

### Docker Installation

1. **Docker Image bauen und starten:**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Logs anzeigen:**
   ```bash
   docker-compose logs -f
   ```

3. **Anwendung stoppen:**
   ```bash
   docker-compose down
   ```

Die Anwendung ist dann unter http://localhost:8501 verfügbar.

## 🚀 Nutzung

### 1. Dokumente hochladen

1. Klicke auf "PDF-Dateien auswählen" in der Seitenleiste
2. Wähle eine oder mehrere PDF-Dateien aus deinen Vorlesungsunterlagen
3. Klicke auf "Dokumente verarbeiten"
4. Warte, bis die Verarbeitung abgeschlossen ist

### 2. Fragen stellen

1. Gib deine Frage in das Chat-Eingabefeld ein
2. Drücke Enter oder klicke auf das Senden-Symbol
3. Die KI analysiert deine Dokumente und gibt eine Antwort mit Quellenangaben

### 3. Quellenangaben prüfen

- Jede Antwort enthält automatische Quellenangaben
- Klicke auf "Quellenangaben" um Details zu sehen:
  - Dateiname
  - Seitenzahl
  - Relevanter Textausschnitt

### 4. Dokumente verwalten

- Lösche einzelne Dokumente mit dem 🗑️ Symbol
- Lösche die gesamte Konversation mit "Konversation löschen"
- Setze alles zurück mit "Alles zurücksetzen"

## ⚙️ Konfiguration

Die Anwendung kann über die `.env` Datei konfiguriert werden:

```bash
# Erforderlich
OPENAI_API_KEY=your_api_key_here

# Optional - Modell-Konfiguration
LLM_MODEL=gpt-4o-mini                    # Chat-Modell
EMBEDDING_MODEL=text-embedding-3-small   # Embedding-Modell
TEMPERATURE=0.2                          # Kreativität (0.0-2.0)
MAX_TOKENS=2000                          # Max. Antwortlänge

# Optional - Chunking-Konfiguration
CHUNK_SIZE=1000                          # Chunk-Größe in Zeichen
CHUNK_OVERLAP=200                        # Überlappung zwischen Chunks

# Optional - Storage
CHROMA_PERSIST_DIR=./data/chroma_db      # ChromaDB Speicherort
UPLOAD_DIR=./data/uploads                # Upload-Verzeichnis

# Optional - Retrieval
RETRIEVAL_K=4                            # Anzahl relevanter Dokumente

# Optional - Anwendung
LOG_LEVEL=INFO                           # Logging-Level
BATCH_SIZE=10                            # Batch-Größe für Processing
```

## 📁 Projektstruktur

```
studien-rag-assistent/
├── .claude/                  # Claude Code Konfiguration
│   ├── CLAUDE.md            # Entwicklungsrichtlinien
│   └── settings.json        # Editor-Einstellungen
├── docker/                   # Docker-Konfiguration
│   ├── Dockerfile           # Container-Definition
│   └── docker-compose.yml   # Service-Orchestrierung
├── src/                      # Quellcode
│   ├── config.py            # Zentrale Konfiguration
│   ├── document_processor.py # PDF-Verarbeitung
│   ├── vector_store.py      # ChromaDB Integration
│   ├── rag_chain.py         # RAG-Pipeline
│   └── ui.py                # Streamlit Interface
├── data/                     # Daten (persistent)
│   ├── uploads/             # Hochgeladene PDFs
│   └── chroma_db/           # Vektordatenbank
├── tests/                    # Unit & Integration Tests
├── requirements.txt          # Python Dependencies
├── .env.example             # Umgebungsvariablen-Vorlage
├── run.py                   # Start-Script
└── README.md                # Diese Datei
```

## 🧪 Tests

Tests ausführen:

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Bestimmte Test-Datei
pytest tests/test_document_processor.py
```

## 🔧 Entwicklung

### Code Quality Tools

```bash
# Code formatieren
black src/ tests/

# Imports sortieren
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Best Practices

- **Type Hints**: Verwende Type Hints in allen Funktionen
- **Docstrings**: Dokumentiere alle öffentlichen Funktionen
- **Error Handling**: Implementiere proper try-except Blöcke
- **Logging**: Nutze logging statt print statements
- **Tests**: Schreibe Tests für neue Features

## 📊 Architektur

```
User Interface (Streamlit)
    ↓
RAG Chain (LangChain)
    ↓
Vector Store (ChromaDB) ←→ Document Processor
    ↓
OpenAI API (Embeddings & LLM)
```

### Komponenten

1. **Document Processor**:
   - Lädt PDF-Dateien
   - Extrahiert Text mit PyPDFLoader
   - Chunked Text mit RecursiveCharacterTextSplitter

2. **Vector Store**:
   - Speichert Embeddings in ChromaDB
   - Implementiert Similarity Search
   - Verwaltet Collections

3. **RAG Chain**:
   - Conversational Retrieval Chain
   - Conversation Memory
   - Custom Prompts für deutsche Antworten

4. **UI**:
   - File Upload & Management
   - Chat Interface
   - Source Citations Display

## 🐛 Troubleshooting

### Problem: "OpenAI API key not found"
**Lösung**: Überprüfe, ob die `.env` Datei existiert und `OPENAI_API_KEY` gesetzt ist.

### Problem: "ChromaDB collection error"
**Lösung**: Lösche das `data/chroma_db` Verzeichnis und starte neu.

### Problem: "PDF kann nicht geladen werden"
**Lösung**: Stelle sicher, dass die PDF-Datei nicht beschädigt ist und nicht passwortgeschützt.

### Problem: Docker Container startet nicht
**Lösung**:
```bash
docker-compose logs
docker-compose down -v
docker-compose up --build
```

## 🔒 Sicherheit

- **API Keys**: Niemals API Keys in Git committen
- **Secrets**: Verwende `.env` für sensitive Daten
- **Input Validation**: PDFs werden auf Gültigkeit geprüft
- **Error Handling**: Graceful degradation bei Fehlern

## 📝 Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert.

## 🤝 Contributing

Contributions sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Öffne einen Pull Request

## 📧 Support

Bei Fragen oder Problemen:
- Öffne ein Issue im Repository
- Kontaktiere das Entwicklungsteam

## 🎓 Credits

Entwickelt mit:
- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://openai.com/)

---

**Made with ❤️ for students**
