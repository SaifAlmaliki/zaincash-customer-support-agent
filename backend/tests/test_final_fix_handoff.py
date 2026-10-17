"""Real LangGraph + agent/tools + API runner; only providers and storage IO are fake."""
import asyncio
import json
from contextlib import contextmanager
from dataclasses import replace
from types import SimpleNamespace

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ProgrammingError

from app.config import Settings
from app.kb.contracts import EmbeddingBatch, Passage
from app.kb.service import KnowledgeService
from app.pipeline.contracts import FieldPick
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.stage6_draft.agent import RagDrafter
from app.pipeline.stage6_draft.drafting import DraftExecutionError
from app.services import batch_jobs
from tests.fakes import FakeClassifier, make_output
from tests.helpers import make_ticket
from tests.rag_fakes import (
    REPLY,
    Checker,
    Knowledge,
    ScriptedChat,
    answer,
    call,
    draft_state,
    script,
)
from tests.test_graph import REPO


@pytest.fixture
def runner_env(monkeypatch, tax):
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                        database_url="postgresql+psycopg://support:support@localhost:5433/support_test")
    assert make_url(settings.database_url).database == "support_test"
    saved = []
    run = SimpleNamespace(counts={})

    @contextmanager
    def sessions():
        yield SimpleNamespace(get=lambda *args: run, commit=lambda: None)

    monkeypatch.setattr(batch_jobs, "save_outcomes", lambda session, run_id, outcomes: saved.extend(outcomes))

    def build(steps, *, knowledge=None, checker=None, classify_delay=0, models=None):
        model = models[0] if models else ScriptedChat(steps=steps)
        per_ticket_models = iter(models) if models else None
        agent = RagDrafter(settings, model_factory=lambda: next(per_ticket_models) if per_ticket_models else model,
                           knowledge=knowledge or Knowledge(), investigation=object(),
                           credential_checker=checker or Checker())
        classifier = FakeClassifier(make_output(
            "failed_transfer", cost=0.25, flags={"fraud_suspected": 0.9},
            picks={"txn_ref": FieldPick("ZC2410000123", 0.99, "jev_pick")}), delay=classify_delay)
        graph = build_graph(PipelineDeps(mode="jev", taxonomy=tax, txn_repo=REPO,
                                        jev=classifier, drafter=agent))
        app = SimpleNamespace(state=SimpleNamespace(
            settings=settings, session_factory=sessions, pipeline_builder=lambda *args: graph))
        ticket = make_ticket("حولت رقم العملية ZC2410000123 وما وصلت", customer_phone="07809876543")
        return app, ticket, model

    return build, saved, run, settings


def assert_completed_evidence(outcome, cost):
    assert outcome.classifier.classification.category == "failed_transfer"
    assert outcome.extracted["txn_ref"].value == "ZC2410000123"
    assert outcome.lookup.status == "matched"
    assert outcome.lookup.txn.txn_ref == "ZC2410000123"
    assert outcome.decision.priority == "P1"
    assert "fraud_suspected" in outcome.decision.reasons
    assert outcome.cost_usd == pytest.approx(cost)
    assert sum(e["kind"] == "draft" for e in outcome.draft.trace) == 1


@pytest.fixture
def outer_deadlines(monkeypatch):
    contexts = []
    original = asyncio.timeout

    def record(seconds):
        context = original(seconds)
        if seconds == 180:
            contexts.append(context)
        return context

    monkeypatch.setattr(asyncio, "timeout", record)
    return contexts


@pytest.mark.parametrize("phase,cost", [("retrieval", 0.28), ("model", 0.35), ("checker", 0.293)])
async def test_outer_deadline_handoff_keeps_real_graph_evidence_and_cost(runner_env, outer_deadlines, phase, cost):
    build, saved, run, _ = runner_env
    entered = asyncio.Event()

    async def stall(_):
        entered.set()
        await asyncio.Event().wait()

    class GatedKnowledge(Knowledge):
        async def search(self, *args, **kwargs):
            entered.set()
            return await super().search(*args, **kwargs)

    class GatedChecker(Checker):
        async def check(self, reply):
            entered.set()
            return await super().check(reply)

    steps = script()
    if phase == "model":
        # Measured completed response; the interrupted call has no billed response.
        steps[0].response_metadata["cost"] = 0.08
        steps[1] = stall
    app, ticket, model = build(
        steps, knowledge=GatedKnowledge(delay=10) if phase == "retrieval" else None,
        checker=GatedChecker(delay=10) if phase == "checker" else None)
    job = asyncio.create_task(batch_jobs.process_batch(app, 1, [ticket], "jev"))
    await asyncio.wait_for(entered.wait(), 5)
    # Force the *real outer timeout* while a nested LangGraph task is active.
    outer_deadlines[0].reschedule(asyncio.get_running_loop().time() - 1)
    await asyncio.wait_for(job, 5)
    assert len(saved) == 1
    outcome = saved[0]
    assert_completed_evidence(outcome, cost)
    assert outcome.status == "failed" and "TimeoutError" in outcome.error
    assert "draft_timeout" in outcome.decision.reasons
    assert outcome.draft.cost_usd == pytest.approx(cost - 0.25)
    assert model.calls == (1 if phase == "retrieval" else 2)
    assert run.total_cost_usd == pytest.approx(cost)
    stages = [e["node"] for e in outcome.draft.trace if e["kind"] == "stage"]
    assert stages == ["prepare", "jev_classify", "extract", "lookup", "decide"]
    if phase != "retrieval":
        assert outcome.draft.trace[-1]["citation_sources"][0]["id"] == "p1"
    if phase == "checker":
        assert outcome.draft.text == REPLY and outcome.draft.citations == ("p1",)


async def test_remaining_ticket_budget_finishes_draft_before_outer_timeout(runner_env, monkeypatch):
    build, saved, run, _ = runner_env
    monkeypatch.setattr(batch_jobs, "TICKET_TIMEOUT_S", 0.7, raising=False)
    app, ticket, model = build(script(), knowledge=Knowledge(delay=10), classify_delay=0.3)
    await asyncio.wait_for(batch_jobs.process_batch(app, 1, [ticket], "jev"), 2)
    assert_completed_evidence(saved[0], 0.28)
    assert saved[0].status == "escalated" and saved[0].error is None
    assert saved[0].decision.reasons == ("fraud_suspected", "draft_timeout")
    assert run.status == "completed" and model.calls == 1


async def test_exhausted_draft_budget_does_not_start_paid_work(runner_env, monkeypatch):
    build, saved, _, _ = runner_env
    monkeypatch.setattr(batch_jobs, "TICKET_TIMEOUT_S", 0.4)
    app, ticket, model = build(script(), classify_delay=0.32)
    await batch_jobs.process_batch(app, 1, [ticket], "jev")
    assert_completed_evidence(saved[0], 0.25)
    assert model.calls == 0
    assert saved[0].decision.reasons == ("fraud_suspected", "draft_timeout")


async def test_outer_timeout_before_draft_preserves_last_streamed_state(runner_env, monkeypatch, outer_deadlines):
    from app.pipeline import graph as pipeline_graph

    build, saved, _, _ = runner_env
    entered = asyncio.Event()
    original = pipeline_graph._Nodes.lookup

    async def stalled_lookup(node, state):
        entered.set()
        await asyncio.Event().wait()
        return await original(node, state)

    monkeypatch.setattr(pipeline_graph._Nodes, "lookup", stalled_lookup)
    app, ticket, model = build(script())
    job = asyncio.create_task(batch_jobs.process_batch(app, 1, [ticket], "jev"))
    await asyncio.wait_for(entered.wait(), 5)
    outer_deadlines[0].reschedule(asyncio.get_running_loop().time() - 1)
    await asyncio.wait_for(job, 5)
    outcome, = saved
    assert outcome.status == "failed" and outcome.cost_usd == 0.25
    assert outcome.classifier.classification.flags["fraud_suspected"] == 0.9
    assert outcome.extracted["txn_ref"].value == "ZC2410000123"
    assert outcome.lookup is None and outcome.decision is None and model.calls == 0


async def test_concurrent_timeout_and_success_do_not_share_handoff(runner_env, outer_deadlines, monkeypatch):
    build, saved, _, _ = runner_env
    entered = asyncio.Event()
    fast_saved = asyncio.Event()

    async def stall(_):
        entered.set()
        await asyncio.Event().wait()

    original_save = batch_jobs.save_outcomes

    def save(session, run_id, outcomes):
        original_save(session, run_id, outcomes)
        if outcomes[0].ticket.external_id == "fast":
            fast_saved.set()

    monkeypatch.setattr(batch_jobs, "save_outcomes", save)
    app, ticket, _ = build(script(), models=[ScriptedChat(steps=[script()[0], stall]),
                                            ScriptedChat(steps=script("other-policy"))])
    slow = asyncio.create_task(batch_jobs.process_batch(
        app, 1, [ticket, replace(ticket, external_id="fast")], "jev"))
    await asyncio.wait_for(entered.wait(), 5)
    await asyncio.wait_for(fast_saved.wait(), 5)
    outer_deadlines[0].reschedule(asyncio.get_running_loop().time() - 1)
    await asyncio.wait_for(slow, 5)
    by_id = {o.ticket.external_id: o for o in saved}
    assert_completed_evidence(by_id["T-1"], 0.28)
    assert_completed_evidence(by_id["fast"], 0.293)
    assert by_id["fast"].draft.citations == ("other-policy",)
    assert "draft_timeout" not in by_id["fast"].decision.reasons
    assert "other-policy" not in json.dumps(by_id["T-1"].draft.trace)
    assert len(saved) == 2


async def test_genuine_runner_cancellation_propagates_without_terminal_persistence(runner_env):
    build, saved, _, _ = runner_env
    entered = asyncio.Event()

    async def stall(_):
        entered.set()
        await asyncio.Event().wait()

    app, ticket, _ = build([script()[0], stall])
    job = asyncio.create_task(batch_jobs.process_batch(app, 1, [ticket], "jev"))
    await asyncio.wait_for(entered.wait(), 5)
    job.cancel()
    with pytest.raises(asyncio.CancelledError):
        await job
    assert saved == []


class PaidEmbeddings:
    model = "openai/text-embedding-3-small"
    dimensions = 768

    async def embed(self, texts):
        return EmbeddingBatch(((1.0,) + (0.0,) * 767,), 0.125)


def faulty_knowledge(settings, monkeypatch, fault):
    # Real search construction, database worker, tools and agent; only SQL IO replaced.
    service = KnowledgeService(None, settings, PaidEmbeddings())
    reads = 0

    def read(statement, call):
        nonlocal reads
        reads += 1
        if reads == 1:
            return (Passage("p1", 1, 0, "سياسة محفوظة", "policy.md", 0.9),)
        raise fault

    monkeypatch.setattr(service, "_read_passages", read)
    return service


@pytest.mark.parametrize("fault", [RuntimeError("PRIVATE key=secret SQL"),
                                   ProgrammingError("PRIVATE SQL", {"key": "secret"}, ValueError("PRIVATE"))])
async def test_real_search_fault_is_failed_not_kb_unavailable_through_api(runner_env, monkeypatch, fault):
    build, saved, run, settings = runner_env
    service = faulty_knowledge(settings, monkeypatch, fault)
    app, ticket, model = build([script()[0], answer(call("search_knowledge_base", query="p2"), id="second")],
                               knowledge=service)
    await batch_jobs.process_batch(app, 1, [ticket], "jev")
    outcome, = saved
    assert_completed_evidence(outcome, 0.52)
    assert outcome.status == "failed"
    assert type(fault).__name__ in outcome.error
    assert "kb_unavailable" not in outcome.decision.reasons
    assert outcome.draft.trace[-1]["error_type"] == type(fault).__name__
    assert outcome.draft.trace[-1]["citation_sources"][0]["id"] == "p1"
    assert model.calls == 2 and run.total_cost_usd == pytest.approx(0.52)
    public = json.dumps(outcome.draft.trace) + outcome.error
    assert "PRIVATE" not in public and "secret" not in public


async def test_real_search_fault_carries_safe_draft_execution_error(runner_env, monkeypatch):
    _, _, _, settings = runner_env
    service = faulty_knowledge(settings, monkeypatch, RuntimeError("PRIVATE secret"))
    model = ScriptedChat(steps=[script()[0], answer(call("search_knowledge_base", query="p2"), id="second")])
    agent = RagDrafter(settings, model_factory=lambda: model, knowledge=service,
                       investigation=object(), credential_checker=Checker())
    with pytest.raises(DraftExecutionError) as caught:
        await agent.draft(draft_state(reasons=("fraud_suspected",)))
    assert "RuntimeError" in str(caught.value) and "PRIVATE" not in str(caught.value)
    assert caught.value.result.cost_usd == pytest.approx(0.27)
    assert caught.value.result.reasons == ("fraud_suspected",)


async def test_real_search_deadline_remains_safe_kb_unavailability(runner_env, monkeypatch):
    build, saved, _, settings = runner_env
    service = faulty_knowledge(settings, monkeypatch, TimeoutError("PRIVATE database deadline"))
    app, ticket, _ = build([script()[0], answer(call("search_knowledge_base", query="p2"), id="second")],
                           knowledge=service)
    await batch_jobs.process_batch(app, 1, [ticket], "jev")
    assert_completed_evidence(saved[0], 0.52)
    assert saved[0].status == "escalated" and saved[0].error is None
    assert saved[0].decision.reasons == ("fraud_suspected", "kb_unavailable")
    assert "PRIVATE" not in json.dumps(saved[0].draft.trace)
