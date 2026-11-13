import json
import urllib.request

with urllib.request.urlopen("http://localhost:8000/api/knowledge") as response:
    raw = response.read().decode("utf-8")

docs = json.loads(raw)
print("type", type(docs).__name__)
if isinstance(docs, dict):
    print(json.dumps(docs, ensure_ascii=False)[:2000])
elif isinstance(docs, list):
    print("count", len(docs))
    if docs:
        print("keys", sorted(docs[0].keys()))
    for doc in docs:
        print(
            doc.get("id"),
            doc.get("filename") or doc.get("name"),
            doc.get("status"),
            doc.get("chunk_count"),
            doc.get("passage_count"),
            doc.get("indexed_chunks"),
        )
