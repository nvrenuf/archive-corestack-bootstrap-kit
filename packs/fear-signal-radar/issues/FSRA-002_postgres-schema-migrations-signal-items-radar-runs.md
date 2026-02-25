Title: FSRA-002 Postgres schema + migrations for signal_items and radar_runs
Target Version: 0.1.0
Priority: P0
Labels: pack:fear-signal-radar, fsra, mvp, database, migration, security
Owner:
Context:
Persistent storage is required to dedupe, audit, and compare radar snapshots. This issue defines initial tables and indexes for ingested signal items and run metadata.
Scope:
- Create initial SQL migration with `signal_items` and `radar_runs`.
- Add indexes for lookup and run reporting.
- Enforce uniqueness on normalized content hash to prevent duplicate records.
Non-Goals:
- ORM integration.
- Historical trend tables beyond MVP requirements.
- Dashboard read APIs.
Security Requirements:
- Corestack direct internet access remains prohibited; DB is internal-only.
- Collector path remains write-only through ingest; no direct collector DB credentials.
- Persist sanitized text only; raw unsafe payloads must not be stored.
- Add bounded field sizes to reduce oversized payload risk.
- Maintain fetch traceability fields for audit logging.
Acceptance Criteria (testable bullets):
- `migrations/001_init.sql` exists and creates tables `signal_items` and `radar_runs`.
- `signal_items` includes columns for `id`, `topic_id`, `source`, `source_item_id`, `url`, `content_hash`, `published_at`, `ingested_at`, `payload_json`.
- `radar_runs` includes columns for `id`, `topic_id`, `started_at`, `finished_at`, `status`, `items_scanned`, `items_ingested`.
- `migrations/001_init.sql` defines unique constraint/index on `signal_items(content_hash)`.
- Migration includes indexes on `signal_items(topic_id, source, published_at)` and `radar_runs(topic_id, started_at)`.
- Migration applies cleanly on an empty Postgres instance using repo migration runner.
Implementation Notes:
- Prefer `jsonb` for structured payload metadata.
- Use `timestamptz` for all temporal fields.
- Ensure idempotent rollback notes are included in migration header comments.
Deliverables (file paths):
- migrations/001_init.sql
Dependencies:
- FSRA-001
Definition of Done:
- Migration is committed and verified on fresh DB.
- Table/index definitions are documented in migration comments.
- Dedupe uniqueness is enforced by database constraints.
