# Studien-RAG-Assistent - Installation & Setup für Workshop-Teilnehmer

> **Willkommen!** Diese Anleitung führt dich Schritt-für-Schritt durch die Installation und Nutzung des Studien-RAG-Assistenten.
> **Zielgruppe:** Studierende ohne Programmiererfahrung
> **Zeit:** 15-30 Minuten

---

## Inhaltsverzeichnis

1. [Was wirst du installieren?](#was-wirst-du-installieren)
2. [Voraussetzungen](#voraussetzungen)
3. [Schritt 1: Docker installieren](#schritt-1-docker-installieren)
4. [Schritt 2: Projekt herunterladen](#schritt-2-projekt-herunterladen)
5. [Schritt 3: OpenAI API Key einrichten](#schritt-3-openai-api-key-einrichten)
6. [Schritt 4: Anwendung starten](#schritt-4-anwendung-starten)
7. [Schritt 5: Erste Schritte](#schritt-5-erste-schritte)
8. [Bonus: n8n Automation installieren](#bonus-n8n-automation-installieren)
9. [Probleme lösen](#probleme-lösen)
10. [Anwendung stoppen](#anwendung-stoppen)

---

## Was wirst du installieren?

Du installierst eine KI-gestützte Lernplattform, die dir hilft, deine Vorlesungsunterlagen (PDFs) zu durchsuchen und zu verstehen. Die Plattform bietet:

- **RAG-Chat**: Stelle Fragen zu deinen PDFs und erhalte Antworten mit Quellenangaben
- **Knowledge Graph**: Visualisiere Konzepte und deren Beziehungen
- **Flashcards**: Lerne mit Spaced Repetition (wissenschaftlich bewiesen effektiv!)
- **Voice Input**: Stelle Fragen per Spracheingabe

**Technologie:** Die Plattform nutzt OpenAI's GPT-4o-mini für intelligente Antworten.

---

## Voraussetzungen

### Was du brauchst:

1. **Computer mit:**
   - Windows 10/11, macOS 11+, oder Linux
   - Mindestens 8 GB RAM (empfohlen: 16 GB)
   - Mindestens 10 GB freier Festplattenspeicher
   - Internetverbindung

2. **OpenAI API Key** (kostet Geld, aber günstig!)
   - Ungefähre Kosten: ~0,50€ - 2€ pro Monat bei normaler Nutzung
   - Wird später eingerichtet (Schritt 3)

---

## Schritt 1: Docker installieren

Docker ist eine Software, die alle benötigten Programme in "Containern" ausführt. Das macht die Installation super einfach!

### Windows

1. **Docker Desktop herunterladen:**
   - Gehe zu: https://www.docker.com/products/docker-desktop/
   - Klicke auf "Download for Windows"
   - Führe die heruntergeladene `Docker Desktop Installer.exe` aus

2. **Installation:**
   - Folge den Anweisungen im Installer
   - Akzeptiere die Standardeinstellungen
   - **WICHTIG:** Wenn du nach WSL 2 gefragt wirst, wähle "Install WSL 2" aus
   - Nach der Installation: Computer neu starten

3. **Docker starten:**
   - Öffne Docker Desktop (Suche im Startmenü nach "Docker Desktop")
   - Warte bis unten links "Engine running" steht (kann 1-2 Minuten dauern)

4. **Testen:**
   - Öffne die **Eingabeaufforderung** (CMD):
     - Windows-Taste drücken
     - "cmd" eingeben
     - Enter drücken
   - Eingeben: `docker --version`
   - Du solltest etwas wie `Docker version 24.0.6` sehen

### macOS

1. **Docker Desktop herunterladen:**
   - Gehe zu: https://www.docker.com/products/docker-desktop/
   - Wähle je nach Mac:
     - **Apple Silicon (M1/M2/M3)**: Download for Mac (Apple chip)
     - **Intel Mac**: Download for Mac (Intel chip)
   - Öffne die heruntergeladene `.dmg` Datei
   - Ziehe Docker in den Programme-Ordner

2. **Docker starten:**
   - Öffne Docker aus dem Programme-Ordner
   - Bei der ersten Nutzung: Erlaube den Zugriff (Administrator-Passwort eingeben)
   - Warte bis oben rechts ein grüner Punkt erscheint

3. **Testen:**
   - Öffne **Terminal** (Spotlight: Cmd+Space → "Terminal" eingeben)
   - Eingeben: `docker --version`
   - Du solltest etwas wie `Docker version 24.0.6` sehen

### Linux (Ubuntu/Debian)

```bash
# Terminal öffnen (Ctrl+Alt+T)

# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Aktuellen Benutzer zur Docker-Gruppe hinzufügen
sudo usermod -aG docker $USER

# Neu einloggen (oder Computer neu starten)
newgrp docker

# Testen
docker --version
```

---

## Schritt 2: Projekt herunterladen

### Option A: Mit Git (empfohlen, wenn du Git hast)

```bash
# Terminal/CMD öffnen
cd Desktop  # Oder ein anderer Ordner deiner Wahl
git clone https://github.com/yourusername/studien-rag-assistent.git
cd studien-rag-assistent
```

### Option B: Als ZIP herunterladen (einfacher für Anfänger)

1. **Projekt herunterladen:**
   - Gehe zu: https://github.com/yourusername/studien-rag-assistent
   - Klicke oben rechts auf den grünen Button "Code"
   - Wähle "Download ZIP"

2. **Entpacken:**
   - **Windows:** Rechtsklick auf die ZIP-Datei → "Alle extrahieren" → Zielordner wählen (z.B. Desktop)
   - **macOS:** Doppelklick auf die ZIP-Datei
   - **Linux:** Rechtsklick → "Hier entpacken"

3. **Ordner öffnen:**
   - Navigiere in den entpackten Ordner `studien-rag-assistent`
   - Du solltest Dateien wie `README.md`, `docker/`, `backend/`, `frontend/` sehen

---

## Schritt 3: OpenAI API Key einrichten

Der Studien-RAG-Assistent nutzt OpenAI's KI-Modelle. Dafür brauchst du einen API Key.

### 3.1 OpenAI Account erstellen

1. **Gehe zu:** https://platform.openai.com/signup
2. **Registriere dich** mit E-Mail oder Google/Microsoft Account
3. **Verifiziere** deine E-Mail-Adresse

### 3.2 API Key erstellen

1. **Einloggen:** https://platform.openai.com/
2. **Gehe zu API Keys:**
   - Klicke oben rechts auf dein Profilbild
   - Wähle "View API keys" oder gehe direkt zu: https://platform.openai.com/api-keys
3. **Neuen Key erstellen:**
   - Klicke auf "+ Create new secret key"
   - Name: "Studien-RAG-Assistent" (optional)
   - Klicke "Create secret key"
4. **Key kopieren:**
   - **WICHTIG:** Kopiere den Key SOFORT (er wird nur einmal angezeigt!)
   - Der Key sieht so aus: `sk-proj-abc123...`
   - Speichere ihn temporär in einem Texteditor

### 3.3 Guthaben aufladen (falls nötig)

**Neu registriert?** Du bekommst evtl. $5 gratis Guthaben.

**Guthaben aufladen:**
1. Gehe zu: https://platform.openai.com/settings/organization/billing
2. Klicke "Add payment method"
3. Füge eine Kreditkarte hinzu
4. **Optional:** Setze ein monatliches Limit (z.B. $5-10)

**Kosten-Übersicht:**
- GPT-4o-mini: ~$0.15 pro 1 Million Input-Tokens (~750.000 Wörter)
- Embeddings: ~$0.02 pro 1 Million Tokens
- **Realistische monatliche Kosten:** 0,50€ - 2€ bei normaler Nutzung

### 3.4 API Key in der Anwendung eintragen

1. **Im Projekt-Ordner:** Öffne den Ordner `studien-rag-assistent`
2. **Datei erstellen:**

   **Windows:**
   - Rechtsklick in den Ordner → "Neu" → "Textdokument"
   - Benenne es um zu `.env` (OHNE `.txt` am Ende!)
   - Wenn Windows die Endung versteckt:
     - Öffne den Ordner
     - Klicke oben auf "Ansicht"
     - Aktiviere "Dateinamenerweiterungen"

   **macOS/Linux:**
   - Terminal öffnen
   - Navigiere zum Projekt: `cd /pfad/zum/studien-rag-assistent`
   - Datei erstellen: `cp .env.example .env`

3. **API Key eintragen:**
   - Öffne die `.env` Datei mit einem Texteditor (Notepad, TextEdit, nano, VS Code, etc.)
   - Ändere die erste Zeile:
     ```bash
     OPENAI_API_KEY=sk-proj-dein-echter-key-hier
     ```
   - Ersetze `sk-proj-dein-echter-key-hier` mit deinem echten API Key
   - Speichern und schließen

**WICHTIG:** Teile deinen API Key NIEMALS mit anderen! Er ist wie ein Passwort.

---

## Schritt 4: Anwendung starten

Jetzt wird's spannend! Wir starten die komplette Plattform.

### Windows

1. **Datei-Explorer öffnen:**
   - Navigiere zum Projekt-Ordner `studien-rag-assistent`

2. **Startskript ausführen:**
   - Doppelklick auf `START.bat`
   - Ein schwarzes Fenster (Eingabeaufforderung) öffnet sich
   - Du siehst viele Zeilen wie "Pulling image...", "Creating container..."

3. **Warten:**
   - **Beim ersten Start:** Dauert 5-10 Minuten (Docker lädt alle Programme herunter)
   - **Bei späteren Starts:** Nur noch ~30 Sekunden
   - Warte bis du diese Zeile siehst:
     ```
     ========================================
       Start abgeschlossen!
     ========================================
     ```

4. **Docker Desktop prüfen:**
   - Öffne Docker Desktop
   - Unter "Containers" solltest du sehen:
     - `study-platform-backend` (grün)
     - `study-platform-frontend` (grün)
     - `study-platform-neo4j` (grün)
     - `study-platform-streamlit` (grün)

### macOS/Linux

1. **Terminal öffnen:**
   - **macOS:** Spotlight (Cmd+Space) → "Terminal"
   - **Linux:** Ctrl+Alt+T

2. **Zum Projekt navigieren:**
   ```bash
   cd ~/Desktop/studien-rag-assistent
   # Passe den Pfad an, wenn du das Projekt woanders gespeichert hast
   ```

3. **Startskript ausführen:**
   ```bash
   chmod +x START.sh  # Macht das Skript ausführbar (nur beim ersten Mal nötig)
   ./START.sh
   ```

4. **Warten:**
   - Beim ersten Start: 5-10 Minuten
   - Du siehst:
     ```
     [1/4] Stoppe alte Container...
     [2/4] Starte alle Services...
     [3/4] Warte 10 Sekunden...
     ========================================
       Start abgeschlossen!
     ========================================
     ```

### Überprüfen ob alles läuft

Öffne deinen Browser und teste diese URLs:

- **Frontend (Hauptanwendung):** http://localhost:3000
  - Du solltest das Dashboard sehen
- **Backend API Docs:** http://localhost:8000/docs
  - Du solltest die Swagger API-Dokumentation sehen
- **Neo4j Browser:** http://localhost:7474
  - Du solltest die Neo4j Datenbank-Oberfläche sehen
- **Streamlit (Legacy UI):** http://localhost:8501
  - Du solltest die alte Oberfläche sehen (optional)

**Funktioniert alles?** Perfekt! Weiter zu Schritt 5.

**Probleme?** Siehe [Probleme lösen](#probleme-lösen) am Ende dieser Anleitung.

---

## Schritt 5: Erste Schritte

### 5.1 Erstes Dokument hochladen

1. **Öffne die Anwendung:** http://localhost:3000

2. **Gehe zu "Data Management":**
   - Klicke in der linken Navigation auf "Data Management"
   - Wähle oben den Tab "Documents"

3. **PDF hochladen:**
   - Klicke auf "Choose File" oder ziehe eine PDF-Datei in die Dropzone
   - **Empfehlung:** Starte mit einem kleinen PDF (5-20 Seiten)
   - Klicke "Upload"

4. **Warten:**
   - Du siehst einen Fortschrittsbalken
   - Die Anwendung:
     - Liest das PDF
     - Teilt es in Chunks (Textabschnitte)
     - Erstellt Embeddings (Vektoren für Suche)
     - Extrahiert Konzepte für den Knowledge Graph
     - Generiert Flashcards
   - **Dauer:** 30 Sekunden - 2 Minuten je nach PDF-Größe

5. **Erfolg:**
   - Du siehst: "Document uploaded successfully!"
   - Das Dokument erscheint in der Liste

### 5.2 Erste RAG-Query (Frage stellen)

1. **Gehe zu "RAG Chat":**
   - Klicke in der Navigation auf "RAG Chat"

2. **Frage stellen:**
   - Gib unten eine Frage ein, z.B.:
     - "Was sind die Hauptthemen in diesem Dokument?"
     - "Erkläre mir das Konzept XYZ"
     - "Fasse die wichtigsten Punkte zusammen"
   - Klicke "Send" oder drücke Enter

3. **Antwort erhalten:**
   - Du siehst eine KI-generierte Antwort
   - Unter der Antwort: **Quellen** (Seite + Dokument)
   - Du kannst auf Quellen klicken, um den Original-Text zu sehen

4. **Voice Input testen (optional):**
   - Klicke auf das Mikrofon-Symbol
   - Erlaube Mikrofon-Zugriff im Browser
   - Sprich deine Frage
   - Die Frage wird automatisch eingetragen

### 5.3 Knowledge Graph erkunden

1. **Gehe zu "Knowledge Graph":**
   - Klicke in der Navigation auf "Knowledge Graph"

2. **Graph anschauen:**
   - Du siehst eine Visualisierung aller extrahierten Konzepte
   - **Knoten (Kreise):** Konzepte (z.B. "Algorithmus", "Datenstruktur")
   - **Kanten (Linien):** Beziehungen zwischen Konzepten

3. **Interaktiv nutzen:**
   - **Zoom:** Mausrad scrollen
   - **Pan:** Klicken & Ziehen
   - **Konzept auswählen:** Klick auf einen Knoten
   - **Details ansehen:** Details erscheinen rechts

4. **Path Finding:**
   - Wähle zwei Konzepte aus
   - Klicke "Find Shortest Path"
   - Die Anwendung zeigt den kürzesten Verbindungsweg

### 5.4 Flashcards lernen

1. **Gehe zu "Flashcards":**
   - Klicke in der Navigation auf "Flashcards"

2. **Flashcards anschauen:**
   - Du siehst automatisch generierte Karteikarten
   - Jede Karte hat:
     - Frage (Vorderseite)
     - Antwort (Rückseite)
     - Quelle (welches Dokument)

3. **Lernen starten:**
   - Klicke "Start Learning"
   - Du siehst eine Karte mit der Frage
   - Denke über die Antwort nach
   - Klicke "Show Answer"
   - Bewerte dich selbst:
     - **5 (Perfect):** Sofort richtig
     - **4 (Good):** Nach kurzem Nachdenken richtig
     - **3 (Pass):** Schwierig, aber richtig
     - **2 (Fail):** Falsch, aber verstanden
     - **1 (Again):** Komplett falsch

4. **Spaced Repetition:**
   - Die Anwendung nutzt den **SM-2 Algorithmus**
   - Karten die du gut kannst, kommen seltener
   - Karten die du nicht kannst, kommen häufiger
   - Statistiken zeigen deinen Fortschritt

### 5.5 Eigene Flashcards erstellen

1. **In "Flashcards":**
   - Klicke "Create New Flashcard"
   - Fülle aus:
     - **Question:** Deine Frage
     - **Answer:** Deine Antwort
     - **Source:** (optional) Quelle/Dokument
   - Klicke "Create"

2. **Flashcards bearbeiten:**
   - Klicke auf das Stift-Symbol bei einer Karte
   - Ändere Frage/Antwort
   - Klicke "Save"

3. **Flashcards löschen:**
   - Klicke auf das Papierkorb-Symbol
   - Bestätige die Löschung

---

## Bonus: n8n Automation installieren

n8n ist ein Workflow-Automation-Tool (wie Zapier, aber Open Source). Du kannst damit z.B. automatisch PDFs aus E-Mails in den RAG-Assistenten hochladen.

**Hinweis:** Wir nutzen n8n aktuell nicht im Workshop, aber hier ist die Anleitung für später!

### Was ist n8n?

- **Workflow-Builder:** Verbinde verschiedene Tools & Services
- **No-Code:** Alles per Drag & Drop
- **Open Source:** Komplett kostenlos
- **Beispiele:**
  - "Wenn PDF in Gmail ankommt → Automatisch hochladen"
  - "Jeden Montag → Zusammenfassung meiner Flashcard-Stats per E-Mail"
  - "Wenn ich in Google Docs schreibe → Als Flashcard speichern"

### n8n mit Docker installieren

1. **Docker Compose Datei erstellen:**

   Erstelle eine neue Datei `docker-compose-n8n.yml` im Projekt-Ordner:

   ```yaml
   version: '3.8'

   services:
     n8n:
       image: n8nio/n8n:latest
       container_name: n8n
       ports:
         - "5678:5678"
       environment:
         - N8N_BASIC_AUTH_ACTIVE=true
         - N8N_BASIC_AUTH_USER=admin
         - N8N_BASIC_AUTH_PASSWORD=admin123  # ÄNDERN!
         - N8N_HOST=localhost
         - N8N_PORT=5678
         - N8N_PROTOCOL=http
         - WEBHOOK_URL=http://localhost:5678/
       volumes:
         - n8n_data:/home/node/.n8n
       restart: unless-stopped

   volumes:
     n8n_data:
       driver: local
   ```

2. **n8n starten:**

   **Windows:**
   ```cmd
   cd C:\Pfad\zu\studien-rag-assistent
   docker-compose -f docker-compose-n8n.yml up -d
   ```

   **macOS/Linux:**
   ```bash
   cd ~/Desktop/studien-rag-assistent
   docker-compose -f docker-compose-n8n.yml up -d
   ```

3. **n8n öffnen:**
   - Browser öffnen: http://localhost:5678
   - Einloggen mit:
     - Username: `admin`
     - Password: `admin123` (oder was du geändert hast)

4. **Erster Workflow:**
   - Klicke "New Workflow"
   - Ziehe Nodes (z.B. "Gmail Trigger", "HTTP Request", "IF")
   - Verbinde sie per Drag & Drop
   - Konfiguriere jeden Node
   - Klicke "Execute Workflow" zum Testen

### Beispiel-Workflow: PDF aus E-Mail hochladen

1. **Nodes hinzufügen:**
   - **Gmail Trigger:** Überwacht Posteingang nach E-Mails mit Anhang
   - **Filter:** Prüft ob Anhang eine PDF ist
   - **HTTP Request:** Sendet PDF an `/api/documents/upload`
   - **Slack:** Sendet Benachrichtigung "PDF hochgeladen!"

2. **Konfiguration:**

   **Gmail Trigger:**
   - Authentication: Google OAuth2 einrichten
   - Trigger: "On new email"
   - Filter: "Has attachment"

   **IF Node:**
   - Condition: `{{ $json["attachments"][0]["contentType"] }}` equals `application/pdf`

   **HTTP Request:**
   - Method: POST
   - URL: `http://host.docker.internal:8000/api/documents/upload`
   - Body Type: Form-Data
   - File Field: `{{ $json["attachments"][0]["data"] }}`

3. **Aktivieren:**
   - Toggle oben rechts auf "Active"
   - Workflow läuft jetzt im Hintergrund!

### n8n stoppen

```bash
docker-compose -f docker-compose-n8n.yml down
```

---

## Probleme lösen

### Problem: "Docker ist nicht installiert" oder "Docker command not found"

**Lösung:**
- Stelle sicher, dass Docker Desktop läuft (Windows/Mac)
- Linux: Überprüfe Installation mit `sudo systemctl status docker`
- Neustart des Computers

### Problem: "Port 3000 is already allocated"

**Bedeutung:** Ein anderes Programm nutzt bereits Port 3000.

**Lösung:**

**Windows:**
```cmd
# Finde das Programm
netstat -ano | findstr :3000

# Beende den Prozess (ersetze PID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Finde das Programm
lsof -i :3000

# Beende den Prozess
kill -9 <PID>
```

Oder ändere den Port in `docker/docker-compose-full.yml`:
```yaml
frontend:
  ports:
    - "3001:3000"  # Nutze Port 3001 statt 3000
```

### Problem: ".env file not found"

**Lösung:**
- Überprüfe, dass die `.env` Datei im Hauptordner liegt (nicht in `docker/` oder `backend/`)
- Stelle sicher, dass die Datei wirklich `.env` heißt (nicht `.env.txt`)
- Windows: Aktiviere "Dateinamenerweiterungen" in den Ordner-Optionen

### Problem: "OpenAI API Error: Incorrect API key"

**Lösung:**
- Überprüfe deinen API Key in der `.env` Datei
- Stelle sicher, dass keine Leerzeichen vor/nach dem Key sind
- Erstelle einen neuen API Key bei OpenAI
- Prüfe ob dein OpenAI-Account Guthaben hat

### Problem: "Backend health check failed"

**Bedeutung:** Backend-Container startet nicht richtig.

**Lösung:**
```bash
# Logs anschauen
docker logs study-platform-backend

# Häufige Fehler:
# - "OPENAI_API_KEY not set" → .env Datei prüfen
# - "Permission denied" → Docker neu starten
# - "Module not found" → Container neu bauen:
docker-compose -f docker/docker-compose-full.yml build --no-cache backend
```

### Problem: "Neo4j connection refused"

**Lösung:**
```bash
# Neo4j Logs prüfen
docker logs study-platform-neo4j

# Container neustarten
docker restart study-platform-neo4j

# 30 Sekunden warten (Neo4j braucht Zeit zum Starten)
```

### Problem: Frontend zeigt "Network Error"

**Lösung:**
1. Prüfe ob Backend läuft: http://localhost:8000/health
2. Öffne Browser-Konsole (F12) → "Console" Tab
3. Schaue nach CORS-Fehlern
4. Container neustarten:
   ```bash
   cd docker
   docker-compose -f docker-compose-full.yml restart
   ```

### Problem: "Disk space full"

**Bedeutung:** Docker verbraucht viel Speicher.

**Lösung:**
```bash
# Ungenutzte Container/Images löschen
docker system prune -a

# Volumes löschen (VORSICHT: Löscht Daten!)
docker volume prune
```

### Problem: Alles ist langsam

**Lösungen:**
1. **Docker mehr RAM geben:**
   - Docker Desktop öffnen → Settings → Resources
   - RAM auf 6-8 GB erhöhen
   - CPU auf 4 Cores erhöhen

2. **Nur benötigte Services starten:**
   ```bash
   # Nur Backend + Frontend (ohne Neo4j)
   docker-compose -f docker/docker-compose-full.yml up -d backend frontend
   ```

3. **Alte Daten löschen:**
   - In der App: Data Management → "Clear All"

---

## Anwendung stoppen

### Alles stoppen (empfohlen)

**Windows:**
- Doppelklick auf `stop.bat`

**macOS/Linux:**
```bash
./stop.sh
```

### Nur einzelne Services stoppen

```bash
cd docker
docker-compose -f docker-compose-full.yml stop backend
docker-compose -f docker-compose-full.yml stop frontend
```

### Alles löschen (inkl. Daten!)

**VORSICHT:** Löscht alle Daten (PDFs, Flashcards, Graph)!

```bash
cd docker
docker-compose -f docker-compose-full.yml down -v
```

---

## Nächste Schritte

Jetzt bist du bereit! Hier sind ein paar Ideen:

### Sofort loslegen:
1. Lade deine Vorlesungs-PDFs hoch
2. Stelle Fragen zum Stoff
3. Lerne mit den automatisch generierten Flashcards
4. Erkunde den Knowledge Graph

### Erweiterte Nutzung:
- **Anpassungen:** Lies `PROJEKTDOKUMENTATION.md` für technische Details
- **Entwicklung:** Schaue in den Code (`backend/`, `frontend/`)
- **Automation:** Richte n8n Workflows ein
- **Eigene Modelle:** Experimentiere mit anderen OpenAI-Modellen

### Community:
- Teile deine Erfahrungen
- Erstelle Issues auf GitHub bei Problemen
- Trage bei: Pull Requests sind willkommen!

---

## Ressourcen

### Dokumentation:
- [PROJEKTDOKUMENTATION.md](./PROJEKTDOKUMENTATION.md) - Technische Details
- [README.md](./README.md) - Projekt-Übersicht
- [SETUP.md](./SETUP.md) - Erweiterte Setup-Optionen

### Externe Links:
- [Docker Docs](https://docs.docker.com/)
- [OpenAI Platform](https://platform.openai.com/)
- [n8n Docs](https://docs.n8n.io/)
- [LangChain Docs](https://python.langchain.com/)

### Support:
- **GitHub Issues:** https://github.com/yourusername/studien-rag-assistent/issues
- **Discord/Slack:** (falls vorhanden)

---

## Tipps & Tricks

### Geld sparen bei OpenAI:
1. **Nutze kleine PDFs:** Große PDFs (>100 Seiten) kosten mehr
2. **Batch Processing:** Lade mehrere PDFs auf einmal hoch
3. **Setze API Limits:** In deinem OpenAI Account unter "Usage limits"
4. **Nutze Cache:** Die App cached Ergebnisse, stelle dieselbe Frage nicht mehrfach

### Bessere RAG-Ergebnisse:
1. **Spezifische Fragen:** "Erkläre Quicksort" statt "Was ist das?"
2. **Kontext geben:** "Bezogen auf die Vorlesung Algorithmen..."
3. **Folge-Fragen:** Die App hat Conversation Memory
4. **Quellen prüfen:** Schau dir die zitierten Stellen an

### Effektives Lernen mit Flashcards:
1. **Täglich lernen:** Nur 10-15 Minuten pro Tag
2. **Ehrlich bewerten:** Sei streng bei der Selbstbewertung
3. **Eigene Karten erstellen:** Ergänze Auto-Generated Karten
4. **Aktives Recall:** Sprich Antworten laut aus

### Performance-Optimierung:
1. **Nur nötige Services:** Stoppe Streamlit wenn du es nicht brauchst
2. **Regelmäßig aufräumen:** Lösche alte PDFs
3. **Docker Ressourcen:** Gib Docker mehr RAM in den Settings

---

## Häufig gestellte Fragen (FAQ)

**Q: Wie viel kostet die Nutzung?**
A: Die Software ist kostenlos. Nur OpenAI API kostet ~0,50€-2€/Monat.

**Q: Sind meine Daten sicher?**
A: Ja! Alles läuft lokal auf deinem Computer. Nur API-Calls gehen zu OpenAI.

**Q: Kann ich eigene Modelle nutzen?**
A: Ja! Ändere `LLM_MODEL` in der `.env` Datei (z.B. zu `gpt-4`).

**Q: Funktioniert es offline?**
A: Teilweise. Embeddings & LLM-Calls brauchen Internet. Graph/Flashcards funktionieren offline.

**Q: Wie lösche ich alle Daten?**
A: In der App: Data Management → "Clear All". Oder Docker Volume löschen.

**Q: Kann ich mehrere PDFs gleichzeitig hochladen?**
A: Aktuell nein, aber es ist geplant!

**Q: Unterstützt es andere Sprachen?**
A: Ja! OpenAI versteht viele Sprachen. Passe ggf. Voice-Settings an.

**Q: Wie aktualisiere ich die App?**
A:
```bash
git pull origin main  # Neueste Version holen
./START.sh            # Neu starten
```

---

**Viel Erfolg beim Lernen!**

Bei Fragen oder Problemen: Schau in die Dokumentation oder erstelle ein GitHub Issue.

**Version:** 2.0.0
**Letzte Aktualisierung:** November 2025
