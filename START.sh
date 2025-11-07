#!/bin/bash
set -e

echo ""
echo "========================================"
echo "  Studien-RAG-Assistent wird gestartet"
echo "========================================"
echo ""

if ! command -v docker &> /dev/null; then
    echo "FEHLER: Docker ist nicht installiert!"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "FEHLER: .env Datei nicht gefunden!"
    exit 1
fi

echo "[1/4] Stoppe alte Container..."
cd docker
docker-compose -f docker-compose-full.yml down 2>/dev/null || true

echo ""
echo "[2/4] Starte alle Services..."
docker-compose -f docker-compose-full.yml up -d

echo ""
echo "[3/4] Warte 10 Sekunden..."
sleep 10

echo ""
echo "========================================"
echo "  Start abgeschlossen!"
echo "========================================"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo ""

docker-compose -f docker-compose-full.yml logs -f
