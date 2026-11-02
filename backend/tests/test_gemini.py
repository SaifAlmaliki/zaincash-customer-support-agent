from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage2_classify.gemini import ExtractedSpan, GeminiExtractor, GeminiFields
from tests.fakes import FakeStructuredLLM
from tests.helpers import make_ticket


async def test_extractor_requests_only_named_fields():
    llm = FakeStructuredLLM([GeminiFields(amount=ExtractedSpan(value="50000", verbatim_span="خمسين الف"))])
    nt = normalize(make_ticket("حولت خمسين الف"))
    picks, cost = await GeminiExtractor(llm).extract(nt, ["amount"])
    assert set(picks) == {"amount"}
    assert picks["amount"].normalized == "50000"
    assert "Return only these fields: amount." in llm.calls[0]["prompt"]
    assert llm.calls[0]["temperature"] == 0.0 and cost > 0
