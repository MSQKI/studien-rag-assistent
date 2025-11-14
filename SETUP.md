# 🚀 Setup-Anleitung - Studien-RAG-Assistent

Komplette Schritt-für-Schritt Anleitung zur Installation und Inbetriebnahme.

---

## 📋 Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Installation](#installation)
3. [Konfiguration](#konfiguration)
4. [Erste Schritte](#erste-schritte)
5. [Lokale Entwicklung](#lokale-entwicklung)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Voraussetzungen

### Erforderliche Software

| Software | Version | Download |
|----------|---------|----------|
| **Docker** | 20.10+ | [docker.com](https://www.docker.com/get-started) |
| **Docker Compose** | 2.0+ | Inklusive in Docker Desktop |
| **OpenAI API Key** | - | [platform.openai.com](https://platform.openai.com/api-keys) |

### Optional (nur für lokale Entwicklung)

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **Git** | 2.0+ | [git-scm.com](https://git-scm.com/) |

### System-Anforderungen

- **RAM**: Mindestens 8 GB (16 GB empfohlen)
- **Speicherplatz**: 5-10 GB frei
- **Betriebssystem**: Windows 10/11, macOS 10.15+, oder Linux
- **Internet**: Für OpenAI API-Zugriff

---

## 📥 Installation

### Schritt 1: Repository herunterladen

**Option A: Mit Git (empfohlen)**
```bash
git clone https://github.com/dein-username/studien-rag-assistent.git
cd studien-rag-assistent
```

**Option B: Als ZIP herunterladen**
1. Gehe zu: https://github.com/dein-username/studien-rag-assistent
2. Klicke auf **"Code"** → **"Download ZIP"**
3. Entpacke die ZIP-Datei
4. Öffne Terminal/CMD im entpackten Ordner

### Schritt 2: Docker prüfen

**Prüfe ob Docker läuft:**
```bash
docker --version
docker-compose --version
```

**Erwartete Ausgabe:**
```
Docker version 24.0.x
Docker Compose version 2.x.x
```

**Falls Docker nicht läuft:**
- Windows/Mac: Starte Docker Desktop
- Linux: `sudo systemctl start docker`

---

## ⚙️ Konfiguration

### Schritt 3: OpenAI API Key einrichten

**3.1 API Key besorgen:**
1. Gehe zu: https://platform.openai.com/api-keys
2. Logge dich ein (oder erstelle Account)
3. Klicke **"Create new secret key"**
4. Kopiere den Key (beginnt mit `sk-...`)

**3.2 `.env` Datei erstellen:**

**Windows:**
```bash
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

**3.3 API Key einfügen:**

Öffne `.env` und ändere:
```env
OPENAI_API_KEY=sk-...hier-deinen-echten-key-einfügen...
```

**Beispiel:**
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...

# LLM Settings (kann meist so bleiben)
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
TEMPERATURE=0.2
MAX_TOKENS=2000

# Document Processing (kann meist so bleiben)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4

# Neo4j (kann meist so bleiben)
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=studyplatform2024
```

**Wichtig:**
- ✅ Speichere die Datei
- ✅ Prüfe dass der Key vollständig ist
- ⚠️ Teile den Key niemals öffentlich!

---

## 🎬 Erste Schritte

### Schritt 4: Anwendung starten

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Was passiert jetzt:**
```
✓ Docker Container werden gestartet...
  - Backend (FastAPI)
  - Frontend (React)
  - Neo4j (Graph Database)

✓ Images werden heruntergeladen (beim ersten Mal ~2-5 Min)
✓ Datenbanken werden initialisiert
✓ Dienste starten...

Fertig! 🎉
```

**Startup-Zeit:**
- **Erstes Mal**: 3-5 Minuten (Downloads)
- **Danach**: 30-60 Sekunden

### Schritt 5: Überprüfen ob alles läuft

**5.1 Öffne im Browser:**
```
Frontend:    http://localhost:3000
Backend API: http://localhost:8000/docs
Neo4j UI:    http://localhost:7474
```

**5.2 Health Check:**
```bash
curl http://localhost:8000/health
```

**Erwartete Antwort:**
```json
{"status": "healthy"}
```

**5.3 Container Status prüfen:**
```bash
docker ps
```

**Erwartete Container:**
- `studien-rag-backend`
- `studien-rag-frontend`
- `studien-rag-neo4j`

---

## 📚 Anwendung nutzen

### Schritt 6: Erstes Dokument hochladen

1. **Öffne**: http://localhost:3000
2. Klicke auf **"Datenverwaltung"** (obere Navigation)
3. Gehe zum Tab **"Dokumente"**
4. Klicke **"Dokument hochladen"**
5. Wähle ein **PDF-Dokument** (z.B. Vorlesungsskript)
6. Warte ~30 Sekunden (Progress Bar wird angezeigt)
7. ✅ Fertig! Das Dokument ist jetzt durchsuchbar

**Unterstützte Formate:**
- ✅ PDF (empfohlen)
- ✅ Mit Text, Tabellen, Bildern (OCR)

### Schritt 7: Erste Frage stellen

1. Gehe zu **"RAG Chat"**
2. Stelle eine Frage zu deinem Dokument:
   - *"Was sind die Hauptthemen?"*
   - *"Erkläre mir [Konzept]"*
   - *"Fasse Kapitel 3 zusammen"*
3. ✅ Du erhältst eine Antwort mit **Quellenangaben**!

**Tipp:** Klicke auf das 🎤 Mikrofon für Spracheingabe!

### Schritt 8: Knowledge Graph erkunden

1. Gehe zu **"Knowledge Graph"**
2. Siehst alle **automatisch extrahierten Konzepte**
3. Klicke auf **Nodes** für Details
4. Nutze **Zoom** und **Suche**

### Schritt 9: Mit Karteikarten lernen

1. Gehe zu **"Karteikarten"**
2. Automatisch generierte Karten werden angezeigt
3. Klicke Karte zum **Umdrehen**
4. Bewerte: **"Ja"** (gewusst) oder **"Nein"** (nicht gewusst)
5. System merkt sich **Wiederholungsintervalle**!

---

## 🛠️ Lokale Entwicklung

Falls du am Code entwickeln möchtest:

### Backend (FastAPI)

```bash
# 1. In backend-Verzeichnis wechseln
cd backend

# 2. Virtual Environment erstellen
python -m venv .venv

# 3. Aktivieren
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Dependencies installieren
pip install -r requirements.txt

# 5. Backend starten
uvicorn app.main:app --reload --port 8000
```

**Backend läuft auf:** http://localhost:8000

### Frontend (React)

```bash
# 1. In frontend-Verzeichnis wechseln
cd frontend

# 2. Dependencies installieren
npm install

# 3. Frontend starten
npm run dev
```

**Frontend läuft auf:** http://localhost:3000

### Tests ausführen

**Frontend (Playwright E2E):**
```bash
cd frontend
npx playwright test
npx playwright show-report  # Report anzeigen
```

**Backend (pytest):**
```bash
cd backend
pytest
pytest --cov=app  # Mit Coverage
```

---

## 🛑 Anwendung stoppen

**Windows:**
```bash
stop.bat
```

**macOS/Linux:**
```bash
./stop.sh
```

**Oder manuell:**
```bash
docker-compose -f docker-compose-full.yml down
```

**Daten bleiben erhalten!** Alle Dokumente, Karteikarten und der Graph sind persistent gespeichert.

---

## 🐛 Troubleshooting

### Problem 1: "Port already in use"

**Fehler:**
```
Error: bind: address already in use
```

**Lösung:**
```bash
# Finde Prozess auf Port 3000 (Frontend)
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Oder ändere Port in docker-compose-full.yml
```

### Problem 2: "OPENAI_API_KEY not set"

**Fehler:**
```
ValueError: OPENAI_API_KEY is required
```

**Lösung:**
1. Prüfe ob `.env` existiert: `ls -la .env`
2. Öffne `.env` und prüfe ob Key gesetzt ist
3. Stelle sicher dass **kein Leerzeichen** um das `=` ist
4. Starte neu: `stop.bat && start.bat`

### Problem 3: Neo4j startet nicht

**Fehler:**
```
Neo4j connection failed
```

**Lösung:**
```bash
# 1. Warte 30-60 Sekunden nach Start
# Neo4j braucht Zeit zum Hochfahren

# 2. Prüfe Neo4j Logs
docker logs studien-rag-neo4j

# 3. Neo4j UI öffnen
http://localhost:7474
# Login: neo4j / studyplatform2024

# 4. Falls weiterhin Probleme:
docker-compose -f docker-compose-full.yml restart neo4j
```

### Problem 4: Frontend zeigt "Failed to fetch"

**Lösung:**
1. **Prüfe Backend:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Prüfe CORS:**
   - Öffne Browser Console (F12)
   - Suche nach CORS-Fehlern

3. **Prüfe `.env`:**
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Neustart:**
   ```bash
   docker-compose -f docker-compose-full.yml restart backend
   ```

### Problem 5: Dokument-Upload schlägt fehl

**Lösung:**
1. **Prüfe Dateigröße**: Max. 50 MB
2. **Prüfe Format**: Nur PDF unterstützt
3. **Prüfe Logs:**
   ```bash
   docker logs studien-rag-backend
   ```
4. **Prüfe Speicherplatz:**
   ```bash
   df -h  # Linux/Mac
   ```

### Problem 6: ChromaDB Fehler

**Fehler:**
```
ChromaDB connection failed
```

**Lösung:**
```bash
# 1. Stoppe Anwendung
./stop.sh

# 2. Lösche ChromaDB (Achtung: Daten gehen verloren!)
rm -rf data/chroma_db/

# 3. Starte neu
./start.sh
```

### Problem 7: Docker läuft nicht

**Lösung:**
- **Windows/Mac**: Starte Docker Desktop
- **Linux**: `sudo systemctl start docker`
- **Prüfe Status**: `docker info`

---

## 📊 Logs & Debugging

### Container Logs anzeigen

**Alle Logs:**
```bash
docker-compose -f docker-compose-full.yml logs -f
```

**Nur Backend:**
```bash
docker logs -f studien-rag-backend
```

**Nur Neo4j:**
```bash
docker logs -f studien-rag-neo4j
```

### Container neu starten

```bash
# Einzelner Container
docker-compose -f docker-compose-full.yml restart backend

# Alle Container
docker-compose -f docker-compose-full.yml restart
```

### Komplett neu aufsetzen

**Achtung: Löscht alle Daten!**
```bash
docker-compose -f docker-compose-full.yml down -v
rm -rf data/
docker-compose -f docker-compose-full.yml up -d
```

---

## 🔄 Updates

### Neue Version pullen

```bash
git pull origin main
docker-compose -f docker-compose-full.yml down
docker-compose -f docker-compose-full.yml up -d --build
```

---

## 📞 Hilfe & Support

**Problem nicht gelöst?**

1. **Prüfe Logs**: `docker-compose logs`
2. **Suche in Issues**: https://github.com/dein-username/studien-rag-assistent/issues
3. **Öffne Issue**: Beschreibe Problem + Logs + System-Info

**System-Info sammeln:**
```bash
# Windows
systeminfo

# macOS/Linux
uname -a
docker --version
docker-compose --version
```

---

## ✅ Checkliste: Setup erfolgreich?

- [ ] Docker läuft
- [ ] `.env` existiert mit gültigem API Key
- [ ] `docker ps` zeigt 3 Container
- [ ] http://localhost:3000 öffnet Frontend
- [ ] http://localhost:8000/docs öffnet API Docs
- [ ] Dokument hochladen funktioniert
- [ ] RAG Chat antwortet auf Fragen
- [ ] Knowledge Graph zeigt Konzepte
- [ ] Karteikarten werden angezeigt

**Alle Punkte ✅?** Glückwunsch! 🎉 Du bist bereit!

---

**Made with ❤️ for students**

Bei Fragen: [Issue öffnen](https://github.com/dein-username/studien-rag-assistent/issues)
