"""Builders and a scripted intake model. Evidence quotes use the real source text."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.intake.contracts import (
    Analysis,
    EvidenceRef,
    Fact,
    IntakeState,
    Message,
    ModelCall,
    Readiness,
    ReviewText,
    TurnContext,
)
from app.intake.errors import ModelUnavailable


def message(text, *, language="ar", at=None, attachments=(), role="user"):
    return Message(
        id=uuid4(),
        role=role,
        text=text,
        language=language,
        created_at=at or datetime.now(UTC),
        attachment_ids=list(attachments),
    )


def fact(key, value, source: Message, *, normalized=None, status="known"):
    return Fact(
        key=key,
        status=status,
        value=value if status == "known" else None,
        normalized=normalized if status == "known" else None,
        evidence=[EvidenceRef(kind="message", source_id=source.id, quote=source.text)],
    )


def context(messages=(), facts=(), *, category="other", revision=0, attachments=()):
    items = list(messages)
    language = items[-1].language if items else "ar"
    state = IntakeState(
        language=language,
        category=category,
        facts={item.key: item for item in facts},
        additional_issues=[],
        additional_needed=[],
        questions=[],
        readiness=Readiness(
            quality="collecting", missing=[], conflicts=[], reason="Collecting customer context.", next_key="issue"
        ),
    )
    return TurnContext(
        session_id=uuid4(),
        revision=revision,
        state=state,
        messages=items,
        attachments=list(attachments),
        current_message_id=items[-1].id if items else None,
    )


def grounded_analysis(turn: TurnContext) -> Analysis:
    source = next(item for item in reversed(turn.messages) if item.role == "user")
    return Analysis(
        language=source.language,
        category="general_inquiry",
        updates=[fact("issue", source.text, source)],
        additional_issues=[],
        suggested_question=None,
        additional_needed=[],
        reinspect_images=[],
    )


def grounded_review(state: IntakeState, language: str) -> ReviewText:
    issue = state.facts["issue"].value or ""
    customer = issue if language == "ar" else f"The customer reported: {issue}"
    employee = issue if language == "ar" else f"أبلغ الزبون بالمشكلة التالية: {issue}"
    return ReviewText(customer_text=customer, employee_text_ar=employee, fact_keys=["issue"])


class ScriptedIntakeModel:
    """Returns scripted analyses and reviews. Callables see the current context."""

    def __init__(self, analyses=None, reviews=None):
        self.analyses = list(analyses or [])
        self.reviews = list(reviews or [])
        self.calls: list[tuple] = []

    def _next(self, items, default, *args):
        item = items.pop(0) if items else default
        if isinstance(item, Exception):
            raise item
        if callable(item):
            item = item(*args)
        if isinstance(item, Exception):
            raise item
        return item

    async def analyze(self, turn: TurnContext, images, budget):
        budget.consume()
        try:
            value = self._next(self.analyses, grounded_analysis, turn)
        except ModelUnavailable:
            raise
        except Exception as exc:
            budget.trace.append({"error": type(exc).__name__})
            raise
        self.calls.append(("analyze", turn.current_message_id, [image.id for image in images]))
        return ModelCall(value, list(budget.trace))

    async def summarize(self, state: IntakeState, language: str, budget):
        budget.consume()
        value = self._next(self.reviews, grounded_review, state, language)
        self.calls.append(("summarize", language, [key for key in state.facts]))
        return ModelCall(value, list(budget.trace))


def image_evidence(key: str, value: str, source_id: UUID, quote: str) -> Fact:
    return Fact(
        key=key, status="known", value=value,
        evidence=[EvidenceRef(kind="image", source_id=source_id, quote=quote)],
    )
