import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_products(sql):
    with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print(f"Executed SQL: {sql}")
            print(f"Retrieved rows: {len(rows)}")
            return rows