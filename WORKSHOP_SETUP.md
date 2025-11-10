# Workshop-Vorbereitung: Studien-RAG-Assistent

## Willkommen zum GenAI Workshop!

Diese Anleitung hilft dir, deine lokale Entwicklungsumgebung für den Workshop vorzubereiten. Bitte führe **alle Schritte vor dem Workshop** durch, damit wir direkt mit dem Bauen starten können.

---

## 🎯 Was du benötigst

### System Requirements
- **Windows 10 64-bit** (Build 19045 oder höher) oder **Windows 11**
- Mindestens **8 GB RAM** (16 GB empfohlen)
- **10 GB freier Festplattenspeicher**
- **Admin-Rechte** auf deinem Computer

---

## 📋 Installations-Checkliste

### 1. Docker Desktop installieren

Docker ermöglicht es uns, alle Komponenten in Containern zu betreiben.

**Schritte:**
1. Lade Docker Desktop herunter: [Docker Desktop für Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Starte das Installationsprogramm und folge den Anweisungen
3. **Wichtig:** Aktiviere während der Installation "Use WSL 2 instead of Hyper-V"
4. Nach der Installation: **Computer neu starten**
5. Docker Desktop öffnen und warten bis es vollständig gestartet ist

**Verifikation:**
```bash
docker --version
docker compose version
```

Du solltest Versionsnummern sehen (z.B. Docker version 24.x.x).

📖 **Offizielle Dokumentation:** https://docs.docker.com/desktop/

---

### 2. Python installieren

Das Projekt benötigt Python für die RAG-Pipeline.

**Schritte:**
1. Besuche: [Python Downloads](https://www.python.org/downloads/)
2. Lade **Python 3.11** oder **3.12** herunter (Windows Installer 64-bit)
3. **Wichtig:** Während der Installation:
   - ✅ Hake "Add Python to PATH" an
   - ✅ Wähle "Install for all users" (optional)
4. Klicke auf "Install Now"

**Verifikation:**
```bash
python --version
pip --version
```

Du solltest Python 3.11.x oder 3.12.x sehen.

📖 **Offizielle Dokumentation:** https://www.python.org/downloads/windows/

---

### 3. Git installieren (falls noch nicht vorhanden)

Git wird für Versionskontrolle benötigt (optional, aber empfohlen).

**Download:** [Git für Windows](https://git-scm.com/download/win)

**Verifikation:**
```bash
git --version
```

---

### 4. n8n lokal installieren

n8n ist ein Workflow-Automatisierungs-Tool, das wir für erweiterte GenAI-Pipelines nutzen.

**Einfachste Methode mit Docker:**

```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

**Für permanente Installation (empfohlen):**

Erstelle eine Datei `docker-compose-n8n.yml`:

```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**Starten:**
```bash
docker compose -f docker-compose-n8n.yml up -d
```

**Zugriff:** Öffne http://localhost:5678 im Browser

📖 **Offizielle Dokumentation:** https://docs.n8n.io/hosting/installation/docker/

---

## 🚀 Projekt Setup

### Schritt 1: ZIP-Datei entpacken

Du erhältst die Projekt-ZIP-Datei vor dem Workshop. Entpacke sie in einen Ordner deiner Wahl, z.B.:
```
C:\Users\DeinName\Documents\studien-rag-assistent
```

### Schritt 2: Terminal öffnen

Öffne das Terminal (PowerShell oder CMD) im Projektordner:
- **Methode 1:** Rechtsklick im Ordner → "Terminal hier öffnen"
- **Methode 2:** `cd` zu deinem Projektordner

### Schritt 3: Python Dependencies installieren

```bash
pip install -r requirements.txt
```

Dies installiert alle benötigten Python-Pakete (LangChain, Streamlit, ChromaDB, etc.).

### Schritt 4: .env Datei vorbereiten

Im Projektordner findest du eine `.env.example` Datei. Erstelle eine Kopie und benenne sie in `.env` um:

```bash
copy .env.example .env
```

**Wichtig:** Der OpenAI API-Key wird dir am Workshop-Tag zur Verfügung gestellt. Die `.env` Datei bleibt vorerst leer bzw. hat Platzhalter.

---

## ✅ Verifikation vor dem Workshop

### Test 1: Docker funktioniert
```bash
docker ps
```
Sollte keine Fehler anzeigen (kann leer sein).

### Test 2: Streamlit-UI starten (ohne API-Key)

```bash
streamlit run app/streamlit_ui.py
```

**Erwartetes Ergebnis:**
- Browser öffnet sich automatisch auf http://localhost:8501
- Du siehst die Benutzeroberfläche des RAG-Assistenten
- **Hinweis:** Ohne API-Key werden einige Funktionen noch nicht funktionieren - das ist normal!

Siehst du die Oberfläche? **Perfekt!** ✓

### Test 3: n8n erreichbar

Öffne http://localhost:5678 im Browser.
- Du solltest das n8n Login/Interface sehen

---

## 🛠️ Troubleshooting

### Docker startet nicht
- **Lösung:** Stelle sicher, dass Virtualisierung im BIOS aktiviert ist
- WSL 2 muss installiert sein: `wsl --install` in PowerShell (als Admin)

### "Python not found"
- **Lösung:** Python ist nicht im PATH. Installiere Python erneut und achte auf "Add to PATH"

### Port 8501 oder 5678 bereits belegt
- **Lösung:** Anderes Programm nutzt den Port. Finde es mit:
  ```bash
  netstat -ano | findstr :8501
  ```

### pip install schlägt fehl
- **Lösung:** Aktualisiere pip:
  ```bash
  python -m pip install --upgrade pip
  ```

---

## 📚 Nützliche Ressourcen

### Projekt-Technologien
- **Streamlit:** https://docs.streamlit.io/
- **LangChain:** https://python.langchain.com/docs/
- **ChromaDB:** https://docs.trychroma.com/
- **OpenAI API:** https://platform.openai.com/docs/

### Docker & n8n
- **Docker Compose:** https://docs.docker.com/compose/
- **n8n Workflows:** https://docs.n8n.io/workflows/

---

## 🎓 Am Workshop-Tag

Am Workshop-Tag wirst du:
1. ✅ Den **OpenAI API-Key** erhalten und in die `.env` Datei eintragen
2. ✅ Eigene Dokumente hochladen und den RAG-Assistenten testen
3. ✅ Den Code erweitern und eigene Features implementieren
4. ✅ n8n-Workflows für automatisierte GenAI-Pipelines bauen

---

## ❓ Fragen vor dem Workshop?

Falls du Probleme bei der Installation hast, notiere dir:
- Welcher Schritt funktioniert nicht?
- Welche Fehlermeldung erscheint?
- Welches Betriebssystem nutzt du?

Wir klären das dann am Anfang des Workshops!

---

## 🎉 Du bist bereit!

Wenn alle Verifikationsschritte funktionieren, bist du perfekt vorbereitet. Wir freuen uns auf den Workshop!

**Checklist:**
- [ ] Docker Desktop installiert und läuft
- [ ] Python 3.11/3.12 installiert
- [ ] n8n über Docker erreichbar (localhost:5678)
- [ ] Projekt-ZIP entpackt
- [ ] Dependencies installiert (`pip install -r requirements.txt`)
- [ ] Streamlit-UI startet (localhost:8501)

**Status:** Ready to build! 🚀
