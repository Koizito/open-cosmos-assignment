# Open Cosmos Assignment

A small polling service that fetches data points from a mock time-series server, stores them in PostgreSQL, and exposes them via a REST API.

Data points are discarded based on two rules: age (older than 1 hour) and tags (`system` and `suspect`). End users see only non-discarded data. Administrators can see all data, including the reason each discarded point was excluded.

## Requirements

- Docker (with the `compose` plugin)
- Python 3.14+
- The provided mock data server binary at `./backend-data-server/data-server`

## Setup

Create a virtual environment and install the dependencies:

```bash
python -m venv oc_venv
source oc_venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
./run.sh
```

This script will:

1. Start PostgreSQL via Docker Compose.
2. Wait for the database to accept connections.
3. Apply `schema.sql` (creates the `readings` table).
4. Start the mock data server on port `28462`.
5. Start the API on port `8000`.

Press `Ctrl+C` to stop the mock server and the API. The PostgreSQL container keeps running; stop it with `docker compose down`.

### Configuration

The following environment variables are optional and have sensible defaults for local development.
They are read once at startup in config.py.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://app:app@localhost:5432/app` | PostgreSQL connection string |
| `ADMIN_TOKEN` | `secret` | Token required for the admin endpoint |
| `POLLER_URL` | `http://localhost:28462/` | Data source endpoint |
| `POLLER_INTERVAL` | `1` | Seconds between polls |

To override a value, set the environment variable before running `./run.sh`:

```bash
ADMIN_TOKEN=my-secret-token ./run.sh
```

## API

### `GET /readings`

Returns non-discarded data points. Both filters are optional and inclusive.

| Query parameter | Format | Description |
|---|---|---|
| `start_time` | ISO 8601 | Only return points at or after this time |
| `end_time` | ISO 8601 | Only return points at or before this time |

**Example:**

```bash
curl "http://localhost:8000/readings?start_time=2026-09-25T22:41:00Z&end_time=2026-09-25T22:42:00Z"
```

### `GET /admin/readings`

Returns all data points, including discarded ones. Each point includes a `discard_reasons` field listing why it was discarded (`[]` if it wasn't).

Both filters are optional and inclusive.

| Query parameter | Format | Description |
|---|---|---|
| `start_time` | ISO 8601 | Only return points at or after this time |
| `end_time` | ISO 8601 | Only return points at or before this time |

Requires the `X-Admin-Token` header.

**Example:**

```bash
curl -H "X-Admin-Token: secret" \
  "http://localhost:8000/admin/readings?start_time=2026-09-25T22:41:00Z&end_time=2026-09-25T22:42:00Z"
```

## Tests

The tests require the PostgreSQL container to be running:

```bash
docker compose up -d db
pytest
```

Note that the tests use the same database as development and will delete its contents on each run.