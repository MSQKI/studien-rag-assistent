@echo off
echo ========================================
echo Study Platform - Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/3] Checking configuration...
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo.
    echo Please create a .env file with your OpenAI API key:
    echo.
    echo OPENAI_API_KEY=sk-your-key-here
    echo.
    pause
    exit /b 1
)

echo [2/3] Starting all services...
cd docker
docker-compose -f docker-compose-full.yml up -d

echo.
echo [3/3] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo Services are starting!
echo ========================================
echo.
echo Frontend:     http://localhost:3000
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/api/docs
echo Neo4j:        http://localhost:7474
echo Streamlit:    http://localhost:8501
echo.
echo Neo4j Login:
echo   Username: neo4j
echo   Password: studyplatform2024
echo.
echo ========================================
echo.
echo Opening frontend in browser...
start http://localhost:3000
echo.
echo To view logs: docker-compose -f docker/docker-compose-full.yml logs -f
echo To stop: docker-compose -f docker/docker-compose-full.yml down
echo.
pause
