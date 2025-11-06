# Quick Start Guide

Schnellanleitung zum Starten des Studien-RAG-Assistenten in 5 Minuten.

## Voraussetzungen

- Python 3.11 oder höher
- OpenAI API Key ([hier erhalten](https://platform.openai.com/api-keys))

## 🚀 Installation & Start (Lokale Entwicklung)

### 1. Virtuelle Umgebung erstellen

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Umgebungsvariablen konfigurieren

```bash
# Kopiere die Vorlage
cp .env.example .env

# Bearbeite .env und füge deinen OpenAI API Key hinzu
# OPENAI_API_KEY=sk-...
```

Windows PowerShell:
```powershell
Copy-Item .env.example .env
notepad .env
```

### 4. Anwendung starten

```bash
python run.py
```

Die Anwendung öffnet sich automatisch im Browser unter http://localhost:8501

## 🐳 Docker (Schnellste Methode)

### 1. .env Datei erstellen

```bash
cp .env.example .env
# Füge deinen OpenAI API Key hinzu
```

### 2. Container starten

```bash
cd docker
docker-compose up -d
```

### 3. Browser öffnen

Öffne http://localhost:8501

### Container verwalten

```bash
# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down

# Container neu bauen
docker-compose up --build
```

## 📚 Erste Schritte

### 1. PDF hochladen

1. Klicke in der Seitenleiste auf "PDF-Dateien auswählen"
2. Wähle deine Vorlesungs-PDFs aus
3. Klicke "Dokumente verarbeiten"
4. Warte, bis die Verarbeitung abgeschlossen ist

### 2. Fragen stellen

Beispielfragen:
- "Was sind die Hauptthemen in Kapitel 3?"
- "Erkläre mir das Konzept von [Begriff]"
- "Welche Formeln werden für [Thema] verwendet?"
- "Fasse die wichtigsten Punkte zu [Thema] zusammen"

### 3. Quellenangaben prüfen

- Jede Antwort enthält automatisch Quellenangaben
- Klicke auf "Quellenangaben" um Details zu sehen
- Sieh dir die relevanten Textausschnitte an

## ⚙️ Konfiguration

Die wichtigsten Einstellungen in `.env`:

```bash
# Erforderlich
OPENAI_API_KEY=sk-...

# Optional - für bessere Qualität
LLM_MODEL=gpt-4o-mini          # Oder gpt-4 für höhere Qualität
TEMPERATURE=0.2                # 0.0 = faktisch, 2.0 = kreativ

# Optional - für große Dokumente
CHUNK_SIZE=1500                # Größere Chunks für längeren Kontext
RETRIEVAL_K=6                  # Mehr Quellen pro Antwort
```

## 🔧 Entwicklung

### Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage Report
pytest --cov=src --cov-report=html
```

### Code formatieren

```bash
# Mit Makefile (empfohlen)
make format

# Manuell
black src/ tests/
isort src/ tests/
```

### Pre-commit Hooks installieren

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## 🐛 Troubleshooting

### Problem: "OpenAI API key not found"

```bash
# Stelle sicher, dass .env existiert
cat .env

# Überprüfe, ob OPENAI_API_KEY gesetzt ist
# Windows PowerShell
Get-Content .env | Select-String OPENAI

# Linux/macOS
grep OPENAI_API_KEY .env
```

### Problem: "Module not found"

```bash
# Stelle sicher, dass virtuelle Umgebung aktiv ist
# Sollte (.venv) im Prompt zeigen

# Dependencies erneut installieren
pip install -r requirements.txt
```

### Problem: "ChromaDB error"

```bash
# Lösche ChromaDB und starte neu
rm -rf data/chroma_db/*
python run.py
```

### Problem: Port 8501 bereits belegt

```bash
# Verwende einen anderen Port
streamlit run src/ui.py --server.port=8502
```

## 💡 Tipps für beste Ergebnisse

1. **PDF-Qualität**: Verwende text-basierte PDFs (keine gescannten Bilder)
2. **Chunk-Size**: Passe `CHUNK_SIZE` an deine Dokumente an
   - Größere Werte (1500-2000) für längeren Kontext
   - Kleinere Werte (500-1000) für präzisere Antworten
3. **Retrieval-K**: Erhöhe `RETRIEVAL_K` für umfassendere Antworten
4. **Temperature**: Verwende niedrige Werte (0.1-0.3) für faktische Antworten
5. **Modell**: Verwende `gpt-4` für höhere Qualität (teurer)

## 📖 Weitere Ressourcen

- [Vollständige Dokumentation](README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## 🆘 Support

Bei Problemen:
1. Prüfe die [Troubleshooting-Sektion](#-troubleshooting)
2. Lies die [vollständige Dokumentation](README.md)
3. Öffne ein [Issue](https://github.com/yourusername/studien-rag-assistent/issues)

---

**Viel Erfolg beim Studieren! 🎓**
