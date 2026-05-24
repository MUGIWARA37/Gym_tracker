# Smart Gym Workout Tracker

Smart Gym Workout Tracker is a full-stack fitness management platform built with Django REST Framework and Vue 3.

```
┌──────────────┐      HTTP/JSON      ┌────────────────────┐
│   Vue SPA    │  <--------------->  │  Django REST API   │
└──────────────┘                     └─────────┬──────────┘
                                               │
                                               ▼
                                         PostgreSQL/SQLite
```

## Project overview

The app lets authenticated users manage workout plans, exercises, and live workout sessions with logs and timers.
It also tracks body progress, nutrition goals, and in-app notifications. Roles include User, Coach, and Admin.

## Technologies

- **Backend:** Django 5, Django REST Framework, SimpleJWT, drf-spectacular
- **Database:** SQLite (dev), PostgreSQL-ready via `DATABASE_URL`
- **Frontend:** Vue 3, Vue Router, Pinia, TailwindCSS
- **HTTP:** Axios (with JWT interceptors)
- **Charts:** Chart.js
- **Jobs:** django-cron (7‑day inactivity reminders)

## Prerequisites

- Python 3.11+
- Node 18+
- pip, npm

## Environment setup

Backend:

```bash
cp backend/.env.example backend/.env
```

Frontend:

```bash
cp frontend/.env.example frontend/.env
```

## Backend setup

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Running the project

Run the backend and frontend in separate terminals:

```bash
cd backend && python manage.py runserver
```

```bash
cd frontend && npm run dev
```

## API documentation

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`

## Scheduled reminders

For the 7-day inactivity reminder, run:

```bash
python manage.py runcrons
```

## Running tests

```bash
cd backend && pytest
cd frontend && npm run test
```

## Deployment (Docker Compose)

```bash
docker compose up --build
```

The Docker setup includes Django + PostgreSQL + Nginx. Nginx routes `/api/` to the backend,
serves the Vue `dist/` build for frontend routes, and exposes `/media/` for uploads.
