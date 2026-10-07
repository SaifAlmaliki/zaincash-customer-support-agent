import pytest
from langgraph.types import RetryPolicy

from app.pipeline.classify.jev import JevClassifier
from app.pipeline.contracts import DraftResult
from app.pipeline.drafting import NullDrafter
from app.pipeline.graph import PipelineDeps, build_graph, run_batch
from app.pipeline.lookup import InMemoryTransactionRepo, txn_from_dict
from tests.fakes import FakeClassifier, FakeJevRunnable, make_output
from tests.helpers import make_ticket

REPO = InMemoryTransactionRepo([txn_from_dict({
    "txn_ref": "ZC2410000123", "sender_phone": "07809876543", "receiver_phone": "07701234567",
    "receiver_name": "علي", "amount_iqd": 50000, "type": "p2p", "status": "pending",
    "created_at": "2026-10-06T18:10:00+03:00",
})])
FAST_RETRY = RetryPolicy(max_attempts=2, initial_interval=0.01, jitter=False)


def _deps(tax, mode="jev", jev=None, gemini=None, drafter=None):
    return PipelineDeps(mode=mode, taxonomy=tax, txn_repo=REPO, jev=jev, gemini=gemini,
                        drafter=drafter or NullDrafter(), retry=FAST_RETRY)


async def _run(deps, tickets, concurrency=4):
    return await run_batch(build_graph(deps), tickets, concurrency=concurrency)


async def test_jev_mode_happy_path(tax):
    runnable = FakeJevRunnable(picks={"amount": ("50 الف", 0.9), "date": ("امس", 0.9),
                                      "txn_ref": ("ZC2410000123", 0.95)})
    jev = JevClassifier(runnable, tax, model_id="jev-1.13.0", t_jev=0.6, min_top_prob=0.6,
                        price_in_per_m=0.042, max_state_chars=6000)
    t = make_ticket("حولت ٥٠ الف امس رقم العملية ZC2410000123 وما وصلت",
                    customer_phone="07809876543")
    [o], summary = await _run(_deps(tax, jev=jev), [t])
    assert o.status == "pending_review", o.decision
    assert o.decision.team == "Payments Ops" and o.decision.priority == "P2"
    assert o.lookup.status == "matched" and o.extracted["amount"].value == 50000
    assert o.cost_usd > 0 and o.latency_ms >= 0
    assert summary.total == 1 and summary.by_status == {"pending_review": 1}


async def test_empty_ticket_escalates_without_model_calls(tax):
    jev = FakeClassifier(make_output())
    [o], _ = await _run(_deps(tax, jev=jev), [make_ticket("   ")])
    assert o.status == "escalated" and o.decision.reasons == ("empty_ticket",)
    assert jev.calls == 0


async def test_cascade_uncertain_jev_goes_to_gemini(tax):
    jev = FakeClassifier(make_output(confidence=0.3, uncertain=True, reasons=("low_confidence",)))
    gem = FakeClassifier(make_output("wrong_recipient", confidence=1.0, source="gemini", path="gemini"))
    [o], summary = await _run(_deps(tax, "cascade", jev, gem), [make_ticket("غلطت بالرقم")])
    assert gem.calls == 1
    assert o.classifier.path == "gemini_fallback"
    assert o.classifier.classification.category == "wrong_recipient"
    assert summary.fallback_rate == 1.0


async def test_cascade_confident_jev_skips_gemini(tax):
    jev, gem = FakeClassifier(make_output()), FakeClassifier(make_output(source="gemini"))
    await _run(_deps(tax, "cascade", jev, gem), [make_ticket("حولت وما وصلت")])
    assert gem.calls == 0


async def test_cascade_degrades_when_jev_fails(tax):
    jev = FakeClassifier(raises=RuntimeError("jev down"))
    gem = FakeClassifier(make_output(source="gemini", path="gemini"))
    [o], summary = await _run(_deps(tax, "cascade", jev, gem), [make_ticket("حولت وما وصلت")])
    assert o.classifier.degraded and summary.degraded


async def test_failed_ticket_does_not_stop_batch(tax):
    jev = FakeClassifier(make_output(), fail_for={"T-2"})
    tickets = [make_ticket("a", external_id=f"T-{i}") for i in range(1, 4)]
    outcomes, summary = await _run(_deps(tax, jev=jev), tickets)
    assert [o.status for o in outcomes][1] == "failed"
    assert "boom" in outcomes[1].error
    assert summary.failed_ids == ["T-2"] and summary.total == 3


async def test_concurrency_is_limited(tax):
    jev = FakeClassifier(make_output(), delay=0.02)
    tickets = [make_ticket("a", external_id=f"T-{i}") for i in range(6)]
    await _run(_deps(tax, jev=jev), tickets, concurrency=2)
    assert jev.max_inflight <= 2


async def test_drafter_reasons_escalate(tax):
    class Guarded:
        async def draft(self, state):
            return DraftResult(text="مرحبا", reasons=("draft_failed_guardrail",))

    jev = FakeClassifier(make_output("general_inquiry", priority="P4"))
    [o], summary = await _run(_deps(tax, jev=jev, drafter=Guarded()), [make_ticket("شكد العمولة")])
    assert o.status == "escalated" and o.draft.text == "مرحبا"
    assert summary.escalation_reasons == {"draft_failed_guardrail": 1}


def test_deps_validate_mode(tax):
    with pytest.raises(ValueError):
        PipelineDeps(mode="cascade", taxonomy=tax, txn_repo=REPO, jev=FakeClassifier(make_output()))
    with pytest.raises(ValueError):
        PipelineDeps(mode="fast", taxonomy=tax, txn_repo=REPO)


async def test_empty_batch(tax):
    outcomes, summary = await _run(_deps(tax, jev=FakeClassifier(make_output())), [])
    assert outcomes == [] and summary.total == 0
