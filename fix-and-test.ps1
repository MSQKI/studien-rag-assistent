# Fix and Test Script für Windows PowerShell
# Testet lokal und baut dann Docker neu

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Studien-RAG-Assistent - Fix & Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Lokalen Test
Write-Host "1. Teste lokale Version..." -ForegroundColor Yellow
Write-Host "   Starte Streamlit lokal..." -ForegroundColor Gray
Write-Host "   Drücke Ctrl+C zum Beenden" -ForegroundColor Gray
Write-Host ""

# Teste, ob .venv aktiviert ist
if ($env:VIRTUAL_ENV) {
    Write-Host "   ✅ Virtuelle Umgebung ist aktiv" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Virtuelle Umgebung nicht aktiv!" -ForegroundColor Red
    Write-Host "   Führe aus: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

# Starte lokale App
Write-Host ""
Write-Host "Öffne http://localhost:8501 im Browser" -ForegroundColor Cyan
Write-Host "Teste: PDF hochladen, dann Dokument löschen" -ForegroundColor Cyan
Write-Host "Prüfe: Chunks-Zahl sollte auf 0 gehen!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Drücke Ctrl+C wenn fertig, dann Enter für Docker-Build" -ForegroundColor Yellow
Write-Host ""

try {
    python run.py
} catch {
    Write-Host "App wurde gestoppt" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "2. Docker Build" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$response = Read-Host "Docker Image neu bauen? (j/n)"

if ($response -eq "j" -or $response -eq "J") {
    Write-Host ""
    Write-Host "Baue Docker Image..." -ForegroundColor Yellow
    Write-Host "Das dauert ca. 5-10 Minuten..." -ForegroundColor Gray
    Write-Host ""

    Set-Location docker

    # Stoppe alte Container
    Write-Host "Stoppe alte Container..." -ForegroundColor Gray
    docker-compose down

    # Baue neu
    Write-Host "Baue neues Image..." -ForegroundColor Gray
    docker-compose build --no-cache

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Build erfolgreich!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Starte Container..." -ForegroundColor Yellow
        docker-compose up -d

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Container gestartet!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Öffne http://localhost:8501" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Logs anschauen:" -ForegroundColor Gray
            Write-Host "  docker-compose logs -f" -ForegroundColor Gray
            Write-Host ""
        } else {
            Write-Host ""
            Write-Host "❌ Fehler beim Starten!" -ForegroundColor Red
            Write-Host "Prüfe Logs: docker-compose logs" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "❌ Build fehlgeschlagen!" -ForegroundColor Red
        Write-Host "Prüfe die Fehlermeldungen oben" -ForegroundColor Yellow
    }

    Set-Location ..
} else {
    Write-Host ""
    Write-Host "Docker-Build übersprungen" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fertig!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
