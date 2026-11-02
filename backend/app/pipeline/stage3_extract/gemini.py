"""Gemini field extractor. Every span is verified against the ticket text."""
from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel, Field

from app.llm import LLMUnavailable, StructuredLLM
from app.pipeline.contracts import FieldPick, NormalizedTicket
from app.pipeline.stage3_extract.prompts import render_prompt
from app.text import to_ascii_digits

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


def verified_pick(span: ExtractedSpan | None, match_text: str, confidence: float) -> FieldPick:
    if span is None or not span.verbatim_span.strip():
        return FieldPick(None, 0.0, "gemini")
    verbatim = to_ascii_digits(span.verbatim_span.strip())
    if verbatim not in match_text:
        return FieldPick(None, 0.0, "gemini")  # hallucinated span, so reject it
    return FieldPick(verbatim, confidence, "gemini", normalized=span.value)


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
