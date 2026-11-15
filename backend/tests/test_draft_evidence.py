from app.services.draft_evidence import draft_evidence


def row(ref, at, **extra):
    return {"txn_ref": ref, "sender_phone": "07851110004", "receiver_phone": None,
            "receiver_name": "متجر الرافدين", "amount_iqd": 12000, "type": "card", "status": "declined",
            "created_at": at, "biller": None, "agent_id": None,
            "failure_reason": "الدفع الإلكتروني غير مفعّل على البطاقة", **extra}


def tool(name, result, status="ok"):
    return {"kind": "tool", "tool": name, "status": status, "arguments": {}, "result": result}


def found(trace):
    return draft_evidence(trace, [])["investigated_transactions"]


def test_rows_are_deduplicated_and_newest_first():
    rows = found([
        tool("get_customer_recent_transactions",
             [row("A", "2026-10-06T20:00:00+03:00"), row("B", "2026-10-07T09:00:00+03:00")]),
        tool("search_transactions", [row("B", "2026-10-07T09:00:00+03:00", amount_iqd=1)]),
    ])
    assert [r["txn_ref"] for r in rows] == ["B", "A"]
    assert rows[0]["amount_iqd"] == 12000
    assert rows[0] == row("B", "2026-10-07T09:00:00+03:00")


def test_failed_tool_calls_contribute_nothing():
    result = [row("A", "2026-10-06T20:00:00+03:00")]
    assert found([tool("get_customer_recent_transactions", result, status="error"),
                  tool("get_customer_recent_transactions", result, status="cancelled")]) == []


def test_lookup_single_and_null_results():
    rows = found([tool("lookup_transaction", row("C", "2026-10-07T09:00:00+03:00")),
                  tool("lookup_transaction", None)])
    assert [r["txn_ref"] for r in rows] == ["C"]


def test_malformed_rows_are_dropped():
    valid = row("OK", "2026-10-07T09:00:00+03:00")
    missing_ref = row("X", "2026-10-07T09:00:00+03:00")
    del missing_ref["txn_ref"]
    rows = found([tool("get_customer_recent_transactions", [
        missing_ref, row("S", "2026-10-07T09:00:00+03:00", amount_iqd="45000"),
        row("T", "…"), None, "x", valid,
    ])])
    assert [r["txn_ref"] for r in rows] == ["OK"]


def test_other_tools_are_ignored():
    assert found([tool("search_knowledge_base", [row("A", "2026-10-06T20:00:00+03:00")])]) == []
