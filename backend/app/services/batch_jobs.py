"""Run the existing graph; checkpoint completed tickets using independent sessions."""
import asyncio
import logging
from dataclasses import replace
from datetime import UTC, datetime
from time import perf_counter

from app.db.models import RunRow
from app.db.repository import SqlTransactionRepo, save_outcomes
from app.services.intake_recovery import fail_intake_placeholders, reconcile_intake_run
from app.pipeline.contracts import DraftResult, TicketOutcome
from app.pipeline.execution import TicketExecution, ticket_execution
from app.pipeline.graph import outcome_from_state, summarize

logger = logging.getLogger(__name__)
TICKET_TIMEOUT_S = 180


async def process_batch(app, run_id, tickets, mode):
    sf = app.state.session_factory
    graph = app.state.pipeline_builder(app.state.settings, mode, SqlTransactionRepo(sf))
    limiter = asyncio.Semaphore(max(1, min(app.state.settings.pipeline_concurrency, 20)))
    outcomes = []

    async def process(ticket):
        async with limiter:
            trace, state = [], None
            start = perf_counter()
            execution = TicketExecution(asyncio.timeout(TICKET_TIMEOUT_S))
            token = ticket_execution.set(execution)
            try:
                async with execution.timeout:
                    async for kind, event in graph.astream({"ticket": ticket}, stream_mode=["updates", "values"]):
                        if kind == "values":
                            state = event
                        else:
                            for node in event:
                                trace.append({"kind": "stage", "node": node, "status": "completed",
                                              "elapsed_ms": round((perf_counter() - start) * 1000)})
                outcome = outcome_from_state(state)
            except Exception as exc:
                logger.warning("Ticket %s failed: %s", ticket.external_id, type(exc).__name__)
                state = execution.draft_state or state or {}
                outcome = TicketOutcome(ticket=ticket, status="failed",
                                        error=f"{type(exc).__name__}: processing could not complete. Check server logs and retry.",
                                        classifier=state.get("classifier"), extracted=state.get("extracted", {}),
                                        lookup=state.get("lookup"), decision=state.get("decision"),
                                        draft=state.get("draft"), cost_usd=round(state.get("cost_usd", 0.0), 6),
                                        latency_ms=round((perf_counter() - start) * 1000))
            finally:
                ticket_execution.reset(token)
            draft = outcome.draft or DraftResult()
            outcome = replace(outcome, draft=replace(draft, trace=tuple(trace) + draft.trace))
            with sf() as session:
                save_outcomes(session, run_id, [outcome])
                run = session.get(RunRow, run_id)
                checkpoint = summarize([*outcomes, outcome])
                run.counts = checkpoint.to_dict() | {"expected_total": len(tickets)}
                run.total_cost_usd = checkpoint.total_cost_usd
                run.degraded = checkpoint.degraded
                session.commit()
            # Only durable results can contribute to progress, costs and summary counts.
            outcomes.append(outcome)

    completed = await asyncio.gather(*(process(ticket) for ticket in tickets), return_exceptions=True)
    persistence_failed = any(isinstance(item, BaseException) for item in completed)
    summary = summarize(outcomes)
    with sf() as session:
        run = session.get(RunRow, run_id)
        run.status = "failed" if persistence_failed else "completed_with_errors" if summary.failed_ids else "completed"
        run.counts = summary.to_dict() | {"expected_total": len(tickets)}
        if persistence_failed:
            run.counts = run.counts | {"error": "Some results could not be saved. Durable results were retained; retry this batch."}
        run.total_cost_usd = summary.total_cost_usd
        run.degraded = summary.degraded
        run.finished_at = datetime.now(UTC)
        if persistence_failed and fail_intake_placeholders(
            session, run_id, "Some results could not be saved. Durable results were retained; retry this batch."
        ):
            reconcile_intake_run(session, run)
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
            if fail_intake_placeholders(session, run_id, "Batch interrupted. Completed results were retained."):
                reconcile_intake_run(session, run)
            session.commit()
