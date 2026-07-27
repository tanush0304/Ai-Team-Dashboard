import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")


def execute_sql(sql: str):
    """
    Executes a validated SELECT query and returns rows as dictionaries.
    """

    if not DATABASE_URL:
        raise Exception("DATABASE_URL not found in .env")

    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conn:

            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    except Exception as e:
        raise Exception(f"Database execution failed: {e}")