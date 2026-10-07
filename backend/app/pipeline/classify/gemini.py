"""Gemini classifier (n-sample self-consistency) and field extractor. Every span is verified against the ticket text."""
from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel, Field

from app.llm import LLMUnavailable, StructuredLLM
from app.pipeline.contracts import (
    FIELD_NAMES, FLAG_NAMES, Candidates, ClassificationResult, ClassifierOutput, FieldPick,
    NormalizedTicket,
)
from app.pipeline.normalize import to_ascii_digits
from app.pipeline.prompts import render_prompt
from app.taxonomy import Taxonomy

GEMINI_EXTRACT_CONFIDENCE = 0.6


class ExtractedSpan(BaseModel):
    value: str = Field(description="Normalized value")
    verbatim_span: str = Field(description="Exact substring copied from the ticket")


class _Fields(BaseModel):
    txn_ref: ExtractedSpan | None = None
    amount: ExtractedSpan | None = None
    phone: ExtractedSpan | None = None
    date: ExtractedSpan | None = None


class GeminiFields(_Fields):
    pass


class GeminiAnalysis(_Fields):
    category: str = Field(description="Exactly one category id from the taxonomy")
    priority: Literal["P1", "P2", "P3", "P4"]
    fraud_suspected: bool = False
    money_lost: bool = False
    multi_issue: bool = False
    urgent_or_angry: bool = False
    mentions_specific_transaction: bool = False
    asks_for_human: bool = False


def verified_pick(span: ExtractedSpan | None, match_text: str, confidence: float) -> FieldPick:
    if span is None or not span.verbatim_span.strip():
        return FieldPick(None, 0.0, "gemini")
    verbatim = to_ascii_digits(span.verbatim_span.strip())
    if verbatim not in match_text:
        return FieldPick(None, 0.0, "gemini")  # hallucinated span, so reject it
    return FieldPick(verbatim, confidence, "gemini", normalized=span.value)


class GeminiClassifier:
    def __init__(self, llm: StructuredLLM, taxonomy: Taxonomy, *, t_gem: float, samples: int = 3,
                 temperature: float = 0.7, max_state_chars: int = 6000) -> None:
        self._llm, self._tax, self._t_gem = llm, taxonomy, t_gem
        self._n, self._temperature, self._max_chars = samples, temperature, max_state_chars

    async def classify(self, nt: NormalizedTicket, cands: Candidates) -> ClassifierOutput:
        prompt = render_prompt(
            "gemini_classify_v1",
            taxonomy=self._tax.render(),
            received_at=nt.ticket.received_at.isoformat(),
            channel=nt.ticket.channel,
            ticket=nt.ticket.text[: self._max_chars],
        )
        samples = await self._llm.sample(
            prompt, GeminiAnalysis, temperature=self._temperature, n=self._n
        )
        parsed = [s.parsed for s in samples if s.parsed is not None]
        cost = sum(s.cost_usd for s in samples)
        if not parsed:
            raise LLMUnavailable(f"all {self._n} Gemini samples failed: {samples[0].error}")
        votes = Counter(a.category for a in parsed if a.category in self._tax.categories)
        category, count = votes.most_common(1)[0] if votes else ("other", 0)
        confidence = count / self._n
        agreeing = [a for a in parsed if a.category == category] or parsed
        priority, p_count = Counter(a.priority for a in agreeing).most_common(1)[0]
        uncertain = confidence < self._t_gem
        rep = agreeing[0]
        classification = ClassificationResult(
            category=category,
            category_confidence=confidence,
            category_probs={c: v / self._n for c, v in votes.items()},
            priority=priority,
            priority_confidence=p_count / len(agreeing),
            flags={f: sum(bool(getattr(a, f)) for a in parsed) / len(parsed) for f in FLAG_NAMES},
            source="gemini",
            uncertain=uncertain,
            model="gemini",
        )
        picks = {f: verified_pick(getattr(rep, f), nt.match_text, confidence) for f in FIELD_NAMES}
        return ClassifierOutput(
            classification=classification,
            picks=picks,
            path="gemini",
            reasons=("low_confidence",) if uncertain else (),
            cost_usd=cost,
        )


class GeminiExtractor:
    def __init__(self, llm: StructuredLLM, *, max_state_chars: int = 6000) -> None:
        self._llm, self._max_chars = llm, max_state_chars

    async def extract(
        self, nt: NormalizedTicket, fields: Sequence[str]
    ) -> tuple[dict[str, FieldPick], float]:
        prompt = render_prompt(
            "gemini_extract_v1",
            fields=", ".join(fields),
            received_at=nt.ticket.received_at.isoformat(),
            ticket=nt.ticket.text[: self._max_chars],
        )
        [sample] = await self._llm.sample(prompt, GeminiFields, temperature=0.0, n=1)
        if sample.parsed is None:
            raise LLMUnavailable(sample.error or "extraction failed")
        picks = {
            f: verified_pick(getattr(sample.parsed, f), nt.match_text, GEMINI_EXTRACT_CONFIDENCE)
            for f in fields
        }
        return picks, sample.cost_usd
