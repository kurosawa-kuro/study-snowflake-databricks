from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import snowflake.connector


DEFAULT_TEST_QUERY = "SELECT 1 AS ok"
DEFAULT_CONTEXT_QUERY = """
SELECT
  CURRENT_ACCOUNT() AS current_account,
  CURRENT_ROLE() AS current_role,
  CURRENT_WAREHOUSE() AS current_warehouse,
  CURRENT_DATABASE() AS current_database,
  CURRENT_SCHEMA() AS current_schema
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SQL against Snowflake for connectivity or file-based checks."
    )
    parser.add_argument(
        "--mode",
        choices=["query", "context"],
        default="query",
        help="Run a free-form query or print the current Snowflake context.",
    )
    parser.add_argument(
        "--query",
        default=DEFAULT_TEST_QUERY,
        help="SQL query to run when --mode=query.",
    )
    parser.add_argument(
        "--sql-file",
        help="Optional .sql file to execute sequentially, split by semicolons.",
    )
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        raise SystemExit(2)
    return value


def load_statements(sql_file: str) -> list[str]:
    content = Path(sql_file).read_text(encoding="utf-8")
    return [statement.strip() for statement in content.split(";") if statement.strip()]


def connect() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=require_env("SNOWFLAKE_ACCOUNT"),
        user=require_env("SNOWFLAKE_USER"),
        password=require_env("SNOWFLAKE_PASSWORD"),
        warehouse=require_env("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


def run_statements(
    cursor: snowflake.connector.cursor.SnowflakeCursor,
    statements: list[str],
) -> list[tuple] | None:
    last_rows = None
    for statement in statements:
        cursor.execute(statement)
        if cursor.description:
            last_rows = cursor.fetchall()
        else:
            last_rows = None
    return last_rows


def main() -> None:
    args = parse_args()

    with connect() as connection:
        with connection.cursor() as cursor:
            if args.sql_file:
                statements = load_statements(args.sql_file)
                last_rows = run_statements(cursor, statements)
                print("Snowflake SQL file execution succeeded.")
                print(f"SQL file: {args.sql_file}")
                print("Statements:")
                for statement in statements:
                    print(f"- {' '.join(statement.split())}")
                print(f"Rows: {last_rows}")
                return

            if args.mode == "context":
                cursor.execute(DEFAULT_CONTEXT_QUERY)
                rows = cursor.fetchall()
                print("Snowflake context query succeeded.")
                print(f"Query: {' '.join(DEFAULT_CONTEXT_QUERY.split())}")
                print(f"Rows: {rows}")
                return

            cursor.execute(args.query)
            rows = cursor.fetchall()
            print("Snowflake SQL query succeeded.")
            print(f"Query: {args.query}")
            print(f"Rows: {rows}")


if __name__ == "__main__":
    main()
