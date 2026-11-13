"""One customer turn: interpret, merge evidence, then ask or prepare a review."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import replace
from uuid import UUID, uuid4

from langgraph.graph import END, StateGraph

from app.intake.answers import quick_answer
from app.intake.contracts import QuestionRecord, TurnContext, TurnResult
from app.intake.errors import IntakeError, InvalidEvidence, ModelUnavailable
from app.intake.evidence import merge_analysis
from app.intake.model import ModelBudget
from app.intake.policy import ask_for, assess_readiness, choose_question
from app.intake.review import build_review
from app.models_config.types import ModelChoice


class IntakeGraph:
    def __init__(self, model, taxonomy, store, settings, *,
                 choice_for: Callable[[UUID], tuple[ModelChoice, float]] | None = None) -> None:
        self.model = model
        self.taxonomy = taxonomy
        self.store = store
        self.settings = settings
        self.choice_for = choice_for
        graph = StateGraph(dict)
        graph.add_node("analyze", self._analyze)
        graph.add_node("merge", self._merge)
        graph.add_node("ask", self._ask)
        graph.add_node("review", self._review)
        graph.set_entry_point("analyze")
        graph.add_edge("analyze", "merge")
        graph.add_conditional_edges("merge", self._route, {"ask": "ask", "review": "review"})
        graph.add_edge("ask", END)
        graph.add_edge("review", END)
        self._compiled = graph.compile()

    async def advance(self, context: TurnContext, answer: dict | None = None) -> TurnResult:
        budget = await self._budget(context)
        try:
            if answer is not None:
                outcome = await self._answer(context, answer, budget)
            else:
                outcome = await self._compiled.ainvoke({
                    "context": context,
                    "images": self._images(context, [item for item in context.messages if item.id == context.current_message_id]),
                    "budget": budget,
                    "trace": [],
                })
        except IntakeError as exc:
            exc.trace = list(budget.trace or exc.trace)
            raise
        return TurnResult(outcome["state"], outcome.get("assistant_text"), outcome.get("review"), outcome.get("trace", []))

    async def _answer(self, context: TurnContext, answer: dict, budget: ModelBudget) -> dict:
        analysis = quick_answer(context, answer["key"], answer["choice"])
        state = self._merge({
            "context": context, "analysis": analysis, "visible_image_ids": set(), "budget": budget, "trace": [],
        })
        if self._route(state) == "review":
            return await self._review(state)
        return self._ask(state)

    async def review(self, context: TurnContext, *, allow_partial: bool, language: str) -> TurnResult:
        budget = await self._budget(context)
        try:
            return await self._review_current(context, allow_partial=allow_partial, language=language, budget=budget)
        except IntakeError as exc:
            exc.trace = list(budget.trace or exc.trace)
            raise

    def ask(self, context: TurnContext, key: str) -> TurnResult:
        question = ask_for(context.state, key, context.revision + 1)
        readiness = assess_readiness(context.state, self.taxonomy).model_copy(update={"next_key": key})
        outcome = self._ask({"state": context.state.model_copy(update={"readiness": readiness}), "question": question})
        return TurnResult(outcome["state"], outcome["assistant_text"], None, [])

    async def _review_current(self, context: TurnContext, *, allow_partial: bool, language: str, budget: ModelBudget) -> TurnResult:
        if not context.messages and not any(not item.removed for item in context.attachments):
            raise InvalidEvidence("Add a message or screenshot before review.")
        unbound = [item for item in context.attachments if not item.removed and item.message_id is None]
        trace = []
        if context.needs_analysis or unbound:
            images = self._images(context, [item for item in context.messages if item.id == context.current_message_id])
            images += [self.store.load_for_session(context.session_id, item.id) for item in unbound]
            analyzed = await self._analyze({"context": context, "images": images, "budget": budget, "trace": []})
            state = merge_analysis(analyzed["context"], analyzed["analysis"], visible_image_ids=analyzed["visible_image_ids"])
            context = replace(context, state=state)
            trace = analyzed["trace"]
        readiness = assess_readiness(context.state, self.taxonomy, allow_partial=allow_partial)
        if readiness.quality == "collecting" and not allow_partial:
            raise InvalidEvidence("More detail is needed before review.")
        if readiness.quality == "collecting":
            readiness = readiness.model_copy(update={"quality": "partial_context"})
        state = context.state.model_copy(update={"language": language, "readiness": readiness})
        call = await self.model.summarize(state, language, budget)
        snapshot = build_review(
            context, state, call.value, publication=context.revision + 1, language=language, taxonomy=self.taxonomy
        )
        return TurnResult(state, _invitation(language), snapshot, [*trace, *call.trace])

    async def _budget(self, context: TurnContext) -> ModelBudget:
        timeout, choice = self.settings.intake_timeout_s, None
        if self.choice_for is not None:
            try:
                choice, timeout = await asyncio.to_thread(self.choice_for, context.session_id)
            except Exception as exc:
                # Never fall back to a different provider for a customer conversation.
                raise ModelUnavailable("The assistant is temporarily unavailable.", trace=[]) from exc
        return ModelBudget(timeout, self.settings.intake_max_model_requests, choice=choice)

    def _images(self, context: TurnContext, messages: list):
        wanted = {attachment_id for message in messages for attachment_id in message.attachment_ids}
        images = []
        for attachment in context.attachments:
            if attachment.id in wanted and not attachment.removed:
                images.append(self.store.load_for_session(context.session_id, attachment.id))
        return images

    async def _analyze(self, state: dict) -> dict:
        call = await self.model.analyze(state["context"], state["images"], state["budget"])
        analysis = call.value
        trace = [*state.get("trace", []), *call.trace]
        already = {image.id for image in state["images"]}
        extra = []
        owned = {item.id: item for item in state["context"].attachments if not item.removed}
        for image_id in analysis.reinspect_images:
            if image_id in owned and image_id not in already:
                extra.append(self.store.load_for_session(state["context"].session_id, image_id))
        if extra:
            # Ground the first pass before reinspection, and carry it into the
            # second pass so newly extracted facts are not silently discarded.
            merged = merge_analysis(state["context"], analysis, visible_image_ids=already)
            state = {**state, "context": replace(state["context"], state=merged)}
            again = await self.model.analyze(state["context"], [*state["images"], *extra], state["budget"])
            analysis = again.value
            trace = [*trace, *again.trace]
        return {**state, "analysis": analysis, "trace": trace, "visible_image_ids": already | {image.id for image in extra}}

    def _merge(self, state: dict) -> dict:
        merged = merge_analysis(state["context"], state["analysis"], visible_image_ids=state["visible_image_ids"])
        readiness = assess_readiness(merged, self.taxonomy)
        question = choose_question(
            merged, state["analysis"].suggested_question, state["context"].revision + 1, self.taxonomy
        )
        readiness = readiness.model_copy(update={"next_key": question.key if question is not None else None})
        return {**state, "state": merged.model_copy(update={"readiness": readiness}), "question": question}

    @staticmethod
    def _route(state: dict) -> str:
        readiness = state["state"].readiness
        if readiness.quality == "sufficient_context" or state.get("question") is None:
            return "review"
        return "ask"

    @staticmethod
    def _ask(state: dict) -> dict:
        question = state["question"]
        record = QuestionRecord(
            key=question.key, basis_revision=question.basis_revision, message_id=uuid4(), outcome="asked",
            reason=question.reason, attempt=question.attempt,
        )
        updated = state["state"].model_copy(update={"questions": [*state["state"].questions, record]})
        return {**state, "state": updated, "assistant_text": question.text, "review": None}

    async def _review(self, state: dict) -> dict:
        language = state["state"].language
        call = await self.model.summarize(state["state"], language, state["budget"])
        snapshot = build_review(
            state["context"], state["state"], call.value, publication=state["context"].revision + 1,
            language=language, taxonomy=self.taxonomy,
        )
        return {
            **state,
            "assistant_text": _invitation(language),
            "review": snapshot,
            "trace": [*state.get("trace", []), *call.trace],
        }


def _invitation(language: str) -> str:
    if language == "ar":
        return "راجع التفاصيل قبل الإرسال."
    return "Please review the details before submitting."
