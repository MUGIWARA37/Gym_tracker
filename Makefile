.PHONY: run build build-frontend-dist clean up

FRONTEND_IMAGE ?= gym_tracker-frontend
FRONTEND_BUILD_CONTAINER ?= gym_tracker-frontend-build

run: build-frontend-dist
	docker compose build backend
	docker compose up -d

build:
	docker compose build frontend backend

clean:
	rm -rf backend/.env frontend/.env
	rm -rf frontend/dist frontend/node_modules
	rm -rf backend/venv backend/db.sqlite3 backend/staticfiles
	find backend -type d -name "__pycache__" -prune -exec rm -rf {} +
	find backend -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find backend -type f -name "*.pyc" -delete

build-frontend-dist:
	docker compose build frontend
	rm -rf frontend/dist
	docker create --name $(FRONTEND_BUILD_CONTAINER) $(FRONTEND_IMAGE) >/dev/null
	docker cp $(FRONTEND_BUILD_CONTAINER):/app/dist frontend/dist
	docker rm $(FRONTEND_BUILD_CONTAINER) >/dev/null

up:
	docker compose up -d
