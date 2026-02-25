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


def _conn_as_role(postgres_db, user: str, password: str) -> psycopg.Connection:
    conn_url = postgres_db.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql://", 1
    )
    parsed = urlparse(conn_url)

    return psycopg.connect(
        host=parsed.hostname,
        port=parsed.port,
        dbname=parsed.path.lstrip("/"),
        user=user,
        password=password,
        autocommit=True,
    )


def test_ingest_writer_permissions(admin_conn, postgres_db):
    _apply_migration(admin_conn)

    with _conn_as_role(postgres_db, "ingest_writer", "ingest_writer") as ingest_conn:
        ingest_conn.execute(
            """
            INSERT INTO signal_items (id, topic_id, platform, content_type, url, hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                "44444444-4444-4444-4444-444444444444",
                "work-money",
                "reddit",
                "post",
                "https://example.com/4",
                "hash-4444",
            ),
        )

        with pytest.raises(errors.InsufficientPrivilege) as select_err:
            ingest_conn.execute("SELECT * FROM signal_items").fetchall()
        assert select_err.value.sqlstate == "42501"

        with pytest.raises(errors.InsufficientPrivilege) as delete_err:
            ingest_conn.execute("DELETE FROM signal_items")
        assert delete_err.value.sqlstate == "42501"

        ingest_conn.execute(
            """
            INSERT INTO radar_runs (run_id, topic_id, started_at, time_window_days, status)
            VALUES (%s, %s, now(), %s, %s)
            """,
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "work-money", 7, "running"),
        )

        ingest_conn.execute(
            """
            UPDATE radar_runs
            SET status = %s, finished_at = now()
            WHERE run_id = %s
            """,
            ("ok", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )


def test_synth_reader_permissions(admin_conn, postgres_db):
    _apply_migration(admin_conn)

    admin_conn.execute(
        """
        INSERT INTO signal_items (id, topic_id, platform, content_type, url, hash)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            "55555555-5555-5555-5555-555555555555",
            "work-money",
            "youtube",
            "video",
            "https://example.com/5",
            "hash-5555",
        ),
    )
    admin_conn.execute(
        """
        INSERT INTO radar_runs (run_id, topic_id, started_at, time_window_days, status)
        VALUES (%s, %s, now(), %s, %s)
        """,
        ("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "work-money", 7, "ok"),
    )

    with _conn_as_role(postgres_db, "synth_reader", "synth_reader") as synth_conn:
        assert synth_conn.execute("SELECT COUNT(*) FROM signal_items").fetchone()[0] >= 1
        assert synth_conn.execute("SELECT COUNT(*) FROM radar_runs").fetchone()[0] >= 1

        with pytest.raises(errors.InsufficientPrivilege) as insert_err:
            synth_conn.execute(
                """
                INSERT INTO signal_items (id, topic_id, platform, content_type, url, hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    "66666666-6666-6666-6666-666666666666",
                    "work-money",
                    "news",
                    "article",
                    "https://example.com/6",
                    "hash-6666",
                ),
            )
        assert insert_err.value.sqlstate == "42501"

        with pytest.raises(errors.InsufficientPrivilege) as update_err:
            synth_conn.execute("UPDATE radar_runs SET status = 'error'")
        assert update_err.value.sqlstate == "42501"

        with pytest.raises(errors.InsufficientPrivilege) as delete_err:
            synth_conn.execute("DELETE FROM radar_runs")
        assert delete_err.value.sqlstate == "42501"
