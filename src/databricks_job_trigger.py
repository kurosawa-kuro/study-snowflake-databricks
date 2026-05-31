from __future__ import annotations

import argparse
import json
import os
import sys

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trigger a Databricks job run through the Jobs API."
    )
    parser.add_argument("--job-id", type=int, required=True, help="Databricks Job ID.")
    parser.add_argument(
        "--notebook-params",
        default="{}",
        help="JSON object string passed as notebook_params.",
    )
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        raise SystemExit(2)
    return value


def main() -> None:
    args = parse_args()
    host = require_env("DATABRICKS_HOST")
    token = require_env("DATABRICKS_TOKEN")

    try:
        notebook_params = json.loads(args.notebook_params)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON for --notebook-params: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    response = requests.post(
        f"{host.rstrip('/')}/api/2.1/jobs/run-now",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "job_id": args.job_id,
            "notebook_params": notebook_params,
        },
        timeout=300,
    )
    if not response.ok:
        print(
            f"Databricks job trigger failed: {response.status_code} {response.text}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    payload = response.json()
    print("Databricks job trigger succeeded.")
    print(f"job_id: {args.job_id}")
    print(f"run_id: {payload.get('run_id')}")
    print(f"number_in_job: {payload.get('number_in_job')}")


if __name__ == "__main__":
    main()
