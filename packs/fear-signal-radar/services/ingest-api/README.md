# Ingest API (FSRA-003)

FastAPI write-only ingest service for Fear Signal Radar.

## Required env

- `INGEST_TOKEN`
- `INGEST_DB_HOST`
- `INGEST_DB_PORT`
- `INGEST_DB_NAME`
- `INGEST_DB_USER` (must be `ingest_writer`)
- `INGEST_DB_PASSWORD`
- `INGEST_MAX_BODY_BYTES` (optional; default `1048576`)

## Run locally

```bash
uvicorn app.main:create_app --factory --app-dir packs/fear-signal-radar/services/ingest-api --host 0.0.0.0 --port 8080
```
