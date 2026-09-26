#!/usr/bin/env bash
set -euo pipefail

MOCK_SERVER="${MOCK_SERVER:-./backend-data-server/data-server}"
MOCK_PORT="${MOCK_PORT:-28462}"

if [[ ! -x "$MOCK_SERVER" ]]; then
    echo "Mock server not found or not executable: $MOCK_SERVER" >&2
    echo "Set MOCK_SERVER=/path/to/data-server to override." >&2
    exit 1
fi

echo "Starting Postgres..."
docker compose up -d db

echo "Waiting for Postgres..."
until docker compose exec -T db pg_isready -U app -d app >/dev/null 2>&1; do
    sleep 1
done

echo "Applying schema..."
docker compose exec -T db psql -U app -d app < schema.sql

echo "Starting mock server on port $MOCK_PORT..."
"$MOCK_SERVER" --port "$MOCK_PORT" &
MOCK_PID=$!

echo "Starting API..."
uvicorn api:app &
API_PID=$!

cleanup() {
    kill "$MOCK_PID" "$API_PID" 2>/dev/null || true
    wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

wait