#!/usr/bin/env bash
set -euo pipefail

# run_stack.sh
# Convenience script to build and run the local stack and apply migrations + seeds.
# Usage: run from repository root or from inside hubspot_clone/docker
#   cd hubspot_clone/docker && ./run_stack.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT_DIR/docker"
BACKEND_DIR="$ROOT_DIR/backend"

ENV_EXAMPLE="$BACKEND_DIR/.env.example"
ENV_FILE="$BACKEND_DIR/.env"

echo "Using repo root: $ROOT_DIR"

if [ ! -f "$ENV_FILE" ]; then
  if [ -f "$ENV_EXAMPLE" ]; then
    echo "No .env found for backend — copying from .env.example"
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "Please review and update $ENV_FILE (SECRET_KEY, passwords, CORS_ORIGINS) if needed."
  else
    echo "Missing $ENV_EXAMPLE — cannot create .env. Exiting." >&2
    exit 1
  fi
fi

cd "$COMPOSE_DIR"

echo "Building and starting docker-compose services..."
docker compose up -d --build

echo "Waiting for Postgres to become ready..."
MAX_WAIT=60
WAITED=0
until docker compose exec -T db pg_isready -U hubspot >/dev/null 2>&1 || [ $WAITED -ge $MAX_WAIT ]; do
  echo "  Postgres is not ready yet... ($WAITED/$MAX_WAIT)"
  sleep 2
  WAITED=$((WAITED+2))
done

if [ $WAITED -ge $MAX_WAIT ]; then
  echo "Postgres did not become ready in time. Check container logs: docker compose logs db" >&2
  exit 2
fi

echo "Applying Alembic migrations inside backend container..."
docker compose exec backend bash -lc "cd /app && python -m alembic -c /app/alembic.ini upgrade head"

echo "Seeding pipeline stages (idempotent)..."
docker compose exec db psql -U hubspot -d hubspot -c "INSERT INTO pipeline_stages (name, step_order) VALUES ('Lead',1) ON CONFLICT (name) DO NOTHING;"
docker compose exec db psql -U hubspot -d hubspot -c "INSERT INTO pipeline_stages (name, step_order) VALUES ('Qualified',2) ON CONFLICT (name) DO NOTHING;"
docker compose exec db psql -U hubspot -d hubspot -c "INSERT INTO pipeline_stages (name, step_order) VALUES ('Proposal',3) ON CONFLICT (name) DO NOTHING;"
docker compose exec db psql -U hubspot -d hubspot -c "INSERT INTO pipeline_stages (name, step_order) VALUES ('Won',4) ON CONFLICT (name) DO NOTHING;"
docker compose exec db psql -U hubspot -d hubspot -c "INSERT INTO pipeline_stages (name, step_order) VALUES ('Lost',5) ON CONFLICT (name) DO NOTHING;"

echo "All done. Services are running. Quick checks:"
echo "  docker compose ps"
echo "  docker compose logs -f backend"

echo "Note: frontend dev server runs on port 5173, backend on 8000, nginx on 8080 (see docker-compose.yml)."
echo "To create an admin user via API (example):"
echo "  curl -X POST http://localhost:8000/api/auth/register -H 'Content-Type: application/json' -d '{\"email\":\"admin@example.com\",\"password\":\"yourpassword\",\"full_name\":\"Admin\",\"role\":\"admin\"}'"

exit 0

