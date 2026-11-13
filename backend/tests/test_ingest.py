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
    assert tickets[4].customer_phone == "07734445566" and tickets[4].channel == "whatsapp"


def test_phones_are_canonical_and_missing_phones_stay_empty(tmp_path):
    p = tmp_path / "phones.jsonl"
    p.write_text('{"external_id": "A", "text": "x", "customer_phone": "+964 780 987 6543"}\n'
                 '{"external_id": "B", "text": "y"}\n', encoding="utf-8")
    a, b = load_tickets(p, now=NOW)
    assert a.customer_phone == "07809876543"
    assert b.customer_phone is None


def test_invalid_phone_names_the_row(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text('{"external_id": "A", "text": "x", "customer_phone": "12345"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="Row 1 \\(A\\).*valid ZainCash phone number"):
        load_tickets(p, now=NOW)


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
