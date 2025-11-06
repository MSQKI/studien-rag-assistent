# 🐳 Docker + ChromaDB - Vollständiger Guide

Dieser Guide erklärt **genau**, wie Docker und ChromaDB zusammenarbeiten und wie du sicherstellst, dass es bei **jedem Studierenden** läuft.

---

## 🎯 **Das Problem und die Lösung**

### **Problem:**
- Lokal funktioniert es ✅
- Docker zeigt "Connection error" ❌

### **Ursache:**
Das Docker-Image wurde **VOR** dem Setzen des API Keys gebaut, oder mit einem alten/falschen Key.

### **Lösung:**
Image **NEU bauen** nachdem .env korrekt gesetzt wurde!

---

## ✅ **Schritt-für-Schritt: Docker zum Laufen bringen**

### **Schritt 1: .env Datei prüfen**

```powershell
# Im Projekt-Root
cd C:\Users\EricChittka\Documents\MS_Github\studien-rag-assistent

# .env anschauen
Get-Content .env | Select-String "OPENAI_API_KEY"

# MUSS zeigen:
# OPENAI_API_KEY=sk-proj-...ein-langer-key...
```

**Falls der Key fehlt oder falsch ist:**
```powershell
notepad .env
# → Trage korrekten API Key ein
# → Speichern!
```

---

### **Schritt 2: Docker Image NEU bauen**

**Option A: Automatisches Script (empfohlen)**

```powershell
# Im Projekt-Root
.\docker-rebuild.ps1
```

Das Script:
1. ✅ Prüft .env
2. ✅ Stoppt alte Container
3. ✅ Löscht altes Image
4. ✅ Baut NEU mit aktuellem API Key
5. ✅ Startet Container
6. ✅ Verifiziert Verbindung

**Option B: Manuell**

```powershell
# 1. Ins docker/ Verzeichnis
cd docker

# 2. Container stoppen
docker-compose down

# 3. Altes Image löschen
docker rmi docker-rag-assistant

# 4. NEU bauen (5-10 Minuten!)
docker-compose build --no-cache

# 5. Starten
docker-compose up -d

# 6. Logs prüfen
docker-compose logs -f
```

---

## 📊 **Wie Docker + ChromaDB funktioniert**

### **Architektur:**

```
Host-System (dein Computer)
├── studien-rag-assistent/
│   ├── .env                         ← API Key
│   ├── data/
│   │   ├── uploads/                 ← PDFs (persistent!)
│   │   │   └── vorlesung.pdf
│   │   └── chroma_db/               ← Vektordatenbank (persistent!)
│   │       └── chroma.sqlite3
│   └── docker/
│       └── docker-compose.yml
│
└── Docker Container
    ├── Läuft auf: http://localhost:8501
    ├── Mounted Volumes:
    │   ├── ../data/uploads  → /app/data/uploads
    │   └── ../data/chroma_db → /app/data/chroma_db
    └── Environment: OPENAI_API_KEY aus .env
```

### **Was passiert:**

1. **docker-compose.yml** definiert:
   ```yaml
   volumes:
     - ../data/chroma_db:/app/data/chroma_db  # Host → Container
     - ../data/uploads:/app/data/uploads

   env_file:
     - ../.env  # API Key wird geladen
   ```

2. **Beim Start:**
   - Container startet
   - Lädt .env → `OPENAI_API_KEY` ist verfügbar
   - Mountet `data/` Verzeichnis
   - ChromaDB speichert in `/app/data/chroma_db` (= dein lokales `data/chroma_db/`)

3. **Persistenz:**
   - ✅ PDFs bleiben auf deinem Computer
   - ✅ ChromaDB bleibt auf deinem Computer
   - ✅ Auch nach `docker-compose down`

---

## 🔒 **Isolation zwischen Studierenden**

### **Wie jeder seine eigene Datenbank hat:**

```
Student A                          Student B
├── Projekt-Ordner A/             ├── Projekt-Ordner B/
│   ├── .env (API Key A)          │   ├── .env (API Key B)
│   ├── data/                     │   ├── data/
│   │   ├── uploads/              │   │   ├── uploads/
│   │   │   └── mathe.pdf         │   │   │   └── physik.pdf
│   │   └── chroma_db/            │   │   └── chroma_db/
│   │       └── (DB von A)        │   │       └── (DB von B)
│   └── docker/                   │   └── docker/
│
└── Container A                   └── Container B
    Port 8501                         Port 8501 (auf anderem PC!)
    Zugriff auf data/ von A           Zugriff auf data/ von B
```

**Garantien:**
- ✅ Jeder Student hat sein eigenes Projekt-Verzeichnis
- ✅ Docker mounted NUR das lokale `data/` Verzeichnis
- ✅ KEINE gemeinsame Datenbank
- ✅ KEINE Verbindung zwischen Containern
- ✅ Jeder braucht seinen eigenen API Key

---

## 🎓 **Anleitung für Studierende**

### **Variante 1: Git Clone (empfohlen für Entwickler)**

```bash
# 1. Repository klonen
git clone <repo-url> mein-rag-assistent
cd mein-rag-assistent

# 2. .env erstellen
cp .env.example .env
# Öffne .env und trage deinen API Key ein!

# 3. Docker starten
cd docker
docker-compose up -d

# 4. Browser öffnen
# http://localhost:8501
```

### **Variante 2: ZIP Download (einfacher für Studierende)**

1. **Projekt als ZIP herunterladen**
2. **ZIP entpacken** in eigenes Verzeichnis (z.B. `C:\Studium\RAG-Assistent\`)
3. **`.env` erstellen:**
   - Kopiere `.env.example` → `.env`
   - Öffne `.env` mit Editor
   - Trage deinen OpenAI API Key ein
4. **Docker starten:**
   ```powershell
   cd docker
   docker-compose up -d
   ```
5. **Browser öffnen:** http://localhost:8501

---

## 🐛 **Troubleshooting**

### **Problem 1: "Connection error" beim PDF-Upload**

**Ursache:** API Key wird nicht gefunden oder ist ungültig

**Lösung:**
```powershell
# 1. Prüfe .env im Projekt-Root
Get-Content .env | Select-String "OPENAI_API_KEY"

# 2. Falls leer oder falsch → neu bauen!
cd docker
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### **Problem 2: Container startet nicht**

**Ursache:** Port 8501 ist bereits belegt

**Lösung:**
```powershell
# Option A: Stoppe andere Streamlit-Instanz
# (z.B. lokale Version mit python run.py)

# Option B: Ändere Port in docker-compose.yml
# Öffne docker/docker-compose.yml
# Ändere:
ports:
  - "8502:8501"  # Nutze 8502 statt 8501

# Dann: http://localhost:8502
```

---

### **Problem 3: Alte Daten bleiben nach Neustart**

**Das ist GEWOLLT!** ChromaDB ist persistent.

**Zum Löschen:**
```powershell
# Option A: Über UI → "Alles zurücksetzen"

# Option B: Manuell löschen
cd data
rm -r chroma_db/*
rm -r uploads/*

# Container neu starten
cd docker
docker-compose restart
```

---

### **Problem 4: "The OPENAI_API_KEY variable is not set"**

**Ursache:** .env fehlt oder liegt im falschen Verzeichnis

**Lösung:**
```powershell
# .env MUSS im Projekt-Root sein, NICHT in docker/!

# Richtig:
studien-rag-assistent/
├── .env          ← HIER! ✅
└── docker/
    └── docker-compose.yml

# Falsch:
docker/
├── .env          ← NICHT hier! ❌
└── docker-compose.yml
```

---

### **Problem 5: Chunks werden nicht gelöscht**

**Ursache:** Alte Code-Version im Docker-Image

**Lösung:** Image NEU bauen
```powershell
.\docker-rebuild.ps1
```

---

## 📋 **Checkliste für Dozenten**

Wenn du das für Studierende bereitstellst:

- [ ] ✅ README.md mit klaren Instruktionen
- [ ] ✅ .env.example mit Platzhalter
- [ ] ✅ DOCKER-CHROMADB-GUIDE.md (diese Datei)
- [ ] ✅ docker-rebuild.ps1 Script
- [ ] ✅ Hinweis: Jeder braucht eigenen API Key
- [ ] ✅ Geschätzte Kosten kommunizieren (~$0.01 pro PDF)
- [ ] ✅ Warnung: API Keys NIEMALS teilen!
- [ ] ✅ Optional: Demo-Key für ersten Test (mit Rate Limit!)

---

## 🔐 **Datenschutz & Sicherheit**

### **Was gespeichert wird:**

**Lokal (bei jedem Studierenden):**
- ✅ PDFs in `data/uploads/`
- ✅ ChromaDB in `data/chroma_db/`
- ✅ Chat-Historie (in Memory, nicht persistent)

**Bei OpenAI:**
- ✅ Nur Text-Chunks für Embeddings (temporär)
- ✅ Fragen und Antworten (gemäß OpenAI Policy)
- ❌ KEINE kompletten PDFs
- ❌ KEINE dauerhafte Speicherung

**Nicht gespeichert:**
- ❌ Keine Cloud-Synchronisation
- ❌ Keine zentrale Datenbank
- ❌ Keine Telemetrie (deaktiviert)

---

## 💰 **Kosten**

**Geschätzte Kosten pro Student:**

| Aktion | Kosten |
|--------|--------|
| 1 PDF verarbeiten (50 Seiten) | ~$0.005 |
| 100 Fragen stellen | ~$0.50 |
| Monatliche Nutzung (realistisch) | ~$2-5 |

**Tipps zum Sparen:**
- Nur relevante PDFs hochladen
- Dokumente löschen wenn nicht mehr benötigt
- `gpt-4o-mini` nutzen (nicht `gpt-4`)

---

## ✅ **Erfolgs-Checkliste**

Nach Setup sollte funktionieren:

- [ ] ✅ `docker-compose ps` zeigt "Up"
- [ ] ✅ http://localhost:8501 öffnet sich
- [ ] ✅ PDF-Upload funktioniert
- [ ] ✅ Frage wird beantwortet mit Quellenangaben
- [ ] ✅ Chunks-Zahl wird korrekt angezeigt
- [ ] ✅ Dokument löschen funktioniert
- [ ] ✅ "Alles zurücksetzen" funktioniert
- [ ] ✅ Nach Container-Neustart sind Daten noch da

---

## 🆘 **Support**

Bei Problemen:

1. ✅ Lies diese Anleitung
2. ✅ Prüfe Logs: `docker-compose logs`
3. ✅ Nutze `docker-rebuild.ps1`
4. ✅ Öffne Issue auf GitHub

---

## 🚀 **Quick Commands**

```powershell
# Build neu
.\docker-rebuild.ps1

# Container starten
cd docker && docker-compose up -d

# Container stoppen
cd docker && docker-compose down

# Logs live
cd docker && docker-compose logs -f

# In Container einloggen
cd docker && docker-compose exec rag-assistant /bin/bash

# Alles löschen (inkl. Daten!)
cd docker && docker-compose down -v
```

---

**Das war's! Docker + ChromaDB sollte jetzt bei jedem laufen! 🎉**
