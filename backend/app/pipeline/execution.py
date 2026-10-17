"""Ticket-local deadline and terminal handoff across LangGraph's child tasks."""
import asyncio
from contextvars import ContextVar
from dataclasses import dataclass

from app.pipeline.state import PipelineState

# Leave time for the graph's final state to reach the runner. The outer timeout
# still owns the ticket; the handoff also covers cancellation during this margin.
DRAFT_HANDOFF_RESERVE_S = 0.1


@dataclass
class TicketExecution:
    timeout: asyncio.Timeout
    draft_state: PipelineState | None = None

    def draft_budget(self, maximum: float) -> float:
        deadline = self.timeout.when()
        if deadline is None:
            return maximum
        return max(0.0, min(maximum, deadline - asyncio.get_running_loop().time() - DRAFT_HANDOFF_RESERVE_S))


# Each API ticket sets/reset its own cell; child tasks inherit the same cell.
# Exception attributes alone cannot cross a cancelled graph stream reliably.
ticket_execution: ContextVar[TicketExecution | None] = ContextVar("ticket_execution", default=None)
