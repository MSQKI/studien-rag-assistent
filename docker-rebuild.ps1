# Docker Image NEU bauen und starten
# Dieses Script behebt das API Key Problem in Docker

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Image Rebuild" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob .env existiert
if (!(Test-Path .env)) {
    Write-Host "❌ .env nicht gefunden!" -ForegroundColor Red
    Write-Host "Erstelle zuerst .env mit API Key!" -ForegroundColor Yellow
    exit 1
}

# Prüfe API Key
$apiKey = Get-Content .env | Select-String "OPENAI_API_KEY=" | Select-Object -First 1
if (!$apiKey -or $apiKey -match "your_openai_api_key_here") {
    Write-Host "❌ API Key in .env nicht gesetzt!" -ForegroundColor Red
    Write-Host "Öffne .env und trage deinen API Key ein" -ForegroundColor Yellow
    notepad .env
    exit 1
}

Write-Host "✅ .env gefunden mit API Key" -ForegroundColor Green
Write-Host ""

# Wechsle ins docker/ Verzeichnis
Set-Location docker

Write-Host "1. Stoppe alte Container..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "2. Lösche altes Image..." -ForegroundColor Yellow
docker rmi docker-rag-assistant 2>$null
docker rmi docker_rag-assistant 2>$null

Write-Host ""
Write-Host "3. Baue NEUES Image (5-10 Minuten)..." -ForegroundColor Yellow
Write-Host "   Das dauert, weil --no-cache verwendet wird" -ForegroundColor Gray
Write-Host ""

docker-compose build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Build fehlgeschlagen!" -ForegroundColor Red
    Write-Host "Prüfe die Fehlermeldungen oben" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

Write-Host ""
Write-Host "✅ Build erfolgreich!" -ForegroundColor Green
Write-Host ""

Write-Host "4. Starte Container..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Start fehlgeschlagen!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host ""
Write-Host "✅ Container gestartet!" -ForegroundColor Green
Write-Host ""

Write-Host "5. Warte auf Startup..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "6. Prüfe Logs..." -ForegroundColor Yellow
Write-Host ""

$logs = docker-compose logs --tail=30 2>&1

# Prüfe auf Erfolg
if ($logs -match "HTTP/1.1 200 OK") {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ ✅ ✅ ERFOLG! ✅ ✅ ✅" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "OpenAI API verbunden!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Öffne im Browser:" -ForegroundColor Cyan
    Write-Host "  http://localhost:8501" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Logs anschauen:" -ForegroundColor Gray
    Write-Host "  cd docker" -ForegroundColor Gray
    Write-Host "  docker-compose logs -f" -ForegroundColor Gray
    Write-Host ""
} elseif ($logs -match "Connection error") {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ Immer noch Connection Error!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Debugging-Schritte:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Prüfe API Key im Container:" -ForegroundColor Yellow
    Write-Host "   docker-compose exec rag-assistant /bin/bash" -ForegroundColor Gray
    Write-Host "   echo `$OPENAI_API_KEY" -ForegroundColor Gray
    Write-Host "   exit" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Vollständige Logs:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. API Key auf OpenAI prüfen:" -ForegroundColor Yellow
    Write-Host "   https://platform.openai.com/account/api-keys" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "⚠️  Status unklar" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Prüfe Logs manuell:" -ForegroundColor Gray
    Write-Host "  docker-compose logs -f" -ForegroundColor Gray
    Write-Host ""
}

Set-Location ..

Write-Host ""
Write-Host "Fertig!" -ForegroundColor Cyan
