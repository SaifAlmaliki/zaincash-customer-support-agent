"""Real support_test/pgvector integration; only the embedding provider is faked."""
import asyncio
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import UTC, datetime
from time import monotonic

import httpx
import pytest
from sqlalchemy import create_engine, event, func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.config import Settings
from app.db.document_models import UploadedDocument
from app.db.models import RunRow, TicketResultRow, TicketRow
from app.db.session import init_db, make_engine, make_sessionmaker, reset_db
from app.kb.documents import DocumentValidationError, document_view, store_document
from app.kb.embeddings import EmbeddingError, OpenRouterEmbedder
from app.kb.models import KnowledgeChunk, KnowledgeDocumentIndex
from app.kb.service import (
    DocumentNotFoundError,
    IndexAttemptLostError,
    KnowledgeError,
    KnowledgeService,
)
from tests.kb_fakes import FakeEmbedder, GatedEmbedder, LateEmbedder, PaidEmbedder
from tests.test_kb_parse import make_pdf

pytestmark = pytest.mark.integration


@pytest.fixture
def settings():
    return Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                    embedding_model=FakeEmbedder.model)


@pytest.fixture
def support_test(settings):
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "support_test"
        reset_db(engine)
        yield make_sessionmaker(engine)
    finally:
        engine.dispose()


def upload(sf, filename="policy.txt", content="سياسة تحويل تجريبية"):
    with sf.begin() as session:
        document = store_document(session, filename, content.encode("utf-8"))
        return document.id


def view(sf, document_id):
    with sf() as session:
        return document_view(session, session.get(UploadedDocument, document_id))


def count_chunks(sf):
    with sf() as session:
        return session.scalar(select(func.count()).select_from(KnowledgeChunk))


async def test_cosine_ranking_cutoff_and_duplicate_stable_ids(support_test, settings):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, PaidEmbedder())
    # Insert the irrelevant policy first: ordering by source ID instead of distance is wrong.
    cash = upload(sf, "cash.md", "سياسة السحب النقدي")
    transfer = upload(sf, "transfer.txt", "سياسة تحويل الأموال")
    assert view(sf, transfer)["status"] == "awaiting_indexing"
    assert (await knowledge.search("تحويل")).passages == ()
    for document_id in (cash, transfer):
        result = await knowledge.index_document(document_id)
        assert result["status"] == "indexed"
        assert result["chunk_count"] == 1
        assert result["embedding_model"] == FakeEmbedder.model
        assert result["embedding_dimensions"] == 768
        assert result["cost_usd"] == pytest.approx(0.125)
    result = await knowledge.search("تحويل")
    assert result.cost_usd == pytest.approx(0.125)
    assert len(result.passages) == 1
    passage = result.passages[0]
    assert (passage.document_id, passage.filename, passage.text) == (
        transfer, "transfer.txt", "سياسة تحويل الأموال")
    assert passage.score == pytest.approx(1)
    assert passage.chunk_index == 0
    assert passage.page_start is passage.page_end is None
    assert len(passage.id) == 64
    assert int(passage.id, 16) > 0
    assert upload(sf, "renamed.txt", "سياسة تحويل الأموال") == transfer
    await knowledge.index_document(transfer)
    assert count_chunks(sf) == 2
    assert (await knowledge.search("تحويل")).passages[0].id == passage.id
    all_scores = KnowledgeService(sf, settings.model_copy(update={"kb_min_similarity": -1}),
                                  FakeEmbedder())
    ranked = (await all_scores.search("تحويل")).passages
    assert [p.document_id for p in ranked] == [transfer, cash]
    assert [p.score for p in ranked] == pytest.approx([1, 0])
    chunks = knowledge.list_chunks(transfer)
    assert chunks[0]["id"] == passage.id
    assert chunks[0]["text"] == passage.text
    assert "embedding" not in chunks[0]


async def test_category_filters_include_general_policies_and_validate_tags(support_test, settings):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, FakeEmbedder())
    tagged = upload(sf, "tagged.txt", "تحويل خاص")
    general = upload(sf, "general.txt", "تحويل عام")
    other = upload(sf, "other.txt", "تحويل آخر")
    await knowledge.index_document(tagged, category_tags=["general_inquiry", "general_inquiry"])
    await knowledge.index_document(general)
    await knowledge.index_document(other, category_tags=["other"])
    assert view(sf, tagged)["category_tags"] == ["general_inquiry"]
    result = await knowledge.search("تحويل", category="general_inquiry")
    assert {p.document_id for p in result.passages} == {tagged, general}
    assert {p.document_id for p in (await knowledge.search("تحويل", category="other")).passages} == {other, general}
    with pytest.raises(ValueError):
        await knowledge.index_document(tagged, category_tags=["x'); DROP TABLE kb_chunks; --"])
    with pytest.raises(ValueError):
        await knowledge.search("تحويل", category="not-a-category")
    assert count_chunks(sf) == 3
    await knowledge.index_document(tagged)  # None preserves existing tags; [] clears them.
    assert view(sf, tagged)["category_tags"] == ["general_inquiry"]
    await knowledge.index_document(tagged, category_tags=[])
    assert view(sf, tagged)["category_tags"] == []


async def test_search_limits_are_bounded(support_test, settings):
    knowledge = KnowledgeService(support_test, settings, FakeEmbedder())
    for number in range(12):
        await knowledge.index_document(upload(support_test, content=f"تحويل {number}"))
    assert len((await knowledge.search("تحويل", k=0)).passages) == 1
    assert len((await knowledge.search("تحويل")).passages) == 5
    assert len((await knowledge.search("تحويل", k=100)).passages) == 10


@pytest.mark.parametrize(("filename", "content", "status"), [
    ("bad.exe", b"text", 422), ("bad.pdf", b"not-pdf", 422),
    ("empty.txt", b"", 413), ("huge.txt", b"x" * (10 * 1024 * 1024 + 1), 413),
    ("bad.txt", b"\xff", 422),
])
def test_shared_source_validation(support_test, filename, content, status):
    with support_test.begin() as session:
        with pytest.raises(DocumentValidationError) as caught:
            store_document(session, filename, content)
        assert caught.value.status_code == status
        assert session.scalar(select(func.count()).select_from(UploadedDocument)) == 0


def test_source_validation_sanitizes_name_preserves_bom_and_caller_transaction(support_test):
    with support_test() as session:
        doc = store_document(session, r"C:\upload\POLICY.MD", b"\xef\xbb\xbf# policy")
        assert doc.filename == "POLICY.MD"
        assert doc.content == b"\xef\xbb\xbf# policy"
        assert doc.content_type == "text/markdown"
        session.rollback()
    with support_test() as session:
        assert session.scalar(select(func.count()).select_from(UploadedDocument)) == 0


async def test_schema_initialization_is_idempotent_and_delete_preserves_ticket_evidence(support_test, settings):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, FakeEmbedder())
    document_id = upload(sf)
    await knowledge.index_document(document_id)
    passage = (await knowledge.search("تحويل")).passages[0]
    snapshot = asdict(passage)
    with sf.begin() as session:
        ticket = TicketRow(external_id="evidence", text="تحويل", source="paste",
                           received_at=datetime.now(UTC))
        run = RunRow(mode="jev", prompt_version="test")
        session.add_all([ticket, run])
        session.flush()
        result = TicketResultRow(run_id=run.id, ticket_id=ticket.id, status="drafted",
                                 citations=[passage.id], agent_trace=[{
                                     "kind": "tool", "retrieved_passages": [snapshot]}])
        session.add(result)
        session.flush()
        result_id = result.id
    init_db(sf.kw["bind"])
    assert count_chunks(sf) == 1
    with sf.begin() as session:
        session.delete(session.get(UploadedDocument, document_id))
    assert count_chunks(sf) == 0
    with sf() as session:
        assert session.get(KnowledgeDocumentIndex, document_id) is None
        result = session.get(TicketResultRow, result_id)
        assert result.citations == [passage.id]
        assert result.agent_trace[0]["retrieved_passages"] == [snapshot]


async def test_claim_locks_source_even_before_index_row_exists(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    checked = []

    def observe_claim(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.startswith("INSERT INTO kb_document_indexes"):
            # Independent connection: the source must already be locked before index creation.
            with sf() as observer, pytest.raises(OperationalError) as caught:
                observer.execute(select(UploadedDocument).where(
                    UploadedDocument.id == document_id).with_for_update(nowait=True))
            assert caught.value.orig.sqlstate == "55P03"
            checked.append(True)

    engine = sf.kw["bind"]
    event.listen(engine, "before_cursor_execute", observe_claim)
    try:
        await KnowledgeService(sf, settings, FakeEmbedder()).index_document(document_id)
    finally:
        event.remove(engine, "before_cursor_execute", observe_claim)
    assert checked


async def test_competing_callers_refuse_active_attempt_and_release_transactions(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    provider = GatedEmbedder()
    knowledge = KnowledgeService(sf, settings, provider)
    first = asyncio.create_task(knowledge.index_document(document_id, category_tags=["other"]))
    await asyncio.wait_for(provider.entered.wait(), 5)
    try:
        assert sf.kw["bind"].pool.checkedout() == 0
        # A second service instance has no shared in-memory lock with the first.
        second = KnowledgeService(sf, settings, PaidEmbedder())
        result = await second.index_document(document_id, category_tags=["general_inquiry"])
        assert result["status"] == "indexing"
        assert result["category_tags"] == ["other"]
        assert result["cost_usd"] == 0
        with sf.begin() as session:
            session.execute(select(UploadedDocument).where(
                UploadedDocument.id == document_id).with_for_update(nowait=True))
        assert count_chunks(sf) == 0
    finally:
        provider.release.set()
        await first
    assert view(sf, document_id)["cost_usd"] == pytest.approx(0.125)
    assert count_chunks(sf) == 1


@pytest.mark.parametrize("fails", [False, True])
async def test_deletion_during_embedding_never_resurrects_source(support_test, settings, fails):
    sf = support_test
    document_id = upload(sf)
    provider = GatedEmbedder(error=EmbeddingError("provider failed", cost_usd=0.125) if fails else None)
    knowledge = KnowledgeService(sf, settings, provider)
    job = asyncio.create_task(knowledge.index_document(document_id))
    await asyncio.wait_for(provider.entered.wait(), 5)
    with sf.begin() as session:
        session.delete(session.get(UploadedDocument, document_id))
    provider.release.set()
    with pytest.raises(DocumentNotFoundError) as caught:
        await job
    assert caught.value.cost_usd == pytest.approx(0.125)
    with sf() as session:
        assert session.get(UploadedDocument, document_id) is None
        assert session.get(KnowledgeDocumentIndex, document_id) is None
    assert count_chunks(sf) == 0


@pytest.mark.parametrize("fails", [False, True])
async def test_recovery_and_new_attempt_fence_late_success_or_failure(support_test, settings, fails):
    sf = support_test
    document_id = upload(sf)
    provider = GatedEmbedder(error=EmbeddingError("old failure", cost_usd=0.125) if fails else None)
    old_service = KnowledgeService(sf, settings, provider)
    old_job = asyncio.create_task(old_service.index_document(document_id, category_tags=["other"]))
    await asyncio.wait_for(provider.entered.wait(), 5)
    new_service = KnowledgeService(sf, settings, PaidEmbedder())
    try:
        assert new_service.recover_interrupted() == 1
        recovered = view(sf, document_id)
        assert recovered["status"] == "failed"
        assert "retry" in recovered["error"].lower()
        assert new_service.recover_interrupted() == 0
        winner = await new_service.index_document(document_id, category_tags=["general_inquiry"])
        assert winner["status"] == "indexed"
    finally:
        provider.release.set()
    with pytest.raises(IndexAttemptLostError) as caught:
        await old_job
    assert caught.value.cost_usd == pytest.approx(0.125)
    assert view(sf, document_id) == winner
    assert count_chunks(sf) == 1
    assert (await new_service.search("تحويل", category="other")).passages == ()


async def test_failed_reindex_keeps_previous_chunks_atomically_and_is_retryable(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    knowledge = KnowledgeService(sf, settings, PaidEmbedder())
    await knowledge.index_document(document_id)
    original = knowledge.list_chunks(document_id)
    gate = GatedEmbedder()
    reindex = asyncio.create_task(KnowledgeService(sf, settings, gate).index_document(document_id))
    await asyncio.wait_for(gate.entered.wait(), 5)
    assert count_chunks(sf) == 1
    assert (await knowledge.search("تحويل")).passages == ()

    def fail_publish(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.startswith("INSERT INTO kb_chunks"):
            raise RuntimeError("secret raw SQL/provider body")

    engine = sf.kw["bind"]
    event.listen(engine, "before_cursor_execute", fail_publish)
    gate.release.set()
    try:
        failed = await reindex
    finally:
        event.remove(engine, "before_cursor_execute", fail_publish)
    assert failed["status"] == "failed"
    assert "secret" not in failed["error"]
    assert failed["cost_usd"] == pytest.approx(0.25)
    assert knowledge.list_chunks(document_id) == original
    assert (await knowledge.search("تحويل")).passages == ()
    assert (await knowledge.index_document(document_id))["status"] == "indexed"
    assert count_chunks(sf) == 1


async def test_parser_and_provider_failures_keep_source_and_record_safe_cost(support_test, settings):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, FakeEmbedder())
    empty = upload(sf, content=" \n ")
    failed = await knowledge.index_document(empty)
    assert failed["status"] == "failed"
    assert "empty" in failed["error"].lower()
    document_id = upload(sf)
    gate = GatedEmbedder(error=EmbeddingError("PRIVATE provider body", cost_usd=0.125))
    gate.release.set()
    failed = await KnowledgeService(sf, settings, gate).index_document(document_id)
    assert failed["status"] == "failed"
    assert "PRIVATE" not in failed["error"]
    assert "retry" in failed["error"].lower()
    assert failed["cost_usd"] == pytest.approx(0.125)
    assert view(sf, document_id)["size"] > 0
    assert count_chunks(sf) == 0
    assert (await knowledge.index_document(document_id))["status"] == "indexed"


async def test_model_changes_require_reindex_and_keep_chunk_ids(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    old = KnowledgeService(sf, settings, FakeEmbedder())
    await old.index_document(document_id)
    original_id = (await old.search("تحويل")).passages[0].id
    provider = FakeEmbedder()
    provider.model = "test/new-model"
    new = KnowledgeService(sf, settings.model_copy(update={"embedding_model": provider.model}), provider)
    assert (await new.search("تحويل")).passages == ()
    await new.index_document(document_id)
    assert (await old.search("تحويل")).passages == ()
    assert (await new.search("تحويل")).passages[0].id == original_id
    with pytest.raises(ValueError):
        KnowledgeService(sf, settings, provider)


@pytest.mark.parametrize("mismatch", ["dimensions", "chunk_model", "attempt"])
async def test_incompatible_or_unowned_chunks_cannot_be_searched(support_test, settings, mismatch):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, FakeEmbedder())
    document_id = upload(sf)
    await knowledge.index_document(document_id)
    with sf.begin() as session:
        if mismatch == "dimensions":
            session.get(KnowledgeDocumentIndex, document_id).embedding_dimensions = 42
        else:
            chunk = session.scalar(select(KnowledgeChunk))
            if mismatch == "chunk_model":
                chunk.embedding_model = "different/model"
            else:
                chunk.attempt_id = "outdated-attempt"
    assert (await knowledge.search("تحويل")).passages == ()


async def test_search_rechecks_compatibility_after_query_embedding(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    await KnowledgeService(sf, settings, FakeEmbedder()).index_document(document_id)
    query_provider = GatedEmbedder()
    search = asyncio.create_task(KnowledgeService(sf, settings, query_provider).search("تحويل"))
    await asyncio.wait_for(query_provider.entered.wait(), 5)
    assert sf.kw["bind"].pool.checkedout() == 0
    provider = FakeEmbedder()
    provider.model = "test/replacement"
    new = KnowledgeService(sf, settings.model_copy(update={"embedding_model": provider.model}), provider)
    await new.index_document(document_id)
    query_provider.release.set()
    result = await search
    assert result.passages == ()
    assert result.cost_usd == pytest.approx(0.125)


@pytest.mark.parametrize("cancel", [False, True])
async def test_index_deadline_or_cancellation_preserves_real_adapter_partial_cost(
    support_test, settings, monkeypatch, cancel,
):
    sf = support_test
    document_id = upload(sf, content="تحويل " * 6000)  # More than one 32-item provider batch.
    entered = asyncio.Event()
    timeout_contexts = []
    original_timeout = asyncio.timeout

    def record_deadline(seconds):
        context = original_timeout(seconds)
        if seconds == 120:
            timeout_contexts.append(context)
        return context

    calls = 0

    async def respond(request):
        nonlocal calls
        calls += 1
        if calls == 2:
            entered.set()
            await asyncio.Event().wait()
        inputs = json.loads(request.content)["input"]
        return httpx.Response(200, json={
            "data": [{"index": i, "embedding": [1.0] + [0.0] * 767} for i in range(len(inputs))],
            "usage": {"cost": 0.25},
        })

    monkeypatch.setattr(asyncio, "timeout", record_deadline)
    provider = OpenRouterEmbedder(settings, transport=httpx.MockTransport(respond))
    job = asyncio.create_task(KnowledgeService(sf, settings, provider).index_document(document_id))
    await asyncio.wait_for(entered.wait(), 5)
    assert len(timeout_contexts) == 1  # Enforced job deadline, independent of adapter's 20s deadline.
    if cancel:
        job.cancel()
        with pytest.raises(asyncio.CancelledError) as caught:
            await job
        assert caught.value.cost_usd == pytest.approx(0.25)
    else:
        timeout_contexts[0].reschedule(asyncio.get_running_loop().time() - 1)
        failed = await job
        assert "timed out" in failed["error"].lower()
    failed = view(sf, document_id)
    assert failed["status"] == "failed"
    assert failed["cost_usd"] == pytest.approx(0.25)
    assert count_chunks(sf) == 0


async def test_search_database_failure_preserves_completed_query_cost(support_test, settings):
    sf = support_test
    knowledge = KnowledgeService(sf, settings, PaidEmbedder())

    def fail_read(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.startswith("SELECT") and "kb_chunks" in statement:
            raise RuntimeError("PRIVATE database details")

    engine = sf.kw["bind"]
    event.listen(engine, "before_cursor_execute", fail_read)
    try:
        with pytest.raises(KnowledgeError) as caught:
            await knowledge.search("تحويل")
    finally:
        event.remove(engine, "before_cursor_execute", fail_read)
    assert caught.value.cost_usd == pytest.approx(0.125)
    assert "PRIVATE" not in str(caught.value)


@pytest.fixture
def index_deadlines(monkeypatch):
    contexts = []
    original = asyncio.timeout

    def record(seconds):
        context = original(seconds)
        if seconds == 120:
            contexts.append(context)
        return context

    monkeypatch.setattr(asyncio, "timeout", record)
    return contexts


async def test_late_provider_success_after_expired_deadline_cannot_publish(
    support_test, settings, index_deadlines,
):
    document_id = upload(support_test)
    provider = LateEmbedder()
    job = asyncio.create_task(KnowledgeService(support_test, settings, provider).index_document(document_id))
    await asyncio.wait_for(provider.entered.wait(), 5)
    index_deadlines[0].reschedule(asyncio.get_running_loop().time() - 1)
    result = await asyncio.wait_for(job, 5)
    assert result["status"] == "failed"
    assert "timed out" in result["error"].lower()
    assert result["cost_usd"] == pytest.approx(0.125)
    assert count_chunks(support_test) == 0


async def test_parsing_is_inside_job_deadline_and_late_parser_cannot_publish(
    support_test, settings, index_deadlines, monkeypatch,
):
    from app.kb import service

    parse = service.parse_document
    release = threading.Event()
    entered = asyncio.Event()
    finished = asyncio.Event()
    loop = asyncio.get_running_loop()

    def gated_parse(filename, content):
        loop.call_soon_threadsafe(entered.set)
        release.wait(5)
        result = parse(filename, content)
        loop.call_soon_threadsafe(finished.set)
        return result

    monkeypatch.setattr(service, "parse_document", gated_parse)
    document_id = upload(support_test)
    job = asyncio.create_task(KnowledgeService(support_test, settings, PaidEmbedder()).index_document(document_id))
    await asyncio.wait_for(entered.wait(), 5)
    try:
        assert support_test.kw["bind"].pool.checkedout() == 0
        index_deadlines[0].reschedule(loop.time() - 1)
        result = await asyncio.wait_for(job, 5)
        assert result["status"] == "failed"
        assert result["cost_usd"] == 0
    finally:
        release.set()
        await asyncio.wait_for(finished.wait(), 5)
    assert count_chunks(support_test) == 0


async def test_removed_index_attempt_cannot_be_recreated_by_late_completion(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    provider = GatedEmbedder()
    job = asyncio.create_task(KnowledgeService(sf, settings, provider).index_document(document_id))
    await asyncio.wait_for(provider.entered.wait(), 5)
    with sf.begin() as session:
        session.delete(session.get(KnowledgeDocumentIndex, document_id))
    provider.release.set()
    with pytest.raises(IndexAttemptLostError) as caught:
        await job
    assert caught.value.cost_usd == pytest.approx(0.125)
    assert view(sf, document_id)["status"] == "awaiting_indexing"
    assert count_chunks(sf) == 0


async def test_provider_model_change_during_embedding_fails_without_wrong_vectors(support_test, settings):
    sf = support_test
    document_id = upload(sf)
    provider = GatedEmbedder()
    job = asyncio.create_task(KnowledgeService(sf, settings, provider).index_document(document_id))
    await asyncio.wait_for(provider.entered.wait(), 5)
    provider.model = "test/changed-mid-call"
    provider.release.set()
    result = await job
    assert result["status"] == "failed"
    assert result["cost_usd"] == pytest.approx(0.125)
    assert count_chunks(sf) == 0


async def test_pdf_page_metadata_and_repeated_text_chunk_identity(support_test, settings):
    sf = support_test
    with sf.begin() as session:
        document_id = store_document(session, "policy.pdf", make_pdf(["Policy", "", "Policy"])).id
    knowledge = KnowledgeService(sf, settings, FakeEmbedder())
    await knowledge.index_document(document_id)
    chunks = knowledge.list_chunks(document_id)
    assert [chunk["text"] for chunk in chunks] == ["Policy", "Policy"]
    assert [(chunk["page_start"], chunk["page_end"]) for chunk in chunks] == [(1, 1), (3, 3)]
    assert chunks[0]["id"] != chunks[1]["id"]
    await knowledge.index_document(document_id)
    assert knowledge.list_chunks(document_id) == chunks
    passages = (await knowledge.search("Policy")).passages
    assert {p.page_start for p in passages} == {1, 3}
    assert all(p.filename == "policy.pdf" for p in passages)


def test_job_deadline_bounds_source_lock_wait_before_claim(support_test, settings, monkeypatch):
    from app.kb import service

    monkeypatch.setattr(service, "INDEXING_TIMEOUT_S", 0.05)
    document_id = upload(support_test)
    knowledge = KnowledgeService(support_test, settings, PaidEmbedder())
    with support_test() as holder, ThreadPoolExecutor() as workers:
        holder.execute(select(UploadedDocument).where(
            UploadedDocument.id == document_id).with_for_update())
        job = workers.submit(asyncio.run, knowledge.index_document(document_id))
        try:
            with pytest.raises(KnowledgeError) as caught:
                job.result(timeout=1)
            assert caught.value.cost_usd == 0
        finally:
            holder.rollback()
    assert view(support_test, document_id)["status"] == "awaiting_indexing"
    assert count_chunks(support_test) == 0


@pytest.mark.parametrize("blocked", ["pool", "checkout"])
async def test_db_deadline_includes_pool_and_checkout_without_late_claim(
    support_test, settings, monkeypatch, blocked,
):
    from app.kb import service

    monkeypatch.setattr(service, "INDEXING_TIMEOUT_S", 0.05)
    document_id = upload(support_test)
    engine = create_engine(support_test.kw["bind"].url, pool_size=1, max_overflow=0, pool_timeout=0.5)
    sf = make_sessionmaker(engine)
    release = threading.Event()
    returned = threading.Event()
    main_thread = threading.get_ident()
    pool_timeout = engine.pool.timeout()
    with engine.connect() as connection:
        statement_timeout = connection.scalar(text("SHOW statement_timeout"))

    def delayed_checkout(_dbapi, _record, _proxy):
        release.wait(0.5)

    def checked_in(_dbapi, _record):
        if threading.get_ident() != main_thread:
            returned.set()

    holder = engine.connect() if blocked == "pool" else None
    if blocked == "checkout":
        event.listen(engine, "checkout", delayed_checkout)
    event.listen(engine, "checkin", checked_in)
    try:
        started = monotonic()
        with pytest.raises(KnowledgeError) as caught:
            await KnowledgeService(sf, settings, PaidEmbedder()).index_document(document_id)
        assert caught.value.cost_usd == 0
        assert monotonic() - started < 0.25
    finally:
        release.set()
        if holder is not None:
            holder.close()
        assert await asyncio.to_thread(returned.wait, 2)
        # A fresh query queued behind the worker proves it returned the sole connection.
        with sf() as session:
            assert session.scalar(select(func.count()).select_from(KnowledgeDocumentIndex)) == 0
            assert session.scalar(text("SHOW statement_timeout")) == statement_timeout
        assert engine.pool.timeout() == pool_timeout
        engine.dispose()
    assert view(support_test, document_id)["status"] == "awaiting_indexing"


async def test_db_deadline_is_cumulative_across_publication_statements(support_test, settings, monkeypatch):
    from app.kb import service

    document_id = upload(support_test)
    monkeypatch.setattr(service, "INDEXING_TIMEOUT_S", 0.15)
    completed_delays = []
    failed_written = threading.Event()

    def slow_publication(_conn, cursor, statement, _parameters, _context, _many):
        if statement.startswith(("DELETE FROM kb_chunks", "INSERT INTO kb_chunks")):
            cursor.execute("SELECT pg_sleep(0.12)")
            completed_delays.append(statement.split()[0])

    def changed_index(_conn, _cursor, statement, parameters, _context, _many):
        if statement.startswith("UPDATE kb_document_indexes") and parameters.get("status") == "failed":
            failed_written.set()

    engine = support_test.kw["bind"]
    event.listen(engine, "before_cursor_execute", slow_publication)
    event.listen(engine, "after_cursor_execute", changed_index)
    try:
        started = monotonic()
        try:
            result = await KnowledgeService(support_test, settings, PaidEmbedder()).index_document(document_id)
            assert result["status"] == "failed"
            assert result["cost_usd"] == pytest.approx(0.125)
        except KnowledgeError as exc:
            assert exc.cost_usd == pytest.approx(0.125)
        assert monotonic() - started < 0.22
        assert await asyncio.to_thread(failed_written.wait, 2)
        # Acquire the source lock after failure bookkeeping so assertions see its commit.
        with support_test.begin() as session:
            session.execute(select(UploadedDocument).where(
                UploadedDocument.id == document_id).with_for_update())
        assert completed_delays == ["DELETE"]
    finally:
        event.remove(engine, "before_cursor_execute", slow_publication)
        event.remove(engine, "after_cursor_execute", changed_index)
    assert count_chunks(support_test) == 0
    assert view(support_test, document_id)["status"] == "failed"
    assert view(support_test, document_id)["cost_usd"] == pytest.approx(0.125)


async def test_db_deadline_second_cancel_during_failure_bookkeeping_keeps_cost(support_test, settings):
    document_id = upload(support_test)
    provider = GatedEmbedder()
    knowledge = KnowledgeService(support_test, settings, provider)
    entered = asyncio.Event()
    release = threading.Event()
    returned = threading.Event()
    loop = asyncio.get_running_loop()

    def gate_failure(_conn, _cursor, statement, parameters, _context, _many):
        if statement.startswith("UPDATE kb_document_indexes") and parameters.get("status") == "failed":
            loop.call_soon_threadsafe(entered.set)
            release.wait(0.5)

    def checked_in(_dbapi, _record):
        if entered.is_set():
            returned.set()

    engine = support_test.kw["bind"]
    event.listen(engine, "after_cursor_execute", gate_failure)
    event.listen(engine, "checkin", checked_in)
    job = asyncio.create_task(knowledge.index_document(document_id))
    try:
        await asyncio.wait_for(provider.entered.wait(), 2)
        job.cancel()
        await asyncio.wait_for(entered.wait(), 2)
        job.cancel()
        with pytest.raises(asyncio.CancelledError) as caught:
            await job
        assert getattr(caught.value, "cost_usd", None) == pytest.approx(0.125)
    finally:
        release.set()
        assert await asyncio.to_thread(returned.wait, 2)
        event.remove(engine, "after_cursor_execute", gate_failure)
        event.remove(engine, "checkin", checked_in)
    assert count_chunks(support_test) == 0


@pytest.mark.parametrize("external_timeout", [True, False])
async def test_db_deadline_search_cancellation_is_nonblocking_and_retains_cost(
    support_test, settings, external_timeout,
):
    knowledge = KnowledgeService(support_test, settings, PaidEmbedder())
    await knowledge.index_document(upload(support_test))
    returned = threading.Event()

    def slow_read(_conn, cursor, statement, _parameters, _context, _many):
        if statement.startswith("SELECT") and "kb_chunks" in statement:
            cursor.execute("SELECT pg_sleep(0.5)")

    def checked_in(_dbapi, _record):
        returned.set()

    engine = support_test.kw["bind"]
    event.listen(engine, "before_cursor_execute", slow_read)
    event.listen(engine, "checkin", checked_in)
    try:
        started = monotonic()
        if external_timeout:
            with pytest.raises(TimeoutError) as caught:
                async with asyncio.timeout(0.05):
                    await knowledge.search("تحويل")
            assert caught.value.__cause__.cost_usd == pytest.approx(0.125)
        else:
            job = asyncio.create_task(knowledge.search("تحويل"))
            asyncio.get_running_loop().call_later(0.05, job.cancel)
            with pytest.raises(asyncio.CancelledError) as caught:
                await job
            assert caught.value.cost_usd == pytest.approx(0.125)
        assert monotonic() - started < 0.25
        assert await asyncio.to_thread(returned.wait, 2)
    finally:
        event.remove(engine, "before_cursor_execute", slow_read)
        event.remove(engine, "checkin", checked_in)
    assert len((await knowledge.search("تحويل")).passages) == 1


async def test_db_deadline_cancelled_publication_cannot_commit_late(support_test, settings):
    document_id = upload(support_test)
    entered = asyncio.Event()
    released = threading.Event()
    failed_written = threading.Event()
    loop = asyncio.get_running_loop()

    def gate_commit(session):
        if any(isinstance(row, KnowledgeDocumentIndex) and row.status == "indexed"
               for row in session.identity_map.values()):
            loop.call_soon_threadsafe(entered.set)
            released.wait(0.5)

    def changed_index(_conn, _cursor, statement, parameters, _context, _many):
        if statement.startswith("UPDATE kb_document_indexes") and parameters.get("status") == "failed":
            failed_written.set()

    engine = support_test.kw["bind"]
    event.listen(Session, "before_commit", gate_commit)
    event.listen(engine, "after_cursor_execute", changed_index)
    job = asyncio.create_task(KnowledgeService(support_test, settings, PaidEmbedder()).index_document(document_id))
    try:
        await asyncio.wait_for(entered.wait(), 2)
        started = monotonic()
        job.cancel()
        with pytest.raises(asyncio.CancelledError) as caught:
            await job
        assert caught.value.cost_usd == pytest.approx(0.125)
        assert monotonic() - started < 0.25
    finally:
        released.set()
        try:
            assert await asyncio.to_thread(failed_written.wait, 2)
        finally:
            event.remove(Session, "before_commit", gate_commit)
            event.remove(engine, "after_cursor_execute", changed_index)
    with support_test.begin() as session:
        session.execute(select(UploadedDocument).where(
            UploadedDocument.id == document_id).with_for_update())
    assert count_chunks(support_test) == 0
    assert view(support_test, document_id)["status"] == "failed"
    assert view(support_test, document_id)["cost_usd"] == pytest.approx(0.125)
