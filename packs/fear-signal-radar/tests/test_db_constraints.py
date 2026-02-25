from __future__ import annotations

import psycopg
import pytest
from psycopg import errors
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


def _insert_signal(conn: psycopg.Connection, row_id: str, row_hash: str) -> None:
    conn.execute(
        """
        INSERT INTO signal_items (
            id, topic_id, platform, content_type, url, hash
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (row_id, "work-money", "reddit", "post", "https://example.com/1", row_hash),
    )


def test_unique_hash_constraint_enforced(admin_conn):
    apply_migration(admin_conn)

    _insert_signal(admin_conn, "11111111-1111-1111-1111-111111111111", "dup-hash")

    with pytest.raises(errors.UniqueViolation):
        _insert_signal(admin_conn, "22222222-2222-2222-2222-222222222222", "dup-hash")
