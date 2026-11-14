import httpx
import pytest
from pydantic import BaseModel

from app.llm import LLMUnavailable, StructuredChatLLM
from app.pipeline.contracts import ExtractedField
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage3_extract.extract import fill_gaps
from app.telemetry.calls import call_context
from tests.helpers import make_ticket
from tests.telemetry.messages import raw


class _S(BaseModel):
    x: int


class _Chat:
    def __init__(self, results):
        self.results = list(results)

    def with_structured_output(self, schema, **kw):
        return self

    async def ainvoke(self, prompt):
        item = self.results.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


def llm(results, **kw):
    options = dict(chat_factory=lambda t: _Chat(results), price_in_per_m=1.0, price_out_per_m=2.0,
                   provider="openrouter", model="google/gemini-3.8-flash")
    return StructuredChatLLM(**(options | kw))


async def test_each_attempt_is_recorded():
    results = [httpx.ConnectError("x"), {"raw": raw(1000, 100), "parsed": _S(x=1), "parsing_error": None}]
    with call_context(ticket_id=1) as calls:
        [sample] = await llm(results).sample("p", _S, temperature=0.0)
    assert sample.parsed == _S(x=1)
    assert [(c.attempt, c.status) for c in calls.calls] == [(1, "error"), (2, "ok")]
    assert calls.calls[1].cost_usd == pytest.approx((1000 + 200) / 1e6)
    assert calls.calls[1].cost_source == "estimate" and calls.calls[0].error == "ConnectError"


async def test_unknown_price_and_local_sources():
    ok = {"raw": raw(10, 1), "parsed": _S(x=1), "parsing_error": None}
    with call_context() as calls:
        await llm([ok], price_known=False).sample("p", _S, temperature=0.0)
        await llm([dict(ok)], local=True, provider="ollama", model="qwen3:4b").sample("p", _S, temperature=0.0)
    assert [c.cost_source for c in calls.calls] == ["unknown", "local"]
    assert calls.calls[1].locality == "local"


class _FailingExtractor:
    async def extract(self, nt, fields):
        error = LLMUnavailable("bad json")
        error.cost_usd = 0.003
        raise error


async def test_failed_parse_cost_reaches_the_ticket():
    nt = normalize(make_ticket("حولت فلوس"))
    extracted = {f: ExtractedField(None, None, None, None, "none", 0.0) for f in ("txn_ref", "amount", "phone", "date")}
    _, cost = await fill_gaps(extracted, nt, ["amount"], _FailingExtractor())
    assert cost == pytest.approx(0.003)
