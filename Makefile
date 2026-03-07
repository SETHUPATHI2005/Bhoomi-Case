.PHONY: help build up down logs health test install dev prod clean docs

help:
	@echo "Land Cases Search - Available Commands"
	@echo "======================================="
	@echo "  make install    - Install Python dependencies"
	@echo "  make dev        - Start development server (with auto-reload)"
	@echo "  make prod       - Start production server (docker-compose)"
	@echo "  make up         - Start Docker containers"
	@echo "  make down       - Stop Docker containers"
	@echo "  make logs       - View Docker logs"
	@echo "  make test       - Run test suite"
	@echo "  make health     - Check API health"
	@echo "  make build      - Build Docker image"
	@echo "  make clean      - Clean cache and temporary files"
	@echo "  make docs       - Open API documentation"

install:
	pip install -r backend/requirements.txt

dev:
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

build:
	docker-compose build

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f backend

health:
	python -c "import requests; r = requests.get('http://localhost:8000/health'); print(r.json() if r.status_code == 200 else 'UNHEALTHY')"

test:
	pytest -q backend/tests --tb=short

test-verbose:
	pytest -v backend/tests

test-coverage:
	pytest --cov=backend.app --cov-report=html backend/tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov *.egg-info dist build
	rm -f land_cases.db

docs:
	python -m webbrowser http://localhost:8000/docs

setup-env:
	cp .env.example .env
	@echo ".env file created. Please update with your settings."
