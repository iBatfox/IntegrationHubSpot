# AI Agent Guidance for HubSpot Clone

## Purpose
This repository is a local CRM/marketing automation MVP. The agent should help with backend API features, frontend UI pages, containerization, and integration-extension work while preserving the lightweight, minimal architecture.

## Key areas
- `backend/`: FastAPI backend using SQLAlchemy, Alembic, JWT authentication, and repository-style CRUD.
- `frontend/`: React + Vite frontend with pages for login, contacts, dashboard, and pipeline view.
- `docker/`: Docker Compose for PostgreSQL, backend, frontend, and nginx reverse proxy.
- `docs/architecture.md`: architecture overview and extension points.

## Recommended workflow
- Use `docker/docker-compose.yml` for a full local development stack.
- Use `backend/.env.example` as the environment reference for backend configuration.
- Backend API docs are available at `/docs` when the backend is running.

## Build / run commands
- Full stack: `cd docker && docker compose up --build`
- Backend only: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`
- Frontend only: `cd frontend && npm install && npm run dev`

## What the agent should know
- Do not introduce unnecessary architecture complexity or large refactors without explicit request.
- Preserve existing API routes and database schema behavior when changing backend logic.
- Backend configuration lives in `backend/app/core/config.py` and is driven by `.env` values.
- The frontend uses `frontend/src/api.ts` for API calls and basic React Router navigation.
- `nginx/nginx.conf` is used for local proxying between frontend and backend.

## Useful references
- [README](README.md)
- [Architecture overview](docs/architecture.md)

## When to ask instead of acting
- Before modifying database migrations or schemas.
- Before changing authentication or security logic.
- Before upgrading package versions.
- Before deleting files or changing production configuration.
