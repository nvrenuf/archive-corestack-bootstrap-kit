from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg

PACK_DIR = Path(__file__).resolve().parents[1]
MIGRATION_PATH = PACK_DIR / "migrations" / "0001_init.sql"
DOCKER_SOCKET = Path.home() / ".docker" / "run" / "docker.sock"

if "DOCKER_HOST" not in os.environ and DOCKER_SOCKET.exists():
    os.environ["DOCKER_HOST"] = f"unix://{DOCKER_SOCKET}"


def conn_kwargs_from_url(conn_url: str) -> dict[str, object]:
    parsed = urlparse(conn_url)
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "dbname": parsed.path.lstrip("/"),
        "user": parsed.username,
        "password": parsed.password,
        "autocommit": True,
    }


def apply_migration(conn: psycopg.Connection) -> None:
    assert MIGRATION_PATH.exists(), f"Migration file not found: {MIGRATION_PATH}"
    conn.execute(MIGRATION_PATH.read_text(encoding="utf-8"))
