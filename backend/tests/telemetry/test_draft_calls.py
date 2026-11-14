import pytest

from app.config import Settings
from app.pipeline.stage6_draft.agent import RagDrafter
from app.pipeline.stage6_draft.model_info import DraftModelInfo
from app.telemetry.calls import call_context
from tests.rag_fakes import Checker, Knowledge, ScriptedChat, draft_state, script


def drafter(info=None):
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    model = ScriptedChat(steps=script())
    return RagDrafter(settings, model_factory=lambda: model, knowledge=Knowledge(), investigation=object(),
                      credential_checker=Checker(), info=info)


async def test_each_model_response_is_a_draft_row():
    with call_context(run_id=1, ticket_id=1) as calls:
        result = await drafter().draft(draft_state())
    rows = [c for c in calls.calls if c.process == "draft"]
    assert len(rows) == len([e for e in result.trace if e["kind"] == "model"]) == 2
    assert all(r.cost_source == "provider" and r.cost_usd == pytest.approx(0.01) for r in rows)
    assert all(r.input_tokens == 100 and r.output_tokens == 20 and r.latency_ms >= 0 for r in rows)


async def test_local_draft_model_is_free():
    info = DraftModelInfo("qwen3:4b", (0.0, 0.0), 30, "nomic-embed-text", provider="ollama", locality="local")
    with call_context(ticket_id=1) as calls:
        await drafter(info).draft(draft_state())
    rows = [c for c in calls.calls if c.process == "draft"]
    assert {(r.provider, r.locality, r.cost_source, r.cost_usd) for r in rows} == {("ollama", "local", "local", 0.0)}
