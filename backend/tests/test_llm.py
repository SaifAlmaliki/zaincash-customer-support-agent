from types import SimpleNamespace

from pydantic import BaseModel

from app.llm import GeminiStructuredLLM


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
