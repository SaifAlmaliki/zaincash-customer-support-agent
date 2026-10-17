"""Per-ticket drafting state and the public Task 5 handoff contracts."""
from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from app.kb.contracts import Passage
from app.pipeline.state import PipelineState

ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
Note = Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)]
Reference = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=32)]


class DraftAlreadySubmitted(RuntimeError):
    """Terminal guard rejection; no execution, count change or trace mutation."""


class DraftToolLimit(RuntimeError):
    """Execution budget exhausted; no execution, count change or trace mutation."""


class DraftToolInputError(ValueError):
    """Invalid shape or out-of-scope investigation argument; failed call is traced."""


class DraftSubmission(BaseModel):
    """Shape-only submission. Task 4/5 checks grounding, Arabic and the 120-word limit.

    Empty citations remain representable so failed drafts can be reviewed. The
    immutable tuple accepts JSON lists on input; model_dump(mode='json') emits lists.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    reply_ar: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=6000)]
    citations: tuple[ShortText, ...] = Field(max_length=10)
    used_txn_ref: Reference | None = None
    internal_note: Note = ""

    @field_validator("citations", mode="before")
    @classmethod
    def json_citations(cls, value):
        return tuple(value) if isinstance(value, list) else value


@dataclass
class DraftContext:
    """Construct once per ticket; tools own cost accounting and serialized mutation.

    Task 5 reads submission/retrieved/trace/reasons/notes/cost_usd after execution.
    Propagated search exceptions still carry their original cost metadata: do NOT
    add it again, even when an outer asyncio.timeout wraps cancellation.
    max_tool_calls may lower, but cannot raise, the hard six-call limit.
    """

    state: PipelineState
    max_tool_calls: int = field(default=6, kw_only=True)
    retrieved: dict[str, Passage] = field(default_factory=dict, init=False)
    trace: list[dict] = field(default_factory=list, init=False)
    cost_usd: float = field(default=0.0, init=False)
    tool_count: int = field(default=0, init=False)
    reasons: list[str] = field(default_factory=list, init=False)
    notes: list[str] = field(default_factory=list, init=False)
    submission: DraftSubmission | None = field(default=None, init=False)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
    investigated_refs: set[str] = field(default_factory=set, init=False, repr=False)

    def __post_init__(self) -> None:
        if type(self.max_tool_calls) is not int or not 1 <= self.max_tool_calls <= 6:
            raise ValueError("max_tool_calls must be an integer in 1–6")
        self.state = deepcopy(self.state)
        if decision := self.state.get("decision"):
            self.reasons.extend(dict.fromkeys(decision.reasons))
