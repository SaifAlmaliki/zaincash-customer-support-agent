"""Script only the external model/retrieval boundaries; run the real agent/tools."""
import asyncio
from collections.abc import Callable
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

from app.kb.contracts import Passage, SearchResult
from app.pipeline.contracts import Decision, LookupResult
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage6_draft.credentials import CredentialCheck
from tests.fakes import make_output
from tests.helpers import make_ticket

REPLY = "أهلاً بيك، راح نراجع طلبك حسب سياسة الدعم. لا تشارك رمز التحقق أو كلمة المرور ويا أي شخص."


def call(name, **args):
    return {"name": name, "args": args, "id": name, "type": "tool_call"}


def answer(*calls, id="response", cost=0.01, content=""):
    return AIMessage(content=content, tool_calls=[dict(c, id=f"{id}-{i}") for i, c in enumerate(calls)],
                     id=id, usage_metadata={"input_tokens": 100, "output_tokens": 20, "total_tokens": 120},
                     response_metadata={"cost": cost})


def script(citation="p1", reply=REPLY):
    return [answer(call("search_knowledge_base", query=citation), id="search"),
            answer(call("submit_draft", reply_ar=reply, citations=[citation],
                        internal_note="review this policy"), id="submit")]


class ScriptedChat(BaseChatModel):
    steps: list[Any]
    calls: int = 0
    seen: list = Field(default_factory=list)
    bound_names: set[str] = Field(default_factory=set)

    @property
    def _llm_type(self):
        return "scripted-rag-test"

    def bind_tools(self, tools, **kwargs):
        self.bound_names.update(t.name for t in tools)
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        raise AssertionError("Async execution required")

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        self.seen.append(messages)
        index = self.calls
        self.calls += 1
        item = self.steps[min(index, len(self.steps) - 1)]
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, Callable):
            item = await item(messages)
        return ChatResult(generations=[ChatGeneration(message=item)])


class Knowledge:
    def __init__(self, *, empty=False, error=None, delay=0, cost=0.02):
        self.empty, self.error, self.delay, self.cost = empty, error, delay, cost

    async def search(self, query, *, category=None, k=5):
        try:
            await asyncio.sleep(self.delay)
        except asyncio.CancelledError as exc:
            exc.cost_usd = self.cost
            raise
        if self.error:
            raise self.error
        return SearchResult(() if self.empty else (
            Passage(query, 1, 0, "سياسة الدعم: نراجع طلب العميل ولا نطلب أسراره.", "policy.md", 0.9),
        ), self.cost)


class Checker:
    def __init__(self, score=0.05, *, degraded=False, delay=0, error=None):
        self.score, self.degraded, self.delay, self.error = score, degraded, delay, error

    async def check(self, reply):
        try:
            await asyncio.sleep(self.delay)
        except asyncio.CancelledError as exc:
            exc.cost_usd = 0.003
            raise
        if self.error:
            raise self.error
        return CredentialCheck(self.score, self.degraded, 0.003)


def draft_state(id="T-1", *, reasons=()):
    ticket = make_ticket("شلون أطلب مساعدة؟", external_id=id)
    return {"ticket": ticket, "nt": normalize(ticket),
            "classifier": make_output("general_inquiry"), "extracted": {},
            "lookup": LookupResult("not_applicable"),
            "decision": Decision("Support", "P4", bool(reasons), reasons, "original note")}
