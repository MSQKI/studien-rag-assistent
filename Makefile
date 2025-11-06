.PHONY: help install install-dev run test lint format clean docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make run          - Run the application locally"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Clean up generated files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Running
run:
	python run.py

# Testing
test:
	pytest --cov=src --cov-report=term-missing --cov-report=html

test-quick:
	pytest -x --ff

test-unit:
	pytest -m unit

# Code Quality
lint:
	flake8 src/ tests/
	mypy src/
	bandit -r src/

format:
	black src/ tests/
	isort src/ tests/

format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Docker
docker-build:
	cd docker && docker-compose build

docker-up:
	cd docker && docker-compose up -d

docker-down:
	cd docker && docker-compose down

docker-logs:
	cd docker && docker-compose logs -f

# Development
dev-setup: install-dev
	@echo "Creating .env file from template..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Please edit .env and add your OpenAI API key"; fi
	@echo "Setup complete!"
