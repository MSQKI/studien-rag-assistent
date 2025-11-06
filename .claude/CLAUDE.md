# Studien-RAG-Assistent

## Projekt-Übersicht
Ein RAG-System für Studierende zum Durchsuchen und Befragen von Vorlesungsunterlagen.

## Technische Standards
- Verwende Type Hints in allen Python-Dateien
- Implementiere proper error handling mit try-except
- Nutze async/await wo möglich für bessere Performance
- Chunk-Size: 1000 Zeichen mit 200 Overlap
- Verwende RecursiveCharacterTextSplitter für bessere Semantik

## OpenAI Integration
- Model für Chat: gpt-4o-mini
- Model für Embeddings: text-embedding-3-small
- Temperature: 0.2 für faktische Antworten
- Max tokens: 2000

## Docker & Deployment
- Multi-stage build für kleinere Images
- Volume mounts für persistente Daten
- Health checks implementieren

## Entwicklungsrichtlinien
- Alle neuen Features mit Tests versehen
- Dokumentation in Docstrings
- Type hints für alle Funktionen
- Logging statt print statements
- Environment variables für Konfiguration

## Architektur
```
User Interface (Streamlit)
    ↓
RAG Chain (LangChain)
    ↓
Vector Store (ChromaDB) ←→ Document Processor
    ↓
OpenAI API (Embeddings & LLM)
```

## Best Practices
- Chunking: RecursiveCharacterTextSplitter mit semantischen Boundaries
- Metadata: Immer Seitenzahl und Dokumentname tracken
- Citations: Jede Antwort mit Quellenangaben versehen
- Error Handling: Graceful degradation, keine crashes
- Performance: Batch processing für große Dokumente
