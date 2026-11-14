import json
import urllib.parse
from pathlib import Path

import psycopg


def read(name: str) -> str:
    return Path("/run/secrets", name).read_text(encoding="utf-8").strip()


user = urllib.parse.quote(read("postgres_user"), safe="")
password = urllib.parse.quote(read("postgres_password"), safe="")
database = urllib.parse.quote(read("postgres_db"), safe="")
url = f"postgresql://{user}:{password}@db:5432/{database}"
with psycopg.connect(url) as conn:
    row = conn.execute(
        "select state from intake_sessions where id = %s",
        ("e831d520-d267-474c-9fe7-cc1c01f89fd4",),
    ).fetchone()
state = row[0]
facts = {
    key: {"status": value.get("status"), "value": value.get("value"), "normalized": value.get("normalized")}
    for key, value in state.get("facts", {}).items()
}
print(json.dumps({"category": state.get("category"), "facts": facts}, ensure_ascii=False, indent=2))
