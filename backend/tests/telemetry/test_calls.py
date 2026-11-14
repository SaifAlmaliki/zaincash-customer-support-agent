import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import httpx
import pytest
from langchain_core.messages import AIMessage

from app.telemetry.calls import (
    AiCall,
    Timer,
    call_context,
    cost_for,
    current_calls,
    embed_process,
    record,
    short_error,
    usage_of,
)

NOW = datetime(2026, 11, 14, 9, tzinfo=UTC)


def call(**kw):
    return AiCall(**({"process": "classify", "provider": "typesafe", "model": "jev-1.13.0",
                      "locality": "cloud", "started_at": NOW, "latency_ms": 5} | kw))


def test_record_without_context_is_dropped():
    record(call())
    assert current_calls.get() is None


def test_contexts_buffer_and_nest():
    with call_context(run_id=1, ticket_id=2) as outer:
        record(call())
        with call_context(document_id=9) as inner:
            record(call(process="kb_index"))
        record(call(process="extract"))
    assert [c.process for c in outer.calls] == ["classify", "extract"]
    assert [c.process for c in inner.calls] == ["kb_index"]
    assert current_calls.get() is None


@pytest.mark.parametrize("kwargs, expected", [
    ({"local": True, "provider_cost": 0.5, "prices": (1.0, 1.0)}, (0.0, "local")),
    ({"local": False, "provider_cost": 0.5, "prices": (1.0, 1.0)}, (0.5, "provider")),
    ({"local": False, "provider_cost": None, "prices": (3.0, 15.0)}, ((1000 * 3 + 200 * 15) / 1e6, "estimate")),
    ({"local": False, "provider_cost": None, "prices": None}, (0.0, "unknown")),
])
def test_cost_precedence(kwargs, expected):
    cost, source = cost_for(input_tokens=1000, output_tokens=200, **kwargs)
    assert source == expected[1] and cost == pytest.approx(expected[0])


def test_estimate_needs_input_tokens():
    assert cost_for(input_tokens=None, output_tokens=None, provider_cost=None,
                    prices=(1.0, 1.0), local=False) == (0.0, "unknown")


def test_usage_of_reads_langchain_and_ollama_metadata():
    message = AIMessage("", usage_metadata={"input_tokens": 10, "output_tokens": 3, "total_tokens": 13},
                        response_metadata={"cost": 0.002})
    assert usage_of(message) == (10, 3, 0.002)
    ollama = AIMessage("", response_metadata={"prompt_eval_count": 900, "eval_count": 100})
    assert usage_of(ollama) == (900, 100, None)
    assert usage_of(SimpleNamespace()) == (None, None, None)
    assert usage_of(AIMessage("", response_metadata={"cost": -1})) == (None, None, None)


def test_short_error_never_includes_the_message():
    assert short_error(ValueError("ticket text: حولت 50 الف")) == "ValueError"
    error = httpx.HTTPStatusError("x", request=httpx.Request("GET", "http://x"),
                                  response=httpx.Response(429))
    error.status_code = 429
    assert short_error(error) == "HTTPStatusError: HTTP 429"


def test_embed_process_follows_the_context():
    assert embed_process() == "kb_search"
    with call_context(document_id=3):
        assert embed_process() == "kb_index"
    with call_context(run_id=1, ticket_id=2):
        assert embed_process() == "draft_search"
    with call_context(intake_session_id=uuid.uuid4()):
        assert embed_process() == "kb_search"


def test_timer_measures_elapsed_ms():
    timer = Timer()
    assert timer.started_at.tzinfo is not None and timer.ms() >= 0
