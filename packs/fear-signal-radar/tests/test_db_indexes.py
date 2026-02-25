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


def test_expected_indexes_exist(admin_conn):
    apply_migration(admin_conn)

    rows = admin_conn.execute(
        """
        SELECT tablename, indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename IN ('signal_items', 'radar_runs')
        ORDER BY tablename, indexname
        """
    ).fetchall()

    existing = {(table, index) for table, index in rows}
    required = {
        ("signal_items", "idx_signal_hash"),
        ("signal_items", "idx_signal_topic_platform"),
        ("signal_items", "idx_signal_published_at"),
        ("signal_items", "idx_signal_topic_published"),
        ("radar_runs", "idx_radar_topic_started"),
    }

    assert required.issubset(existing)
