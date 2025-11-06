# 🚀 Setup-Anleitung - Schritt für Schritt

## ✅ Checkliste vor dem Start

- [x] OpenAI API Key in `.env` eingetragen
- [ ] Python 3.11+ installiert
- [ ] Virtuelle Umgebung erstellt
- [ ] Dependencies installiert
- [ ] Test-PDF vorbereitet

---

## 📋 Schritt-für-Schritt Anleitung

### 1️⃣ Python-Version prüfen

```bash
python --version
```

**Erwartete Ausgabe:** `Python 3.11.x` oder höher

❌ **Falls Python < 3.11:**
- Lade Python 3.11+ herunter: https://www.python.org/downloads/
- Installiere es und versuche es erneut

---

### 2️⃣ Virtuelle Umgebung erstellen

```bash
# Im Projekt-Verzeichnis:
python -m venv .venv
```

**Was passiert:** Erstellt einen `.venv` Ordner mit isolierter Python-Umgebung

---

### 3️⃣ Virtuelle Umgebung aktivieren

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**Erfolg:** Du siehst `(.venv)` vor deinem Prompt:
```
(.venv) C:\Users\EricChittka\Documents\MS_Github\studien-rag-assistent>
```

---

### 4️⃣ Dependencies installieren

```bash
pip install -r requirements.txt
```

**Was wird installiert:**
- ✅ LangChain (RAG Framework)
- ✅ ChromaDB (Vektordatenbank) ← **Automatisch installiert!**
- ✅ OpenAI (API Client)
- ✅ Streamlit (Web-Interface)
- ✅ PyPDF (PDF-Verarbeitung)
- ✅ Alle anderen Dependencies

**Dauer:** 2-5 Minuten

⚠️ **Mögliche Warnungen:** Ignoriere Warnings wie "pip version outdated" - nicht kritisch!

---

### 5️⃣ .env überprüfen

```bash
# Windows PowerShell
Get-Content .env

# Windows CMD
type .env
```

**Muss enthalten:**
```env
OPENAI_API_KEY=sk-proj-...dein-key...
```

✅ **Wichtig:** Der Key muss mit `sk-` beginnen!

---

### 6️⃣ Anwendung starten

```bash
python run.py
```

**Erwartete Ausgabe:**
```
============================================================
🎓 Studien-RAG-Assistent
============================================================

✅ Environment configuration loaded successfully
   - LLM Model: gpt-4o-mini
   - Embedding Model: text-embedding-3-small
   - ChromaDB Path: .\data\chroma_db

Starting Streamlit application...
============================================================

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

🎉 **Erfolg!** Der Browser öffnet sich automatisch.

---

## 🧪 Erste Schritte im Interface

### 1. PDF hochladen

1. **Seitenleiste öffnen** (falls nicht sichtbar, klicke auf `>` oben links)
2. **Klicke auf "PDF-Dateien auswählen"**
3. **Wähle eine Test-PDF aus** (z.B. Vorlesungsskript)
4. **Klicke "Dokumente verarbeiten"**

**Was passiert:**
- ✅ PDF wird gelesen
- ✅ Text wird in Chunks aufgeteilt
- ✅ Embeddings werden erstellt (OpenAI API Call)
- ✅ Chunks werden in ChromaDB gespeichert

**Dauer:** 10-30 Sekunden pro PDF (abhängig von Größe)

### 2. Erste Frage stellen

Beispiele:
```
"Was ist das Hauptthema dieses Dokuments?"
"Erkläre mir den Begriff [X] aus dem Dokument"
"Welche wichtigen Punkte werden in Kapitel 3 erwähnt?"
```

**Was passiert:**
- ✅ Deine Frage wird in Embedding umgewandelt
- ✅ Ähnliche Chunks werden aus ChromaDB abgerufen
- ✅ GPT-4o-mini generiert Antwort basierend auf Kontext
- ✅ Quellenangaben mit Seitenzahlen werden angezeigt

### 3. Quellenangaben prüfen

- Klicke auf **"📚 Quellenangaben"** unter der Antwort
- Sieh dir **Dateiname, Seitenzahl und Textausschnitt** an
- Verifiziere die Antwort anhand der Quellen

---

## 🐛 Troubleshooting

### Problem 1: "Python not found"

```bash
# Überprüfe Python-Installation
where python
```

**Lösung:** Installiere Python 3.11+ von https://www.python.org/

---

### Problem 2: "Cannot activate virtual environment"

**Windows PowerShell:**
```powershell
# Execution Policy ändern (einmalig)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Dann erneut versuchen
.venv\Scripts\Activate.ps1
```

---

### Problem 3: "pip install fails"

```bash
# pip updaten
python -m pip install --upgrade pip

# Erneut versuchen
pip install -r requirements.txt
```

---

### Problem 4: "OpenAI API error"

**Mögliche Ursachen:**
1. ❌ API Key falsch kopiert
2. ❌ API Key hat kein Guthaben
3. ❌ API Key hat keine Berechtigung

**Lösung:**
```bash
# .env überprüfen
type .env

# Key muss sein: OPENAI_API_KEY=sk-proj-...
# KEIN Leerzeichen, KEINE Anführungszeichen
```

**Guthaben prüfen:** https://platform.openai.com/account/billing/overview

---

### Problem 5: "Port 8501 already in use"

```bash
# Anderen Port verwenden
streamlit run src/ui.py --server.port=8502
```

---

### Problem 6: "Module not found"

```bash
# Stelle sicher, dass .venv aktiviert ist
# Du musst (.venv) im Prompt sehen!

# Falls nicht:
.venv\Scripts\activate

# Dependencies erneut installieren
pip install -r requirements.txt
```

---

## 📊 Verzeichnis-Struktur nach Installation

```
studien-rag-assistent/
├── .venv/                    ← Virtuelle Umgebung (NEU)
├── data/
│   ├── uploads/             ← PDFs werden hier gespeichert
│   └── chroma_db/           ← Vector-Store (automatisch erstellt)
├── src/                     ← Python-Code
├── .env                     ← Deine Konfiguration (mit API Key)
└── ...
```

---

## ✅ Erfolgs-Checkliste

Nach erfolgreichem Setup solltest du haben:

- ✅ `(.venv)` im Terminal-Prompt sichtbar
- ✅ Browser zeigt Streamlit-App auf http://localhost:8501
- ✅ Keine Error-Messages beim Start
- ✅ Seitenleiste mit "📄 Dokumente hochladen" sichtbar
- ✅ Test-PDF erfolgreich hochgeladen und verarbeitet
- ✅ Erste Frage erfolgreich beantwortet mit Quellenangaben

---

## 🎯 Nächste Schritte

1. **Teste mit deinen echten Vorlesungsunterlagen**
2. **Experimentiere mit verschiedenen Fragen**
3. **Passe Einstellungen in `.env` an** (optional)
4. **Gib Feedback** falls etwas nicht funktioniert

---

## 💡 Tipps für beste Ergebnisse

### PDF-Qualität
- ✅ Verwende text-basierte PDFs (keine Scans)
- ✅ PDFs sollten nicht passwortgeschützt sein
- ✅ Strukturierte Dokumente funktionieren besser

### Fragen stellen
- ✅ Sei spezifisch: "Erkläre X aus Kapitel 3" statt nur "Was ist X?"
- ✅ Nutze Follow-up-Fragen (Konversations-Memory!)
- ✅ Frage nach Zusammenfassungen, Erklärungen, Vergleichen

### Performance
- ✅ Erste Frage dauert länger (Cold Start)
- ✅ Große PDFs (>100 Seiten) brauchen mehr Zeit
- ✅ Mehrere kleine PDFs sind oft besser als eine große

---

## 🆘 Immer noch Probleme?

1. **Lies die vollständige Dokumentation:** `README.md`
2. **Check QUICKSTART.md** für alternative Methoden
3. **Öffne ein Issue** mit detaillierter Fehlerbeschreibung

---

**Viel Erfolg! 🎓**
