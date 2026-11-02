from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from app.pipeline.contracts import FieldPick, NormalizedTicket


class FieldExtractor(Protocol):
    async def extract(
        self, nt: NormalizedTicket, fields: Sequence[str]
    ) -> tuple[dict[str, FieldPick], float]: ...
