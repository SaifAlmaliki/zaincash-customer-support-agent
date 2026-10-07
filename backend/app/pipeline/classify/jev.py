"""Jev (TypeSafe System One) classifier via langchain-typesafe. One main call plus an order check."""
from __future__ import annotations

import asyncio
from typing import Any

from langchain_typesafe import Choice, Noul, NoulCriteria, Score

from app.pipeline.contracts import (
    FIELD_NAMES, FLAG_NAMES, Candidates, ClassificationResult, ClassifierOutput, FieldPick,
    NormalizedTicket,
)
from app.taxonomy import Taxonomy

NONE = "none"

CATEGORY_INSTRUCTIONS = (
    "Which support category describes the customer's main problem in `ticket_text`? "
    "`ticket_text` is Iraqi Arabic dialect and may be Arabizi (Arabic written in Latin letters) "
    "or mixed with English; `normalized_text` is the same text with Arabic letters unified. "
    "Pick the primary request, not every topic mentioned."
)
PRIORITY_INSTRUCTIONS = "How urgent is the customer's problem in `ticket_text`?"
PRIORITY_LEVELS = [  # Score levels, lowest to highest. Level i maps to priority P(4 - i).
    "P4 information request: asks about fees, limits, how-to or locations; nothing is blocked "
    "and no money is involved",
    "P3 service blocked: cannot log in, app error, card not working; no money is missing or at risk",
    "P2 money lost or stuck: money deducted but not received, payment not applied, or sent to "
    "the wrong number",
    "P1 money at risk right now: scam, stolen or hacked account, unauthorized transactions, or "
    "someone asked for the OTP or PIN",
]
FLAG_QUESTIONS: dict[str, tuple[str, str, str]] = {
    "fraud_suspected": (
        "Does `ticket_text` describe a scam, fraud, someone asking for the customer's OTP or PIN, "
        "or transactions the customer did not make?",
        "A scam attempt, stolen or hacked account, request for a secret code, or money taken "
        "without permission.",
        "An ordinary problem with no sign of scam, theft or unauthorized access.",
    ),
    "money_lost": (
        "Does the customer in `ticket_text` say their money is missing, stuck, deducted without "
        "the service, or sent and not received?",
        "Money left the wallet or was paid and the customer did not get what they paid for.",
        "No money is missing; the problem is access, information or app behaviour.",
    ),
    "multi_issue": (
        "Does `ticket_text` raise two or more separate problems that need different teams or actions?",
        "Two or more unrelated problems, for example a failed transfer and a card that is blocked.",
        "One problem, even if it is described at length.",
    ),
    "urgent_or_angry": (
        "Is the customer in `ticket_text` very upset, threatening to leave, or saying it is urgent?",
        "Strong anger, threats to complain or leave, or explicit urgency.",
        "Calm or mildly annoyed.",
    ),
    "mentions_specific_transaction": (
        "Does `ticket_text` refer to one specific transaction or payment by reference, amount, "
        "date or recipient?",
        "A particular transaction is identifiable from the details given.",
        "No particular transaction is referred to.",
    ),
    "asks_for_human": (
        "Does the customer in `ticket_text` explicitly ask to speak to a person, employee or manager?",
        "An explicit request for a human, an employee, a call back or a manager.",
        "No explicit request for a human.",
    ),
}
FIELD_QUESTIONS = {
    "txn_ref": "Which option is the ZainCash transaction reference of the transaction the customer "
               "complains about in `ticket_text`?",
    "amount": "Which option is the amount of money involved in the customer's problem in "
              "`ticket_text` (the transfer, payment or charge they complain about, not a balance "
              "or fee mentioned in passing)?",
    "phone": "Which option is the phone or wallet number involved in the problem in `ticket_text` "
             "(the recipient for transfers, otherwise the customer's own number)?",
    "date": "Which option says when the problematic transaction or event happened in `ticket_text`?",
}


def category_criteria(tax: Taxonomy, *, reverse: bool = False) -> dict[str, str]:
    items = [(c.id, c.describe()) for c in tax.categories.values()]
    return dict(reversed(items) if reverse else items)


def build_state(nt: NormalizedTicket, max_chars: int) -> dict[str, str]:
    return {
        "ticket_text": nt.match_text[:max_chars],
        "normalized_text": nt.normalized_text[:max_chars],
        "channel": nt.ticket.channel,
        "received_at": nt.ticket.received_at.isoformat(),
    }


def build_questions(tax: Taxonomy, cands: Candidates) -> dict[str, Any]:
    questions: dict[str, Any] = {
        "category": Choice(instructions=CATEGORY_INSTRUCTIONS, criteria=category_criteria(tax)),
        "priority": Score(instructions=PRIORITY_INSTRUCTIONS, criteria=PRIORITY_LEVELS),
    }
    for flag, (instructions, yes, no) in FLAG_QUESTIONS.items():
        questions[flag] = Noul(instructions=instructions, criteria=NoulCriteria(true=yes, false=no))
    for field in FIELD_NAMES:
        spans = [c.span for c in cands.for_field(field)]
        if spans:
            criteria: dict[str, str | None] = {s: None for s in spans}
            criteria[NONE] = "None of these is the requested value."
            questions[f"pick_{field}"] = Choice(instructions=FIELD_QUESTIONS[field], criteria=criteria)
    return questions


def build_order_check(tax: Taxonomy) -> dict[str, Any]:
    return {
        "category": Choice(
            instructions=CATEGORY_INSTRUCTIONS, criteria=category_criteria(tax, reverse=True)
        )
    }


def _input_tokens(response: Any) -> int:
    usage = getattr(response, "usage", None)
    if usage is None:
        return 0
    if isinstance(usage, dict):
        return int(usage.get("input_tokens", 0) or 0)
    return int(getattr(usage, "input_tokens", 0) or 0)


def _priority(answer: Any) -> tuple[str, float]:
    probs = {int(k): float(v) for k, v in (getattr(answer, "probabilities", None) or {}).items()}
    level = max(probs, key=probs.get) if probs else int(round(float(answer.score)))
    level = min(max(level, 0), 3)
    return f"P{4 - level}", float(getattr(answer, "confidence", 0.0) or 0.0)


def _picks(response: Any) -> dict[str, FieldPick]:
    picks: dict[str, FieldPick] = {}
    for field in FIELD_NAMES:
        qid = f"pick_{field}"
        if qid not in response.choices:
            picks[field] = FieldPick(None, 0.0, "none")
            continue
        a = response.choices[qid]
        value = None if a.choice == NONE else str(a.choice)
        picks[field] = FieldPick(value, float(a.confidence), "jev_pick")
    return picks


class JevClassifier:
    def __init__(self, runnable: Any, taxonomy: Taxonomy, *, model_id: str, t_jev: float,
                 min_top_prob: float, price_in_per_m: float, max_state_chars: int) -> None:
        self._runnable, self._tax, self._model_id = runnable, taxonomy, model_id
        self._t_jev, self._min_top = t_jev, min_top_prob
        self._price, self._max_chars = price_in_per_m, max_state_chars

    async def classify(self, nt: NormalizedTicket, cands: Candidates) -> ClassifierOutput:
        state = build_state(nt, self._max_chars)
        main, order = await asyncio.gather(
            self._runnable.ainvoke({"state": state, "questions": build_questions(self._tax, cands)}),
            self._runnable.ainvoke({"state": state, "questions": build_order_check(self._tax)}),
        )
        cat = main.choices["category"]
        probs = {str(k): float(v) for k, v in cat.probabilities.items()}
        valid = cat.choice in self._tax.categories
        confidence = float(cat.confidence)
        order_agrees = order.choices["category"].choice == cat.choice
        uncertain = (
            not valid
            or max(probs.values(), default=0.0) < self._min_top
            or confidence < self._t_jev
            or not order_agrees
        )
        priority, priority_conf = _priority(main.scores["priority"])
        classification = ClassificationResult(
            category=cat.choice if valid else "other",
            category_confidence=confidence,
            category_probs=probs,
            priority=priority,
            priority_confidence=priority_conf,
            flags={f: float(main.nouls[f].noul) for f in FLAG_NAMES},
            source="jev",
            uncertain=uncertain,
            model=str(getattr(main, "model", None) or self._model_id),
        )
        tokens = _input_tokens(main) + _input_tokens(order)
        return ClassifierOutput(
            classification=classification,
            picks=_picks(main),
            path="jev",
            reasons=("low_confidence",) if uncertain else (),
            cost_usd=tokens * self._price / 1e6,
        )
