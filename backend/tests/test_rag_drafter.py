import asyncio
import copy
import json

import httpx
import pytest

from app.config import Settings
from app.kb.embeddings import EmbeddingError
from app.kb.service import KnowledgeError
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


def drafter(steps=None, *, knowledge=None, checker=None, timeout=30, investigation=None):
    from app.pipeline.stage6_draft.agent import RagDrafter

    model = ScriptedChat(steps=steps or script())
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="",
                        agent_timeout_s=timeout)
    return RagDrafter(settings, model_factory=lambda: model, knowledge=knowledge or Knowledge(),
                      investigation=investigation or object(), credential_checker=checker or Checker()), model


def events(result, kind):
    return [e for e in result.trace if e["kind"] == kind]


async def test_real_agent_search_submit_keeps_sources_usage_and_existing_escalation():
    agent, model = drafter()
    state = draft_state(reasons=("fraud_suspected",))
    before = copy.deepcopy(state)
    result = await agent.draft(state)
    assert result.text == REPLY and result.citations == ("p1",)
    assert result.reasons == ("fraud_suspected",)
    assert [e["tool"] for e in events(result, "tool")] == ["search_knowledge_base", "submit_draft"]
    assert events(result, "tool")[0]["retrieved_passages"][0]["filename"] == "policy.md"
    assert events(result, "draft")[-1]["internal_note"] == "review this policy"
    assert result.cost_usd == pytest.approx(0.043)
    assert len(events(result, "model")) == 2
    assert model.bound_names == {"lookup_transaction", "search_transactions", "get_customer_recent_transactions",
                                 "get_customer_ticket_history", "check_service_status", "search_knowledge_base",
                                 "flag_for_human", "submit_draft"}
    assert state == before
    json.dumps(result.trace, ensure_ascii=False)


@pytest.mark.parametrize("citations, finding", [([], "missing_citations"), (["foreign"], "invalid_citations")])
async def test_rejected_submission_is_retained(citations, finding):
    steps = script()
    steps[1] = answer(call("submit_draft", reply_ar=REPLY, citations=citations), id="submit")
    agent, _ = drafter(steps)
    result = await agent.draft(draft_state())
    assert result.text == REPLY
    assert result.reasons == ("draft_failed_guardrail",)
    assert finding in events(result, "guardrail")[-1]["findings"]


async def test_empty_retrieval_never_invents_reply():
    agent, _ = drafter(knowledge=Knowledge(empty=True))
    result = await agent.draft(draft_state())
    assert "no_kb_support" in result.reasons
    assert result.text is None
    # A model's unsupported submission is still available for reviewer inspection.
    assert events(result, "draft")[-1]["reply_ar"] == REPLY
    assert result.cost_usd == pytest.approx(0.043)


async def test_plain_assistant_text_is_not_a_submission():
    agent, _ = drafter([answer(content=REPLY)])
    result = await agent.draft(draft_state())
    assert result.text is None and result.reasons == ("draft_not_submitted",)
    assert result.cost_usd == 0.01


async def test_retrieval_then_plain_text_has_rejected_trace_status():
    agent, _ = drafter([script()[0], answer(content=REPLY, id="plain")])
    result = await agent.draft(draft_state())
    assert result.reasons == ("draft_not_submitted",)
    assert events(result, "draft")[-1]["status"] == "rejected"


@pytest.mark.parametrize("phase, expected_cost", [("retrieval", 0.03), ("model", 0.03), ("checker", 0.043)])
async def test_overall_deadline_includes_every_phase_and_keeps_paid_cost(phase, expected_cost):
    async def stall(_):
        await asyncio.sleep(10)
    steps = script()
    if phase == "model":
        steps[1] = stall
    agent, _ = drafter(steps, timeout=0.05,
                       knowledge=Knowledge(delay=10 if phase == "retrieval" else 0),
                       checker=Checker(delay=10 if phase == "checker" else 0))
    result = await agent.draft(draft_state(reasons=("fraud_suspected",)))
    assert result.reasons == ("fraud_suspected", "draft_timeout")
    assert result.cost_usd == pytest.approx(expected_cost)
    if phase == "checker":
        assert result.text == REPLY and result.citations == ("p1",)


@pytest.mark.parametrize("error", [EmbeddingError("unavailable", cost_usd=0.02),
                                  KnowledgeError("unavailable", cost_usd=0.02)])
async def test_search_failure_cost_is_owned_by_tools_only(error):
    agent, _ = drafter(knowledge=Knowledge(error=error))
    result = await agent.draft(draft_state())
    assert result.reasons == ("kb_unavailable",)
    assert result.cost_usd == pytest.approx(0.03)


async def test_model_failure_retains_earlier_response_cost_and_sources():
    agent, _ = drafter([script()[0], httpx.HTTPStatusError(
        "unauthorized", request=httpx.Request("POST", "https://example.test"), response=httpx.Response(401))])
    result = await agent.draft(draft_state())
    assert result.reasons == ("llm_unavailable",)
    assert result.cost_usd == pytest.approx(0.03)
    assert events(result, "tool")[0]["retrieved_passages"][0]["id"] == "p1"


async def test_invalid_tool_arguments_are_traced_and_not_accepted():
    agent, _ = drafter([answer(call("search_knowledge_base", query="x", k=True))])
    result = await agent.draft(draft_state())
    assert result.reasons == ("draft_not_submitted",)
    assert events(result, "tool")[0]["error_type"] == "DraftToolInputError"


async def test_seven_calls_in_one_response_execute_only_six():
    agent, _ = drafter([answer(*(call("flag_for_human", reason="asks_for_human", note=str(i)) for i in range(7)))])
    result = await agent.draft(draft_state())
    assert result.reasons == ("asks_for_human", "draft_tool_limit")
    assert len(events(result, "tool")) == 6


async def test_submission_freezes_later_calls_in_same_response():
    steps = script()
    steps[1] = answer(call("submit_draft", reply_ar=REPLY, citations=["p1"]),
                      call("flag_for_human", reason="asks_for_human", note="must not execute"),
                      call("submit_draft", reply_ar="نص آخر", citations=[]), id="submit")
    agent, model = drafter(steps)
    result = await agent.draft(draft_state())
    assert result.text == REPLY and result.reasons == ()
    assert len(events(result, "tool")) == 2 and model.calls == 2


@pytest.mark.parametrize("score, rejected", [(0.1999, False), (0.2, True), (0.8, True)])
async def test_credential_score_is_strictly_below_point_two(score, rejected):
    agent, _ = drafter(checker=Checker(score))
    result = await agent.draft(draft_state())
    assert ("draft_failed_guardrail" in result.reasons) is rejected
    assert ("requests_credentials" in events(result, "guardrail")[-1]["findings"]) is rejected


async def test_degraded_checker_is_explicit_and_deterministic_checks_still_run():
    agent, _ = drafter(script(reply="أرسل رمز التحقق إلينا"), checker=Checker(None, degraded=True))
    result = await agent.draft(draft_state())
    assert "draft_failed_guardrail" in result.reasons
    assert events(result, "guardrail")[-1]["credential_check_degraded"] is True


async def test_concurrent_tickets_cannot_exchange_citations_cost_or_callback_state():
    from app.pipeline.stage6_draft.agent import RagDrafter

    models = iter([ScriptedChat(steps=script("first")), ScriptedChat(steps=script("second"))])
    agent = RagDrafter(Settings(_env_file=None), model_factory=lambda: next(models), knowledge=Knowledge(delay=0.01),
                       investigation=object(), credential_checker=Checker())
    a, b = await asyncio.gather(agent.draft(draft_state("first")), agent.draft(draft_state("second")))
    assert a.citations == ("first",) and b.citations == ("second",)
    assert a.cost_usd == b.cost_usd == pytest.approx(0.043)
    assert "second" not in json.dumps(a.trace) and "first" not in json.dumps(b.trace)


async def test_duplicate_provider_response_ids_count_usage_once():
    steps = script()
    for step in steps:
        step.response_metadata["id"] = "same-provider-response"
    agent, _ = drafter(steps)
    result = await agent.draft(draft_state())
    assert result.cost_usd == pytest.approx(0.033)
    assert len(events(result, "model")) == 1


@pytest.mark.parametrize("phase", ["model", "retrieval", "checker"])
async def test_programming_faults_are_not_provider_unavailability(phase):
    steps = script()
    if phase == "model":
        steps[1] = RuntimeError("programming fault")
    agent, _ = drafter(steps, knowledge=Knowledge(error=RuntimeError("programming fault") if phase == "retrieval" else None),
                       checker=Checker(error=RuntimeError("programming fault") if phase == "checker" else None))
    with pytest.raises(RuntimeError, match="programming fault"):
        await agent.draft(draft_state())


async def test_external_cancellation_is_not_converted_to_timeout():
    agent, _ = drafter(knowledge=Knowledge(delay=10))
    task = asyncio.create_task(agent.draft(draft_state()))
    await asyncio.sleep(0.02)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


async def test_provider_token_cost_estimate_is_retained_on_later_failure():
    steps = script()
    steps[0].response_metadata = {}
    agent, _ = drafter([steps[0], httpx.HTTPStatusError(
        "unauthorized", request=httpx.Request("POST", "https://example.test"), response=httpx.Response(401))])
    result = await agent.draft(draft_state())
    assert result.cost_usd == pytest.approx(0.02015)
    assert events(result, "model")[0]["cost_source"] == "token_estimate"


async def test_model_retry_does_not_repeat_search_and_is_bounded():
    agent, model = drafter([script()[0], httpx.ConnectError("offline")])
    result = await agent.draft(draft_state())
    assert model.calls == 4  # search response, then three attempts at the next response
    assert len(events(result, "tool")) == 1
    assert result.cost_usd == pytest.approx(0.03)
    assert result.reasons == ("llm_unavailable",)


async def test_retry_backoff_cannot_extend_overall_deadline():
    agent, model = drafter([script()[0], httpx.ConnectError("offline")], timeout=0.05)
    result = await agent.draft(draft_state())
    assert result.reasons == ("draft_timeout",) and model.calls == 2
    assert result.cost_usd == pytest.approx(0.03)


async def test_graph_recursion_bounds_unknown_tool_loop():
    agent, model = drafter([answer(call("unknown_tool"))])
    result = await agent.draft(draft_state())
    assert result.reasons == ("draft_tool_limit",)
    # Unknown calls can be rejected within the model node without a tools step.
    assert 1 < model.calls <= 18
    assert events(result, "tool") == []


async def test_sixth_execution_may_submit_successfully():
    steps = [script()[0], *(answer(call("flag_for_human", reason="asks_for_human", note="review"), id=f"flag-{i}")
                           for i in range(4)), script()[1]]
    agent, model = drafter(steps)
    result = await agent.draft(draft_state())
    assert result.text == REPLY and result.reasons == ("asks_for_human",)
    assert len(events(result, "tool")) == 6 and model.calls == 6


async def test_failed_tool_fences_queued_paid_calls_after_return():
    steps = [answer(call("search_knowledge_base", query="first"),
                    call("search_knowledge_base", query="second"),
                    call("flag_for_human", reason="asks_for_human", note="late"))]
    agent, _ = drafter(steps, knowledge=Knowledge(error=EmbeddingError("offline", cost_usd=0.02)))
    result = await agent.draft(draft_state())
    await asyncio.sleep(0.03)
    assert len(events(result, "tool")) == 1
    assert result.cost_usd == pytest.approx(0.03) and result.reasons == ("kb_unavailable",)


async def test_checker_timeout_keeps_already_computed_deterministic_findings():
    agent, _ = drafter(script(reply="أرسل رمز التحقق إلينا"), checker=Checker(delay=10), timeout=0.05)
    result = await agent.draft(draft_state())
    assert result.reasons == ("draft_timeout", "draft_failed_guardrail")
    assert "requests_credentials" in events(result, "guardrail")[-1]["findings"]


async def test_context_is_bounded_and_prompt_separates_untrusted_evidence():
    agent, model = drafter([answer(content="no submission")])
    state = draft_state()
    from dataclasses import replace
    state["ticket"] = replace(state["ticket"], text="UNTRUSTED" * 20000)
    await agent.draft(state)
    system, human = model.seen[0]
    assert "untrusted" in system.content and "UNTRUSTED" not in system.content
    assert len(human.content) < 40000
    payload = json.loads(human.content)
    assert payload["classifier"]["classification"]["category"] == "general_inquiry"


@pytest.mark.parametrize("reported", [0.0, 0.01])
async def test_callback_partial_response_and_error_cost_are_alternatives(reported):
    from uuid import uuid4

    from langchain_core.outputs import ChatGeneration, LLMResult

    from app.pipeline.stage6_draft.agent import _ModelUsage
    from app.pipeline.stage6_draft.context import DraftContext

    ledger = _ModelUsage(DraftContext(draft_state()), Settings(_env_file=None))
    response = LLMResult(generations=[[ChatGeneration(message=answer(cost=reported))]])
    run_id = uuid4()
    await ledger.on_llm_end(response, run_id=run_id)
    error = httpx.ConnectError("interrupted")
    error.cost_usd = 0.01
    await ledger.on_llm_error(error, run_id=run_id, response=response)
    assert ledger.cost_usd == reported
