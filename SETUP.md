# 🚀 Setup-Anleitung - Studien-RAG-Assistent

**Für Studierende: So richtest du deine eigene Lernplattform ein**

---

## ✅ Voraussetzungen (5 Minuten Installation)

### 1. Docker Desktop installieren
- **Windows/Mac**: https://www.docker.com/products/docker-desktop
- **Linux**: `sudo apt-get install docker docker-compose`

### 2. OpenAI API Key besorgen
1. Gehe zu https://platform.openai.com/api-keys
2. Registriere dich (falls noch nicht geschehen)
3. Klicke "Create new secret key"
4. **Kopiere den Key** (beginnt mit `sk-...`)
5. ⚠️ **Wichtig**: Der Key wird nur einmal angezeigt!

---

## 📥 Installation (3 einfache Schritte)

### Schritt 1: Repository herunterladen
```bash
git clone <repository-url>
cd studien-rag-assistent
```

### Schritt 2: API Key konfigurieren

**Windows:**
```batch
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

Füge deinen OpenAI API Key ein:
```
OPENAI_API_KEY=sk-...dein-key-hier...
```
Speichern und schließen!

### Schritt 3: Starten

**Windows:**
```batch
start.bat
```

**macOS/Linux:**
```bash
./start.sh
```

---

## 🎯 Zugriff

Nach ~1 Minute sind alle Services bereit:

| Service | URL | Beschreibung |
|---------|-----|--------------|
| **Frontend** | http://localhost:3000 | ⭐ Hauptanwendung (hier arbeitest du!) |
| API Docs | http://localhost:8000/docs | Backend-Dokumentation |
| Neo4j Browser | http://localhost:7474 | Graph-Datenbank (Passwort: studyplatform2024) |
| Streamlit | http://localhost:8501 | Legacy RAG-Interface |

---

## 📚 Erste Schritte

### 1. Dokument hochladen
1. Öffne http://localhost:3000
2. Gehe zu **"Datenverwaltung"**
3. Klicke **"Dokument hochladen"**
4. Wähle dein PDF-Vorlesungsskript
5. Warte ~30 Sekunden (Progress-Bar)
6. ✅ Fertig!

### 2. Frage stellen
1. Gehe zu **"RAG Chat"**
2. Stelle eine Frage: z.B. *"Erkläre mir das Konzept X"*
3. **NEU: Spracheingabe!** Klicke das Mikrofon-Symbol und sprich deine Frage
4. Erhalte Antwort mit **Quellenangaben**
5. **NEU: Antwort anhören!** Die Antwort wird automatisch vorgelesen oder klicke den Lautsprecher-Button

### 3. Karteikarten lernen
1. Gehe zu **"Karteikarten"**
2. Lerne fällige Karten (Klicke auf Karte zum Umdrehen)
3. Bewerte dich: "Ja" (gewusst) oder "Nein"
4. System merkt sich optimale Wiederholungsintervalle!

### 4. Knowledge Graph ansehen
1. Gehe zu **"Knowledge Graph"**
2. Sieh alle Konzepte visualisiert
3. **Klicke Nodes** für Details
4. **Verbindungen** zeigen Beziehungen

---

## 🛠️ Verwaltung

### Stoppen
```bash
# Windows
stop.bat

# macOS/Linux
./stop.sh
```

### Neustart
Einfach nochmal `start.bat` oder `start.sh` ausführen!

### Daten löschen
```bash
cd docker
docker-compose -f docker-compose-full.yml down -v
```
⚠️ **Achtung**: Löscht ALLE Daten (Dokumente, Karteikarten, Graph)!

### Logs ansehen
```bash
cd docker
docker-compose -f docker-compose-full.yml logs -f
```

---

## 💾 Deine Daten

Alle Daten werden persistent gespeichert in:
- `data/chroma_db/` → Vector Database (RAG)
- `data/uploads/` → Hochgeladene PDFs
- Docker Volumes → Neo4j Graph, PostgreSQL Flashcards

**Deine Daten bleiben erhalten** auch nach:
- Stoppen der Services
- Computer-Neustart
- Docker-Neustart

---

## ❓ Häufige Probleme

### "Docker ist nicht installiert"
→ Installiere Docker Desktop von https://www.docker.com

### "FEHLER: .env Datei nicht gefunden"
→ Erstelle `.env` Datei mit deinem OpenAI API Key (siehe Schritt 2)

### "Container starten nicht"
```bash
cd docker
docker-compose -f docker-compose-full.yml down
docker-compose -f docker-compose-full.yml up --build -d
```

### Frontend zeigt Fehler
1. Warte 2 Minuten nach Start (Services brauchen Zeit)
2. Prüfe ob Backend läuft: http://localhost:8000/docs
3. Prüfe Logs: `docker-compose logs backend`

### "No flashcards due for review"
→ Normal! Bedeutet keine Karten sind heute fällig. Komm morgen wieder!

### Graph zeigt nichts
→ Lade zuerst Dokumente hoch! Konzepte werden automatisch extrahiert.

---

## 💡 Tipps

1. **Mehrere PDFs gleichzeitig hochladen**: Spart Zeit!
2. **Regelmäßig Karteikarten lernen**: 10 Min/Tag reichen
3. **Graph nutzen**: Zeigt Zusammenhänge zwischen Konzepten
4. **Daten bearbeiten**: Unter "Datenverwaltung" kannst du alles anpassen
5. **Sichere deine Daten**: `data/` Ordner regelmäßig backup
6. **🎤 Voice im RAG Chat**:
   - Klicke Mikrofon-Symbol um Fragen zu sprechen
   - Antworten werden automatisch vorgelesen
   - Funktioniert in Chrome, Edge, Safari (Mikrofon-Berechtigung erforderlich)

---

## 🔒 Sicherheit

- ⚠️ **Teile deinen API Key NIE**
- ✅ Die Plattform läuft **lokal** auf deinem Computer
- ✅ Deine Dokumente werden **nur lokal** gespeichert
- ✅ Nur API-Anfragen gehen zu OpenAI (für KI-Antworten)

---

## 📧 Support

Probleme?
1. Prüfe diese Anleitung nochmal
2. Schaue in `README.md` für Details
3. Öffne ein Issue im Repository

---

**Viel Erfolg beim Lernen! 📚🎓**
