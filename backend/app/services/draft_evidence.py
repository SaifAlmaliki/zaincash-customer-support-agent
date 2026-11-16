"""Validate historical trace fragments without consulting mutable knowledge tables."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from app.datetime import parse_dt

TRANSACTION_TOOLS = frozenset({"lookup_transaction", "search_transactions", "get_customer_recent_transactions"})


class _TraceModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="ignore", allow_inf_nan=False)


class CitationSource(_TraceModel):
    id: str = Field(min_length=1, max_length=128)
    document_id: int = Field(gt=0)
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1, max_length=1200)
    filename: str = Field(min_length=1, max_length=255)
    score: float = Field(ge=-1, le=1)
    page_start: int | None = Field(default=None, ge=1)
    page_end: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def ordered_pages(self):
        if (self.page_start is None) != (self.page_end is None):
            raise ValueError("Incomplete page range.")
        if self.page_start is not None and self.page_end < self.page_start:
            raise ValueError("Invalid page range.")
        return self


class InvestigatedTransaction(_TraceModel):
    """A row a drafting tool returned: a candidate for the reviewer, never a confirmed match."""

    # Every field is required: a row the trace bound cut short must be dropped, not shown as partial.
    txn_ref: str = Field(min_length=1, max_length=32)
    sender_phone: str = Field(max_length=32)
    receiver_phone: str | None = Field(max_length=32)
    receiver_name: str | None = Field(max_length=2000)
    amount_iqd: int = Field(ge=0)
    type: str = Field(max_length=64)
    status: str = Field(max_length=64)
    created_at: str = Field(max_length=40)
    biller: str | None = Field(max_length=2000)
    agent_id: str | None = Field(max_length=64)
    failure_reason: str | None = Field(max_length=2000)

    @field_validator("created_at")
    @classmethod
    def parseable(cls, value):
        parse_dt(value)
        return value


def _transactions(event):
    if event.get("kind") != "tool" or event.get("status") != "ok" or event.get("tool") not in TRANSACTION_TOOLS:
        return []
    # Prefer the full snapshot; older traces only have the display-bounded result.
    result = event["transactions"] if "transactions" in event else event.get("result")
    rows = result if isinstance(result, list) else [result]
    return [txn for item in rows if (txn := _validated(InvestigatedTransaction, item)) is not None]


class _Guardrail(_TraceModel):
    kind: Literal["guardrail"]
    findings: list[str] = Field(default_factory=list)
    credential_check_degraded: bool | None = None
    requests_credentials: float | None = Field(default=None, ge=0, le=1)


class _Draft(_TraceModel):
    kind: Literal["draft"]
    internal_note: str | None = None
    findings: list[str] = Field(default_factory=list)


def _validated(model, value):
    try:
        return model.model_validate(value)
    except ValidationError:
        return None


def draft_evidence(trace, citations):
    """Old/corrupt fields are unknown, never inferred as a successful guardrail.

    First valid snapshot wins; a later malformed or conflicting trace entry must
    not replace evidence actually retrieved. Only persisted cited IDs are exposed.
    """
    sources, findings, investigated = {}, [], {}
    degraded = credentials = internal_note = None
    for event in trace if isinstance(trace, list) else []:
        if not isinstance(event, dict):
            continue
        for txn in _transactions(event):
            investigated.setdefault(txn.txn_ref, txn)
        snapshots = event.get("retrieved_passages", [])
        if event.get("kind") == "draft":
            snapshots = event.get("citation_sources", [])
        for item in snapshots if isinstance(snapshots, list) else []:
            source = _validated(CitationSource, item)
            if source is not None:
                sources.setdefault(source.id, source.model_dump())
        guardrail = _validated(_Guardrail, event)
        if guardrail is not None:
            findings.extend(guardrail.findings)
            if guardrail.credential_check_degraded is not None:
                degraded = guardrail.credential_check_degraded
            if guardrail.requests_credentials is not None:
                credentials = guardrail.requests_credentials
        draft = _validated(_Draft, event)
        if draft is not None:
            findings.extend(draft.findings)
            if draft.internal_note is not None:
                internal_note = draft.internal_note
    cited = dict.fromkeys(c for c in citations if isinstance(c, str)) if isinstance(citations, list) else {}
    return {"citation_sources": [sources[c] for c in cited if c in sources],
            "guardrail_findings": list(dict.fromkeys(findings)),
            "credential_check_degraded": degraded, "requests_credentials": credentials,
            "internal_note": internal_note,
            "investigated_transactions": [
                txn.model_dump() for txn in sorted(investigated.values(), key=lambda t: parse_dt(t.created_at), reverse=True)]}
