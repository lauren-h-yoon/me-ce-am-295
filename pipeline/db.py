"""Postgres connection helper (psycopg 3 + pgvector)."""
from __future__ import annotations

from pathlib import Path

from pipeline import config as C

SCHEMA_PATH = C.REPO_ROOT / "db" / "schema.sql"


def get_conn():
    import psycopg
    from pgvector.psycopg import register_vector

    conn = psycopg.connect(C.rag.database_url)
    register_vector(conn)
    return conn


def init_schema():
    sql = SCHEMA_PATH.read_text()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
