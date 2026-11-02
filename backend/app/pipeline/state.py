import operator
from typing import Annotated, TypedDict

from app.pipeline.contracts import (
    Candidates,
    ClassifierOutput,
    Decision,
    DraftResult,
    ExtractedField,
    LookupResult,
    NormalizedTicket,
    Ticket,
)


class PipelineState(TypedDict, total=False):
    ticket: Ticket
    nt: NormalizedTicket
    cands: Candidates
    classifier: ClassifierOutput
    extracted: dict[str, ExtractedField]
    lookup: LookupResult
    decision: Decision
    draft: DraftResult
    draft_error: str
    cost_usd: Annotated[float, operator.add]
    started_at: float
    finished_at: float
