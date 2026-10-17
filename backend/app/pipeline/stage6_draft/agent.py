"""One bounded, isolated LangChain agent invocation per ticket."""
from __future__ import annotations

import asyncio
import json
import math
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from time import perf_counter
from typing import Any

import httpx
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelResponse
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from openrouter.errors import OpenRouterError

from app.config import Settings
from app.kb.embeddings import EmbeddingError
from app.kb.service import KnowledgeError, KnowledgeExecutionError, KnowledgeService
from app.llm import LLMUnavailable
from app.pipeline.contracts import DraftResult
from app.pipeline.execution import ticket_execution
from app.pipeline.stage6_draft.context import DraftContext, DraftToolInputError, DraftToolLimit
from app.pipeline.stage6_draft.credentials import CredentialChecker
from app.pipeline.stage6_draft.drafting import DraftExecutionError
from app.pipeline.stage6_draft.guardrails import check_draft
from app.pipeline.stage6_draft.investigation import SqlInvestigationRepo
from app.pipeline.stage6_draft.model import DraftProviderResponseError
from app.pipeline.stage6_draft.tools import _bounded, _json, build_tools
from app.pipeline.state import PipelineState

PROMPT_VERSION = "draft_v1"
SYSTEM_PROMPT = Path(__file__).with_name("prompts").joinpath(f"{PROMPT_VERSION}.md").read_text(encoding="utf-8")
_PROVIDER_ERRORS = (httpx.HTTPError, OpenRouterError, LLMUnavailable)


def _number(value: Any) -> float:
    try:
        return float(value) if type(value) in (int, float) and math.isfinite(value) and value >= 0 else 0.0
    except OverflowError:
        return 0.0


def _error_cost(error: BaseException) -> float:
    if hasattr(error, "cost_usd"):
        return _number(error.cost_usd)
    if isinstance(error, TimeoutError) and error.__cause__ is not None:
        return _number(getattr(error.__cause__, "cost_usd", 0))
    return 0.0


class _ModelUsage(AsyncCallbackHandler):
    """Execution-time accounting: no dependence on the final graph response."""

    run_inline = True

    def __init__(self, context: DraftContext, settings: Settings):
        self.context, self.settings = context, settings
        self.seen: set[str] = set()
        self.cost_usd = 0.0

    async def on_llm_end(self, response, *, run_id, **kwargs):
        for batch in response.generations:
            for generation in batch:
                message = getattr(generation, "message", None)
                if message is None:
                    continue
                self._record_response(message.response_metadata or {}, message.usage_metadata or {},
                                      fallback_id=message.id or run_id)

    def _record_response(self, metadata, usage, *, fallback_id, error_type=None):
        response_id = str(metadata.get("id") or fallback_id)
        if response_id in self.seen:
            return
        self.seen.add(response_id)
        cost = (_number(usage.get("input_tokens")) * self.settings.price_gemini_flash_in
                + _number(usage.get("output_tokens")) * self.settings.price_gemini_flash_out) / 1e6
        source = "token_estimate"
        reported = metadata.get("cost")
        if type(reported) in (int, float) and math.isfinite(reported) and reported >= 0:
            cost, source = float(reported), "provider"
        self.cost_usd += cost
        entry = {"kind": "model", "status": "error" if error_type else "ok", "response_id": response_id,
                 "model": metadata.get("model_name") or self.settings.gemini_model,
                 "usage": _bounded(usage), "cost_usd": cost, "cost_source": source}
        if error_type:
            entry["error_type"] = error_type
        self.context.trace.append(entry)

    async def on_llm_error(self, error, *, run_id, **kwargs):
        if isinstance(error, DraftProviderResponseError):
            self._record_response(error.response_metadata, error.usage_metadata,
                                  fallback_id=run_id, error_type=type(error).__name__)
            return
        partial = kwargs.get("response")
        has_response = partial is not None and any(
            getattr(generation, "message", None) is not None
            for batch in partial.generations for generation in batch)
        if partial is not None:
            await self.on_llm_end(partial, run_id=run_id)
        # Partial response usage (even zero or an already-seen ID) and explicit
        # error cost are alternative outcomes of the SAME model invocation.
        cost = 0.0 if has_response else _error_cost(error)
        self.cost_usd += cost
        self.context.trace.append({"kind": "model", "status": "error", "model": self.settings.gemini_model,
                                   "error_type": type(error).__name__, "cost_usd": cost})


class _Execution(AgentMiddleware):
    """Retry model requests only; fence queued tools after failure or submission."""

    def __init__(self, context: DraftContext):
        self.context = context
        self.lock = asyncio.Lock()
        self.stopped = False

    async def awrap_model_call(self, request, handler):
        # create_agent's direct-return edge requires ALL calls in a batch to be
        # direct. A mixed submit/investigate batch must still stop without buying
        # another model response. The accepted reply lives only in submission.
        if self.context.submission is not None:
            return ModelResponse(result=[AIMessage(content="Draft submitted.")])
        for attempt in range(3):
            try:
                return await handler(request)
            except _PROVIDER_ERRORS as exc:
                status = getattr(exc, "status_code", None)
                if isinstance(exc, httpx.HTTPStatusError):
                    status = exc.response.status_code
                transient = isinstance(exc, httpx.TransportError) or (
                    isinstance(status, int) and (status in (408, 429) or status >= 500))
                if not transient or attempt == 2:
                    raise LLMUnavailable("Drafting model unavailable") from exc
                await asyncio.sleep(0.5 * 2**attempt)

    async def awrap_tool_call(self, request, handler):
        # ToolNode runs a batch concurrently. A second fence ensures a failed
        # sibling cannot leave queued paid work executing after ainvoke raises.
        async with self.lock:
            if self.stopped or self.context.submission is not None:
                return ToolMessage(content="Draft execution is closed.", tool_call_id=request.tool_call["id"])
            try:
                return await handler(request)
            except BaseException:
                self.stopped = True
                raise


class RagDrafter:
    def __init__(self, settings: Settings, *, model_factory: Callable[[], BaseChatModel],
                 knowledge: KnowledgeService, investigation: SqlInvestigationRepo,
                 credential_checker: CredentialChecker):
        self.settings, self.model_factory = settings, model_factory
        self.knowledge, self.investigation = knowledge, investigation
        self.credential_checker = credential_checker

    async def draft(self, state: PipelineState) -> DraftResult:
        context = DraftContext(state, max_tool_calls=self.settings.agent_max_tool_calls)
        usage = _ModelUsage(context, self.settings)
        execution = _Execution(context)
        checker_cost = 0.0
        findings: list[str] = []
        started = perf_counter()
        failure = None
        unexpected = None
        cancelled = None
        ticket_run = ticket_execution.get()
        budget = ticket_run.draft_budget(self.settings.agent_timeout_s) if ticket_run else self.settings.agent_timeout_s
        try:
            async with asyncio.timeout(budget):
                if budget <= 0:
                    raise TimeoutError
                payload = {key: _bounded(_json(context.state[key]), self.settings.max_state_chars)
                           for key in ("ticket", "nt", "classifier", "extracted", "lookup", "decision")
                           if key in context.state}
                payload.update(tool_execution_limit=context.max_tool_calls, retrieval_k=self.settings.kb_top_k)
                agent = create_agent(model=self.model_factory(),
                                     tools=build_tools(context, self.knowledge, self.investigation),
                                     system_prompt=SYSTEM_PROMPT, middleware=[execution])
                await agent.ainvoke({"messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}]},
                                   config={"recursion_limit": 2 * context.max_tool_calls + 6, "callbacks": [usage]})
                if context.submission is not None:
                    submission = context.submission
                    findings = check_draft(submission.reply_ar, list(submission.citations),
                                           submission.used_txn_ref, context.state, context.retrieved)
                    entry = {"kind": "guardrail", "status": "checking", "findings": findings,
                             "credential_check_degraded": True, "requests_credentials": None, "cost_usd": 0.0}
                    context.trace.append(entry)
                    try:
                        check = await self.credential_checker.check(submission.reply_ar)
                    except (Exception, asyncio.CancelledError) as exc:
                        checker_cost = _error_cost(exc)
                        entry.update(status="error", error_type=type(exc).__name__, cost_usd=checker_cost)
                        raise
                    checker_cost = check.cost_usd
                    if not check.degraded and check.requests_credentials is not None and check.requests_credentials >= 0.2:
                        findings.append("requests_credentials")
                    findings[:] = list(dict.fromkeys(findings))
                    entry.update(status="failed" if findings else "passed", cost_usd=checker_cost,
                                 credential_check_degraded=check.degraded, requests_credentials=check.requests_credentials)
                    # Deliver an expired deadline even if a synchronous check used
                    # the remainder without yielding to the event loop.
                    if perf_counter() - started >= budget:
                        raise TimeoutError
                else:
                    searched = any(e.get("tool") == "search_knowledge_base" and e.get("status") == "ok"
                                   for e in context.trace)
                    context.reasons.append("no_kb_support" if searched and not context.retrieved else "draft_not_submitted")
        except asyncio.CancelledError as exc:
            # Finalize measured work before propagating the SAME cancellation.
            # A genuine caller cancellation must not become a timeout result.
            cancelled = exc
            if ticket_run is not None and ticket_run.timeout.expired():
                failure = "draft_timeout"
        except TimeoutError:
            failure = "draft_timeout"
        except (DraftToolLimit, GraphRecursionError):
            failure = "draft_tool_limit"
        except DraftToolInputError:
            failure = "draft_not_submitted"
        except (EmbeddingError, KnowledgeError):
            failure = "kb_unavailable"
        except LLMUnavailable:
            failure = "llm_unavailable"
        except Exception as exc:
            unexpected = exc
        finally:
            execution.stopped = True

        if failure:
            context.reasons.append(failure)
        if findings:
            context.reasons.append("draft_failed_guardrail")
        submission = context.submission
        if submission is not None and not context.retrieved:
            context.reasons.append("no_kb_support")
        reasons = tuple(dict.fromkeys(context.reasons))
        cost = context.cost_usd + usage.cost_usd + checker_cost
        rejected = failure or findings or submission is None or not context.retrieved
        status = "cancelled" if cancelled is not None else "error" if unexpected else "rejected" if rejected else "submitted"
        context.trace.append({"kind": "draft", "status": status,
                              "prompt_version": PROMPT_VERSION, "model": self.settings.gemini_model,
                              "embedding_model": self.settings.embedding_model,
                              "reply_ar": submission.reply_ar if submission else None,
                              "citations": list(submission.citations) if submission else [],
                              "used_txn_ref": submission.used_txn_ref if submission else None,
                              "internal_note": submission.internal_note if submission else "",
                              "notes": context.notes, "reasons": list(reasons), "findings": findings,
                              "citation_sources": [asdict(p) for p in context.retrieved.values()],
                              "tool_count": context.tool_count, "duration_ms": round((perf_counter() - started) * 1000, 3),
                              "cost_usd": cost, "model_cost_usd": usage.cost_usd,
                              "search_cost_usd": context.cost_usd, "credential_cost_usd": checker_cost})
        result = DraftResult(text=submission.reply_ar if submission and context.retrieved else None,
                             citations=submission.citations if submission else (), trace=tuple(context.trace),
                             reasons=reasons, cost_usd=cost)
        if cancelled is not None:
            cancelled.draft_result = result
            raise cancelled
        if unexpected is not None:
            context.trace[-1]["error_type"] = (unexpected.diagnostic_type if isinstance(unexpected, KnowledgeExecutionError)
                                              else type(unexpected).__name__)
            raise DraftExecutionError(unexpected, result) from unexpected
        return result
