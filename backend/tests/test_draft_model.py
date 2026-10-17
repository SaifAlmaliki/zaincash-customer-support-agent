"""Real ChatOpenRouter + create_agent; only HTTP and external retrieval are faked."""
import json

import httpx
import pytest

from app.config import Settings
from app.pipeline.factory import make_draft_model
from app.pipeline.graph import PipelineDeps, build_graph, run_batch
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.pipeline.stage6_draft.agent import RagDrafter
from tests.fakes import FakeClassifier, make_output
from tests.rag_fakes import Checker, Knowledge, draft_state


def response_payload(*, id, choices, cost=0.01):
    usage = {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120}
    if cost is not None:
        usage["cost"] = cost
    return {"id": id, "object": "chat.completion", "created": 1, "system_fingerprint": None,
            "model": "google/gemini-3.8-flash", "choices": choices, "usage": usage}


def search_response():
    return response_payload(id="gen-search", choices=[{
        "index": 0, "finish_reason": "tool_calls",
        "message": {"role": "assistant", "content": None, "tool_calls": [{
            "id": "call-search", "type": "function", "function": {
                "name": "search_knowledge_base", "arguments": json.dumps({"query": "p1"}),
            },
        }]},
    }])


async def run_provider_pipeline(monkeypatch, tax, *, response, conversion_bug=False):
    calls = 0

    async def send(_client, request, **kwargs):
        nonlocal calls
        calls += 1
        assert calls <= 2, "Conversion failures must not restart paid work"
        assert str(request.url) == "https://openrouter.ai/api/v1/chat/completions"
        return httpx.Response(200, request=request, json=search_response() if calls == 1 else response)

    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    if conversion_bug:
        from langchain_openrouter import ChatOpenRouter

        original = ChatOpenRouter._create_chat_result

        def broken_conversion(self, response):
            raw = response if isinstance(response, dict) else response.model_dump(by_alias=True)
            if raw["id"] != "gen-search":
                raise ValueError("unexpected conversion programming fault")
            return original(self, response)

        monkeypatch.setattr(ChatOpenRouter, "_create_chat_result", broken_conversion)

    settings = Settings(_env_file=None, openrouter_api_key="test-key", typesafe_api_key="")
    drafter = RagDrafter(settings, model_factory=lambda: make_draft_model(settings),
                         knowledge=Knowledge(), investigation=object(), credential_checker=Checker())
    graph = build_graph(PipelineDeps(
        mode="jev", txn_repo=InMemoryTransactionRepo([]), taxonomy=tax, drafter=drafter,
        jev=FakeClassifier(make_output("general_inquiry", flags={"fraud_suspected": 1})),
    ))
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    return outcome, calls


@pytest.mark.parametrize("cost, total, source", [(0.01, 0.04, "provider"),
                                               (0.0, 0.03, "provider"),
                                               (None, 0.03015, "token_estimate")])
async def test_empty_choices_escalates_and_keeps_paid_response_usage(monkeypatch, tax, cost, total, source):
    outcome, calls = await run_provider_pipeline(
        monkeypatch, tax, response=response_payload(id="gen-empty", choices=[], cost=cost))
    assert outcome.status == "escalated" and outcome.error is None
    assert outcome.decision.reasons == ("fraud_suspected", "llm_unavailable")
    assert outcome.classifier.classification.category == "general_inquiry"
    assert outcome.cost_usd == pytest.approx(total) and outcome.draft.cost_usd == pytest.approx(total)
    assert outcome.draft.trace[-1]["citation_sources"][0]["id"] == "p1"
    models = [e for e in outcome.draft.trace if e["kind"] == "model"]
    assert models[-1]["status"] == "error" and models[-1]["response_id"] == "gen-empty"
    assert models[-1]["usage"] == {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120}
    assert models[-1]["cost_source"] == source
    assert models[-1]["cost_usd"] == pytest.approx(total - 0.03)
    assert calls == 2


async def test_failed_response_id_is_deduplicated_against_earlier_success(monkeypatch, tax):
    outcome, calls = await run_provider_pipeline(
        monkeypatch, tax, response=response_payload(id="gen-search", choices=[]))
    assert outcome.status == "escalated" and "llm_unavailable" in outcome.decision.reasons
    assert outcome.cost_usd == pytest.approx(0.03) and calls == 2


async def test_other_conversion_value_errors_remain_unexpected(monkeypatch, tax):
    valid = response_payload(id="gen-valid", choices=[{
        "index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "مرحبا"},
    }])
    outcome, calls = await run_provider_pipeline(monkeypatch, tax, response=valid, conversion_bug=True)
    assert outcome.status == "failed" and "ValueError" in outcome.error
    assert "unexpected conversion programming fault" in outcome.error
    assert "llm_unavailable" not in outcome.decision.reasons
    assert outcome.draft.trace[-1]["citation_sources"][0]["id"] == "p1" and calls == 2
