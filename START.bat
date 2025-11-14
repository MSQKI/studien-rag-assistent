@echo off
REM ========================================
REM  Studien-RAG-Assistent - Start Script
REM  Windows Edition
REM ========================================

echo.
echo ========================================
echo   Studien-RAG-Assistent wird gestartet
echo ========================================
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Docker ist nicht installiert oder laeuft nicht!
    echo Bitte installiere Docker Desktop von https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo FEHLER: .env Datei nicht gefunden!
    echo Bitte erstelle eine .env Datei mit deinem OpenAI API Key.
    echo.
    echo Beispiel:
    echo OPENAI_API_KEY=sk-...dein-key-hier...
    echo.
    pause
    exit /b 1
)

echo [1/4] Stoppe alte Container falls vorhanden...
cd docker
docker-compose -f docker-compose-full.yml down 2>nul

echo.
echo [2/4] Starte alle Services (das kann 1-2 Minuten dauern)...
docker-compose -f docker-compose-full.yml up -d

echo.
echo [3/4] Warte bis alle Services bereit sind...
timeout /t 10 /nobreak >nul

echo.
echo [4/4] Ueberpruefe Status...
docker-compose -f docker-compose-full.yml ps

echo.
echo ========================================
echo   Start abgeschlossen!
echo ========================================
echo.
echo Deine Studienplattform ist jetzt verfuegbar:
echo.
echo   Frontend (Hauptanwendung): http://localhost:3000
echo   Backend API Docs:          http://localhost:8000/docs
echo   Neo4j Browser:             http://localhost:7474
echo.
echo Druecke Ctrl+C um die Logs zu beenden (Services laufen weiter)
echo Zum Stoppen: stop.bat ausfuehren
echo.
echo ========================================

REM Show logs
docker-compose -f docker-compose-full.yml logs -f
