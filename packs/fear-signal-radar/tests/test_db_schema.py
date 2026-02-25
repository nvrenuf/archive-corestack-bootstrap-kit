from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg
import pytest
from psycopg import errors
from testcontainers.postgres import PostgresContainer

PACK_DIR = Path(__file__).resolve().parents[1]
MIGRATION_PATH = PACK_DIR / "migrations" / "001_init.sql"
DOCKER_SOCKET = Path.home() / ".docker" / "run" / "docker.sock"

if "DOCKER_HOST" not in os.environ and DOCKER_SOCKET.exists():
    os.environ["DOCKER_HOST"] = f"unix://{DOCKER_SOCKET}"


@pytest.fixture()
def postgres_db():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture()
def admin_conn(postgres_db):
    conn_url = postgres_db.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql://", 1
    )
    parsed = urlparse(conn_url)
    with psycopg.connect(
        host=parsed.hostname,
        port=parsed.port,
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        autocommit=True,
    ) as conn:
        yield conn


def _apply_migration(conn: psycopg.Connection) -> None:
    assert MIGRATION_PATH.exists(), f"Migration file not found: {MIGRATION_PATH}"
    conn.execute(MIGRATION_PATH.read_text(encoding="utf-8"))


def _insert_minimal_signal_item(conn: psycopg.Connection, row_id: str, row_hash: str) -> None:
    conn.execute(
        """
        INSERT INTO signal_items (
            id, topic_id, platform, content_type, url, hash
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (row_id, "work-money", "reddit", "post", "https://example.com/1", row_hash),
    )


def test_tables_exist(admin_conn):
    _apply_migration(admin_conn)

    rows = admin_conn.execute(
        """
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public' AND tablename IN ('signal_items', 'radar_runs')
        ORDER BY tablename
        """
    ).fetchall()

    assert rows == [("radar_runs",), ("signal_items",)]


def test_unique_hash_constraint(admin_conn):
    _apply_migration(admin_conn)

    _insert_minimal_signal_item(admin_conn, "11111111-1111-1111-1111-111111111111", "dup-hash")

    with pytest.raises(errors.UniqueViolation):
        _insert_minimal_signal_item(admin_conn, "22222222-2222-2222-2222-222222222222", "dup-hash")


def test_indexes_exist(admin_conn):
    _apply_migration(admin_conn)

    indexes = admin_conn.execute(
        """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public' AND tablename = 'signal_items'
        ORDER BY indexname
        """
    ).fetchall()

    index_defs = [definition for _, definition in indexes]
    assert any("(topic_id, collected_at)" in d for d in index_defs)
    assert any("(topic_id, platform)" in d for d in index_defs)


def test_migration_idempotency(admin_conn):
    _apply_migration(admin_conn)
    _apply_migration(admin_conn)

    count = admin_conn.execute(
        """
        SELECT COUNT(*)
        FROM pg_tables
        WHERE schemaname = 'public' AND tablename IN ('signal_items', 'radar_runs')
        """
    ).fetchone()[0]
    assert count == 2


def test_default_values(admin_conn):
    _apply_migration(admin_conn)

    _insert_minimal_signal_item(admin_conn, "33333333-3333-3333-3333-333333333333", "defaults-hash")

    row = admin_conn.execute(
        """
        SELECT collected_at, engagement_json, tags_json, raw_ref_json
        FROM signal_items
        WHERE id = '33333333-3333-3333-3333-333333333333'
        """
    ).fetchone()

    assert row[0] is not None
    assert row[1] == {}
    assert row[2] == {}
    assert row[3] == {}
