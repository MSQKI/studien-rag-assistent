# Fix API Key für Docker
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API Key Fix für Docker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Prüfe aktuelles Verzeichnis
$currentDir = Get-Location
Write-Host "Aktuelles Verzeichnis: $currentDir" -ForegroundColor Gray

# Stelle sicher, dass wir im Projekt-Root sind
if ($currentDir.Path -like "*\docker") {
    Write-Host "⚠️  Du bist im docker/ Verzeichnis!" -ForegroundColor Yellow
    Write-Host "Wechsle ins Projekt-Root..." -ForegroundColor Yellow
    Set-Location ..
}

Write-Host ""
Write-Host "1. Prüfe .env Datei..." -ForegroundColor Yellow

if (!(Test-Path .env)) {
    Write-Host "   ❌ .env nicht gefunden!" -ForegroundColor Red
    Write-Host "   Erstelle .env aus .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "   ✅ .env erstellt" -ForegroundColor Green
} else {
    Write-Host "   ✅ .env existiert" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. Prüfe API Key..." -ForegroundColor Yellow

$apiKeyLine = Get-Content .env | Select-String "OPENAI_API_KEY" | Select-Object -First 1

if ($apiKeyLine -match "your_openai_api_key_here" -or $apiKeyLine -match "^OPENAI_API_KEY=\s*$") {
    Write-Host "   ❌ API Key nicht gesetzt!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Öffne .env im Editor..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "WICHTIG:" -ForegroundColor Red
    Write-Host "  - Ersetze 'your_openai_api_key_here' mit deinem echten Key" -ForegroundColor Yellow
    Write-Host "  - Key muss mit 'sk-' oder 'sk-proj-' beginnen" -ForegroundColor Yellow
    Write-Host "  - KEINE Anführungszeichen verwenden!" -ForegroundColor Yellow
    Write-Host "  - KEINE Leerzeichen!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Beispiel:" -ForegroundColor Gray
    Write-Host "  OPENAI_API_KEY=sk-proj-abc123xyz" -ForegroundColor Gray
    Write-Host ""

    notepad .env

    Write-Host ""
    Read-Host "Drücke Enter wenn du den API Key eingetragen hast"

    # Erneut prüfen
    $apiKeyLine = Get-Content .env | Select-String "OPENAI_API_KEY" | Select-Object -First 1

    if ($apiKeyLine -match "sk-") {
        Write-Host "   ✅ API Key gefunden!" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  API Key sieht nicht korrekt aus!" -ForegroundColor Red
        Write-Host "   Aktuelle Zeile: $apiKeyLine" -ForegroundColor Yellow
        $response = Read-Host "Trotzdem fortfahren? (j/n)"
        if ($response -ne "j" -and $response -ne "J") {
            Write-Host "Abgebrochen." -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "   ✅ API Key ist gesetzt" -ForegroundColor Green
    Write-Host "   Key beginnt mit: $(($apiKeyLine -split '=')[1].Substring(0, 8))..." -ForegroundColor Gray
}

Write-Host ""
Write-Host "3. Docker neu starten..." -ForegroundColor Yellow

Set-Location docker

Write-Host "   Stoppe Container..." -ForegroundColor Gray
docker-compose down | Out-Null

Write-Host "   Starte Container neu..." -ForegroundColor Gray
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Container gestartet" -ForegroundColor Green
    Write-Host ""
    Write-Host "4. Prüfe Logs..." -ForegroundColor Yellow
    Write-Host ""

    Start-Sleep -Seconds 3

    $logs = docker-compose logs --tail=20 2>&1

    if ($logs -match "Connection error") {
        Write-Host "   ❌ Immer noch Connection Error!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Debugging:" -ForegroundColor Yellow
        Write-Host "   1. In Container einloggen:" -ForegroundColor Gray
        Write-Host "      docker-compose exec rag-assistant /bin/bash" -ForegroundColor Gray
        Write-Host "   2. API Key prüfen:" -ForegroundColor Gray
        Write-Host "      echo `$OPENAI_API_KEY" -ForegroundColor Gray
        Write-Host ""
    } elseif ($logs -match "HTTP/1.1 200 OK") {
        Write-Host "   ✅ OpenAI API verbunden!" -ForegroundColor Green
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "✅ Alles funktioniert!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Öffne: http://localhost:8501" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "   ⚠️  Status unklar, prüfe Logs:" -ForegroundColor Yellow
        Write-Host "      docker-compose logs -f" -ForegroundColor Gray
        Write-Host ""
    }

} else {
    Write-Host "   ❌ Fehler beim Starten!" -ForegroundColor Red
    Write-Host "   Prüfe: docker-compose logs" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "Fertig!" -ForegroundColor Cyan
