CREATE TABLE IF NOT EXISTS signal_items (
    id UUID PRIMARY KEY,
    topic_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    content_type TEXT NOT NULL,
    source_id TEXT NULL,
    url TEXT NOT NULL,
    author TEXT NULL,
    published_at TIMESTAMPTZ NULL,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    title TEXT NULL,
    text_snippet TEXT NULL,
    engagement_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    tags_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    language TEXT NULL,
    hash TEXT NOT NULL,
    raw_ref_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    CONSTRAINT signal_items_hash_unique UNIQUE (hash)
);

CREATE INDEX IF NOT EXISTS idx_signal_items_topic_collected_at
    ON signal_items (topic_id, collected_at);

CREATE INDEX IF NOT EXISTS idx_signal_items_topic_platform
    ON signal_items (topic_id, platform);

CREATE TABLE IF NOT EXISTS radar_runs (
    run_id UUID PRIMARY KEY,
    topic_id TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ NULL,
    time_window_days INTEGER NOT NULL,
    collector_versions JSONB NOT NULL DEFAULT '{}'::jsonb,
    counts_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL,
    error_text TEXT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ingest_writer') THEN
        CREATE ROLE ingest_writer LOGIN PASSWORD 'ingest_writer';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'synth_reader') THEN
        CREATE ROLE synth_reader LOGIN PASSWORD 'synth_reader';
    END IF;
END
$$;

DO $$
BEGIN
    EXECUTE format('GRANT CONNECT ON DATABASE %I TO ingest_writer', current_database());
    EXECUTE format('GRANT CONNECT ON DATABASE %I TO synth_reader', current_database());
END
$$;

GRANT USAGE ON SCHEMA public TO ingest_writer;
GRANT USAGE ON SCHEMA public TO synth_reader;

REVOKE ALL PRIVILEGES ON TABLE signal_items FROM ingest_writer;
REVOKE ALL PRIVILEGES ON TABLE radar_runs FROM ingest_writer;
REVOKE ALL PRIVILEGES ON TABLE signal_items FROM synth_reader;
REVOKE ALL PRIVILEGES ON TABLE radar_runs FROM synth_reader;

GRANT INSERT ON TABLE signal_items TO ingest_writer;
GRANT INSERT, UPDATE ON TABLE radar_runs TO ingest_writer;
GRANT SELECT ON TABLE radar_runs TO ingest_writer;

GRANT SELECT ON TABLE signal_items TO synth_reader;
GRANT SELECT ON TABLE radar_runs TO synth_reader;
