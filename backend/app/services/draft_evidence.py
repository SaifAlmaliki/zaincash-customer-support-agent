"""Validate historical trace fragments without consulting mutable knowledge tables."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


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
    sources, findings = {}, []
    degraded = credentials = internal_note = None
    for event in trace if isinstance(trace, list) else []:
        if not isinstance(event, dict):
            continue
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
            "internal_note": internal_note}
