# Contributing to Studien-RAG-Assistent

Vielen Dank für dein Interesse, zum Studien-RAG-Assistenten beizutragen!

## 🚀 Schnellstart für Entwickler

### 1. Repository Setup

```bash
# Repository klonen
git clone <repository-url>
cd studien-rag-assistent

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # oder .venv\Scripts\activate auf Windows

# Dev-Dependencies installieren
pip install -r requirements-dev.txt

# Pre-commit hooks installieren
pre-commit install
```

### 2. .env konfigurieren

```bash
cp .env.example .env
# Trage deinen OpenAI API Key ein
```

### 3. Tests ausführen

```bash
pytest
```

## 📝 Entwicklungsrichtlinien

### Code Style

Wir verwenden diese Tools für konsistente Code-Qualität:

- **Black**: Code-Formatierung (Line length: 100)
- **isort**: Import-Sortierung
- **flake8**: Linting
- **mypy**: Type Checking
- **bandit**: Security Scanning

Pre-commit hooks sorgen automatisch für Einhaltung dieser Standards.

### Code Formatieren

```bash
# Alle Dateien formatieren
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Tests

- Schreibe Tests für alle neuen Features
- Minimum Code Coverage: 80%
- Tests sollten unabhängig voneinander laufen

```bash
# Alle Tests
pytest

# Mit Coverage Report
pytest --cov=src --cov-report=html

# Nur Unit Tests
pytest -m unit

# Spezifische Test-Datei
pytest tests/test_config.py
```

### Dokumentation

- Alle öffentlichen Funktionen brauchen Docstrings
- Format: Google Style Python Docstrings
- Type Hints für alle Parameter und Return Values

Beispiel:

```python
def process_document(file_path: Path, chunk_size: int = 1000) -> List[Document]:
    """
    Process a PDF document and split it into chunks.

    Args:
        file_path: Path to the PDF file
        chunk_size: Size of text chunks in characters

    Returns:
        List of processed document chunks

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If chunk_size is invalid
    """
    pass
```

## 🔄 Contribution Workflow

### 1. Issue erstellen

Erstelle zunächst ein Issue für:
- Bug Reports
- Feature Requests
- Verbesserungsvorschläge

### 2. Branch erstellen

```bash
git checkout -b feature/dein-feature-name
# oder
git checkout -b fix/bug-beschreibung
```

Branch-Naming Convention:
- `feature/`: Neue Features
- `fix/`: Bug Fixes
- `docs/`: Dokumentation
- `refactor/`: Code Refactoring
- `test/`: Test-Ergänzungen

### 3. Code schreiben

- Folge den Code Style Richtlinien
- Schreibe Tests
- Aktualisiere Dokumentation
- Committe regelmäßig

### 4. Commit Messages

Verwende aussagekräftige Commit Messages:

```
<type>: <kurze Beschreibung>

<längere Beschreibung falls nötig>

Fixes #<issue-nummer>
```

Types:
- `feat`: Neue Features
- `fix`: Bug Fixes
- `docs`: Dokumentation
- `style`: Code-Formatierung
- `refactor`: Code Refactoring
- `test`: Tests
- `chore`: Build/Config Änderungen

Beispiel:
```
feat: Add support for multiple PDF uploads

Implemented batch processing for PDF uploads with progress bar.
Users can now upload and process multiple PDFs simultaneously.

Fixes #42
```

### 5. Tests ausführen

```bash
# Alle Tests
pytest

# Pre-commit checks
pre-commit run --all-files
```

### 6. Pull Request erstellen

1. Push deinen Branch: `git push origin feature/dein-feature`
2. Öffne einen Pull Request auf GitHub
3. Beschreibe deine Änderungen ausführlich
4. Verlinke relevante Issues
5. Warte auf Code Review

## 🐛 Bug Reports

Ein guter Bug Report enthält:

- **Beschreibung**: Was ist das Problem?
- **Reproduktion**: Schritte zum Reproduzieren
- **Erwartetes Verhalten**: Was sollte passieren?
- **Tatsächliches Verhalten**: Was passiert stattdessen?
- **Environment**: Python-Version, OS, etc.
- **Logs**: Relevante Error-Messages

Template:

```markdown
## Beschreibung
[Kurze Beschreibung des Bugs]

## Reproduktion
1. Schritt 1
2. Schritt 2
3. ...

## Erwartetes Verhalten
[Was sollte passieren]

## Tatsächliches Verhalten
[Was tatsächlich passiert]

## Environment
- Python: [Version]
- OS: [z.B. Windows 11]
- Dependencies: [relevante Package-Versionen]

## Logs
```
[Error Logs]
```
```

## 💡 Feature Requests

Feature Requests sollten enthalten:

- **Use Case**: Warum wird das Feature benötigt?
- **Beschreibung**: Was soll implementiert werden?
- **Beispiele**: Konkrete Anwendungsfälle
- **Alternativen**: Andere Lösungsansätze?

## 🏗️ Architektur

### Projekt-Struktur

```
src/
├── config.py              # Zentrale Konfiguration
├── document_processor.py  # PDF-Verarbeitung
├── vector_store.py        # ChromaDB Integration
├── rag_chain.py          # RAG Pipeline
└── ui.py                 # Streamlit UI
```

### Wichtige Konzepte

1. **Settings**: Zentrale Konfiguration via Pydantic
2. **Lazy Loading**: Ressourcen werden bei Bedarf geladen
3. **Error Handling**: Graceful degradation
4. **Logging**: Strukturiertes Logging mit loguru

## 📚 Weiterführende Ressourcen

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)

## ❓ Fragen?

Bei Fragen:
- Öffne ein Issue
- Kontaktiere das Team

Vielen Dank für deine Contribution! 🙏
