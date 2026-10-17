"""Task 3 contracts: real support_test queries and direct LangChain tool execution."""
import asyncio
import copy
import json
import threading
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import event, text
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.models import IncidentRow, TicketRow, TransactionRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.kb.contracts import EmbeddingBatch
from app.kb.documents import store_document
from app.kb.embeddings import EmbeddingError
from app.kb.service import KnowledgeError, KnowledgeExecutionError, KnowledgeService
from app.pipeline.contracts import Decision, ExtractedField, LookupResult, Ticket
from app.pipeline.stage6_draft import context as draft_context
from app.pipeline.stage6_draft import investigation as draft_investigation
from app.pipeline.stage6_draft.tools import build_tools
from tests.kb_fakes import PaidEmbedder

NOW = datetime(2026, 10, 17, 12, tzinfo=UTC)
PHONE = "07701234567"
OTHER = "07809876543"
REF = "ZC2410000123"


@pytest.fixture
def api():
    return draft_context, draft_investigation, build_tools


@pytest.fixture
def state():
    return {
        "ticket": Ticket("current", "حوالة معلقة", NOW, customer_phone=PHONE),
        "extracted": {
            "txn_ref": ExtractedField(REF, REF, 0, len(REF), "gemini", 1),
            "phone": ExtractedField(OTHER, OTHER, 0, len(OTHER), "gemini", 1),
        },
        "lookup": LookupResult("not_found"),
        "decision": Decision("Payments Ops", "P2", True, ("txn_not_found",), "review"),
    }


@pytest.fixture
def settings():
    return Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                    embedding_model=PaidEmbedder.model)


@pytest.fixture
def sf(settings):
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "support_test"
        reset_db(engine)
        yield make_sessionmaker(engine)
    finally:
        engine.dispose()


def transaction(ref=REF, *, phone=PHONE, receiver=OTHER, amount=50000, when=NOW):
    return TransactionRow(txn_ref=ref, sender_phone=phone, receiver_phone=receiver,
                          amount_iqd=amount, type="p2p", status="pending", created_at=when)


def tools_for(api, state, sf, settings, embedder=None):
    context_module, repo_module, build = api
    context = context_module.DraftContext(state)
    repo = repo_module.SqlInvestigationRepo(sf)
    knowledge = KnowledgeService(sf, settings, embedder or PaidEmbedder())
    return context, {t.name: t for t in build(context, knowledge, repo)}, repo


async def test_exact_and_fuzzy_queries_are_scoped_and_never_confirm_candidates(api, state, sf, settings):
    with sf.begin() as s:
        s.add_all([
            transaction(), transaction("ZC2410000124", amount=50499),
            transaction("ZC2410000125", amount=50501),
            transaction("ZC2410000126", phone=OTHER, receiver="07901111111"),
            transaction("ZC2410000127", when=NOW + timedelta(seconds=1)),
        ])
    context, tools, _ = tools_for(api, state, sf, settings)
    exact = await tools["lookup_transaction"].ainvoke({"txn_ref": REF})
    assert exact["txn_ref"] == REF and exact["amount_iqd"] == 50000
    hits = await tools["search_transactions"].ainvoke({
        "phone": PHONE, "amount_iqd": 50000,
        "date_from": "2026-10-16", "date_to": "2026-10-18",
    })
    assert {hit["txn_ref"] for hit in hits} == {REF, "ZC2410000124"}
    # Searching a ticket counterpart must still require the customer's involvement.
    hits = await tools["search_transactions"].ainvoke({
        "phone": OTHER, "amount_iqd": 50000,
        "date_from": "2026-10-16", "date_to": "2026-10-18",
    })
    assert {hit["txn_ref"] for hit in hits} == {REF, "ZC2410000124"}
    assert context.state["lookup"].status == state["lookup"].status == "not_found"


@pytest.mark.parametrize("stored_phone", [
    "+9647701234567",
    "0770 123-4567",
    "+964 (770) 123 4567",
    "٠٧٧٠ ١٢٣-٤٥٦٧",
    "+۹۶۴\u00a0۷۷۰-۱۲۳ ۴۵۶۷",
], ids=["international", "domestic-spaced", "international-spaced", "arabic-indic", "persian"])
@pytest.mark.parametrize("name,args", [
    ("lookup_transaction", {"txn_ref": REF}),
    ("lookup_transaction", {"txn_ref": "ZC2410000124"}),
    ("search_transactions", {"phone": PHONE, "amount_iqd": 50000,
                             "date_from": "2026-10-16", "date_to": "2026-10-17"}),
    ("get_customer_recent_transactions", {"phone": PHONE}),
    ("get_customer_ticket_history", {"phone": PHONE}),
], ids=["lookup-sender", "lookup-receiver", "search", "recent", "history"])
async def test_stored_phone_formats_match_without_cross_customer_leaks(
    api, state, sf, settings, stored_phone, name, args,
):
    # Missing SQL canonicalization loses the real records; substring/over-broad
    # canonicalization or dropping principal scope leaks the explicitly unrelated ones.
    with sf.begin() as s:
        s.add_all([
            transaction(phone=stored_phone),
            transaction("ZC2410000124", phone=OTHER, receiver=stored_phone),
            transaction("ZC2410000125", phone="+964 770 123 4568", receiver=OTHER),
            transaction("ZC2410000126", phone="96407701234567", receiver=OTHER),
            transaction("ZC2410000127", phone="077012345670", receiver=None),
        ])
        s.add_all([TicketRow(external_id=external_id, text="prior contact", customer_phone=phone,
                            received_at=NOW - timedelta(days=1), source="test")
                   for external_id, phone in [
                       ("own-history", stored_phone), ("other-history", "+964 770 123 4568"),
                       ("invalid-prefix", "96407701234567"), ("extra-digit", "077012345670"),
                       ("no-phone", None),
                   ]])
    if name == "lookup_transaction":
        state["extracted"]["txn_ref"] = replace(state["extracted"]["txn_ref"], value=args["txn_ref"])
    context, tools, _ = tools_for(api, state, sf, settings)
    result = await tools[name].ainvoke(args)
    if name == "lookup_transaction":
        assert result is not None
        assert result["txn_ref"] == args["txn_ref"]
    elif name == "get_customer_ticket_history":
        assert [row["external_id"] for row in result] == ["own-history"]
        assert result[0]["customer_phone"] == stored_phone
    else:
        assert {row["txn_ref"] for row in result} == {REF, "ZC2410000124"}
    assert context.state["lookup"].status == state["lookup"].status == "not_found"
    # Reads must preserve the existing representation, not migrate persistence.
    with sf() as s:
        assert s.get(TransactionRow, REF).sender_phone == stored_phone


@pytest.mark.parametrize("name", ["search_transactions", "get_customer_recent_transactions"])
@pytest.mark.parametrize("has_principal", [True, False], ids=["principal-and-counterpart", "extracted-only"])
async def test_stored_phone_scope_normalizes_principal_and_fallback(
    api, state, sf, settings, name, has_principal,
):
    with sf.begin() as s:
        s.add_all([
            transaction(phone="+٩٦٤ ٧٧٠-١٢٣-٤٥٦٧", receiver="+۹۶۴ ۷۸۰ ۹۸۷ ۶۵۴۳"),
            transaction("ZC2410000124", phone="+964 780 987 6543", receiver="+964 790 111 1111"),
        ])
    if not has_principal:
        state["ticket"] = replace(state["ticket"], customer_phone=None)
        state["extracted"]["phone"] = replace(state["extracted"]["phone"], value=PHONE)
    context, tools, _ = tools_for(api, state, sf, settings)
    args = {"phone": OTHER if has_principal else PHONE}
    if name == "search_transactions":
        args.update(date_from="2026-10-16", date_to="2026-10-17")
    result = await tools[name].ainvoke(args)
    assert [row["txn_ref"] for row in result] == [REF]
    assert context.state["lookup"].status == "not_found"


@pytest.mark.parametrize("suffix", ["１", "१", "x"], ids=["fullwidth-digit", "devanagari-digit", "letter"])
@pytest.mark.parametrize("has_principal", [True, False], ids=["principal", "extracted-only"])
@pytest.mark.parametrize("name", [
    "lookup_transaction", "search_transactions", "get_customer_recent_transactions",
    "get_customer_ticket_history",
])
async def test_unsupported_phone_characters_cannot_match_customer(
    api, state, sf, settings, suffix, has_principal, name,
):
    # Deleting unsupported characters must not turn a different/invalid stored
    # phone into the authorized customer, including on the receiver side.
    with sf.begin() as s:
        s.add_all([
            transaction(phone=PHONE + suffix),
            transaction("ZC2410000124", phone=OTHER, receiver=PHONE + suffix),
            transaction("ZC2410000125", phone="+964 (770) 123 4567"),
        ])
        s.add_all([TicketRow(external_id=external_id, text="prior contact", customer_phone=phone,
                            received_at=NOW - timedelta(days=1), source="test")
                   for external_id, phone in [("invalid", PHONE + suffix), ("valid", "٠٧٧٠ ١٢٣-٤٥٦٧")]])
    if not has_principal:
        state["ticket"] = replace(state["ticket"], customer_phone=None)
        state["extracted"]["phone"] = replace(state["extracted"]["phone"], value=PHONE)
    context, tools, _ = tools_for(api, state, sf, settings)
    args = {"txn_ref": REF} if name == "lookup_transaction" else {"phone": PHONE}
    if name == "search_transactions":
        args.update(date_from="2026-10-16", date_to="2026-10-17")
    result = await tools[name].ainvoke(args)
    if name == "lookup_transaction":
        assert result is None
    elif name == "get_customer_ticket_history":
        assert [row["external_id"] for row in result] == ["valid"]
    else:
        assert [row["txn_ref"] for row in result] == ["ZC2410000125"]
    assert context.state["lookup"].status == "not_found"


@pytest.mark.parametrize("suffix", ["１", "१", "x"], ids=["fullwidth-digit", "devanagari-digit", "letter"])
@pytest.mark.parametrize("name", ["search_transactions", "get_customer_recent_transactions"])
async def test_unsupported_phone_characters_cannot_match_counterpart(
    api, state, sf, settings, suffix, name,
):
    with sf.begin() as s:
        s.add_all([
            transaction(receiver=OTHER + suffix),
            transaction("ZC2410000124", phone=OTHER + suffix, receiver=PHONE),
            transaction("ZC2410000125", receiver="+۹۶۴ ۷۸۰ ۹۸۷ ۶۵۴۳"),
        ])
    context, tools, _ = tools_for(api, state, sf, settings)
    args = {"phone": OTHER}
    if name == "search_transactions":
        args.update(date_from="2026-10-16", date_to="2026-10-17")
    result = await tools[name].ainvoke(args)
    assert [row["txn_ref"] for row in result] == ["ZC2410000125"]
    assert context.state["lookup"].status == "not_found"


async def test_identifiers_cannot_pivot_from_candidate_to_other_customers(api, state, sf, settings):
    stranger = "07901111111"
    with sf.begin() as s:
        s.add_all([transaction(receiver=stranger),
                   transaction("ZC2410000999", phone=stranger, receiver=OTHER)])
    context, tools, _ = tools_for(api, state, sf, settings)
    await tools["get_customer_recent_transactions"].ainvoke({"phone": PHONE})
    for name, args in [
        ("get_customer_recent_transactions", {"phone": stranger}),
        ("get_customer_ticket_history", {"phone": stranger}),
        ("lookup_transaction", {"txn_ref": "ZC2410000999"}),
    ]:
        with pytest.raises(api[0].DraftToolInputError):
            await tools[name].ainvoke(args)
    assert [entry["status"] for entry in context.trace] == ["ok", "error", "error", "error"]


async def test_recent_and_history_anchor_receipt_exclude_current_future_and_limit_ten(api, state, sf, settings):
    with sf.begin() as s:
        s.add_all([transaction(f"ZC241000{i:04d}", when=NOW - timedelta(days=i))
                   for i in range(1, 13)])
        s.add_all([transaction("ZC2410099990", when=NOW - timedelta(days=15)),
                   transaction("ZC2410099991", when=NOW + timedelta(seconds=1))])
        s.add_all([TicketRow(external_id=f"prior-{i}", text="قديم", customer_phone=PHONE,
                            received_at=NOW - timedelta(days=i), source="test")
                   for i in range(1, 13)])
        s.add_all([TicketRow(external_id=name, text="must not leak", customer_phone=phone,
                            received_at=when, source="test") for name, phone, when in [
                                ("current", PHONE, NOW - timedelta(days=1)),
                                ("simultaneous", PHONE, NOW),
                                ("future", PHONE, NOW + timedelta(seconds=1)),
                                ("old", PHONE, NOW - timedelta(days=31)),
                                ("unrelated", OTHER, NOW - timedelta(days=1)),
                            ]])
    _, tools, _ = tools_for(api, state, sf, settings)
    recent = await tools["get_customer_recent_transactions"].ainvoke({"phone": PHONE})
    history = await tools["get_customer_ticket_history"].ainvoke({"phone": PHONE})
    assert [r["txn_ref"] for r in recent] == [f"ZC241000{i:04d}" for i in range(1, 11)]
    assert [r["external_id"] for r in history] == [f"prior-{i}" for i in range(1, 11)]
    short = await tools["get_customer_recent_transactions"].ainvoke({"phone": PHONE, "days": 1})
    assert [r["txn_ref"] for r in short] == ["ZC2410000001"]


async def test_incident_windows_are_inclusive_bounded_and_read_only(api, state, sf, settings):
    with sf.begin() as s:
        s.add_all([IncidentRow(id=name, service=service, started_at=start,
                              ended_at=end, description="x" * 4000)
                   for name, service, start, end in [
                       ("open", "p2p", NOW - timedelta(days=200), None),
                       ("closed-boundary", "p2p", NOW - timedelta(hours=1), NOW),
                       ("start-boundary", "p2p", NOW, None),
                       ("ended", "p2p", NOW - timedelta(days=1), NOW - timedelta(seconds=1)),
                       ("future", "p2p", NOW + timedelta(seconds=1), None),
                       ("other", "bill_pay", NOW, None),
                   ]])
    _, tools, _ = tools_for(api, state, sf, settings)
    thread_ids, read_only = [], []

    def observe(conn, cursor, statement, parameters, ctx, many):
        thread_ids.append(threading.get_ident())
        if statement.lstrip().upper().startswith("SELECT"):
            cursor.execute("SHOW transaction_read_only")
            read_only.append(cursor.fetchone()[0])

    event.listen(sf.kw["bind"], "before_cursor_execute", observe)
    try:
        hits = await tools["check_service_status"].ainvoke({"service": "p2p", "at_time": NOW.isoformat()})
    finally:
        event.remove(sf.kw["bind"], "before_cursor_execute", observe)
    assert {r["id"] for r in hits} == {"open", "closed-boundary", "start-boundary"}
    assert all(len(r["description"]) <= 2000 for r in hits)
    assert thread_ids and set(thread_ids).isdisjoint({threading.get_ident()})
    assert read_only and set(read_only) == {"on"}


async def test_all_eight_tools_and_seven_parallel_calls_execute_only_six(api, state, sf, settings):
    context, tools, _ = tools_for(api, state, sf, settings)
    assert set(tools) == {
        "lookup_transaction", "search_transactions", "get_customer_recent_transactions",
        "get_customer_ticket_history", "check_service_status", "search_knowledge_base",
        "flag_for_human", "submit_draft",
    }
    result = await asyncio.gather(*[
        tools["flag_for_human"].ainvoke({"reason": "asks_for_human", "note": f"note {i}"})
        for i in range(7)
    ], return_exceptions=True)
    assert sum(isinstance(r, api[0].DraftToolLimit) for r in result) == 1
    assert context.tool_count == len(context.trace) == len(context.notes) == 6
    assert context.reasons == ["txn_not_found", "asks_for_human"]
    assert context.submission is None


async def test_submission_is_terminal_including_invalid_later_calls(api, state, sf, settings):
    context, tools, _ = tools_for(api, state, sf, settings)
    assert tools["submit_draft"].return_direct is True
    result = await tools["submit_draft"].ainvoke({
        "reply_ar": "راح نراجع طلبك", "citations": ["policy-id"], "internal_note": "review",
    })
    assert result["reply_ar"] == context.submission.reply_ar == "راح نراجع طلبك"
    assert context.submission.citations == ("policy-id",)
    before = (context.tool_count, copy.deepcopy(context.trace), list(context.reasons), list(context.notes))
    for name, args in [("flag_for_human", {"reason": "fraud_suspected", "note": "later"}),
                       ("submit_draft", {"reply_ar": "replace", "citations": []}),
                       ("search_knowledge_base", {"query": 42})]:
        with pytest.raises(api[0].DraftAlreadySubmitted):
            await tools[name].ainvoke(args)
    assert before == (context.tool_count, context.trace, context.reasons, context.notes)
    with pytest.raises(ValidationError):
        context.submission.reply_ar = "mutated"


@pytest.mark.parametrize("name,args", [
    ("get_customer_recent_transactions", {"phone": PHONE, "days": 0}),
    ("get_customer_ticket_history", {"phone": PHONE, "days": 91}),
    ("get_customer_recent_transactions", {"phone": PHONE, "days": True}),
    ("search_transactions", {"phone": PHONE, "date_from": "2020-01-01", "date_to": "2026-10-17"}),
    ("search_transactions", {"phone": PHONE, "date_from": "2026-10-17", "date_to": "2026-10-16"}),
    ("search_transactions", {"phone": PHONE, "amount_iqd": -1,
                             "date_from": "2026-10-16", "date_to": "2026-10-17"}),
    ("check_service_status", {"service": "p2p", "at_time": "2030-01-01"}),
    ("check_service_status", {"service": "p2p", "at_time": "2020-01-01"}),
    ("check_service_status", {"service": "x" * 65, "at_time": NOW.isoformat()}),
    ("lookup_transaction", {"txn_ref": "x" * 33}),
    ("search_knowledge_base", {"query": "x" * 2001}),
    ("search_knowledge_base", {"query": "تحويل", "k": 11}),
    ("search_knowledge_base", {"query": "تحويل", "category": "unknown"}),
    ("flag_for_human", {"reason": "invented_reason", "note": "review"}),
    ("flag_for_human", {"reason": ["asks_for_human"], "note": "review"}),
    ("flag_for_human", {"reason": "asks_for_human", "note": "x" * 2001}),
    ("submit_draft", {"reply_ar": " ", "citations": []}),
    ("submit_draft", {"reply_ar": "x" * 6001, "citations": []}),
    ("submit_draft", {"reply_ar": "شكرا", "citations": "bad-shape"}),
    ("submit_draft", {"reply_ar": "شكرا", "citations": [], "internal_note": "x" * 2001}),
    ("submit_draft", {"reply_ar": "شكرا", "citations": [], "unexpected": True}),
])
async def test_invalid_calls_count_and_leave_bounded_readable_failure_trace(api, state, sf, settings, name, args):
    context, tools, _ = tools_for(api, state, sf, settings)
    with pytest.raises(api[0].DraftToolInputError):
        await tools[name].ainvoke(args)
    assert context.tool_count == 1 and context.submission is None
    entry, = context.trace
    assert entry["kind"] == "tool" and entry["tool"] == name and entry["status"] == "error"
    assert 0 <= entry["duration_ms"] and entry["error"] and len(entry["error"]) <= 500
    assert len(str(entry["arguments"])) <= 6100


async def test_real_knowledge_search_snapshots_are_isolated_and_json_ready(api, state, sf, settings):
    knowledge = KnowledgeService(sf, settings, PaidEmbedder())
    with sf.begin() as s:
        doc = store_document(s, "policy.txt", "سياسة تحويل الأموال".encode())
        doc_id = doc.id
    await knowledge.index_document(doc_id)
    context, tools, _ = tools_for(api, state, sf, settings)
    other, _, _ = tools_for(api, state, sf, settings)
    result = await tools["search_knowledge_base"].ainvoke({"query": "تحويل", "category": "failed_transfer"})
    assert len(result) == 1
    passage_id = result[0]["id"]
    assert context.retrieved[passage_id].text == "سياسة تحويل الأموال"
    assert other.retrieved == {} and other.trace == [] and other.cost_usd == 0
    assert context.cost_usd == pytest.approx(0.125)
    json.dumps(context.trace, ensure_ascii=False, allow_nan=False)
    snapshot = copy.deepcopy(context.trace[0]["retrieved_passages"])
    result[0]["text"] = "mutated tool output"
    assert context.trace[0]["retrieved_passages"] == snapshot
    assert snapshot[0]["id"] == passage_id and snapshot[0]["filename"] == "policy.txt"
    assert snapshot[0]["text"] == "سياسة تحويل الأموال"


class ErrorEmbedder(PaidEmbedder):
    def __init__(self, kind):
        self.kind = kind
        self.started = asyncio.Event()

    async def embed(self, texts):
        if self.kind == "embedding":
            raise EmbeddingError("provider failed", cost_usd=0.25)
        if self.kind == "knowledge":
            raise KnowledgeError("retrieval failed", cost_usd=0.25)
        if self.kind == "timeout":
            cause = asyncio.CancelledError()
            cause.cost_usd = 0.25
            raise TimeoutError from cause
        self.started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError as exc:
            exc.cost_usd = 0.25
            raise


@pytest.mark.parametrize("kind", ["embedding", "knowledge", "timeout", "cancel"])
async def test_tool_owns_error_and_cancellation_cost_exactly_once(api, state, sf, settings, kind):
    embedder = ErrorEmbedder(kind)
    context, tools, _ = tools_for(api, state, sf, settings, embedder)
    task = asyncio.create_task(tools["search_knowledge_base"].ainvoke({"query": "تحويل"}))
    if kind == "cancel":
        await embedder.started.wait()
        task.cancel()
    with pytest.raises((EmbeddingError, KnowledgeError, TimeoutError, asyncio.CancelledError)):
        await task
    assert context.cost_usd == pytest.approx(0.25)
    assert context.tool_count == 1 and not context.lock.locked()
    assert context.trace[0]["cost_usd"] == pytest.approx(0.25)
    assert context.trace[0]["status"] == ("cancelled" if kind == "cancel" else "error")
    assert context.retrieved == {}


async def test_lock_serializes_operations_and_submit_waits_for_inflight_search(api, state, sf, settings):
    class GatedEmbedder(PaidEmbedder):
        def __init__(self):
            self.started = asyncio.Event()
            self.release = asyncio.Event()

        async def embed(self, texts):
            self.started.set()
            await self.release.wait()
            return EmbeddingBatch(((1.0,) + (0.0,) * 767,), 0.125)

    embedder = GatedEmbedder()
    context, tools, _ = tools_for(api, state, sf, settings, embedder)
    search = asyncio.create_task(tools["search_knowledge_base"].ainvoke({"query": "تحويل"}))
    await embedder.started.wait()
    submit = asyncio.create_task(tools["submit_draft"].ainvoke({"reply_ar": "شكرا", "citations": []}))
    await asyncio.sleep(0)
    assert context.tool_count == 1 and context.submission is None
    embedder.release.set()
    await asyncio.gather(search, submit)
    assert [entry["tool"] for entry in context.trace] == ["search_knowledge_base", "submit_draft"]
    assert context.cost_usd == pytest.approx(0.125)


def test_context_copies_input_and_rejects_raising_hard_call_limit(api, state):
    context = api[0].DraftContext(state)
    state["extracted"].clear()
    assert context.state["extracted"]["txn_ref"].value == REF
    with pytest.raises(ValueError):
        api[0].DraftContext(state, max_tool_calls=7)


async def test_exact_reference_still_requires_customer_and_excludes_future(api, state, sf, settings):
    with sf.begin() as s:
        s.add(transaction(phone=OTHER, receiver="07901111111"))
    _, tools, _ = tools_for(api, state, sf, settings)
    assert await tools["lookup_transaction"].ainvoke({"txn_ref": REF}) is None
    with sf.begin() as s:
        row = s.get(TransactionRow, REF)
        row.sender_phone = PHONE
        row.created_at = NOW + timedelta(seconds=1)
    assert await tools["lookup_transaction"].ainvoke({"txn_ref": REF}) is None


async def test_history_excludes_current_database_id_even_if_external_id_differs(api, state, sf, settings):
    with sf.begin() as s:
        row = TicketRow(external_id="renamed", text="current", customer_phone=PHONE,
                        received_at=NOW - timedelta(days=1), source="test")
        s.add(row)
        s.flush()
        state["ticket"] = replace(state["ticket"], id=row.id)
    _, tools, _ = tools_for(api, state, sf, settings)
    assert await tools["get_customer_ticket_history"].ainvoke({"phone": PHONE}) == []


@pytest.mark.parametrize("value", [10**2000, float("nan"), float("inf")], ids=["huge-int", "nan", "inf"])
async def test_failure_trace_bounds_invalid_numeric_arguments(api, state, sf, settings, value):
    context, tools, _ = tools_for(api, state, sf, settings)
    with pytest.raises(api[0].DraftToolInputError):
        await tools["flag_for_human"].ainvoke({
            "reason": "asks_for_human", "note": "review",
            **{f"bad-{i}": value for i in range(10)},
        })
    assert len(json.dumps(context.trace[0]["arguments"], ensure_ascii=False, allow_nan=False)) <= 6100


async def test_sparse_lookback_boundaries_and_counterpart_history(api, state, sf, settings):
    with sf.begin() as s:
        s.add_all([transaction("ZC2410000201", when=NOW - timedelta(days=14)),
                   transaction("ZC2410000202", when=NOW - timedelta(days=14, microseconds=1))])
        s.add_all([TicketRow(external_id=name, text="x" * 10000, customer_phone=PHONE,
                            received_at=when, source="test") for name, when in [
                                ("inside", NOW - timedelta(days=30)),
                                ("outside", NOW - timedelta(days=30, microseconds=1)),
                            ]])
    _, tools, _ = tools_for(api, state, sf, settings)
    recent = await tools["get_customer_recent_transactions"].ainvoke({"phone": PHONE})
    history = await tools["get_customer_ticket_history"].ainvoke({"phone": PHONE})
    assert [r["txn_ref"] for r in recent] == ["ZC2410000201"]
    assert [r["external_id"] for r in history] == ["inside"]
    assert len(history[0]["text"]) == 2000
    with pytest.raises(api[0].DraftToolInputError):
        await tools["get_customer_ticket_history"].ainvoke({"phone": OTHER})


async def test_discovered_ref_can_be_inspected_but_not_promoted_to_match(api, state, sf, settings):
    with sf.begin() as s:
        s.add(transaction("ZC2410000200"))
    context, tools, _ = tools_for(api, state, sf, settings)
    with pytest.raises(api[0].DraftToolInputError):
        await tools["lookup_transaction"].ainvoke({"txn_ref": "ZC2410000200"})
    await tools["get_customer_recent_transactions"].ainvoke({"phone": "+9647701234567"})
    hit = await tools["lookup_transaction"].ainvoke({"txn_ref": "zc2410000200"})
    assert hit["txn_ref"] == "ZC2410000200"
    assert context.state["lookup"].status == "not_found"


async def test_search_and_incidents_limit_ten_and_all_database_calls_run_off_loop(api, state, sf, settings):
    with sf.begin() as s:
        s.add_all([transaction(f"ZC241000{i:04d}") for i in range(12)])
        s.add_all([IncidentRow(id=f"INC-{i:02d}", service="p2p", started_at=NOW,
                              description="incident") for i in range(12)])
        s.add(transaction())
    _, tools, _ = tools_for(api, state, sf, settings)
    threads = []

    def observe(conn, cursor, statement, parameters, ctx, many):
        threads.append(threading.get_ident())

    event.listen(sf.kw["bind"], "before_cursor_execute", observe)
    try:
        for name, args in [
            ("lookup_transaction", {"txn_ref": REF}),
            ("search_transactions", {"phone": PHONE, "date_from": "2026-10-16", "date_to": "2026-10-18"}),
            ("get_customer_recent_transactions", {"phone": PHONE}),
            ("get_customer_ticket_history", {"phone": PHONE}),
            ("check_service_status", {"service": "p2p", "at_time": NOW.isoformat()}),
            ("search_knowledge_base", {"query": "تحويل"}),
        ]:
            threads.clear()
            result = await tools[name].ainvoke(args)
            assert threads and threading.get_ident() not in threads
            if name in ("search_transactions", "check_service_status"):
                assert len(result) == 10
    finally:
        event.remove(sf.kw["bind"], "before_cursor_execute", observe)


async def test_database_faults_remain_distinct_and_record_paid_search_cost(api, state, sf, settings):
    context, tools, _ = tools_for(api, state, sf, settings)

    def fail(conn, cursor, statement, parameters, ctx, many):
        if statement.lstrip().upper().startswith("SELECT"):
            raise RuntimeError("database programming fault")

    event.listen(sf.kw["bind"], "before_cursor_execute", fail)
    try:
        with pytest.raises(RuntimeError, match="database programming fault"):
            await tools["get_customer_recent_transactions"].ainvoke({"phone": PHONE})
        with pytest.raises(KnowledgeExecutionError):
            await tools["search_knowledge_base"].ainvoke({"query": "تحويل"})
    finally:
        event.remove(sf.kw["bind"], "before_cursor_execute", fail)
    assert context.cost_usd == pytest.approx(0.125)
    assert [t["cost_usd"] for t in context.trace] == [0, 0.125]
    assert [t["error_type"] for t in context.trace] == ["RuntimeError", "RuntimeError"]


async def test_outer_timeout_retains_tool_owned_cost_and_cancelled_waiter_does_not_execute(api, state, sf, settings):
    embedder = ErrorEmbedder("cancel")
    context, tools, _ = tools_for(api, state, sf, settings, embedder)

    async def search_with_deadline():
        async with asyncio.timeout(0.1):
            await tools["search_knowledge_base"].ainvoke({"query": "تحويل"})

    search = asyncio.create_task(search_with_deadline())
    await embedder.started.wait()
    queued = asyncio.create_task(tools["flag_for_human"].ainvoke({"reason": "asks_for_human", "note": "queued"}))
    queued.cancel()
    with pytest.raises(asyncio.CancelledError):
        await queued
    with pytest.raises(TimeoutError):
        await search
    assert context.tool_count == len(context.trace) == 1
    assert context.cost_usd == pytest.approx(0.25)
    assert context.notes == []
