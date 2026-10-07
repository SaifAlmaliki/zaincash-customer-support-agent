"""`support` CLI: init-db, seed-db, run-batch. The same pipeline code is used by the API (Plan 4) and eval (Plan 2)."""
from __future__ import annotations

import asyncio
import json
from enum import Enum
from pathlib import Path

import typer

from app.config import Settings, get_settings
from app.db.repository import (
    SqlTransactionRepo, create_run, finish_run, load_incidents, load_transactions, save_outcomes,
    upsert_tickets,
)
from app.db.session import init_db, make_engine, make_sessionmaker
from app.ingest import load_jsonl, load_tickets
from app.pipeline import factory
from app.pipeline.contracts import Ticket
from app.pipeline.graph import run_batch
from app.pipeline.lookup import InMemoryTransactionRepo, txn_from_dict
from app.pipeline.prompts import PROMPT_VERSION
from app.pipeline.serialize import outcome_to_dict

app = typer.Typer(no_args_is_help=True, add_completion=False, help="ZainCash support pipeline")


class Mode(str, Enum):
    jev = "jev"
    gemini = "gemini"
    cascade = "cascade"


def _sessionmaker(settings: Settings):
    engine = make_engine(settings.database_url)
    init_db(engine)
    return make_sessionmaker(engine)


@app.command("init-db")
def init_db_cmd() -> None:
    """Create the database schema (idempotent)."""
    _sessionmaker(get_settings())
    typer.echo("database ready")


@app.command("seed-db")
def seed_db_cmd(
    transactions: Path = typer.Option(..., exists=True, dir_okay=False, help="transactions JSONL"),
    incidents: Path | None = typer.Option(None, exists=True, dir_okay=False, help="incidents JSONL"),
) -> None:
    """Load mock transactions (and optional service incidents) into Postgres."""
    sf = _sessionmaker(get_settings())
    with sf() as s:
        n = load_transactions(s, [txn_from_dict(r) for r in load_jsonl(transactions)])
        m = load_incidents(s, load_jsonl(incidents)) if incidents else 0
        s.commit()
    typer.echo(f"loaded {n} transactions and {m} incidents")


def _run_in_memory(settings: Settings, mode: str, tickets: list[Ticket],
                   transactions: Path | None):
    records = [txn_from_dict(r) for r in load_jsonl(transactions)] if transactions else []
    graph = factory.build_pipeline(settings, mode, InMemoryTransactionRepo(records))
    return asyncio.run(run_batch(graph, tickets, concurrency=settings.pipeline_concurrency))


def _run_with_db(settings: Settings, mode: str, tickets: list[Ticket]):
    sf = _sessionmaker(settings)
    graph = factory.build_pipeline(settings, mode, SqlTransactionRepo(sf))  # fail fast before writing
    with sf() as s:
        tickets = upsert_tickets(s, tickets, source="dataset")
        run_id = create_run(s, mode=mode, prompt_version=PROMPT_VERSION,
                            model_ids=factory.model_ids(settings, mode))
        s.commit()
    outcomes, summary = asyncio.run(
        run_batch(graph, tickets, concurrency=settings.pipeline_concurrency)
    )
    with sf() as s:
        save_outcomes(s, run_id, outcomes)
        finish_run(s, run_id, summary)
        s.commit()
    return outcomes, summary


@app.command("run-batch")
def run_batch_cmd(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, help=".jsonl, .json or .csv"),
    mode: Mode = typer.Option(Mode.cascade, "--mode"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    out: Path | None = typer.Option(None, "--out", help="write per-ticket results as JSON"),
    no_db: bool = typer.Option(False, "--no-db", help="run without Postgres"),
    transactions: Path | None = typer.Option(None, "--transactions", exists=True, dir_okay=False,
                                             help="transactions JSONL for --no-db runs"),
) -> None:
    """Run the pipeline over a batch of tickets and print the run summary."""
    settings = get_settings()
    tickets = load_tickets(path)[: limit or None]
    try:
        if no_db:
            outcomes, summary = _run_in_memory(settings, mode.value, tickets, transactions)
        else:
            outcomes, summary = _run_with_db(settings, mode.value, tickets)
    except factory.ConfigError as exc:
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps([outcome_to_dict(o) for o in outcomes], ensure_ascii=False,
                                  indent=2, default=str), encoding="utf-8")
