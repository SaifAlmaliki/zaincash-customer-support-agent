#!/bin/sh
# Build DATABASE_URL from mounted secret files, then start the API.
# The password stays out of the image and out of the Compose service environment.
set -eu

for secret in postgres_user postgres_password postgres_db; do
  if [ ! -f "/run/secrets/$secret" ]; then
    echo "Missing /run/secrets/$secret. Copy secrets/${secret}.example to secrets/${secret}." >&2
    exit 1
  fi
done

DATABASE_URL="$(python -c '
import urllib.parse
from pathlib import Path

def read(name: str) -> str:
    return Path("/run/secrets", name).read_text(encoding="utf-8").strip()

user = urllib.parse.quote(read("postgres_user"), safe="")
password = urllib.parse.quote(read("postgres_password"), safe="")
database = urllib.parse.quote(read("postgres_db"), safe="")
print(f"postgresql+psycopg://{user}:{password}@db:5432/{database}", end="")
')"
export DATABASE_URL

support seed-db \
  --transactions tests/fixtures/sample_transactions.jsonl \
  --incidents tests/fixtures/sample_incidents.jsonl
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
