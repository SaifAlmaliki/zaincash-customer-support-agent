"""Rewrite indexed policy chunk text from the current PDF extractor. Embeddings stay."""
from pathlib import Path

import psycopg

from app.kb.parse import parse_document

root = Path(__file__).resolve().parents[1]
secrets = root / "secrets"
user = (secrets / "postgres_user").read_text(encoding="utf-8").strip()
password = (secrets / "postgres_password").read_text(encoding="utf-8").strip()
database = (secrets / "postgres_db").read_text(encoding="utf-8").strip()

pdfs = {path.name: path.read_bytes() for path in (root / "data" / "kb-pdf").glob("*.pdf")}
with psycopg.connect(f"postgresql://{user}:{password}@localhost:5433/{database}") as conn:
    with conn.cursor() as cur:
        cur.execute("select filename, count(*) from kb_chunks group by filename order by filename")
        rows = cur.fetchall()
        print("chunks", rows)
        for filename, count in rows:
            content = pdfs.get(filename)
            if content is None or count != 1:
                print("skip", filename, count)
                continue
            text = parse_document(filename, content)[0].text
            cur.execute(
                "update kb_chunks set text = %s where filename = %s",
                (text, filename),
            )
            print("updated", filename, "chars", len(text))
    conn.commit()
