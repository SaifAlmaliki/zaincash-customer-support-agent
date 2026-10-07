"""Typed contracts shared by every pipeline stage. Keep this module dependency-free."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.taxonomy import FIELD_NAMES

FLAG_NAMES = (
    "fraud_suspected",
    "money_lost",
    "multi_issue",
    "urgent_or_angry",
    "mentions_specific_transaction",
    "asks_for_human",
)
__all__ = ["FIELD_NAMES", "FLAG_NAMES"]


@dataclass(frozen=True)
class Ticket:
    external_id: str
    text: str
    received_at: datetime
    channel: str = "app"
    customer_phone: str | None = None
    id: int | None = None


@dataclass(frozen=True)
class NormalizedTicket:
    ticket: Ticket
    match_text: str  # ASCII digits; same length as ticket.text, so spans index both
    normalized_text: str  # folded Arabic letters, diacritics removed (for models only)
    is_arabizi: bool
    has_latin_mix: bool


@dataclass(frozen=True)
class Candidate:
    field: str  # one of FIELD_NAMES
    value: str  # canonical value, e.g. "ZC2410000123", "07701234567", "50 الف"
    span: str  # exact substring of match_text
    start: int
    end: int


@dataclass
class Candidates:
    txn_ref: list[Candidate] = field(default_factory=list)
    amount: list[Candidate] = field(default_factory=list)
    phone: list[Candidate] = field(default_factory=list)
    date: list[Candidate] = field(default_factory=list)

    def for_field(self, name: str) -> list[Candidate]:
        return getattr(self, name)


@dataclass(frozen=True)
class FieldPick:
    value: str | None  # jev: the chosen candidate span; gemini: the verified verbatim span
    confidence: float
    method: str  # "jev_pick" | "gemini" | "none"
    normalized: str | None = None  # gemini's normalized value (e.g. "50000" for "خمسين الف")


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    category_confidence: float
    category_probs: dict[str, float]
    priority: str
    priority_confidence: float
    flags: dict[str, float]
    source: str  # "jev" | "gemini"
    uncertain: bool
    model: str


@dataclass(frozen=True)
class ClassifierOutput:
    classification: ClassificationResult
    picks: dict[str, FieldPick]
    path: str  # "jev" | "gemini" | "gemini_fallback" | "disagreement"
    reasons: tuple[str, ...] = ()
    cost_usd: float = 0.0
    degraded: bool = False


@dataclass(frozen=True)
class ExtractedField:
    value: str | int | None  # txn_ref str, amount int, phone "07..", date ISO string
    span: str | None
    start: int | None
    end: int | None
    method: str
    confidence: float
    currency: str | None = None


@dataclass(frozen=True)
class TxnRecord:
    txn_ref: str
    sender_phone: str
    receiver_phone: str | None
    receiver_name: str | None
    amount_iqd: int
    type: str
    status: str
    created_at: datetime
    biller: str | None = None
    agent_id: str | None = None
    failure_reason: str | None = None


@dataclass(frozen=True)
class LookupResult:
    # matched | not_found | ambiguous | amount_mismatch | date_mismatch | not_applicable
    status: str
    txn: TxnRecord | None = None
    candidates_found: int = 0


@dataclass(frozen=True)
class Decision:
    team: str
    priority: str
    escalated: bool
    reasons: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class DraftResult:
    text: str | None = None
    citations: tuple[str, ...] = ()
    trace: tuple[dict, ...] = ()
    reasons: tuple[str, ...] = ()
    cost_usd: float = 0.0


@dataclass(frozen=True)
class TicketOutcome:
    ticket: Ticket
    status: str  # pending_review | escalated | failed
    classifier: ClassifierOutput | None = None
    extracted: dict[str, ExtractedField] = field(default_factory=dict)
    lookup: LookupResult | None = None
    decision: Decision | None = None
    draft: DraftResult | None = None
    latency_ms: int = 0
    cost_usd: float = 0.0
    error: str | None = None
