"""Run the existing graph; checkpoint completed tickets using independent sessions."""
import asyncio
import logging
from dataclasses import replace
from datetime import UTC, datetime
from time import perf_counter

from app.db.models import RunRow
from app.db.repository import SqlTransactionRepo, save_outcomes
from app.pipeline.contracts import DraftResult, TicketOutcome
from app.pipeline.graph import outcome_from_state, summarize

logger = logging.getLogger(__name__)


async def process_batch(app, run_id, tickets, mode):
    sf = app.state.session_factory
    graph = app.state.pipeline_builder(app.state.settings, mode, SqlTransactionRepo(sf))
    limiter = asyncio.Semaphore(max(1, min(app.state.settings.pipeline_concurrency, 20)))
    outcomes = []

    async def process(ticket):
        async with limiter:
            trace, state = [], None
            start = perf_counter()
            try:
                async with asyncio.timeout(180):
                    async for kind, event in graph.astream({"ticket": ticket}, stream_mode=["updates", "values"]):
                        if kind == "values":
                            state = event
                        else:
                            for node in event:
                                trace.append({"kind": "stage", "node": node, "status": "completed",
                                              "elapsed_ms": round((perf_counter() - start) * 1000)})
                outcome = outcome_from_state(state)
                draft = outcome.draft or DraftResult()
                outcome = replace(outcome, draft=replace(draft, trace=tuple(trace) + draft.trace))
            except Exception as exc:
                logger.warning("Ticket %s failed: %s", ticket.external_id, type(exc).__name__)
                outcome = TicketOutcome(ticket=ticket, status="failed",
                                        error=f"{type(exc).__name__}: processing could not complete. Check server logs and retry.",
                                        draft=DraftResult(trace=tuple(trace)),
                                        latency_ms=round((perf_counter() - start) * 1000))
            outcomes.append(outcome)
            with sf() as session:
                save_outcomes(session, run_id, [outcome])
                run = session.get(RunRow, run_id)
                run.counts = summarize(outcomes).to_dict() | {"expected_total": len(tickets)}
                session.commit()

    await asyncio.gather(*(process(ticket) for ticket in tickets))
    summary = summarize(outcomes)
    with sf() as session:
        run = session.get(RunRow, run_id)
        run.status = "completed_with_errors" if summary.failed_ids else "completed"
        run.counts = summary.to_dict() | {"expected_total": len(tickets)}
        run.total_cost_usd = summary.total_cost_usd
        run.degraded = summary.degraded
        run.finished_at = datetime.now(UTC)
        session.commit()


def run_job(app, run_id, tickets, mode):
    try:
        asyncio.run(process_batch(app, run_id, tickets, mode))
    except Exception as exc:
        logger.warning("Batch %s failed: %s", run_id, type(exc).__name__)
        with app.state.session_factory() as session:
            run = session.get(RunRow, run_id)
            run.status = "failed"
            run.finished_at = datetime.now(UTC)
            run.counts = run.counts | {"error": "Batch interrupted. Completed results were retained."}
            session.commit()
