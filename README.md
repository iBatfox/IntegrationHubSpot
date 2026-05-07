# HubSpot Clone

Local MVP for a CRM and marketing automation exploration.

## Architecture
- `backend/`: FastAPI backend with SQLAlchemy, Alembic, JWT auth, CRM entities and automation API.
- `frontend/`: React + Vite minimal UI for login, contacts, dashboard and pipeline view.
- `docker/`: `docker-compose.yml` for backend, frontend, PostgreSQL and nginx.
- `nginx/`: reverse proxy configuration.
- `docs/`: architecture and usage notes.

## Quick start

1. Copy `.env.example` to `.env` in `backend/`.
2. Start services:

```bash
cd /hubspot_clone/docker
docker compose up --build
```

3. Open the frontend at `http://localhost:8080`.
4. API docs are available at `http://localhost:8000/docs`.

## Environment
Backend uses `.env` values from `backend/app/core/config.py`.

## Migrations

```bash
cd /hubspot_clone/backend
alembic upgrade head
```

## API Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/contacts/`
- `POST /api/contacts/`
- `GET /api/companies/`
- `GET /api/deals/`
- `GET /api/pipelines/`
- `GET /api/analytics/overview`
- `POST /api/automation/webhook`

## Notes
This is an MVP skeleton designed for further extension with email automation, OpenAI integration and third-party CRM connectors.
