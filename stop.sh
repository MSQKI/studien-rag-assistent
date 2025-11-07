#!/bin/bash
# ========================================
#  Studien-RAG-Assistent - Stop Script
#  macOS / Linux Edition
# ========================================

echo ""
echo "========================================"
echo "  Studien-RAG-Assistent wird gestoppt"
echo "========================================"
echo ""

cd docker
docker-compose -f docker-compose-full.yml down

echo ""
echo "========================================"
echo "  Alle Services wurden gestoppt!"
echo "========================================"
echo ""
echo "Hinweis: Deine Daten (Dokumente, Karteikarten, Graph)"
echo "bleiben erhalten und sind beim nächsten Start wieder da."
echo ""
