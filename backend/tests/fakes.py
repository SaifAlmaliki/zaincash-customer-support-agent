"""Test doubles for the model boundaries. No network in unit tests."""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

from langchain_typesafe import Noul, Score

from app.llm import Sample
from app.pipeline.contracts import (
    FIELD_NAMES,
    FLAG_NAMES,
    ClassificationResult,
    ClassifierOutput,
    FieldPick,
)


class FakeJevRunnable:
    """Mimics TypeSafeClassifier.ainvoke and records each request."""

    def __init__(self, *, category="failed_transfer", top_prob=0.9, confidence=0.9,
                 reversed_choice=None, priority_level=2, flags=None, picks=None,
                 raises=None, model="jev-1.13.0"):
        self.category, self.top_prob, self.confidence = category, top_prob, confidence
        self.reversed_choice, self.priority_level = reversed_choice, priority_level
        self.flags, self.picks = flags or {}, picks or {}
        self.raises, self.model, self.calls = raises, model, []

    async def ainvoke(self, request):
        self.calls.append(request)
        if self.raises:
            raise self.raises
        questions = request["questions"]
        order_check = list(questions) == ["category"]
        choices, scores, nouls = {}, {}, {}
        for qid, q in questions.items():
            if isinstance(q, Score):
                probs = {str(i): (0.85 if i == self.priority_level else 0.05) for i in range(4)}
                scores[qid] = SimpleNamespace(
                    score=float(self.priority_level), probabilities=probs, confidence=0.8
                )
            elif isinstance(q, Noul):
                nouls[qid] = SimpleNamespace(noul=self.flags.get(qid, 0.05))
            elif qid == "category":
                choice = self.reversed_choice if (order_check and self.reversed_choice) else self.category
                choices[qid] = SimpleNamespace(
                    choice=choice,
                    probabilities={choice: self.top_prob, "other": round(1 - self.top_prob, 4)},
                    confidence=self.confidence,
                )
            else:
                value, conf = self.picks.get(qid.removeprefix("pick_"), ("none", 0.9))
                choices[qid] = SimpleNamespace(choice=value, probabilities={value: conf}, confidence=conf)
        return SimpleNamespace(
            choices=choices, scores=scores, nouls=nouls, model=self.model,
            usage=SimpleNamespace(input_tokens=1000, output_tokens=0),
        )


class FakeStructuredLLM:
    """Returns the queued responses in order. Exceptions become failed Samples. The last item repeats."""

    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    async def sample(self, prompt, schema, *, temperature, n=1):
        self.calls.append({"prompt": prompt, "schema": schema, "temperature": temperature, "n": n})
        out = []
        for _ in range(n):
            item = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
            out.append(
                Sample(None, 0.0, repr(item)) if isinstance(item, BaseException) else Sample(item, 0.001)
            )
        return out


class FakeClassifier:
    """Returns a preset output (or raises). Tracks how many calls are in flight at once."""

    def __init__(self, output=None, raises=None, delay=0.0, fail_for=()):
        self.output, self.raises, self.delay, self.fail_for = output, raises, delay, set(fail_for)
        self.calls, self.inflight, self.max_inflight = 0, 0, 0

    async def classify(self, nt, cands):
        self.calls += 1
        self.inflight += 1
        self.max_inflight = max(self.max_inflight, self.inflight)
        try:
            await asyncio.sleep(self.delay)
            if self.raises or nt.ticket.external_id in self.fail_for:
                raise self.raises or RuntimeError("boom")
            return self.output
        finally:
            self.inflight -= 1


class FakeExtractor:
    def __init__(self, picks=None, raises=None):
        self.picks, self.raises, self.requested = picks or {}, raises, []

    async def extract(self, nt, fields):
        self.requested.append(list(fields))
        if self.raises:
            raise self.raises
        return {f: self.picks[f] for f in fields if f in self.picks}, 0.002


def make_output(category="failed_transfer", *, confidence=0.9, uncertain=False, source="jev",
                priority="P2", flags=None, picks=None, path="jev", reasons=(), cost=0.0):
    cls = ClassificationResult(
        category=category, category_confidence=confidence,
        category_probs={category: confidence}, priority=priority, priority_confidence=0.8,
        flags={f: 0.05 for f in FLAG_NAMES} | (flags or {}), source=source,
        uncertain=uncertain, model="test-model",
    )
    default_picks = {f: FieldPick(None, 0.0, "none") for f in FIELD_NAMES}
    return ClassifierOutput(
        cls, default_picks | (picks or {}), path=path, reasons=tuple(reasons), cost_usd=cost
    )
