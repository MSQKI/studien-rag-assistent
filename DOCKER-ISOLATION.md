# 🔒 Docker Isolation - Datenschutz für Studierende

## ✅ Wichtig: Jeder Studierende hat seine EIGENE Datenbank!

Das Docker-Setup ist so konfiguriert, dass **jeder Nutzer seine eigenen, lokalen Daten** hat.

## 🎯 Wie funktioniert die Isolation?

### 1. **Lokale Volumes**

```yaml
# docker-compose.yml
volumes:
  - ../data/chroma_db:/app/data/chroma_db    # Lokal gemountet!
  - ../data/uploads:/app/data/uploads        # Lokal gemountet!
```

**Was bedeutet das:**
- `../data/` verweist auf das `data/` Verzeichnis **auf deinem Computer**
- Jeder Studierende hat sein eigenes `data/` Verzeichnis im heruntergeladenen Projekt
- **KEINE gemeinsame Cloud-Datenbank!**
- **KEINE geteilten Dokumente zwischen Nutzern!**

### 2. **Datenfluss visualisiert**

```
Student A                          Student B
├── studien-rag-assistent/        ├── studien-rag-assistent/
│   ├── data/                     │   ├── data/
│   │   ├── uploads/              │   │   ├── uploads/
│   │   │   └── mathe.pdf         │   │   │   └── physik.pdf
│   │   └── chroma_db/            │   │   └── chroma_db/
│   │       └── [A's Vektoren]    │   │       └── [B's Vektoren]
│   └── docker/                   │   └── docker/
│       └── docker-compose.yml    │       └── docker-compose.yml
│                                 │
└── Container A (Port 8501)       └── Container B (Port 8501)
    └── Zugriff nur auf A's data      └── Zugriff nur auf B's data
```

### 3. **Kein Netzwerk zwischen Containern**

```yaml
# Jeder Container ist isoliert
networks:
  rag-network:
    driver: bridge  # Lokales Bridge-Netzwerk, KEIN externes Netzwerk
```

**Bedeutung:**
- Container können NICHT miteinander kommunizieren
- Jeder Container läuft auf `localhost` des jeweiligen Nutzers
- Keine Verbindung zwischen verschiedenen Studierenden möglich

---

## 🔐 Datenschutz-Garantien

### ✅ Was geschützt ist:

1. **PDFs sind lokal**
   - Werden nur in `data/uploads/` gespeichert
   - Bleiben auf dem Computer des Studierenden
   - Werden NICHT hochgeladen

2. **ChromaDB ist lokal**
   - Vektordatenbank liegt in `data/chroma_db/`
   - Nur auf dem lokalen Computer
   - Keine Cloud-Synchronisation

3. **OpenAI API**
   - Nur Text-Chunks werden an OpenAI gesendet (zum Embedding)
   - KEINE vollständigen PDFs
   - KEINE dauerhaften Speicherung bei OpenAI
   - [OpenAI API Data Usage Policy](https://openai.com/policies/api-data-usage-policies)

4. **Keine Logs nach außen**
   - Logs bleiben im Container bzw. auf dem lokalen System
   - Keine Telemetrie (ChromaDB Telemetry ist deaktiviert!)

### ⚠️ Was du wissen solltest:

1. **API Key muss jeder Studierende selbst erstellen**
   - Jeder braucht seinen eigenen OpenAI API Key
   - Kosten: ca. $0.001 - $0.01 pro PDF (sehr günstig!)

2. **Kosten trägt der API Key Inhaber**
   - Wer den API Key nutzt, bezahlt die OpenAI Kosten
   - **NIEMALS API Keys teilen!**

3. **Lokale Daten bleiben beim Löschen**
   - `docker-compose down` löscht KEINE Daten
   - Nur `docker-compose down -v` löscht Volumes
   - `data/` Verzeichnis bleibt immer erhalten

---

## 📂 Daten-Speicherorte

```
studien-rag-assistent/
├── data/
│   ├── uploads/                  ← Hochgeladene PDFs (persistent!)
│   │   ├── vorlesung1.pdf
│   │   └── skript2.pdf
│   └── chroma_db/                ← Vektordatenbank (persistent!)
│       ├── chroma.sqlite3
│       └── [Embedding-Daten]
│
└── .env                          ← API Key (NIEMALS committen!)
```

**Persistenz:**
- ✅ PDFs bleiben nach Container-Neustart erhalten
- ✅ ChromaDB-Daten bleiben erhalten
- ✅ Auch nach `docker-compose down`
- ❌ Nur bei `docker-compose down -v` werden Volumes gelöscht

---

## 🎓 Setup für Studierende (Isolation garantiert)

### Variante 1: Jeder lädt das Projekt herunter

```bash
# Student A
git clone <repo-url> student-a
cd student-a
cp .env.example .env
# API Key eintragen
docker-compose -f docker/docker-compose.yml up -d

# Student B
git clone <repo-url> student-b
cd student-b
cp .env.example .env
# Anderen API Key eintragen!
docker-compose -f docker/docker-compose.yml up -d
```

**Ergebnis:**
- Zwei komplett getrennte Instanzen
- Zwei verschiedene `data/` Verzeichnisse
- Keine Verbindung zwischen A und B

### Variante 2: ZIP-Download (noch einfacher)

1. **Projekt als ZIP herunterladen**
2. **ZIP entpacken** in eigenes Verzeichnis
3. **Eigenen API Key** in `.env` eintragen
4. **Docker starten**

Jeder hat seine eigene ZIP → eigene Daten!

---

## 🔒 Sicherheits-Checkliste für Dozenten

Wenn du das für Studierende bereitstellst:

- [ ] ✅ Weise darauf hin, dass jeder seinen eigenen API Key braucht
- [ ] ✅ Warne davor, API Keys zu teilen
- [ ] ✅ Erkläre, dass Daten lokal bleiben
- [ ] ✅ Informiere über geschätzte Kosten (ca. $0.01 pro PDF)
- [ ] ✅ Stelle sicher, dass `.env` in `.gitignore` ist (bereits gemacht!)
- [ ] ✅ Optional: Biete einen Demo-Key für erste Tests an (mit Rate Limiting!)

---

## 🧪 Isolation testen

```bash
# Terminal 1 - Student A
cd student-a
docker-compose -f docker/docker-compose.yml up -d
# Öffne: http://localhost:8501
# Lade PDF "A.pdf" hoch

# Terminal 2 - Student B
cd student-b
docker-compose -f docker/docker-compose.yml up -d
# Öffne: http://localhost:8502  (anderer Port!)
# Lade PDF "B.pdf" hoch

# Prüfen:
ls student-a/data/uploads/  # Sollte nur A.pdf zeigen
ls student-b/data/uploads/  # Sollte nur B.pdf zeigen
```

**Wenn das funktioniert: ✅ Perfekte Isolation!**

---

## 🚫 Was NICHT passiert

❌ **NICHT:** Zentrale Datenbank, auf die alle zugreifen
❌ **NICHT:** Cloud-Speicherung der PDFs
❌ **NICHT:** Geteilte ChromaDB zwischen Nutzern
❌ **NICHT:** Synchronisation zwischen Containern
❌ **NICHT:** Netzwerk-Zugriff zwischen Studierenden
❌ **NICHT:** Dauerhafte Speicherung bei OpenAI

---

## ✅ Was TATSÄCHLICH passiert

✅ **JA:** Jeder Studierende hat eigenes `data/` Verzeichnis
✅ **JA:** Container mountet nur lokales `data/` Verzeichnis
✅ **JA:** ChromaDB läuft lokal im Container mit lokalem Volume
✅ **JA:** PDFs bleiben auf dem eigenen Computer
✅ **JA:** OpenAI erhält nur Text-Chunks für Embeddings
✅ **JA:** Vollständige Isolation zwischen Nutzern

---

## 🆘 Häufige Fragen

### "Können andere Studierende meine PDFs sehen?"

**NEIN!** Jeder hat sein eigenes `data/` Verzeichnis. Es gibt keine Verbindung zwischen den Containern.

### "Werden meine Daten in die Cloud hochgeladen?"

**NEIN!** Alles bleibt lokal. Nur Text-Chunks werden an OpenAI für Embeddings gesendet (API-Standard).

### "Was passiert, wenn ich den Container lösche?"

`docker-compose down` → Container weg, **ABER Daten bleiben!**
`docker-compose down -v` → Container UND Volumes weg (Daten gelöscht!)

### "Wie viel kostet das?"

**Ca. $0.001 - $0.01 pro PDF**, abhängig von:
- Seitenzahl
- Text-Menge
- Anzahl der Fragen

Beispiel: 100 PDFs + 1000 Fragen = ca. $5-10

### "Kann ich offline arbeiten?"

**Teilweise:**
- ✅ Container kann offline starten
- ✅ ChromaDB funktioniert offline
- ❌ PDF-Processing braucht OpenAI API (online)
- ❌ Fragen beantworten braucht OpenAI API (online)

---

## 📝 Zusammenfassung

**Kurz gesagt:**

> Jeder Studierende lädt das Projekt herunter, hat seine eigenen Daten in seinem eigenen `data/` Ordner, und der Docker-Container greift nur auf dieses lokale Verzeichnis zu. Es gibt KEINE Verbindung zwischen verschiedenen Studierenden!

**100% Isolation garantiert! ✅**

---

**Bei Fragen zur Datenschutz-Konfiguration: Öffne ein Issue!**
