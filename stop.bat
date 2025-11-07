@echo off
REM ========================================
REM  Studien-RAG-Assistent - Stop Script
REM  Windows Edition
REM ========================================

echo.
echo ========================================
echo   Studien-RAG-Assistent wird gestoppt
echo ========================================
echo.

cd docker
docker-compose -f docker-compose-full.yml down

echo.
echo ========================================
echo   Alle Services wurden gestoppt!
echo ========================================
echo.
echo Hinweis: Deine Daten (Dokumente, Karteikarten, Graph)
echo bleiben erhalten und sind beim naechsten Start wieder da.
echo.
pause
