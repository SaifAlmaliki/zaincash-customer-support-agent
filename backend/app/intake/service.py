"""Customer intake application service. Model calls happen outside the database transaction."""
from __future__ import annotations

from uuid import UUID

from starlette.concurrency import run_in_threadpool

from app.intake.contracts import Credentials, OperationClaim, SessionView
from app.intake.errors import InvalidEvidence, ModelUnavailable


class IntakeService:
    def __init__(self, repo, turns, graph, store) -> None:
        self.repo = repo
        self.turns = turns
        self.graph = graph
        self.store = store

    def create(self, language: str):
        return self.repo.create(language)

    def get(self, credentials: Credentials) -> SessionView:
        return self.repo.get(credentials)

    async def message(self, credentials: Credentials, command: dict) -> SessionView:
        return await self._perform(credentials, "message", command)

    async def review(self, credentials: Credentials, command: dict) -> SessionView:
        return await self._perform(credentials, "review", command)

    async def retry(self, credentials: Credentials, request_id: UUID, expected_revision: int) -> SessionView:
        claimed = await run_in_threadpool(self.turns.retry, credentials, request_id, expected_revision)
        if isinstance(claimed, SessionView):
            return claimed
        return await self._execute(claimed)

    async def _perform(self, credentials: Credentials, kind: str, command: dict) -> SessionView:
        claimed = await run_in_threadpool(
            self.turns.claim, credentials, kind, command["request_id"], command["expected_revision"], command
        )
        if isinstance(claimed, SessionView):
            return claimed
        return await self._execute(claimed)

    async def _execute(self, claim: OperationClaim) -> SessionView:
        try:
            if claim.kind == "review":
                language = claim.payload.get("language") or claim.context.state.language
                result = await self.graph.review(
                    claim.context, allow_partial=bool(claim.payload.get("allow_partial")), language=language
                )
            else:
                result = await self.graph.advance(claim.context)
        except ModelUnavailable as exc:
            return await run_in_threadpool(self.turns.fail, claim, "model_unavailable", list(exc.trace))
        except InvalidEvidence:
            return await run_in_threadpool(self.turns.fail, claim, "invalid_evidence", [])
        return await run_in_threadpool(self.turns.finish, claim, result)
