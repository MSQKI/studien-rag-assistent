# 🚀 Study Platform - Quick Start

## Schnellstart in 3 Schritten

### 1. Voraussetzungen prüfen
```bash
# Docker installiert?
docker --version
docker-compose --version

# Git installiert?
git --version
```

### 2. API Key konfigurieren
```bash
# .env Datei erstellen
cp .env.example .env

# Öffne .env und füge deinen OpenAI API Key ein:
# OPENAI_API_KEY=sk-...
```

### 3. Alle Services starten
```bash
# In das docker Verzeichnis wechseln
cd docker

# Alle Services starten
docker-compose -f docker-compose-full.yml up -d

# Logs verfolgen (optional)
docker-compose -f docker-compose-full.yml logs -f
```

## ✅ Fertig! Services sind verfügbar:

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

## 🎯 Erste Schritte

### 1. Öffne das Frontend
```bash
open http://localhost:3000
```

### 2. Lade ein PDF hoch
- Gehe zu "RAG Chat"
- Klicke auf "PDF hochladen"
- Wähle eine PDF-Datei aus

### 3. Stelle Fragen
- Warte bis das PDF verarbeitet ist
- Stelle Fragen im Chat
- Erhalte Antworten mit Quellenangaben

### 4. Lerne mit Karteikarten
- Gehe zu "Karteikarten"
- Flashcards wurden automatisch generiert
- Lerne mit Spaced Repetition

## 🛠️ Nützliche Befehle

```bash
# Services Status prüfen
docker-compose -f docker-compose-full.yml ps

# Logs anzeigen
docker-compose -f docker-compose-full.yml logs -f backend
docker-compose -f docker-compose-full.yml logs -f neo4j
docker-compose -f docker-compose-full.yml logs -f frontend

# Services neustarten
docker-compose -f docker-compose-full.yml restart backend

# Services stoppen
docker-compose -f docker-compose-full.yml down

# Services stoppen und Volumes löschen (ACHTUNG: Alle Daten!)
docker-compose -f docker-compose-full.yml down -v

# Neu bauen
docker-compose -f docker-compose-full.yml build --no-cache
docker-compose -f docker-compose-full.yml up -d
```

## 🧪 API testen

```bash
# Health Check
curl http://localhost:8000/health

# Flashcard Statistiken
curl http://localhost:8000/api/flashcards/stats/overview

# RAG Statistiken
curl http://localhost:8000/api/rag/stats

# Neo4j Konzepte
curl http://localhost:8000/api/graph/concepts
```

## 🐛 Troubleshooting

### Backend startet nicht
```bash
# Logs prüfen
docker-compose -f docker-compose-full.yml logs backend

# Container neu starten
docker-compose -f docker-compose-full.yml restart backend
```

### Neo4j Connection Error
```bash
# Neo4j Status
docker-compose -f docker-compose-full.yml ps neo4j

# Neo4j Logs
docker-compose -f docker-compose-full.yml logs neo4j

# Warte 30 Sekunden, Neo4j braucht Zeit zum Starten
```

### Frontend zeigt Fehler
```bash
# Prüfe ob Backend läuft
curl http://localhost:8000/health

# Frontend Logs
docker-compose -f docker-compose-full.yml logs frontend

# Frontend neu bauen
docker-compose -f docker-compose-full.yml build frontend --no-cache
docker-compose -f docker-compose-full.yml up -d frontend
```

### Ports bereits belegt
```bash
# Prüfe welcher Prozess den Port nutzt
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Linux/Mac:
lsof -i :8000
lsof -i :3000

# Ändere Ports in docker-compose-full.yml wenn nötig
```

## 📊 Entwicklung

### Frontend Development
```bash
cd frontend
npm install
npm run dev
# Frontend läuft auf http://localhost:5173 (Vite Dev Server)
```

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📚 Weitere Dokumentation

- **ARCHITECTURE.md** - System-Architektur
- **IMPLEMENTATION.md** - Implementierungs-Details
- **API Docs** - http://localhost:8000/api/docs

## 🎉 Viel Erfolg beim Lernen!

Bei Fragen oder Problemen:
1. Prüfe die Logs
2. Siehe Troubleshooting-Abschnitt
3. Öffne ein Issue auf GitHub
