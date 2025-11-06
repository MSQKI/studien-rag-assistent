# Quick Start - Study Platform v2.0

Eine umfassende Lernplattform mit RAG, Voice Buddy, Knowledge Graph und Flashcards.

## 🚀 In 5 Minuten starten

### Voraussetzungen
- Docker & Docker Compose
- OpenAI API Key
- 8GB RAM empfohlen

### 1. Repository klonen (falls noch nicht geschehen)
```bash
git clone https://github.com/your-repo/studien-rag-assistent.git
cd studien-rag-assistent
```

### 2. Umgebungsvariablen konfigurieren
```bash
# .env Datei erstellen
cp .env.example .env

# OpenAI API Key eintragen
# Öffne .env und füge hinzu:
# OPENAI_API_KEY=sk-...
```

### 3. Alle Services starten
```bash
cd docker
docker-compose -f docker-compose-full.yml up -d
```

### 4. Warten bis Services bereit sind
```bash
# Backend Health Check
curl http://localhost:8000/health

# Neo4j Browser öffnen
# http://localhost:7474
# Login: neo4j / studyplatform2024
```

### 5. API testen
```bash
# API Dokumentation öffnen
open http://localhost:8000/api/docs

# Oder mit curl
curl http://localhost:8000/api/flashcards/stats/overview
```

---

## 📍 Service URLs

| Service | URL | Beschreibung |
|---------|-----|--------------|
| **Backend API** | http://localhost:8000 | FastAPI Backend |
| **API Docs** | http://localhost:8000/api/docs | Swagger UI |
| **Neo4j Browser** | http://localhost:7474 | Graph Datenbank |
| **Streamlit UI** | http://localhost:8501 | Original RAG Interface |

---

## 🎯 Erste Schritte

### Flashcard erstellen
```bash
curl -X POST http://localhost:8000/api/flashcards \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Mathematik",
    "question": "Was ist die Ableitung von x²?",
    "answer": "2x",
    "difficulty": 2,
    "tags": ["Analysis", "Ableitungen"]
  }'
```

### Knowledge Graph erkunden
```bash
# Konzepte auflisten
curl http://localhost:8000/api/graph/concepts

# Im Neo4j Browser (http://localhost:7474):
MATCH (n:Concept) RETURN n LIMIT 10
```

### RAG Query (wenn Dokumente vorhanden)
```bash
curl -X POST http://localhost:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Was sind die wichtigsten Konzepte?"
  }'
```

---

## 🛠️ Entwicklung

### Backend Development Mode
```bash
# Backend ohne Docker starten
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Neo4j im Docker lassen
docker run -d -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/studyplatform2024 \
  neo4j:5-community

# Backend mit Hot Reload
uvicorn app.main:app --reload --port 8000
```

### Logs anzeigen
```bash
cd docker
docker-compose -f docker-compose-full.yml logs -f backend
docker-compose -f docker-compose-full.yml logs -f neo4j
```

### Services neu starten
```bash
docker-compose -f docker-compose-full.yml restart backend
docker-compose -f docker-compose-full.yml restart neo4j
```

---

## 🧪 Testing

### API Tests mit Swagger UI
1. Öffne http://localhost:8000/api/docs
2. Klicke auf einen Endpoint (z.B. `POST /api/flashcards`)
3. Klicke "Try it out"
4. Fülle die Parameter aus
5. Klicke "Execute"

### Beispiel: Vollständiger Workflow
```bash
# 1. Flashcard erstellen
CARD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/flashcards \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test",
    "question": "Was ist 2+2?",
    "answer": "4",
    "difficulty": 1
  }')

# ID extrahieren
CARD_ID=$(echo $CARD_RESPONSE | jq -r '.id')

# 2. Nächste fällige Karte abrufen
curl http://localhost:8000/api/flashcards/next/due

# 3. Antwort aufzeichnen
curl -X POST http://localhost:8000/api/flashcards/answer \
  -H "Content-Type: application/json" \
  -d "{
    \"flashcard_id\": \"$CARD_ID\",
    \"correct\": true,
    \"time_spent_seconds\": 30
  }"

# 4. Statistiken abrufen
curl http://localhost:8000/api/flashcards/stats/overview
```

---

## 📊 Features Übersicht

### ✅ Vollständig implementiert
- ✅ FastAPI Backend mit allen Routen
- ✅ Voice Study Buddy (OpenAI Realtime API)
- ✅ Flashcard System (SQLite + Spaced Repetition)
- ✅ Knowledge Graph (Neo4j + Entity Extraction)
- ✅ Docker Compose Setup
- ✅ RAG Services (migriert)

### ⏳ Integration erforderlich
- ⏳ RAG API Routes mit Services verbinden
- ⏳ Document Upload Pipeline
- ⏳ Voice WebSocket mit Flashcards verbinden
- ⏳ Auto-Flashcard Generation
- ⏳ Graph Visualization Endpoints

### 🎨 Frontend (geplant)
- 🎨 React Dashboard
- 🎨 Voice Interface UI
- 🎨 Graph Visualization (D3.js/Cytoscape)
- 🎨 Flashcard Study Interface

---

## 🐛 Troubleshooting

### "Connection refused" beim Backend
```bash
# Services Status prüfen
docker-compose -f docker/docker-compose-full.yml ps

# Backend neu starten
docker-compose -f docker/docker-compose-full.yml restart backend
```

### Neo4j startet nicht
```bash
# Logs prüfen
docker-compose -f docker/docker-compose-full.yml logs neo4j

# Volumes löschen und neu starten
docker-compose -f docker/docker-compose-full.yml down -v
docker-compose -f docker/docker-compose-full.yml up -d
```

### "OPENAI_API_KEY not found"
```bash
# .env Datei prüfen
cat .env | grep OPENAI_API_KEY

# Wenn leer, API Key hinzufügen:
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Services neu starten
docker-compose -f docker/docker-compose-full.yml restart
```

---

## 📚 Weitere Dokumentation

- **ARCHITECTURE.md** - Vollständige System-Architektur
- **IMPLEMENTATION.md** - Detaillierte Implementierungs-Dokumentation
- **API Docs** - http://localhost:8000/api/docs

---

## 🤝 Support

Bei Problemen oder Fragen:
1. Prüfe die Logs: `docker-compose logs`
2. Siehe IMPLEMENTATION.md für Details
3. Öffne ein Issue auf GitHub

---

**Version:** 2.0.0
**Letzte Aktualisierung:** 2025-01-06
