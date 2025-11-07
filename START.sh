#!/bin/bash

echo "========================================"
echo "Study Platform - Quick Start"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

echo "[1/3] Checking configuration..."
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo ""
    echo "OPENAI_API_KEY=sk-your-key-here"
    echo ""
    exit 1
fi

echo "[2/3] Starting all services..."
cd docker
docker-compose -f docker-compose-full.yml up -d

echo ""
echo "[3/3] Waiting for services to be ready..."
sleep 10

echo ""
echo "========================================"
echo "Services are starting!"
echo "========================================"
echo ""
echo "Frontend:     http://localhost:3000"
echo "Backend API:  http://localhost:8000"
echo "API Docs:     http://localhost:8000/api/docs"
echo "Neo4j:        http://localhost:7474"
echo "Streamlit:    http://localhost:8501"
echo ""
echo "Neo4j Login:"
echo "  Username: neo4j"
echo "  Password: studyplatform2024"
echo ""
echo "========================================"
echo ""
echo "To view logs: docker-compose -f docker/docker-compose-full.yml logs -f"
echo "To stop: docker-compose -f docker/docker-compose-full.yml down"
echo ""
