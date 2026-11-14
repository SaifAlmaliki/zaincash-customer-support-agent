import pytest
from langchain_typesafe.client import TypeSafeError

from app.pipeline.stage1_normalize.candidates import find_candidates
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage6_draft.credentials import JevCredentialChecker
from app.telemetry.calls import call_context
from tests.fakes import FakeJevRunnable
from tests.helpers import make_ticket


async def test_classify_records_main_and_order_calls(tax):
    nt = normalize(make_ticket("حولت 50 الف وما وصلت"))
    classifier = JevClassifier(FakeJevRunnable(), tax, model_id="jev-1.13.0", t_jev=0.6,
                               min_top_prob=0.6, price_in_per_m=0.042, max_state_chars=6000)
    with call_context(run_id=1, ticket_id=1) as calls:
        out = await classifier.classify(nt, find_candidates(nt.match_text))
    assert sorted(c.detail["check"] for c in calls.calls) == ["main", "order"]
    assert all(c.process == "classify" and c.provider == "typesafe" for c in calls.calls)
    assert all(c.input_tokens == 1000 and c.cost_source == "estimate" for c in calls.calls)
    assert sum(c.cost_usd for c in calls.calls) == pytest.approx(out.cost_usd)


async def test_classify_failure_records_an_error_row(tax):
    nt = normalize(make_ticket("سؤال"))
    classifier = JevClassifier(FakeJevRunnable(raises=RuntimeError("down")), tax, model_id="jev-1.13.0",
                               t_jev=0.6, min_top_prob=0.6, price_in_per_m=0.042, max_state_chars=6000)
    with call_context(ticket_id=1) as calls, pytest.raises(RuntimeError):
        await classifier.classify(nt, find_candidates(nt.match_text))
    assert {c.status for c in calls.calls} == {"error"}
    assert calls.calls[0].error == "RuntimeError"


class _Runnable:
    def __init__(self, result):
        self.result = result

    async def ainvoke(self, request):
        if isinstance(self.result, BaseException):
            raise self.result
        return self.result


async def test_credential_check_records_tokens_and_errors():
    ok = {"usage": {"input_tokens": 500}, "nouls": {"requests_credentials": {"noul": 0.05}}}
    checker = JevCredentialChecker(_Runnable(ok), price_in_per_m=0.042, model="jev-1.13.0")
    with call_context(ticket_id=1) as calls:
        check = await checker.check("رد")
    [row] = calls.calls
    assert (row.process, row.input_tokens, row.status) == ("credential_check", 500, "ok")
    assert row.cost_usd == pytest.approx(check.cost_usd)
    failing = JevCredentialChecker(_Runnable(TypeSafeError("bad")), price_in_per_m=0.042)
    with call_context(ticket_id=1) as calls:
        await failing.check("رد")
    assert calls.calls[0].status == "error" and calls.calls[0].model == "jev"
