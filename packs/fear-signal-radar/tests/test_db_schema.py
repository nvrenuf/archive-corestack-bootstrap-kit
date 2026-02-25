from __future__ import annotations

import psycopg
import pytest
from testcontainers.postgres import PostgresContainer

from utils import apply_migration, conn_kwargs_from_url


@pytest.fixture()
def postgres_db():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture()
def admin_conn(postgres_db):
    conn_url = postgres_db.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql://", 1
    )
    with psycopg.connect(**conn_kwargs_from_url(conn_url)) as conn:
        yield conn


def test_migration_idempotent_and_tables_exist(admin_conn):
    apply_migration(admin_conn)
    apply_migration(admin_conn)

    tables = admin_conn.execute(
        """
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public' AND tablename IN ('signal_items', 'radar_runs')
        ORDER BY tablename
        """
    ).fetchall()
    assert tables == [("radar_runs",), ("signal_items",)]


def test_pgcrypto_extension_enabled(admin_conn):
    apply_migration(admin_conn)
    row = admin_conn.execute("SELECT extname FROM pg_extension WHERE extname = 'pgcrypto'").fetchone()
    assert row == ("pgcrypto",)


def test_signal_items_columns_and_defaults(admin_conn):
    apply_migration(admin_conn)

    columns = admin_conn.execute(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'signal_items'
        ORDER BY ordinal_position
        """
    ).fetchall()

    expected = {
        "id": ("uuid", "NO"),
        "topic_id": ("text", "NO"),
        "platform": ("text", "NO"),
        "content_type": ("text", "NO"),
        "source_id": ("text", "YES"),
        "url": ("text", "NO"),
        "author": ("text", "YES"),
        "published_at": ("timestamp with time zone", "YES"),
        "collected_at": ("timestamp with time zone", "NO"),
        "title": ("text", "YES"),
        "text_snippet": ("text", "YES"),
        "engagement_json": ("jsonb", "NO"),
        "tags_json": ("jsonb", "NO"),
        "language": ("text", "NO"),
        "hash": ("text", "NO"),
        "raw_ref_json": ("jsonb", "NO"),
    }

    by_name = {name: (dtype, nullable, default) for name, dtype, nullable, default in columns}
    assert set(by_name.keys()) == set(expected.keys())

    for name, (dtype, nullable) in expected.items():
        assert by_name[name][0] == dtype
        assert by_name[name][1] == nullable

    assert "gen_random_uuid()" in (by_name["id"][2] or "")
    assert "now()" in (by_name["collected_at"][2] or "")
    assert "'{}'::jsonb" in (by_name["engagement_json"][2] or "")
    assert "'{}'::jsonb" in (by_name["tags_json"][2] or "")
    assert "'{}'::jsonb" in (by_name["raw_ref_json"][2] or "")
    assert "'en'::text" in (by_name["language"][2] or "")


def test_radar_runs_columns_and_defaults(admin_conn):
    apply_migration(admin_conn)

    columns = admin_conn.execute(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'radar_runs'
        ORDER BY ordinal_position
        """
    ).fetchall()

    expected = {
        "run_id": ("uuid", "NO"),
        "topic_id": ("text", "NO"),
        "started_at": ("timestamp with time zone", "NO"),
        "finished_at": ("timestamp with time zone", "YES"),
        "time_window_days": ("integer", "NO"),
        "collector_versions": ("jsonb", "NO"),
        "counts_json": ("jsonb", "NO"),
        "status": ("text", "NO"),
        "error_text": ("text", "YES"),
    }

    by_name = {name: (dtype, nullable, default) for name, dtype, nullable, default in columns}
    assert set(by_name.keys()) == set(expected.keys())

    for name, (dtype, nullable) in expected.items():
        assert by_name[name][0] == dtype
        assert by_name[name][1] == nullable

    assert "now()" in (by_name["started_at"][2] or "")
    assert "'{}'::jsonb" in (by_name["collector_versions"][2] or "")
    assert "'{}'::jsonb" in (by_name["counts_json"][2] or "")
