from datetime import datetime
from pathlib import Path

import pytest

from app.ingest import load_tickets
from tests.helpers import BAGHDAD

FIXTURES = Path(__file__).parent / "fixtures"
NOW = datetime(2026, 10, 7, 15, 0, tzinfo=BAGHDAD)


def test_jsonl_fixture_loads():
    tickets = load_tickets(FIXTURES / "sample_tickets.jsonl", now=NOW)
    assert [t.external_id for t in tickets] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
    assert tickets[0].customer_phone == "07809876543"
    assert tickets[4].customer_phone is None and tickets[4].channel == "whatsapp"


def test_csv_with_bom_and_missing_columns(tmp_path):
    p = tmp_path / "batch.csv"
    p.write_bytes("\ufeffexternal_id,text\nC-1,حولت 50 الف وبطاقتي 5123456789012346\n".encode())
    [t] = load_tickets(p, now=NOW)
    assert t.external_id == "C-1" and t.channel == "app" and t.received_at == NOW
    assert "************2346" in t.text  # card masked before storage


def test_duplicate_external_ids_keep_first(tmp_path):
    p = tmp_path / "dup.jsonl"
    p.write_text('{"external_id": "X", "text": "first"}\n{"external_id": "X", "text": "second"}\n',
                 encoding="utf-8")
    [t] = load_tickets(p, now=NOW)
    assert t.text == "first"


def test_json_object_without_ids(tmp_path):
    p = tmp_path / "judges.json"
    p.write_text('{"tickets": [{"message": "مرحبا", "received_at": "2026-10-07T08:00:00"}]}',
                 encoding="utf-8")
    [t] = load_tickets(p, now=NOW)
    assert t.external_id == "judges-1" and t.text == "مرحبا"
    assert t.received_at == datetime(2026, 10, 7, 8, 0, tzinfo=BAGHDAD)


def test_unsupported_format(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("hi", encoding="utf-8")
    with pytest.raises(ValueError):
        load_tickets(p)
