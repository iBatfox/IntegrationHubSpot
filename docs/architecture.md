# Architecture Overview

This project is structured as a simple CRM/marketing automation MVP.

## Backend
- `backend/app/main.py` initializes FastAPI and registers API routers.
- `backend/app/core/` contains configuration, database session and security utilities.
- `backend/app/models/` defines SQLAlchemy entities for users, contacts, companies, deals, pipeline stages, email templates and activities.
- `backend/app/schemas/` contains Pydantic models for request validation and response serialization.
- `backend/app/crud/` implements repository-style access to the database.
- `backend/alembic/` includes migration support.

## Frontend
- Built with React + Vite.
- Contains login flow and pages for contacts, analytics and pipeline view.
- Uses a small API client in `frontend/src/api.ts`.

## Containerization
- `docker/docker-compose.yml` boots PostgreSQL, backend, frontend and nginx.
- nginx forwards `/api/` to backend and serves frontend at `/`.

## Extension points
- Add Bitrix24 integration by introducing new webhook/event connectors.
- Add email automation with scheduled tasks and template rendering.
- Add analytics dashboards by expanding the backend analytics APIs and frontend charts.
