"""Offline corpus integrity check; uses the real parser, no settings/DB/providers.

Catches omitted doc2, duplicate bundle members, untranslated prose, corrupt
assets and provenance drift. Run from backend with PYTHONPATH=.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
from pathlib import Path

from app.kb.parse import DocumentParseError, parse_document

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/test-kb"
HISTORY_ID = "aa1a7fbbc54f9f5b9bb5fcbdb8b5da4b49c038f1063e98020e889950f0a3439d"


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def pointer(value, path: str):
    for part in path.strip("/").split("/"):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def main() -> None:
    manifest_path = PACK / "provenance.json"
    assert manifest_path.is_file(), "Missing Arabic pack provenance manifest"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest["documents"]
    assert len(entries) == 13
    originals = {p.name for p in (ROOT / "data/kb").glob("*.md")}
    assert len(originals) == 12
    expected = originals | {"task8-history-policy.md"}
    assert {Path(e["path"]).name for e in entries} == expected
    assert {p.name for p in (PACK / "ar").iterdir()} == expected
    assert manifest["validation_scope"] == "offline_parser_only_not_live_retested"
    chunks_by_file = {}
    arabic_ratios = []
    history_checks = 0
    recovered = []
    for entry in entries:
        path = ROOT / entry["path"]
        assert path.parent == PACK / "ar"
        content = path.read_bytes()
        assert digest(content) == entry["sha256"], path
        text = content.decode("utf-8")
        assert "\ufffd" not in text and text.endswith("\n")
        assert text.startswith("# ") and not re.search(r"[A-Za-z]", text.splitlines()[0])
        assert "مو سياسة حقيقية لزين كاش" in text
        assert f"معرّف الفئة: {entry['category']}" in text
        prose = re.sub(r"^معرّف الفئة: .+$", "", text, flags=re.MULTILINE)
        assert set(re.findall(r"[A-Za-z_]+", prose)) <= {"OTP", "PIN", "CVV", "pending"}, path
        letters = [c for c in prose if c.isalpha()]
        ratio = sum("\u0600" <= c <= "\u06ff" for c in letters) / len(letters)
        assert ratio >= 0.95, (path, ratio)
        arabic_ratios.append(ratio)
        chunks = parse_document(path.name, content)
        assert chunks and all(c.text.strip() for c in chunks)
        chunks_by_file[entry["path"]] = len(chunks)
        source = entry["source"]
        if source["kind"] == "repository_file":
            assert source["path"] == f"data/kb/{path.name}"
            assert entry["category"] == path.stem
            assert digest((ROOT / source["path"]).read_bytes()) == source["sha256"]
        else:
            assert source["kind"] == "saved_citation_text"
            assert path.name == "task8-history-policy.md"
            assert (source["run_id"], source["result_id"], source["document_id"]) == (40, 56, 2)
            assert source["citation_id"] == HISTORY_ID and source["chunk_index"] == 0
            assert digest(source["recovered_text"].encode("utf-8")) == source["sha256"]
            snapshot = ROOT / source["snapshot_path"]
            if snapshot.exists():
                saved = json.loads(snapshot.read_text(encoding="utf-8"))
                for field in [source["json_pointer"], *source["trace_json_pointers"]]:
                    assert pointer(saved, field) == source["recovered_text"]
                    history_checks += 1
            upload = source["original_upload"]
            if (ROOT / upload["path"]).exists():
                raw = (ROOT / upload["path"]).read_bytes()
                assert digest(raw) == upload["sha256"]
                assert parse_document(source["filename"], raw)[0].text == source["recovered_text"]
                history_checks += 1
            recovered.append(entry)
    assert len(recovered) == 1
    bundle = manifest["bundle"]
    assert bundle["order"] == [e["path"] for e in entries]
    raw_bundle = (ROOT / bundle["path"]).read_bytes()
    assert digest(raw_bundle) == bundle["sha256"]
    members = [(ROOT / path).read_bytes() for path in bundle["order"]]
    assert raw_bundle == b"\n---\n\n".join(members)
    assert all(raw_bundle.count(member) == 1 for member in members)
    assert len(re.findall(rb"^# ", raw_bundle, re.MULTILINE)) == 13
    chunks_by_file[bundle["path"]] = len(parse_document(Path(bundle["path"]).name, raw_bundle))
    historical_index = ROOT / manifest["historical_index_path"]
    if historical_index.exists():
        indexed = json.loads(historical_index.read_text(encoding="utf-8"))
        for entry in entries:
            source = entry["source"]
            if source["kind"] != "repository_file":
                continue
            record = next(r for r in indexed if r["terminal"]["id"] == source["live_document_id"])
            assert record["terminal"]["status"] == "indexed"
            assert record["upload"]["sha256"] == record["terminal"]["sha256"] == source["sha256"]
            assert record["upload"]["filename"] == Path(source["path"]).name
            history_checks += 1
    negative = manifest["negative_tests"]
    assert len(negative) == 1
    for entry in negative:
        path = ROOT / entry["path"]
        assert path.parent == PACK / "negative"
        raw = path.read_bytes()
        assert digest(raw) == entry["sha256"] == entry["source"]["sha256"]
        original = ROOT / entry["source"]["path"]
        if original.exists():
            assert original.read_bytes() == raw
            history_checks += 1
        assert raw not in raw_bundle
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                parse_document(path.name, raw)
            except DocumentParseError:
                pass
            else:
                raise AssertionError("Negative PDF was accepted as valid knowledge")
    print(json.dumps({
        "valid_documents": len(entries), "bundle_members": len(members),
        "parser_accepted_files": len(chunks_by_file), "chunks_by_file": chunks_by_file,
        "minimum_arabic_letter_ratio": round(min(arabic_ratios), 4),
        "provenance_hashes": "all verified", "local_historical_checks": history_checks,
        "negative_payloads_rejected": len(negative), "provider_calls": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
