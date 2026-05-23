import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

def _get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Missing Supabase DB configuration: DATABASE_URL")
    return database_url


DB_URL = _get_database_url()

def get_products(sql):
    with psycopg.connect(DB_URL, row_factory=dict_row) as conn:  # pyright: ignore[reportArgumentType]
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print(f"Executed SQL: {sql}")
            print(f"Retrieved rows: {len(rows)}")
            return rows