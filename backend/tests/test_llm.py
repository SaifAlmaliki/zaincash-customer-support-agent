import json
from types import SimpleNamespace

import httpx
import pytest
from pydantic import BaseModel

from app.config import Settings
from app.llm import GeminiStructuredLLM
from app.pipeline.factory import make_gemini_llm


class _S(BaseModel):
    x: int


def _llm():
    return GeminiStructuredLLM(api_key="k", model="m", price_in_per_m=1.0, price_out_per_m=2.0)


def test_to_sample_parsed_with_cost():
    raw = SimpleNamespace(usage_metadata={"input_tokens": 1_000_000, "output_tokens": 500_000})
    s = _llm().to_sample({"raw": raw, "parsed": _S(x=1), "parsing_error": None})
    assert s.parsed == _S(x=1)
    assert s.cost_usd == 2.0
    assert s.error is None


def test_to_sample_exception_and_parse_error():
    assert _llm().to_sample(ValueError("down")).error == "ValueError: down"
    s = _llm().to_sample({"raw": SimpleNamespace(usage_metadata=None), "parsed": None,
                          "parsing_error": "bad json"})
    assert s.parsed is None and s.error == "bad json"


@pytest.mark.parametrize("content, expected", [('{"x": 7}', _S(x=7)), ('{"x": "not an integer"}', None)])
async def test_openrouter_structured_samples_use_configured_key_and_validate_output(monkeypatch, content, expected):
    requests = []

    async def send(_client, request, **_kwargs):
        requests.append(request)
        assert str(request.url) == "https://openrouter.ai/api/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer test-openrouter-key"
        assert request.extensions["timeout"]["read"] == 60.0
        body = json.loads(request.content)
        assert body["model"] == "google/gemini-3.8-flash"
        assert body["response_format"]["type"] == "json_schema"
        assert body["response_format"]["json_schema"]["schema"]["properties"]["x"]["type"] == "integer"
        return httpx.Response(200, request=request, json={
            "id": "gen-test", "object": "chat.completion", "created": 1,
            "model": "google/gemini-3.8-flash", "system_fingerprint": None,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120},
        })

    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    settings = Settings(_env_file=None, openrouter_api_key="test-openrouter-key",
                        gemini_model="google/gemini-3.8-flash")
    samples = await make_gemini_llm(settings).sample("Return x=7", _S, temperature=0.7, n=3)
    assert len(samples) == len(requests) == 3
    assert all(sample.parsed == expected for sample in samples), samples
    assert all(sample.cost_usd > 0 for sample in samples), samples
    assert all(bool(sample.error) == (expected is None) for sample in samples)


@pytest.mark.parametrize("reported_cost", [0.0, 0.0123])
def test_openrouter_reported_cost_takes_precedence_over_token_estimate(reported_cost):
    raw = SimpleNamespace(usage_metadata={"input_tokens": 1_000_000, "output_tokens": 500_000},
                          response_metadata={"cost": reported_cost})
    sample = _llm().to_sample({"raw": raw, "parsed": _S(x=1)})
    assert sample.cost_usd == reported_cost


@pytest.mark.parametrize("max_retries, failure, expected_attempts", [
    (0, 500, 1), (2, 500, 3), (2, 429, 3), (2, 401, 1),
    (0, "transport", 1), (2, "transport", 3),
])
async def test_openrouter_retry_budget_is_bounded(monkeypatch, max_retries, failure, expected_attempts):
    attempts = 0

    async def send(_client, request, **_kwargs):
        nonlocal attempts
        attempts += 1
        # Stop the old SDK's unbounded time-based retry loop without waiting minutes.
        if attempts > expected_attempts:
            raise AssertionError("request retry budget exceeded")
        if failure == "transport":
            raise httpx.ConnectError("connection unavailable", request=request)
        return httpx.Response(failure, request=request,
                              json={"error": {"code": failure, "message": "provider unavailable"}})

    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    llm = GeminiStructuredLLM(api_key="test-key", model="google/gemini-3.8-flash",
                             price_in_per_m=1, price_out_per_m=2, max_retries=max_retries)
    [sample] = await llm.sample("Return x=7", _S, temperature=0, n=1)
    assert attempts == expected_attempts
    assert sample.parsed is None and sample.error
    assert "retry budget exceeded" not in sample.error
