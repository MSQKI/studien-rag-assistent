# 🐳 Docker Setup - Vollständige Anleitung

Diese Anleitung zeigt dir Schritt-für-Schritt, wie du den Studien-RAG-Assistenten mit Docker betreibst.

## 📋 Voraussetzungen

### Windows
- **Docker Desktop für Windows**
  - Download: https://www.docker.com/products/docker-desktop/
  - **Wichtig**: WSL 2 wird benötigt (wird bei Installation automatisch eingerichtet)

### macOS
- **Docker Desktop für Mac**
  - Download: https://www.docker.com/products/docker-desktop/

### Linux
- **Docker Engine** + **Docker Compose**
  ```bash
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install docker.io docker-compose

  # Starte Docker
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

---

## ✅ Schritt 1: Docker Installation prüfen

Nach der Installation von Docker Desktop:

```bash
# Docker-Version prüfen
docker --version

# Sollte zeigen: Docker version 24.x.x oder höher

# Docker Compose prüfen
docker-compose --version

# Sollte zeigen: Docker Compose version v2.x.x oder höher
```

**Windows**: Stelle sicher, dass Docker Desktop läuft (Icon in der Taskleiste)

---

## ✅ Schritt 2: .env Datei erstellen

Die `.env` Datei enthält deine Konfiguration (insbesondere den OpenAI API Key).

### Option A: Kopieren und bearbeiten

```bash
# Im Projekt-Verzeichnis
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

### Option B: Manuell erstellen

Erstelle eine Datei namens `.env` im Projekt-Root mit folgendem Inhalt:

```env
# OpenAI API Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-dein-api-key-hier

# Optional - Model Configuration
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
TEMPERATURE=0.2
MAX_TOKENS=2000

# Optional - Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Optional - Application Settings
LOG_LEVEL=INFO
```

**⚠️ WICHTIG:** Trage deinen echten OpenAI API Key ein!

---

## ✅ Schritt 3: Docker Image bauen

```bash
# Navigiere zum docker/ Verzeichnis
cd docker

# Docker Image bauen (dauert 5-10 Minuten beim ersten Mal)
docker-compose build
```

**Was passiert:**
- ✅ Python 3.11 Base Image wird heruntergeladen
- ✅ Dependencies aus `requirements.txt` werden installiert
- ✅ Anwendungscode wird kopiert
- ✅ Multi-stage Build optimiert die Image-Größe

**Erwartete Ausgabe:**
```
[+] Building 234.5s (12/12) FINISHED
 => [internal] load build definition
 => => transferring dockerfile
 => [internal] load .dockerignore
 => [stage-1 1/6] FROM docker.io/library/python:3.11-slim
 ...
 => exporting to image
 => => naming to docker.io/library/docker-rag-assistant
```

---

## ✅ Schritt 4: Container starten

```bash
# Container im Hintergrund starten
docker-compose up -d
```

**Flags:**
- `-d` = detached mode (läuft im Hintergrund)

**Erwartete Ausgabe:**
```
[+] Running 2/2
 ✔ Network docker_rag-network  Created
 ✔ Container studien-rag-assistent  Started
```

---

## ✅ Schritt 5: Container-Status prüfen

```bash
# Laufende Container anzeigen
docker-compose ps

# Sollte zeigen:
NAME                     STATUS    PORTS
studien-rag-assistent    Up        0.0.0.0:8501->8501/tcp
```

---

## ✅ Schritt 6: Logs anschauen

```bash
# Live-Logs anzeigen
docker-compose logs -f

# Nur letzte 50 Zeilen
docker-compose logs --tail=50

# Logs eines bestimmten Services
docker-compose logs rag-assistant
```

**Erfolgreiche Logs sollten zeigen:**
```
studien-rag-assistent | You can now view your Streamlit app in your browser.
studien-rag-assistent | URL: http://0.0.0.0:8501
studien-rag-assistent | INFO:src.rag_chain:Initialized RAG Assistant
studien-rag-assistent | INFO:src.vector_store:Initialized OpenAI embeddings
```

**Mit `Ctrl+C` beenden (Container läuft weiter im Hintergrund!)**

---

## ✅ Schritt 7: Anwendung öffnen

Öffne deinen Browser und navigiere zu:

```
http://localhost:8501
```

🎉 **Die Anwendung läuft!**

---

## 🔧 Docker-Befehle Cheat Sheet

### Container verwalten

```bash
# Container starten
docker-compose up -d

# Container stoppen
docker-compose down

# Container neu starten
docker-compose restart

# Container stoppen UND Volumes löschen (ACHTUNG: Daten gehen verloren!)
docker-compose down -v
```

### Logs und Debugging

```bash
# Live-Logs
docker-compose logs -f

# Fehlersuche: In Container einloggen
docker-compose exec rag-assistant /bin/bash

# Im Container dann:
ls -la
python --version
env | grep OPENAI
```

### Updates und Rebuilds

```bash
# Nach Code-Änderungen: Image neu bauen
docker-compose build --no-cache

# Container mit neuem Image neu starten
docker-compose up -d --force-recreate
```

### Speicher aufräumen

```bash
# Gestoppte Container löschen
docker container prune

# Ungenutzte Images löschen
docker image prune

# Alles aufräumen (VORSICHT!)
docker system prune -a
```

---

## 📂 Persistente Daten

Die folgenden Verzeichnisse werden als Volumes gemountet (Daten bleiben erhalten):

```yaml
volumes:
  - ../data/chroma_db:/app/data/chroma_db    # Vektordatenbank
  - ../data/uploads:/app/data/uploads        # Hochgeladene PDFs
```

**Das bedeutet:**
- ✅ Dokumente bleiben auch nach Container-Neustart erhalten
- ✅ ChromaDB-Daten sind persistent
- ⚠️ Nur bei `docker-compose down -v` werden Volumes gelöscht!

---

## 🐛 Troubleshooting

### Problem 1: "Port 8501 already in use"

**Ursache:** Port ist bereits belegt (z.B. durch lokale Streamlit-Instanz)

**Lösung 1:** Stoppe die lokale Instanz
```bash
# Alle Python-Prozesse anzeigen
tasklist | findstr python    # Windows
ps aux | grep python         # Linux/Mac

# Prozess beenden (ersetze <PID>)
taskkill /F /PID <PID>       # Windows
kill <PID>                   # Linux/Mac
```

**Lösung 2:** Ändere den Port in `docker-compose.yml`
```yaml
ports:
  - "8502:8501"  # Nutze Port 8502 statt 8501
```

Dann: http://localhost:8502

---

### Problem 2: "ERROR: Cannot connect to Docker daemon"

**Windows:**
- Stelle sicher, dass Docker Desktop läuft
- Prüfe das Icon in der Taskleiste
- Starte Docker Desktop neu

**Linux:**
```bash
# Docker-Service starten
sudo systemctl start docker

# Nutzer zur docker-Gruppe hinzufügen (einmalig)
sudo usermod -aG docker $USER
# Danach: Neu einloggen!
```

---

### Problem 3: "OpenAI API error" im Container

**Prüfen:**
```bash
# In Container einloggen
docker-compose exec rag-assistant /bin/bash

# Environment Variable prüfen
echo $OPENAI_API_KEY

# Sollte deinen Key zeigen, NICHT "your_openai_api_key_here"
```

**Lösung:**
1. `.env` Datei korrigieren
2. Container neu starten:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

### Problem 4: "Build failed" oder "pip install error"

**Ursache:** Netzwerkprobleme oder Cache-Fehler

**Lösung:**
```bash
# Clean Build ohne Cache
docker-compose build --no-cache

# Falls immer noch Fehler: Docker komplett neu starten
# Windows: Docker Desktop > Troubleshoot > Restart Docker Desktop
# Linux:
sudo systemctl restart docker
```

---

### Problem 5: Container startet, aber App nicht erreichbar

**Prüfen:**
```bash
# Container-Status
docker-compose ps

# Health-Check
docker-compose exec rag-assistant curl -f http://localhost:8501/_stcore/health

# Sollte zeigen: OK
```

**Logs anschauen:**
```bash
docker-compose logs rag-assistant | grep ERROR
```

---

## 🔒 Sicherheit & Best Practices

### 1. API Keys schützen

✅ **RICHTIG:**
```bash
# .env ist in .gitignore
# .env ist in .dockerignore
# API Key wird via Environment Variable übergeben
```

❌ **FALSCH:**
```python
# NIEMALS im Code:
api_key = "sk-proj-123456..."
```

### 2. Production Deployment

Für Production solltest du zusätzlich:

```yaml
# docker-compose.yml erweitern mit:
services:
  rag-assistant:
    # Restart Policy
    restart: always

    # Resource Limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

    # Read-only filesystem (außer Volumes)
    read_only: true

    # Health Check verschärfen
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### 3. Logs rotieren

```yaml
# Logging konfigurieren
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## 📊 Performance-Optimierung

### Multi-Stage Build nutzen (bereits implementiert ✅)

Der Dockerfile nutzt bereits Multi-Stage Build für kleinere Images:

```dockerfile
# Stage 1: Builder (mit Build-Dependencies)
FROM python:3.11-slim as builder
# ... pip install ...

# Stage 2: Runtime (nur Runtime-Dependencies)
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

**Ergebnis:** Image ist ~1.5 GB statt ~3 GB

### Caching verbessern

```bash
# requirements.txt zuerst kopieren für besseres Caching
COPY requirements.txt .
RUN pip install -r requirements.txt
# Dann erst Code kopieren
COPY . .
```

---

## 🚀 Production Deployment

### Mit Docker Swarm

```bash
# Swarm initialisieren
docker swarm init

# Stack deployen
docker stack deploy -c docker-compose.yml rag-stack

# Services anzeigen
docker service ls
```

### Mit Kubernetes

Für Kubernetes brauchst du zusätzlich:
- `deployment.yaml`
- `service.yaml`
- `configmap.yaml` (für Config)
- `secret.yaml` (für API Keys)

---

## ✅ Checkliste für erfolgreichen Docker-Start

- [ ] Docker Desktop installiert und läuft
- [ ] `.env` Datei mit gültigem OpenAI API Key erstellt
- [ ] `docker-compose build` erfolgreich
- [ ] `docker-compose up -d` erfolgreich
- [ ] `docker-compose ps` zeigt "Up"
- [ ] Browser öffnet http://localhost:8501
- [ ] PDF-Upload funktioniert
- [ ] Frage wird erfolgreich beantwortet

---

## 🆘 Weitere Hilfe

Bei Problemen:
1. Prüfe die [Troubleshooting-Sektion](#-troubleshooting)
2. Schau dir die Logs an: `docker-compose logs -f`
3. Lies die [vollständige Dokumentation](README.md)
4. Öffne ein Issue auf GitHub

---

## 🎯 Zusammenfassung

**Minimale Befehle für Start:**
```bash
# 1. .env erstellen und API Key eintragen
cp .env.example .env

# 2. In docker/ Verzeichnis wechseln
cd docker

# 3. Bauen und starten
docker-compose up -d

# 4. Browser öffnen
# http://localhost:8501
```

**Das war's!** 🎉

---

**Happy Dockering! 🐳**
