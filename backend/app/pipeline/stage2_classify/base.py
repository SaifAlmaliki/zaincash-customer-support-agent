from __future__ import annotations

from typing import Protocol

from app.pipeline.contracts import Candidates, ClassifierOutput, NormalizedTicket


class Classifier(Protocol):
    async def classify(self, nt: NormalizedTicket, cands: Candidates) -> ClassifierOutput: ...
