.PHONY: help install dev up down test lint format clean

help:
	@echo "AlphaMind AI Makefile Commands:"
	@echo "  make install   Install dependencies"
	@echo "  make up        Start local Docker infrastructure"
	@echo "  make down      Stop local Docker infrastructure"
	@echo "  make dev       Run backend and frontend dev servers"
	@echo "  make test      Run PyTest backend and Jest frontend tests"
	@echo "  make lint      Run Ruff, Mypy, ESLint checks"
	@echo "  make format    Run Black, Ruff auto-formatter"

install:
	pip install -e ".[dev]"
	cd apps/frontend && npm install

up:
	docker-compose up -d

down:
	docker-compose down

dev-backend:
	cd apps/backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd apps/frontend && npm run dev

test:
	pytest --cov=apps/backend/app --cov=packages
	cd apps/frontend && npm test

lint:
	ruff check .
	mypy apps/backend/app packages
	cd apps/frontend && npm run lint

format:
	black .
	ruff check . --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
