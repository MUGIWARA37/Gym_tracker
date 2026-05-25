.PHONY: run build build-frontend-dist clean ensure-env up

FRONTEND_IMAGE ?= gym_tracker-frontend
FRONTEND_BUILD_CONTAINER ?= gym_tracker-frontend-build
SEED_USERNAME ?= demo
SEED_EMAIL ?= demo@example.com
SEED_PASSWORD ?= DemoPass123!

run: ensure-env build-frontend-dist
	docker compose build backend
	docker compose up -d db backend
	docker compose exec -T backend python manage.py migrate
	docker compose exec -T backend python manage.py seed_demo --username $(SEED_USERNAME) --email $(SEED_EMAIL) --password $(SEED_PASSWORD)
	docker compose up -d

build:
	docker compose build frontend backend

ensure-env:
	[ -f backend/.env ] || cp backend/.env.example backend/.env
	[ -f frontend/.env ] || cp frontend/.env.example frontend/.env

clean:
	rm -rf backend/.env frontend/.env
	mkdir -p frontend/dist
	rm -rf frontend/dist/* frontend/node_modules
	rm -rf backend/venv backend/db.sqlite3 backend/staticfiles
	find backend -type d -name "__pycache__" -prune -exec rm -rf {} +
	find backend -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find backend -type f -name "*.pyc" -delete

build-frontend-dist:
	docker compose build frontend
	mkdir -p frontend/dist
	rm -rf frontend/dist/*
	docker create --name $(FRONTEND_BUILD_CONTAINER) $(FRONTEND_IMAGE) >/dev/null
	docker cp $(FRONTEND_BUILD_CONTAINER):/app/dist/. frontend/dist
	docker rm $(FRONTEND_BUILD_CONTAINER) >/dev/null

up:
	docker compose up -d
