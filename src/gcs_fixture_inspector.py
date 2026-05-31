from __future__ import annotations

import argparse
import sys
from pathlib import Path

from google.cloud import storage


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect or download a fixture object from GCS."
    )
    parser.add_argument("--bucket", required=True, help="GCS bucket name.")
    parser.add_argument("--object", required=True, help="GCS object path.")
    parser.add_argument(
        "--output",
        help="Optional local file path. If set, the object is downloaded there.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    client = storage.Client()
    blob = client.bucket(args.bucket).blob(args.object)
    if not blob.exists():
        print(f"GCS object not found: gs://{args.bucket}/{args.object}", file=sys.stderr)
        raise SystemExit(2)

    blob.reload()
    print(f"Found: gs://{args.bucket}/{args.object}")
    print(f"Size: {blob.size} bytes")
    print(f"Updated: {blob.updated}")
    print(f"Content-Type: {blob.content_type}")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(output_path)
        print(f"Downloaded to: {output_path}")


if __name__ == "__main__":
    main()
