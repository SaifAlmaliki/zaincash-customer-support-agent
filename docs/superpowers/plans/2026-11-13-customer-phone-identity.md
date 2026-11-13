# Customer Phone Identity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the customer's ZainCash phone number (`07XXXXXXXXX`) the customer identifier in the backend, the customer intake app, and the employee workspace.

**Architecture:** A new `customers` table keyed by the canonical phone. Every stored ticket and every intake session must reference a customer row. One phone helper in Python (`app/customers/phone.py`) and a matching TypeScript helper in each frontend convert any accepted input to the canonical form. The intake app gets a phone entry screen before the chat. The employee app shows the phone in the queue and ticket header, searches by phone, and gets a `/customers/:phone` page.

**Tech Stack:** FastAPI, SQLAlchemy 2, PostgreSQL 16 (psycopg 3), pytest; React 19, Vite, Vitest, Testing Library (users-frontend only), react-router-dom 7 (employee-frontend).

**Spec:** `docs/superpowers/specs/2026-11-13-customer-phone-identity-design.md`

## Global Constraints

- Canonical phone: 11 ASCII digits matching `^07[3-9][0-9]{8}$`. Store only this form.
- Accepted input before canonicalization: Arabic-Indic (U+0660–U+0669) and Persian (U+06F0–U+06F9) digits, ASCII digits, whitespace (including NBSP), `+`, `-`, `(`, `)`, `.`. Any other character rejects the input. A leading `00964` or `964` becomes `0`. A bare 10-digit `7[3-9]XXXXXXXX` gets a leading `0`.
- Invalid phone message, exact text everywhere it is user-visible in English: `Enter a valid ZainCash phone number, for example 07701234567.`
- Intake API error code for an invalid phone: `invalid_phone`, HTTP 422.
- Test phone constants: `07701234567` (default customer), `07809876543`, `07501112233`, `07712223344`, `07723334455`, `07734445566`, `07745556677`, `07756667788`.
- No in-place data migration. A database with the old schema stops the API at startup with a reset instruction.
- Do not stage or commit `.env.example`. It is deleted in the working tree by the user; always `git add` explicit paths.
- Backend tests run from Windows with: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest <paths> -q"` (Postgres must be up: `docker compose up -d db`).
- users-frontend tests: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run <paths>"`.
- employee-frontend tests: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run <paths>"`.
- Employee locale files: `employee-frontend/src/locales/en.json` and `ar.json` must have identical key sets (`Copy = typeof en`). Same rule for the intake `IntakeCopy` type.

## Spec refinements (decided while planning)

- `load_tickets` (file ingest) still returns `customer_phone=None` for rows without a phone, so `support run-batch --no-db` keeps working on evaluation files. Every **stored** ticket still needs a phone: `upsert_tickets` rejects a missing phone, and `run-batch` without `--no-db` refuses such a file before writing. A present but invalid phone is rejected at load time.
- The Python helper builds on the same rules as `normalize_phone()` but is stricter: it rejects stray letters and non-ASCII digits instead of deleting them (`07701234567x` must not become a valid phone).
- The customer's phone is seeded into the intake state as a known `customer_phone` fact at session creation. That is how it reaches the review summary and the Arabic ticket text.

## Review Focus

1. Junk characters around a valid number (`07701234567x`, full-width or Devanagari digits) must be rejected, not silently stripped — Task 1 and Task 7 phone tests.
2. A browser that saved an intake session before the database reset gets `not_owned` on reload. It must fall back to the phone screen, not stay stuck on an error — Task 7 controller test.
3. The same number in two formats (`+964 780 987 6543`, `07809876543`) must map to one customer and must not make a rerun look like changed content (409) — Task 2 repository test and Task 3 API test.
4. An employee opening `/customers/<not a phone>` must get a localized "not a valid phone number" state, not a raw API error — Task 10 test.
5. Changing the number in the intake app must keep the selected language and not leak the previous session — Task 8 IntakePage test.

---

### Task 1: Canonical phone helper (backend)

**Files:**
- Create: `backend/app/customers/__init__.py`
- Create: `backend/app/customers/phone.py`
- Test: `backend/tests/test_customer_phone.py`

**Interfaces:**
- Produces:
  - `class InvalidPhone(ValueError)`
  - `INVALID_PHONE_MESSAGE: str` = `"Enter a valid ZainCash phone number, for example 07701234567."`
  - `normalize_customer_phone(raw: object) -> str` (raises `InvalidPhone`)
  - `customer_phone_or_none(raw: object) -> str | None` (never raises)

- [ ] **Step 1: Write the failing test**

`backend/tests/test_customer_phone.py`:

```python
import pytest

from app.customers.phone import InvalidPhone, customer_phone_or_none, normalize_customer_phone


@pytest.mark.parametrize("raw", [
    "07701234567",
    "0770 123 4567",
    "0770-123-4567",
    "(0770) 123-4567",
    "0770.123.4567",
    "+9647701234567",
    "+964 770 123 4567",
    "9647701234567",
    "00964 770 123 4567",
    "7701234567",
    "٠٧٧٠١٢٣٤٥٦٧",
    "+۹۶۴\u00a0۷۷۰-۱۲۳ ۴۵۶۷",
    "  07701234567  ",
])
def test_accepted_formats_become_the_canonical_phone(raw):
    assert normalize_customer_phone(raw) == "07701234567"


@pytest.mark.parametrize("raw", [
    "", "   ", "0770123456", "077012345678", "07201234567", "96407701234567",
    "07701234567x", "0770123456\uff11", "0770123456\u0967", "+1 202 555 0100",
    "0770/123/4567", None, 7701234567,
], ids=["empty", "blank", "short", "long", "bad-prefix", "964-then-0", "letter", "fullwidth",
        "devanagari", "foreign", "slash", "none", "int"])
def test_invalid_input_is_rejected(raw):
    with pytest.raises(InvalidPhone, match="valid ZainCash phone number"):
        normalize_customer_phone(raw)


def test_optional_lookup_never_raises():
    assert customer_phone_or_none("+964 780 987 6543") == "07809876543"
    assert customer_phone_or_none("needle") is None
    assert customer_phone_or_none(None) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_customer_phone.py -q"`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.customers'`

- [ ] **Step 3: Write minimal implementation**

`backend/app/customers/__init__.py`: empty file.

`backend/app/customers/phone.py`:

```python
"""A customer is identified by the canonical ZainCash phone number 07XXXXXXXXX."""
from __future__ import annotations

import re

from app.text import to_ascii_digits

INVALID_PHONE_MESSAGE = "Enter a valid ZainCash phone number, for example 07701234567."
_ALLOWED = re.compile(r"[0-9\s+\-().]*")
_CANONICAL = re.compile(r"07[3-9][0-9]{8}")
_WITHOUT_ZERO = re.compile(r"7[3-9][0-9]{8}")


class InvalidPhone(ValueError):
    """The value is not a ZainCash customer phone number."""


def normalize_customer_phone(raw: object) -> str:
    # Unsupported characters reject the value; deleting them could turn
    # another value into a valid customer number.
    if not isinstance(raw, str):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    text = to_ascii_digits(raw).strip()
    if not _ALLOWED.fullmatch(text):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    digits = re.sub(r"[^0-9]", "", text)
    if digits.startswith("00964"):
        digits = digits[2:]
    if digits.startswith("964"):
        digits = "0" + digits[3:]
    elif _WITHOUT_ZERO.fullmatch(digits):
        digits = "0" + digits
    if not _CANONICAL.fullmatch(digits):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    return digits


def customer_phone_or_none(raw: object) -> str | None:
    try:
        return normalize_customer_phone(raw)
    except InvalidPhone:
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_customer_phone.py -q"`
Expected: PASS (all cases)

- [ ] **Step 5: Commit**

```bash
git add backend/app/customers/__init__.py backend/app/customers/phone.py backend/tests/test_customer_phone.py
git commit -m "feat(customers): add the canonical customer phone helper"
```

---

### Task 2: Customers table, required ticket phone, startup check

**Files:**
- Modify: `backend/app/db/models.py` (add `CustomerRow`; change `TicketRow.customer_phone`)
- Create: `backend/app/customers/repository.py`
- Modify: `backend/app/db/repository.py:19-31` (`upsert_tickets`)
- Modify: `backend/app/db/workspace_schema.py`
- Test: `backend/tests/test_repository.py`, `backend/tests/test_workspace_schema.py` (new)
- Fix existing tests that insert tickets directly: `backend/tests/test_draft_tools.py`, `backend/tests/test_kb_service.py:178-180`, `backend/tests/intake/test_repository.py:94-103`

**Interfaces:**
- Consumes: `normalize_customer_phone`, `InvalidPhone` (Task 1)
- Produces:
  - `app.db.models.CustomerRow` (`phone: str` PK `String(11)`, `created_at`)
  - `TicketRow.customer_phone: Mapped[str]` — `String(11)`, NOT NULL, FK `customers.phone`, indexed
  - `app.customers.repository.ensure_customers(session, phones: Iterable[str]) -> None` (phones must already be canonical)
  - `upsert_tickets(...)` returns tickets whose `customer_phone` is canonical; raises `InvalidPhone("Ticket <external_id>: <message>")` for a missing or invalid phone
  - `app.db.workspace_schema.LegacySchemaError(RuntimeError)`, `LEGACY_SCHEMA_MESSAGE: str`, `assert_customer_schema(connection) -> None`

- [ ] **Step 1: Write the failing tests**

Add to `backend/tests/test_repository.py` (add imports `from app.customers.phone import InvalidPhone` and `CustomerRow` to the `app.db.models` import):

```python
PHONE = "07701234567"


def test_upsert_tickets_stores_one_canonical_customer(sf):
    with sf() as s:
        stored = upsert_tickets(s, [
            make_ticket("x", external_id="A", customer_phone="+964 770 123 4567"),
            make_ticket("y", external_id="B", customer_phone="٠٧٧٠١٢٣٤٥٦٧"),
        ], source="dataset")
        s.commit()
        assert [t.customer_phone for t in stored] == [PHONE, PHONE]
        assert list(s.scalars(select(CustomerRow.phone))) == [PHONE]
        assert set(s.scalars(select(TicketRow.customer_phone))) == {PHONE}


@pytest.mark.parametrize("phone", [None, "", "12345", "07701234567x"])
def test_upsert_tickets_rejects_a_missing_or_invalid_phone(sf, phone):
    with sf() as s:
        with pytest.raises(InvalidPhone, match="Ticket A"):
            upsert_tickets(s, [make_ticket("x", external_id="A", customer_phone=phone)], source="dataset")
```

In the same file, pass `customer_phone=PHONE` to every existing `make_ticket(...)` handed to `upsert_tickets` (lines 44, 46, 54).

Create `backend/tests/test_workspace_schema.py`:

```python
import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, reset_db
from app.db.workspace_schema import LegacySchemaError, upgrade_workspace_schema

pytestmark = pytest.mark.integration


@pytest.fixture
def engine():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    yield engine
    reset_db(engine)
    engine.dispose()


def test_fresh_schema_passes_the_customer_check(engine):
    upgrade_workspace_schema(engine)


def test_nullable_ticket_phone_stops_startup_with_a_reset_instruction(engine):
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE tickets ALTER COLUMN customer_phone DROP NOT NULL"))
    with pytest.raises(LegacySchemaError, match="docker compose down -v"):
        upgrade_workspace_schema(engine)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_repository.py tests/test_workspace_schema.py -q"`
Expected: FAIL with `ImportError: cannot import name 'CustomerRow'` / `'LegacySchemaError'`

- [ ] **Step 3: Implement the model, helper, upsert and check**

`backend/app/db/models.py` — add above `TicketRow` and change the ticket column:

```python
class CustomerRow(Base):
    __tablename__ = "customers"
    phone: Mapped[str] = mapped_column(String(11), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

```python
    customer_phone: Mapped[str] = mapped_column(String(11), ForeignKey("customers.phone"), index=True)
```

`backend/app/customers/repository.py`:

```python
"""Customer rows. A customer exists once any ticket or conversation uses the phone."""
from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import CustomerRow


def ensure_customers(session: Session, phones: Iterable[str]) -> None:
    """Insert missing customers. Each phone must already be canonical."""
    rows = [{"phone": phone} for phone in sorted(set(phones))]
    if rows:
        session.execute(insert(CustomerRow).values(rows).on_conflict_do_nothing(index_elements=["phone"]))
```

`backend/app/db/repository.py` — add imports and replace the start of `upsert_tickets`:

```python
from app.customers.phone import InvalidPhone, normalize_customer_phone
from app.customers.repository import ensure_customers
```

```python
def _ticket_phone(ticket: Ticket) -> str:
    try:
        return normalize_customer_phone(ticket.customer_phone)
    except InvalidPhone as exc:
        raise InvalidPhone(f"Ticket {ticket.external_id}: {exc}") from None


def upsert_tickets(session: Session, tickets: Sequence[Ticket], *, source: str,
                   batch_id: str | None = None) -> list[Ticket]:
    if not tickets:
        return []
    tickets = [replace(t, customer_phone=_ticket_phone(t)) for t in tickets]
    ensure_customers(session, [t.customer_phone for t in tickets])
    rows = [{"external_id": t.external_id, "channel": t.channel, "customer_phone": t.customer_phone,
             "text": t.text, "received_at": t.received_at, "source": source, "batch_id": batch_id}
            for t in tickets]
```

(The rest of the function is unchanged.)

`backend/app/db/workspace_schema.py` — full file:

```python
from sqlalchemy import text

LEGACY_SCHEMA_MESSAGE = (
    "This database was created before customers were identified by phone number. "
    "Reset the demo database: run `docker compose down -v`, then `docker compose up --build -d`, "
    "then load docker/db/seed_demo.sql."
)


class LegacySchemaError(RuntimeError):
    """The database predates the customer phone identity and must be recreated."""


def _nullable(connection, table: str, column: str) -> str | None:
    return connection.scalar(text(
        "SELECT is_nullable FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = :table AND column_name = :column"
    ), {"table": table, "column": column})


def assert_customer_schema(connection) -> None:
    if _nullable(connection, "tickets", "customer_phone") == "YES":
        raise LegacySchemaError(LEGACY_SCHEMA_MESSAGE)


def upgrade_workspace_schema(engine):
    """Apply additive schema upgrades that create_all cannot perform on existing tables."""
    with engine.begin() as connection:
        assert_customer_schema(connection)
        length = connection.scalar(text(
            "SELECT character_maximum_length FROM information_schema.columns "
            "WHERE table_schema = current_schema() AND table_name = 'runs' AND column_name = 'status'"
        ))
        if length is not None and length < 32:
            connection.execute(text("ALTER TABLE runs ALTER COLUMN status TYPE VARCHAR(32)"))
        # Intake sessions created before admin model settings have no pinned model.
        connection.execute(text(
            "ALTER TABLE IF EXISTS intake_sessions ADD COLUMN IF NOT EXISTS model_choice JSONB"
        ))
```

- [ ] **Step 4: Fix tests that insert `TicketRow` directly**

A ticket row now needs an existing customer. Insert customers in a separate flush or transaction before the tickets (no ORM relationship exists to order the inserts).

`backend/tests/test_draft_tools.py`:
- Add `NEAR = "07701234568"` under `OTHER`, and import `CustomerRow` from `app.db.models`.
- In the `sf` fixture, replace `reset_db(engine)` / `yield make_sessionmaker(engine)` with:

```python
        reset_db(engine)
        factory = make_sessionmaker(engine)
        with factory.begin() as s:
            s.add_all([CustomerRow(phone=phone) for phone in (PHONE, OTHER, NEAR)])
        yield factory
```

- In `test_stored_phone_formats_match_without_cross_customer_leaks` (around line 136), stored ticket phones are now always canonical. Replace the `TicketRow` list with:

```python
        s.add_all([TicketRow(external_id=external_id, text="prior contact", customer_phone=phone,
                            received_at=NOW - timedelta(days=1), source="test")
                   for external_id, phone in [("own-history", PHONE), ("other-history", NEAR)]])
```

  and change `assert result[0]["customer_phone"] == stored_phone` to `assert result[0]["customer_phone"] == PHONE`. Leave the transaction rows and the final `sender_phone == stored_phone` assertion as they are (transactions keep their stored formats).
- In `test_unsupported_phone_characters_cannot_match_customer` (around line 200), replace the `TicketRow` list with `[("valid", PHONE)]` only (an invalid ticket phone can no longer be stored). The assertion `== ["valid"]` stays.

`backend/tests/test_kb_service.py` (around line 178): before creating `ticket`, add `session.add(CustomerRow(phone="07701234567")); session.flush()`, and pass `customer_phone="07701234567"` to `TicketRow(...)`. Import `CustomerRow` from `app.db.models`.

`backend/tests/intake/test_repository.py` `test_repeated_init_db_keeps_existing_tickets`: add `session.add(CustomerRow(phone="07701234567")); session.flush()` before the ticket and pass `customer_phone="07701234567"` to `TicketRow(...)`. Import `CustomerRow` from `app.db.models`.

- [ ] **Step 5: Run the touched tests**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_repository.py tests/test_workspace_schema.py tests/test_draft_tools.py tests/test_kb_service.py tests/intake/test_repository.py -q"`
Expected: PASS. (`tests/test_workspace_api.py`, `test_rag_api.py`, `test_embedding_switch.py` and the intake submission/handoff tests fail until Tasks 3–4 because their tickets have no phone yet; that is expected. Do not "fix" them in this task.)

- [ ] **Step 6: Commit**

```bash
git add backend/app/db/models.py backend/app/customers/repository.py backend/app/db/repository.py backend/app/db/workspace_schema.py backend/tests/test_repository.py backend/tests/test_workspace_schema.py backend/tests/test_draft_tools.py backend/tests/test_kb_service.py backend/tests/intake/test_repository.py
git commit -m "feat(customers): store every ticket under a customer phone"
```

---

### Task 3: Require the phone on batch runs, file ingest and the CLI

**Files:**
- Modify: `backend/app/api/schemas.py:13-40` (`TicketInput`)
- Modify: `backend/app/ingest.py:33-51`
- Modify: `backend/app/cli.py:109-135` (`run_batch_cmd`)
- Modify: `backend/tests/fixtures/sample_tickets.jsonl`, `data/demo/rag_tickets.jsonl`
- Test: `backend/tests/test_workspace_api.py`, `backend/tests/test_ingest.py`, `backend/tests/test_cli_run_batch.py` (new)
- Fix: `backend/tests/test_rag_api.py:215-217`, `backend/tests/models_config/test_embedding_switch.py:105,132`

**Interfaces:**
- Consumes: `normalize_customer_phone`, `InvalidPhone` (Task 1); `upsert_tickets` canonicalizes (Task 2)
- Produces: `TicketInput.customer_phone: str` (required, canonical after validation); `load_tickets` returns canonical phones or `None`

- [ ] **Step 1: Write the failing tests**

`backend/tests/test_workspace_api.py`:
- Add `PHONE = "07701234567"` after `pytestmark`.
- Change `start_run` so every ticket gets a default phone:

```python
def start_run(client, tickets=None):
    tickets = tickets or [
        {"external_id": "case-1", "text": "شكد عمولة التحويل؟",
         "received_at": datetime.now(UTC).isoformat()},
    ]
    response = client.post("/api/runs", json={"tickets": [{"customer_phone": PHONE, **t} for t in tickets]})
    assert response.status_code == 202, response.text
    return response.json()["id"]
```

- Add `"customer_phone": PHONE` to each inline ticket dict posted directly to `/api/runs` at lines ~180-182, ~223-225, ~261-263 and ~269-271 (otherwise they now fail validation before reaching what they test).
- Add:

```python
def test_runs_require_and_normalize_the_customer_phone(client):
    missing = client.post("/api/runs", json={"tickets": [{"external_id": "no-phone", "text": "مرحبا"}]})
    assert missing.status_code == 422
    invalid = client.post("/api/runs", json={"tickets": [
        {"external_id": "bad", "text": "مرحبا", "customer_phone": "12345"},
    ]})
    assert invalid.status_code == 422
    assert "valid ZainCash phone number" in invalid.text
    start_run(client, [{"external_id": "formatted", "text": "شكد العمولة؟", "customer_phone": "+964 780 987 6543"}])
    assert client.get("/api/results").json()["items"][0]["ticket"]["customer_phone"] == "07809876543"
    # The same number written differently is the same ticket content, not a conflict.
    again = client.post("/api/runs", json={"tickets": [
        {"external_id": "formatted", "text": "شكد العمولة؟", "customer_phone": "0780 987 6543"},
    ]})
    assert again.status_code == 202, again.text
```

`backend/tests/test_ingest.py` — replace `test_jsonl_fixture_loads` and add two tests:

```python
def test_jsonl_fixture_loads():
    tickets = load_tickets(FIXTURES / "sample_tickets.jsonl", now=NOW)
    assert [t.external_id for t in tickets] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
    assert tickets[0].customer_phone == "07809876543"
    assert tickets[4].customer_phone == "07734445566" and tickets[4].channel == "whatsapp"


def test_phones_are_canonical_and_missing_phones_stay_empty(tmp_path):
    p = tmp_path / "phones.jsonl"
    p.write_text('{"external_id": "A", "text": "x", "customer_phone": "+964 780 987 6543"}\n'
                 '{"external_id": "B", "text": "y"}\n', encoding="utf-8")
    a, b = load_tickets(p, now=NOW)
    assert a.customer_phone == "07809876543"
    assert b.customer_phone is None


def test_invalid_phone_names_the_row(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text('{"external_id": "A", "text": "x", "customer_phone": "12345"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="Row 1 \\(A\\).*valid ZainCash phone number"):
        load_tickets(p, now=NOW)
```

`backend/tests/test_cli_run_batch.py`:

```python
from typer.testing import CliRunner

from app.cli import app


def test_stored_run_refuses_tickets_without_a_customer_phone(tmp_path):
    p = tmp_path / "tickets.jsonl"
    p.write_text('{"external_id": "A", "text": "hi"}\n', encoding="utf-8")
    result = CliRunner().invoke(app, ["run-batch", str(p)])
    assert result.exit_code == 2
    assert "customer phone" in result.output and "A" in result.output


def test_invalid_phone_is_an_input_error_not_a_traceback(tmp_path):
    p = tmp_path / "tickets.jsonl"
    p.write_text('{"external_id": "A", "text": "hi", "customer_phone": "123"}\n', encoding="utf-8")
    result = CliRunner().invoke(app, ["run-batch", str(p), "--no-db"])
    assert result.exit_code == 2
    assert "valid ZainCash phone number" in result.output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_workspace_api.py tests/test_ingest.py tests/test_cli_run_batch.py -q"`
Expected: FAIL (`missing.status_code` is 202, fixture phone mismatch, CLI exit code 1 or 0).

- [ ] **Step 3: Implement**

`backend/app/api/schemas.py` — import `from app.customers.phone import InvalidPhone, normalize_customer_phone`, change the field and add a validator to `TicketInput`:

```python
    customer_phone: str = Field(max_length=32)
```

```python
    @field_validator("customer_phone")
    @classmethod
    def canonical_phone(cls, value):
        try:
            return normalize_customer_phone(value)
        except InvalidPhone as exc:
            raise ValueError(str(exc)) from None
```

`backend/app/ingest.py` — import `from app.customers.phone import InvalidPhone, normalize_customer_phone`; update the module docstring's first line to add "Rows may omit customer_phone; storing such a ticket is rejected later." and replace the phone line in `load_tickets`:

```python
        raw_phone = str(row.get("customer_phone") or "").strip()
        try:
            phone = normalize_customer_phone(raw_phone) if raw_phone else None
        except InvalidPhone as exc:
            raise ValueError(f"Row {i} ({external_id}): {exc}") from None
```

`backend/app/cli.py` — in `run_batch_cmd`, replace `tickets = load_tickets(path)[: limit or None]` with:

```python
    try:
        tickets = load_tickets(path)[: limit or None]
    except ValueError as exc:
        typer.echo(f"Input error: {exc}", err=True)
        raise typer.Exit(code=2) from None
    missing = [t.external_id for t in tickets if not t.customer_phone]
    if missing and not no_db:
        typer.echo("Input error: every stored ticket needs a customer phone. Missing for: "
                   f"{', '.join(missing[:10])}. Add customer_phone or use --no-db.", err=True)
        raise typer.Exit(code=2)
```

- [ ] **Step 4: Give every fixture ticket a phone**

- `backend/tests/fixtures/sample_tickets.jsonl` line 5 (S-005): add `"customer_phone":"07734445566",` after `"channel":"whatsapp",`.
- `data/demo/rag_tickets.jsonl`: RAG-DEMO-GENERAL gets `"customer_phone":"07745556677"`, RAG-DEMO-UNSUPPORTED gets `"customer_phone":"07756667788"` (insert after the `"channel"` value).
- `backend/tests/test_rag_api.py` ~line 216: add `"customer_phone": "07701234567"` to the ticket dict.
- `backend/tests/models_config/test_embedding_switch.py` lines 105 and 132: add `"customer_phone": "07701234567"` to each ticket dict.

- [ ] **Step 5: Run tests to verify they pass**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_workspace_api.py tests/test_ingest.py tests/test_cli_run_batch.py tests/test_rag_api.py tests/models_config/test_embedding_switch.py -q"`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/schemas.py backend/app/ingest.py backend/app/cli.py backend/tests/fixtures/sample_tickets.jsonl data/demo/rag_tickets.jsonl backend/tests/test_workspace_api.py backend/tests/test_ingest.py backend/tests/test_cli_run_batch.py backend/tests/test_rag_api.py backend/tests/models_config/test_embedding_switch.py
git commit -m "feat(runs): require a valid customer phone on every stored ticket"
```

---

### Task 4: Intake sessions belong to a customer phone

**Files:**
- Modify: `backend/app/intake/errors.py`, `backend/app/main.py:112-118`
- Modify: `backend/app/api/intake_schemas.py:14-15`, `backend/app/api/intake.py:58-61`
- Modify: `backend/app/intake/service.py:20-21`, `backend/app/intake/repository.py` (`initial_state`, `session_view`, `IntakeRepository.create`)
- Modify: `backend/app/intake/db_models.py:15-29`, `backend/app/intake/contracts.py:159-171`
- Modify: `backend/app/intake/policy.py`, `backend/app/intake/evidence.py`, `backend/app/intake/prompts/intake_v1.md`
- Modify: `backend/app/intake/submission.py:87-96`
- Modify: `backend/app/db/workspace_schema.py` (`assert_customer_schema`)
- Test: `backend/tests/intake/test_repository.py`, `test_api.py`, `test_handoff.py`, `test_evidence_regressions.py`, `backend/tests/test_workspace_schema.py`
- Fix callers: `backend/tests/intake/{conftest.py,test_api.py,test_handoff.py,test_graph.py,test_recovery_regressions.py,test_repository.py,test_attachments.py,test_turns.py}`, `backend/tests/models_config/test_store.py:91,105`

**Interfaces:**
- Consumes: `normalize_customer_phone`, `InvalidPhone` (Task 1); `ensure_customers` (Task 2)
- Produces:
  - `POST /api/intake/sessions` body `{language, customer_phone}`; 422 `{"detail": {"code": "invalid_phone", "message": ...}}`
  - `SessionView.customer_phone: str` in every intake response
  - `IntakeRepository.create(language: str, customer_phone: str)`, `IntakeService.create(language, customer_phone)`
  - `app.intake.errors.InvalidCustomerPhone(IntakeError)` with `code = "invalid_phone"`
  - `initial_state(language: str, customer_phone: str) -> IntakeState` with a known `customer_phone` fact

- [ ] **Step 1: Update every session-creation call in tests**

Use the edit tool with `replaceAll` per file:
- `.create("ar")` → `.create("ar", "07701234567")` and `.create("en")` → `.create("en", "07701234567")` in `tests/intake/test_repository.py`, `test_attachments.py`, `test_turns.py`, `test_graph.py`, `test_recovery_regressions.py`.
- `json={"language": "en"}` → `json={"language": "en", "customer_phone": "07701234567"}` and `json={"language": "ar"}` → `json={"language": "ar", "customer_phone": "07701234567"}` in `tests/intake/conftest.py`, `test_api.py`, `test_handoff.py`, `test_graph.py`, `test_recovery_regressions.py`.
- `tests/models_config/test_store.py` lines 91 and 105: before each `IntakeSessionRow(...)`, add `session.add(CustomerRow(phone="07701234567")); session.flush()` and pass `customer_phone="07701234567"`. Import `CustomerRow` from `app.db.models`.

- [ ] **Step 2: Write the failing tests**

`backend/tests/intake/test_repository.py` (imports: `from app.db.models import CustomerRow, TicketRow`, `from app.intake.contracts import Fact, IntakeState, Message`):

```python
def test_session_belongs_to_the_signed_in_customer(repo, intake_db):
    credentials, view = repo.create("ar", "+964 770 123 4567")
    assert view.customer_phone == "07701234567"
    with intake_db[1]() as session:
        row = session.get(IntakeSessionRow, credentials.session_id)
        assert row.customer_phone == "07701234567"
        assert session.get(CustomerRow, "07701234567") is not None
        known = IntakeState.model_validate(row.state).facts["customer_phone"]
        assert (known.status, known.value, known.normalized) == ("known", "07701234567", "07701234567")


def test_invalid_phone_cannot_start_a_session(repo):
    from app.intake.errors import InvalidCustomerPhone
    with pytest.raises(InvalidCustomerPhone):
        repo.create("ar", "0770")
```

`backend/tests/intake/test_api.py` (its first line deliberately omits the phone; write this test after Step 1's replace-all, and do not run the replace again):

```python
def test_session_requires_a_valid_customer_phone(intake_client):
    assert intake_client.post("/api/intake/sessions", json={"language": "en"}).status_code == 422
    invalid = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "12345"})
    assert invalid.status_code == 422
    assert invalid.json()["detail"]["code"] == "invalid_phone"
    created = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "٠٧٧٠١٢٣٤٥٦٧"})
    assert created.status_code == 201
    assert created.json()["session"]["customer_phone"] == "07701234567"
    sid = created.json()["credentials"]["session_id"]
    headers = {"Authorization": f"Bearer {created.json()['credentials']['token']}"}
    assert intake_client.get(f"/api/intake/sessions/{sid}", headers=headers).json()["customer_phone"] == "07701234567"
```

`backend/tests/intake/test_handoff.py` — at the end of `test_review_to_employee_handoff` add:

```python
    assert detail["ticket"]["customer_phone"] == "07701234567"
    assert detail["intake"]["facts"]["customer_phone"]["normalized"] == "07701234567"
    assert "07701234567" in detail["ticket"]["text"]
```

`backend/tests/intake/test_evidence_regressions.py`:
- Delete the `("customer_phone", "07701234567", None, "I sent to recipient 07701234567"),` parameter line.
- Replace `test_two_phone_numbers_do_not_lose_their_roles` with:

```python
def test_model_cannot_set_or_change_the_signed_in_phone():
    source = message("My number is 07701234567; recipient number is 07801234567")
    signed_in = Fact(key="customer_phone", status="known", value="07709999999", normalized="07709999999")
    result = merge_analysis(context([source], [signed_in]), proposal(
        fact("customer_phone", "07701234567", source),
        fact("recipient_phone", "07801234567", source),
    ))
    assert result.facts["customer_phone"] == signed_in
    assert result.facts["recipient_phone"].normalized == "07801234567"
```

`backend/tests/test_workspace_schema.py` — add:

```python
def test_intake_sessions_without_a_customer_phone_stop_startup(engine):
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE intake_sessions DROP COLUMN customer_phone"))
    with pytest.raises(LegacySchemaError):
        upgrade_workspace_schema(engine)
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/intake tests/test_workspace_schema.py tests/models_config/test_store.py -q"`
Expected: FAIL (`create()` takes 2 positional arguments, `customer_phone` unknown field, etc.)

- [ ] **Step 4: Implement the backend changes**

`backend/app/intake/errors.py` — append:

```python
class InvalidCustomerPhone(IntakeError):
    code = "invalid_phone"
    public_message = "Enter a valid ZainCash phone number, for example 07701234567."
```

`backend/app/main.py` — in the `intake_failed` status map add `"invalid_phone": 422,`.

`backend/app/api/intake_schemas.py`:

```python
class CreateSessionInput(IntakeBody):
    language: Literal["ar", "en"]
    customer_phone: str = Field(min_length=1, max_length=32)
```

`backend/app/api/intake.py` `create_session`: `credentials, view = request.app.state.intake.create(body.language, body.customer_phone)`.

`backend/app/intake/service.py`:

```python
    def create(self, language: str, customer_phone: str):
        return self.repo.create(language, customer_phone)
```

`backend/app/intake/db_models.py` — import `ForeignKey` is already imported; add to `IntakeSessionRow` after `token_hash`:

```python
    customer_phone: Mapped[str] = mapped_column(String(11), ForeignKey("customers.phone"), index=True)
```

`backend/app/intake/contracts.py` — add to `SessionView` after `language`:

```python
    customer_phone: str
```

`backend/app/intake/repository.py`:
- Imports: `from app.customers.phone import InvalidPhone, normalize_customer_phone`, `from app.customers.repository import ensure_customers`, add `Fact` to the contracts import, add `InvalidCustomerPhone` to the errors import.
- Replace `initial_state`:

```python
def initial_state(language: str, customer_phone: str) -> IntakeState:
    # The signed-in phone is the customer's identity, so it is known before the first message.
    return IntakeState(
        language=language,
        category="other",
        facts={"customer_phone": Fact(
            key="customer_phone", status="known", value=customer_phone, normalized=customer_phone,
        )},
        additional_issues=[],
        additional_needed=[],
        questions=[],
        readiness=Readiness(
            quality="collecting",
            missing=["issue"],
            conflicts=[],
            reason="Waiting for the customer's report.",
            next_key="issue",
        ),
    )
```

- In `session_view`, add `customer_phone=row.customer_phone,` after `language=row.language,`.
- Replace the start of `IntakeRepository.create`:

```python
    def create(self, language: str, customer_phone: str) -> tuple[Credentials, SessionView]:
        if language not in {"ar", "en"}:
            raise ValueError("language must be ar or en")
        try:
            phone = normalize_customer_phone(customer_phone)
        except InvalidPhone:
            raise InvalidCustomerPhone() from None
        token, token_hash = new_access_token()
        session_id = uuid.uuid4()
        now = datetime.now(UTC)
        with self._sf() as session:
            ensure_customers(session, [phone])
            session.add(IntakeSessionRow(
                id=session_id,
                token_hash=token_hash,
                customer_phone=phone,
                revision=0,
                phase="collecting",
                turn_status="idle",
                language=language,
                state=initial_state(language, phone).model_dump(mode="json"),
```

(The remaining keyword arguments and the method body stay as they are.)

`backend/app/intake/submission.py` `_create` — replace the `phone_fact` lines and the `Ticket(...)` call:

```python
        ticket = Ticket(
            external_id=f"INTAKE-{row.id.hex}", text=snapshot.ticket_text_ar, received_at=now,
            channel="app", customer_phone=row.customer_phone,
        )
```

`backend/app/intake/policy.py`:
- `PRECISE = {"amount", "recipient_phone", "date", "txn_ref"}`
- Delete the `"customer_phone": ...` entries from both `_ASK["en"]` and `_ASK["ar"]`.

`backend/app/intake/evidence.py`:
- `_PRECISE = {"txn_ref", "amount", "recipient_phone", "exact_error", "date"}`
- Delete `_OWN_PHONE`, `_OTHER_PHONE` and `_own_phone_quote` (they are only used for the customer phone).
- In `_normalize_precise`, replace the phone branch with:

```python
    if fact.key == "recipient_phone":
        parsed = normalize_phone(value)
        if parsed is None:
            return fact.model_copy(update={"normalized": None})
        if fact.normalized and _compact(fact.normalized) != parsed:
            raise InvalidEvidence("Normalized phone does not match the reported text.")
        return fact.model_copy(update={"normalized": parsed})
```

- In `merge_analysis`, skip model updates for the signed-in phone (first line inside each loop):

```python
    for update in analysis.updates:
        if update.key == "customer_phone":
            continue  # set from the phone the customer signed in with
        checked = checked_update(update, facts.get(update.key))
        facts[checked.key] = _apply(facts.get(checked.key), checked, messages)
    issues = {item.key: item for item in context.state.additional_issues}
    for issue in analysis.additional_issues:
        if issue.key == "customer_phone":
            continue
        checked = checked_update(issue, issues.get(issue.key))
        issues[issue.key] = _apply(issues.get(issue.key), checked, messages)
```

`backend/app/intake/prompts/intake_v1.md`:
- Line 13 becomes: `- The customer's own phone (customer_phone) is already known from sign-in. Never send a customer_phone update. Map a recipient number to recipient_phone.`
- Line 20: remove `customer_phone, ` from the fact-key list.

`backend/app/db/workspace_schema.py` — extend `assert_customer_schema`:

```python
def _table_exists(connection, table: str) -> bool:
    return connection.scalar(text(
        "SELECT 1 FROM information_schema.tables WHERE table_schema = current_schema() AND table_name = :table"
    ), {"table": table}) is not None


def assert_customer_schema(connection) -> None:
    if _nullable(connection, "tickets", "customer_phone") == "YES":
        raise LegacySchemaError(LEGACY_SCHEMA_MESSAGE)
    if _table_exists(connection, "intake_sessions") and _nullable(connection, "intake_sessions", "customer_phone") is None:
        raise LegacySchemaError(LEGACY_SCHEMA_MESSAGE)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/intake tests/test_workspace_schema.py tests/models_config -q"`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add backend/app/intake backend/app/api/intake.py backend/app/api/intake_schemas.py backend/app/main.py backend/app/db/workspace_schema.py backend/tests/intake backend/tests/test_workspace_schema.py backend/tests/models_config/test_store.py
git commit -m "feat(intake): start each conversation from the customer's phone number"
```

---

### Task 5: Employee API — search by phone and customer profile

**Files:**
- Modify: `backend/app/api/results.py:32-35`
- Create: `backend/app/api/customers.py`
- Modify: `backend/app/main.py:14,120` (register router)
- Test: `backend/tests/test_workspace_api.py`

**Interfaces:**
- Consumes: `customer_phone_or_none`, `normalize_customer_phone`, `InvalidPhone` (Task 1); `CustomerRow` (Task 2); `latest_results_query`, `result_view` (existing, `app/services/workspace_queries.py`)
- Produces:
  - `GET /api/results?q=<phone in any accepted format>` also matches `tickets.customer_phone`
  - `GET /api/customers/{phone}` → `{"phone": str, "created_at": datetime, "ticket_count": int, "results": [result_view items, newest ticket first]}`; 422 `{"detail": "<INVALID_PHONE_MESSAGE>"}`; 404 `{"detail": "No customer with this phone number."}`

- [ ] **Step 1: Write the failing tests**

Append to `backend/tests/test_workspace_api.py`:

```python
def test_result_search_matches_the_customer_phone_in_any_format(client):
    start_run(client, [
        {"external_id": "mine", "text": "تحويل معلق", "customer_phone": "07809876543"},
        {"external_id": "theirs", "text": "سؤال", "customer_phone": "07501112233"},
    ])
    for query in ["07809876543", "+964 780 987 6543", "٠٧٨٠٩٨٧٦٥٤٣"]:
        page = client.get("/api/results", params={"q": query}).json()
        assert [item["ticket"]["external_id"] for item in page["items"]] == ["mine"], query


def test_customer_profile_lists_the_latest_result_of_each_ticket(client):
    start_run(client, [
        {"external_id": "first", "text": "مرحبا", "customer_phone": "07809876543",
         "received_at": "2026-10-07T09:00:00+03:00"},
        {"external_id": "second", "text": "سؤال", "customer_phone": "07809876543",
         "received_at": "2026-10-08T09:00:00+03:00"},
        {"external_id": "other", "text": "سؤال", "customer_phone": "07501112233"},
    ])
    start_run(client, [{"external_id": "first", "text": "مرحبا", "customer_phone": "07809876543"}])
    profile = client.get("/api/customers/+964 780 987 6543")
    assert profile.status_code == 200, profile.text
    body = profile.json()
    assert body["phone"] == "07809876543"
    assert body["ticket_count"] == 2
    assert [item["ticket"]["external_id"] for item in body["results"]] == ["second", "first"]
    latest_first = client.get("/api/results", params={"q": "first"}).json()["items"][0]
    assert body["results"][1]["id"] == latest_first["id"]


def test_customer_profile_rejects_invalid_and_unknown_phones(client):
    invalid = client.get("/api/customers/12345")
    assert invalid.status_code == 422
    assert "valid ZainCash phone number" in invalid.json()["detail"]
    assert client.get("/api/customers/07701234567").status_code == 404
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_workspace_api.py -q -k 'phone or customer'"`
Expected: FAIL (search returns `[]` for phone formats; `/api/customers` is 404 for all)

- [ ] **Step 3: Implement**

`backend/app/api/results.py` — import `from app.customers.phone import customer_phone_or_none` and replace the `if q:` block:

```python
    if q:
        match = TicketRow.text.contains(q, autoescape=True) | TicketRow.external_id.contains(q, autoescape=True)
        phone = customer_phone_or_none(q)
        if phone:
            match = match | (TicketRow.customer_phone == phone)
        query = query.where(TicketResultRow.ticket_id.in_(select(TicketRow.id).where(match)))
```

`backend/app/api/customers.py`:

```python
from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.api.dependencies import SessionDep
from app.customers.phone import InvalidPhone, normalize_customer_phone
from app.db.models import CustomerRow, TicketResultRow, TicketRow
from app.services.workspace_queries import latest_results_query, result_view

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("/{phone}")
def get_customer(phone: str, session: SessionDep):
    try:
        canonical = normalize_customer_phone(phone)
    except InvalidPhone as exc:
        raise HTTPException(422, str(exc)) from None
    customer = session.get(CustomerRow, canonical)
    if customer is None:
        raise HTTPException(404, "No customer with this phone number.")
    rows = session.scalars(
        latest_results_query()
        .join(TicketRow, TicketRow.id == TicketResultRow.ticket_id)
        .where(TicketRow.customer_phone == canonical)
        .order_by(TicketRow.received_at.desc(), TicketResultRow.id.desc())
    )
    ticket_count = session.scalar(
        select(func.count()).select_from(TicketRow).where(TicketRow.customer_phone == canonical)
    ) or 0
    return {
        "phone": canonical,
        "created_at": customer.created_at,
        "ticket_count": ticket_count,
        "results": [result_view(session, row) for row in rows],
    }
```

`backend/app/main.py`: `from app.api import admin, customers, intake, knowledge, results, runs, workspace` and add `customers.router` to the `include_router` tuple.

- [ ] **Step 4: Run tests to verify they pass**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_workspace_api.py -q"`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/results.py backend/app/api/customers.py backend/app/main.py backend/tests/test_workspace_api.py
git commit -m "feat(api): search results by phone and add the customer profile endpoint"
```

---

### Task 6: Demo seed, cleanup script and reset documentation

**Files:**
- Modify: `docker/db/seed_demo.sql`, `docker/db/cleanup.sql`
- Modify: `README.md` (new "Reset the demo database" section; Try-the-demo note)
- Test: `backend/tests/test_seed_demo.py` (new)

**Interfaces:**
- Consumes: `CustomerRow`, `TicketRow` (Task 2); `REPO_ROOT` from `app.config`

- [ ] **Step 1: Write the failing test**

`backend/tests/test_seed_demo.py`:

```python
import re

import pytest
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import REPO_ROOT, Settings
from app.db.models import CustomerRow, TicketRow
from app.db.session import make_engine, make_sessionmaker, reset_db

pytestmark = pytest.mark.integration
SEED = REPO_ROOT / "docker" / "db" / "seed_demo.sql"


def test_demo_seed_gives_every_ticket_a_customer():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    try:
        reset_db(engine)
        raw = engine.raw_connection()
        try:
            raw.driver_connection.autocommit = True  # the script has its own BEGIN/COMMIT
            with raw.driver_connection.cursor() as cursor:
                cursor.execute(SEED.read_text(encoding="utf-8"))
        finally:
            raw.driver_connection.autocommit = False  # do not return an autocommit connection to the pool
            raw.close()
        with make_sessionmaker(engine)() as session:
            phones = list(session.scalars(select(TicketRow.customer_phone)))
            customers = set(session.scalars(select(CustomerRow.phone)))
        assert len(phones) == 7
        assert set(phones) <= customers
        assert all(re.fullmatch(r"07[3-9][0-9]{8}", phone) for phone in phones)
    finally:
        reset_db(engine)
        engine.dispose()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_seed_demo.py -q"`
Expected: FAIL with a foreign-key or not-null violation from the `INSERT INTO tickets`.

- [ ] **Step 3: Update the SQL scripts**

`docker/db/seed_demo.sql`:
- In the emptiness guard add `OR EXISTS (SELECT 1 FROM customers)` after the `runs` check.
- Before `INSERT INTO tickets`, add:

```sql
INSERT INTO customers (phone) VALUES
    ('07809876543'), ('07501112233'), ('07712223344'), ('07723334455'),
    ('07734445566'), ('07745556677'), ('07756667788');
```

- Replace the three `NULL` ticket phones: ticket 5 (`S-005`) → `'07734445566'`, ticket 6 (`RAG-DEMO-GENERAL`) → `'07745556677'`, ticket 7 (`RAG-DEMO-UNSUPPORTED`) → `'07756667788'`.

`docker/db/cleanup.sql`: add `'customers',` to the table list directly after `'tickets',`.

- [ ] **Step 4: Run test to verify it passes**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest tests/test_seed_demo.py -q"`
Expected: PASS

- [ ] **Step 5: Document the reset**

`README.md` — add after the "Quick start" table paragraph ("After you change `.env`…"):

```markdown
### Reset the demo database

Customers are identified by their phone number (`07XXXXXXXXX`), and every ticket and customer conversation belongs to one. A database created before this change cannot be upgraded in place: the API stops at startup and asks for a reset. To reset:

```bash
docker compose down -v
docker compose up --build -d
```

Then load the demo data: in pgAdmin (database `support`, `localhost:5433`), run `docker/db/cleanup.sql` and then `docker/db/seed_demo.sql`.
```

(Use a four-backtick fence for the outer block if your editor needs it; the README itself uses a normal ```` ```bash ```` fence inside the section.)

In "Try the demo", after step 2 add: `Every ticket in a batch file needs a customer_phone. The customer intake app asks for the phone number before the chat starts.`

- [ ] **Step 6: Commit**

```bash
git add docker/db/seed_demo.sql docker/db/cleanup.sql README.md backend/tests/test_seed_demo.py
git commit -m "docs: give demo tickets customer phones and document the database reset"
```

---

### Task 7: Intake app data layer — phone helper, contracts, API, controller

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/phone.ts`, `phone.test.ts`
- Modify: `users-frontend/apps/web/src/features/intake/types.ts:68-81`
- Modify: `users-frontend/apps/web/src/features/intake/contracts.ts:146-161`
- Modify: `users-frontend/apps/web/src/features/intake/api.ts:28-29,88-94`
- Modify: `users-frontend/apps/web/src/features/intake/controller.ts`
- Modify: `users-frontend/apps/web/src/features/intake/test/fixtures.ts`
- Test: `controller.test.ts`, `contracts.test.ts`, `api.test.ts`; fix callers in `IntakePage.test.tsx`, `useIntakeUploads.test.tsx`

**Interfaces:**
- Consumes: backend `POST /api/intake/sessions {language, customer_phone}`, `SessionView.customer_phone`, error code `invalid_phone` (Task 4)
- Produces:
  - `normalizeCustomerPhone(raw: string): string | null`
  - `SessionView.customer_phone: string`
  - `IntakeApi.create(language: Language, customerPhone: string, signal?: AbortSignal)`
  - `ControllerState.needsPhone: boolean`, `ControllerState.phoneError: "invalid" | "failed" | null`
  - `IntakeController.initialize(language: Language, phone?: string)`, `IntakeController.changeNumber(): Promise<void>`
  - `CUSTOMER_PHONE = "07701234567"` exported from `test/fixtures.ts`

- [ ] **Step 1: Write the failing phone test**

`users-frontend/apps/web/src/features/intake/phone.test.ts`:

```ts
import { expect, it } from "vitest"
import { normalizeCustomerPhone } from "./phone"

it.each([
  "07701234567", "0770 123 4567", "0770-123-4567", "(0770) 123-4567", "+9647701234567",
  "+964 770 123 4567", "9647701234567", "00964 770 123 4567", "7701234567",
  "٠٧٧٠١٢٣٤٥٦٧", "+۹۶۴\u00a0۷۷۰-۱۲۳ ۴۵۶۷", "  07701234567  ",
])("accepts %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBe("07701234567")
})

it.each([
  "", "0770123456", "077012345678", "07201234567", "96407701234567", "07701234567x",
  "0770123456\uff11", "0770123456\u0967", "0770/123/4567",
])("rejects %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBeNull()
})
```

- [ ] **Step 2: Run it to verify it fails, then implement**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run src/features/intake/phone.test.ts"`
Expected: FAIL (cannot resolve `./phone`)

`users-frontend/apps/web/src/features/intake/phone.ts`:

```ts
// Same rules as backend/app/customers/phone.py. The server stays authoritative.
const ALLOWED = /^[0-9\s+\-().]*$/
const CANONICAL = /^07[3-9][0-9]{8}$/
const WITHOUT_ZERO = /^7[3-9][0-9]{8}$/

function asciiDigits(value: string) {
  // U+0660–U+0669 and U+06F0–U+06F9 end in the digit value.
  return value.replace(/[\u0660-\u0669\u06f0-\u06f9]/g, (digit) => String(digit.charCodeAt(0) & 0xf))
}

export function normalizeCustomerPhone(raw: string): string | null {
  const text = asciiDigits(raw).trim()
  if (!ALLOWED.test(text)) return null
  let digits = text.replace(/[^0-9]/g, "")
  if (digits.startsWith("00964")) digits = digits.slice(2)
  if (digits.startsWith("964")) digits = `0${digits.slice(3)}`
  else if (WITHOUT_ZERO.test(digits)) digits = `0${digits}`
  return CANONICAL.test(digits) ? digits : null
}
```

Run the same command. Expected: PASS.

- [ ] **Step 3: Update fixtures and every caller**

`test/fixtures.ts`:
- Add `export const CUSTOMER_PHONE = "07701234567"`.
- In `emptySession`, add `customer_phone: CUSTOMER_PHONE,` after `language: "en",`.

Use the edit tool with `replaceAll`, and add `CUSTOMER_PHONE` to each file's `./test/fixtures` import:
- `controller.test.ts`, `useIntakeUploads.test.tsx`: `initialize("en")` → `initialize("en", CUSTOMER_PHONE)`, `initialize("ar")` → `initialize("ar", CUSTOMER_PHONE)`.
- `IntakePage.test.tsx`: `initialize(language)` → `initialize(language, CUSTOMER_PHONE)`, `initialize("en")` → `initialize("en", CUSTOMER_PHONE)`.
- `api.test.ts`: `api.create("en")` → `api.create("en", CUSTOMER_PHONE)`.

- [ ] **Step 4: Write the failing contract and controller tests**

`contracts.test.ts` — add to the `malformed` array:

```ts
  ["customer phone", { ...populated, customer_phone: 4 }],
  ["missing customer phone", { ...populated, customer_phone: "" }],
```

`controller.test.ts` — add inside `describe("intake controller", ...)`:

```ts
  it("asks for the phone before creating a session", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar")
    expect(controller.getSnapshot().needsPhone).toBe(true)
    expect(api.create).not.toHaveBeenCalled()
    await controller.initialize("ar", CUSTOMER_PHONE)
    expect(api.create).toHaveBeenCalledWith("ar", CUSTOMER_PHONE, expect.any(AbortSignal))
    expect(controller.getSnapshot().needsPhone).toBe(false)
    expect(controller.getSnapshot().session?.customer_phone).toBe(CUSTOMER_PHONE)
  })

  it("keeps the phone screen open when the server rejects the number", async () => {
    const api = fakeApi()
    vi.mocked(api.create).mockRejectedValueOnce(new IntakeRequestError("Enter a valid ZainCash phone number, for example 07701234567.", 422, "invalid_phone"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar")
    await controller.initialize("ar", CUSTOMER_PHONE)
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, phoneError: "invalid", session: null })
  })

  it("starts a new report for the same customer", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.startNew("en")
    expect(vi.mocked(api.create).mock.calls[1]?.[1]).toBe(CUSTOMER_PHONE)
  })

  it("changing the number forgets the saved session and asks again", async () => {
    const api = fakeApi()
    const storage = memoryStorage()
    const controller = new IntakeController(api, storage)
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.changeNumber()
    expect(storage.load()).toBeNull()
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, session: null })
    expect(controller.access()).toBeNull()
  })

  it("returns to the phone screen when the saved session no longer exists", async () => {
    const storage = memoryStorage({ credentials: { session_id: "gone", token: "token" }, pending: null })
    const api = fakeApi()
    vi.mocked(api.get).mockRejectedValueOnce(new IntakeRequestError("Conversation not found.", 404, "not_owned"))
    const controller = new IntakeController(api, storage)
    await controller.initialize("ar")
    expect(controller.getSnapshot()).toMatchObject({ needsPhone: true, session: null, error: null })
    expect(storage.load()).toBeNull()
  })
```

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run src/features/intake/contracts.test.ts src/features/intake/controller.test.ts"`
Expected: FAIL (malformed phone accepted; `needsPhone` undefined; `changeNumber` is not a function)

- [ ] **Step 5: Implement types, contracts and API**

`types.ts` — add to `SessionView` after `language: Language`:

```ts
  customer_phone: string
```

`contracts.ts` `parseSession` — add to the condition after `!language(value.language) ||`:

```ts
      typeof value.customer_phone !== "string" || !value.customer_phone ||
```

`api.ts`:

```ts
  create(language: Language, customerPhone: string, signal?: AbortSignal): Promise<{ credentials: Credentials; session: SessionView }>
```

```ts
    async create(language, customerPhone, signal) {
      const response = await fetch(`${baseUrl}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, customer_phone: customerPhone }),
        signal,
      })
```

- [ ] **Step 6: Implement the controller changes**

`controller.ts`:

1. `ControllerState` and `emptyState()` get two fields:

```ts
  needsPhone: boolean
  phoneError: "invalid" | "failed" | null
```

```ts
    needsPhone: false,
    phoneError: null,
```

2. Add a field next to `language`: `private phone: string | null = null`

3. Replace `initialize`:

```ts
  async initialize(language: Language, phone?: string) {
    this.language = language
    if (phone) this.phone = phone
    if (this.credentials && this.snapshot.session) return
    if (!this.initPromise) {
      const generation = this.generation
      this.initPromise = this.boot(language, generation).finally(() => {
        if (generation === this.generation) this.initPromise = null
      })
    }
    return this.initPromise
  }
```

4. In `startNew`, make the first statement inside the enqueued function (after `if (generation !== this.generation) return`):

```ts
      this.phone = this.snapshot.session?.customer_phone ?? this.phone
```

5. Add after `startNew`:

```ts
  async changeNumber() {
    this.generation += 1
    const generation = this.generation
    this.stopPoll()
    this.abortCurrent()
    return this.enqueue(async () => {
      if (generation !== this.generation) return
      this.credentials = null
      this.pending = null
      this.phone = null
      this.uploadIds.clear()
      this.pendingUpload = null
      this.pendingRemoval = null
      this.initPromise = null
      let resumeFailure: string | null = null
      try {
        this.storage.clear()
      } catch {
        resumeFailure = RESUME_UNAVAILABLE
      }
      this.replace({
        ...emptyState(),
        needsPhone: true,
        resumeUnavailable: resumeFailure !== null,
        error: resumeFailure,
      })
    })
  }
```

6. Replace `boot`:

```ts
  private async boot(language: Language, generation: number) {
    try {
      await this.bootNow(language, generation)
    } catch (error) {
      if (generation !== this.generation) return
      if (error instanceof DOMException && error.name === "AbortError") return
      if (this.snapshot.needsPhone) {
        const invalid = error instanceof IntakeRequestError && error.code === "invalid_phone"
        if (invalid) this.phone = null
        this.replace({ ...this.snapshot, busy: false, phoneError: invalid ? "invalid" : "failed" })
        return
      }
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
    }
  }
```

7. Replace `bootNow`:

```ts
  private async bootNow(language: Language, generation: number) {
    let saved: ReturnType<SessionStorage["load"]>
    try {
      saved = this.storage.load()
    } catch {
      saved = null
    }
    if (saved?.credentials) {
      this.credentials = saved.credentials
      this.pending = saved.pending
      try {
        await this.reload(generation)
      } catch (error) {
        if (!(error instanceof IntakeRequestError && error.code === "not_owned")) throw error
        if (generation !== this.generation) return
        // The saved conversation is gone (for example after a database reset).
        this.credentials = null
        this.pending = null
        try { this.storage.clear() } catch { /* The phone screen still opens. */ }
        this.replace({ ...this.snapshot, session: null, busy: false, error: null, needsPhone: true, phoneError: null })
      }
      return
    }
    if (!this.phone) {
      this.replace({ ...this.snapshot, busy: false, needsPhone: true, phoneError: null })
      return
    }
    this.replace({ ...this.snapshot, busy: true, phoneError: null })
    const signal = this.nextSignal()
    const created = await this.api.create(language, this.phone, signal)
    if (generation !== this.generation) return
    this.credentials = created.credentials
    this.pending = null
    this.replace({
      ...this.snapshot,
      session: created.session,
      busy: false,
      error: null,
      pollingExhausted: false,
      needsPhone: false,
      phoneError: null,
    })
    this.persist()
    this.watch(created.session)
  }
```

- [ ] **Step 7: Run the data-layer tests**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run src/features/intake/phone.test.ts src/features/intake/contracts.test.ts src/features/intake/controller.test.ts src/features/intake/api.test.ts src/features/intake/useIntakeUploads.test.tsx"`
Expected: PASS. (`IntakePage.test.tsx` "starts with Iraqi Arabic…" fails until Task 8.)

- [ ] **Step 8: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/phone.ts users-frontend/apps/web/src/features/intake/phone.test.ts users-frontend/apps/web/src/features/intake/types.ts users-frontend/apps/web/src/features/intake/contracts.ts users-frontend/apps/web/src/features/intake/contracts.test.ts users-frontend/apps/web/src/features/intake/api.ts users-frontend/apps/web/src/features/intake/api.test.ts users-frontend/apps/web/src/features/intake/controller.ts users-frontend/apps/web/src/features/intake/controller.test.ts users-frontend/apps/web/src/features/intake/test/fixtures.ts users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/useIntakeUploads.test.tsx
git commit -m "feat(intake-app): create conversations from the customer's phone number"
```

---

### Task 8: Intake app UI — phone screen, profile chip, change number, receipt

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/PhoneGate.tsx`, `buttons.ts`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/ReceiptPanel.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/copy.ts`, `locales/en.json`, `locales/ar.json`, `intake.css`
- Test: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`

**Interfaces:**
- Consumes: `normalizeCustomerPhone` (Task 7); controller `needsPhone`, `phoneError`, `initialize(language, phone)`, `changeNumber()`; `SessionView.customer_phone`
- Produces: `PhoneGate({ copy, busy, serverError, onSubmit(phone) })`; `solidButton`, `quietButton` exports from `buttons.ts`; new `IntakeCopy` keys `phoneTitle`, `phoneHelp`, `phoneLabel`, `phoneContinue`, `phoneInvalid`, `profileLabel`, `changeNumber`, `confirmChange`, `confirmChangeBody`, `receiptFor`

- [ ] **Step 1: Write the failing tests**

`IntakePage.test.tsx` — add `within` to the `@testing-library/react` import, `IntakeRequestError` from `./api`, and `CUSTOMER_PHONE` from fixtures. Replace the test "starts with Iraqi Arabic before asynchronous initialization" with:

```tsx
it("asks for the phone number in Iraqi Arabic before the chat", async () => {
  const user = userEvent.setup()
  const api = fakeApi({ language: "ar" })
  const controller = new IntakeController(api, memoryStorage())
  render(<IntakePage controller={controller} />)
  const phone = await screen.findByRole("textbox", { name: "رقم هاتفك بزين كاش" })
  expect(document.documentElement).toHaveAttribute("lang", "ar")
  expect(document.documentElement).toHaveAttribute("dir", "rtl")
  await user.type(phone, "0770")
  await user.click(screen.getByRole("button", { name: "استمرار" }))
  expect(screen.getByRole("alert")).toHaveTextContent("اكتب رقم زين كاش صحيح، مثل 07701234567.")
  expect(api.create).not.toHaveBeenCalled()
  await user.clear(phone)
  await user.type(phone, "+964 770 123 4567")
  await user.click(screen.getByRole("button", { name: "استمرار" }))
  expect(api.create).toHaveBeenCalledWith("ar", CUSTOMER_PHONE, expect.any(AbortSignal))
  expect(await screen.findByLabelText("رسالتك")).toBeVisible()
})

it("shows the server's invalid-number answer on the phone screen", async () => {
  const user = userEvent.setup()
  const api = fakeApi({ language: "en" })
  vi.mocked(api.create).mockRejectedValueOnce(new IntakeRequestError("Enter a valid ZainCash phone number, for example 07701234567.", 422, "invalid_phone"))
  const controller = new IntakeController(api, memoryStorage())
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "English" }))
  await user.type(screen.getByRole("textbox", { name: "Your ZainCash phone number" }), "07701234567")
  await user.click(screen.getByRole("button", { name: "Continue" }))
  expect(await screen.findByRole("alert")).toHaveTextContent("Enter a valid ZainCash phone number")
  expect(screen.getByRole("textbox", { name: "Your ZainCash phone number" })).toBeVisible()
})

it("shows the signed-in phone and changes number after confirmation", async () => {
  const user = userEvent.setup()
  const { controller } = await collectingController("en", {
    messages: [{ id: "m1", role: "user", text: "old report", language: "en", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
  })
  render(<IntakePage controller={controller} />)
  expect(screen.getByRole("group", { name: "Signed in as" })).toHaveTextContent(CUSTOMER_PHONE)
  await user.click(screen.getByRole("button", { name: "Change number" }))
  await user.click(screen.getByRole("button", { name: "Use another number" }))
  expect(await screen.findByRole("textbox", { name: "Your ZainCash phone number" })).toBeVisible()
  expect(document.documentElement).toHaveAttribute("lang", "en")
  expect(screen.queryByText("old report")).not.toBeInTheDocument()
})
```

In the existing test "requires explicit submission after summary review", after `expect(await screen.findByText("INTAKE-demo")).toBeVisible()` add:

```tsx
  expect(within(screen.getByRole("region", { name: "Ticket received" })).getByText(CUSTOMER_PHONE)).toBeVisible()
```

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run src/features/intake/IntakePage.test.tsx"`
Expected: FAIL (no phone textbox, no "Signed in as" group)

- [ ] **Step 2: Add the copy**

`copy.ts` — add to `IntakeCopy`:

```ts
  phoneTitle: string
  phoneHelp: string
  phoneLabel: string
  phoneContinue: string
  phoneInvalid: string
  profileLabel: string
  changeNumber: string
  confirmChange: string
  confirmChangeBody: string
  receiptFor: string
```

`locales/en.json` — add before `"empty"`:

```json
  "phoneTitle": "Start with your phone number",
  "phoneHelp": "Use the number registered on your ZainCash account. Support uses it to find your account and your reports.",
  "phoneLabel": "Your ZainCash phone number",
  "phoneContinue": "Continue",
  "phoneInvalid": "Enter a valid ZainCash phone number, for example 07701234567.",
  "profileLabel": "Signed in as",
  "changeNumber": "Change number",
  "confirmChange": "Use another number",
  "confirmChangeBody": "Your current report stays saved with this number. You can enter a different number next.",
  "receiptFor": "Submitted for",
```

`locales/ar.json` — add before `"empty"`:

```json
  "phoneTitle": "ابدأ برقم هاتفك",
  "phoneHelp": "استخدم الرقم المسجّل بحساب زين كاش مالتك. الدعم يستخدمه حتى يلگى حسابك وتقاريرك.",
  "phoneLabel": "رقم هاتفك بزين كاش",
  "phoneContinue": "استمرار",
  "phoneInvalid": "اكتب رقم زين كاش صحيح، مثل 07701234567.",
  "profileLabel": "داخل بالرقم",
  "changeNumber": "تغيير الرقم",
  "confirmChange": "استخدم رقم ثاني",
  "confirmChangeBody": "تقريرك الحالي يبقى محفوظ بهالرقم. بعدها تگدر تدخل رقم ثاني.",
  "receiptFor": "انرسل للرقم",
```

- [ ] **Step 3: Add the shared button classes and the phone screen**

`buttons.ts`:

```ts
export const solidButton = "bg-[#da3345] text-white hover:bg-[#c42d3d]"
export const quietButton = "border-border bg-card text-foreground hover:bg-muted"
```

`PhoneGate.tsx`:

```tsx
import { useState, type FormEvent } from "react"
import { Button } from "@workspace/ui/components/button"
import { solidButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import { normalizeCustomerPhone } from "./phone"

export function PhoneGate({
  copy,
  busy,
  serverError,
  onSubmit,
}: {
  copy: IntakeCopy
  busy: boolean
  serverError: "invalid" | "failed" | null
  onSubmit: (phone: string) => void
}) {
  const [value, setValue] = useState("")
  const [checked, setChecked] = useState(false)
  const [sent, setSent] = useState<string | null>(null)
  const phone = normalizeCustomerPhone(value)
  const serverMessage =
    sent === value && serverError
      ? serverError === "invalid" ? copy.phoneInvalid : copy.updateError
      : null
  const error = checked && !phone ? copy.phoneInvalid : serverMessage

  function submit(event: FormEvent) {
    event.preventDefault()
    setChecked(true)
    if (!phone || busy) return
    setSent(value)
    onSubmit(phone)
  }

  return (
    <form className="intake-gate" onSubmit={submit} noValidate>
      <h1 className="intake-gate-title">{copy.phoneTitle}</h1>
      <p className="intake-muted">{copy.phoneHelp}</p>
      <label htmlFor="intake-phone">{copy.phoneLabel}</label>
      <input
        id="intake-phone"
        className="intake-gate-input"
        dir="ltr"
        inputMode="tel"
        autoComplete="tel"
        placeholder="07XXXXXXXXX"
        value={value}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? "intake-phone-error" : undefined}
        onChange={(event) => {
          setValue(event.target.value)
          setChecked(false)
        }}
      />
      {error ? (
        <p id="intake-phone-error" role="alert" className="intake-gate-error">
          {error}
        </p>
      ) : null}
      <Button type="submit" className={solidButton} disabled={busy}>
        {copy.phoneContinue}
      </Button>
    </form>
  )
}
```

- [ ] **Step 4: Wire the page**

`IntakePage.tsx`:

1. Delete lines 10–11 (the two button-class constants) and add imports:

```tsx
import { quietButton, solidButton } from "./buttons"
import { PhoneGate } from "./PhoneGate"
```

2. After `const [confirmNew, setConfirmNew] = useState(false)` add `const [confirmChange, setConfirmChange] = useState(false)`. After `const credentials = controller.access()` add `const needsPhone = snapshot.needsPhone`.

3. After `const hasContent = ...` add:

```tsx
  const inProgress = hasContent && session?.phase !== "submitted"

  function changeNumber() {
    setConfirmChange(false)
    setConfirmNew(false)
    setDraft("")
    clearPreviews()
    setLocale(locale) // keep the language the customer chose
    void controller.changeNumber()
  }
```

4. In the header, wrap the four existing buttons inside `intake-header-actions` (review-now, refresh, retry, start-new) in `{needsPhone ? null : (<> … </>)}`, then insert before the `lang-toggle` div:

```tsx
            {session ? (
              <div className="intake-profile" role="group" aria-label={text.profileLabel}>
                <span className="intake-muted">{text.profileLabel}</span>
                <bdi dir="ltr" className="intake-profile-phone">{session.customer_phone}</bdi>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className={quietButton}
                  onClick={() => (inProgress ? setConfirmChange(true) : changeNumber())}
                >
                  {text.changeNumber}
                </Button>
              </div>
            ) : null}
```

5. After the `confirmNew` dialog block add:

```tsx
        {confirmChange ? (
          <div className="intake-confirm" role="dialog" aria-label={text.changeNumber}>
            <p>{text.confirmChangeBody}</p>
            <div className="intake-actions">
              <Button type="button" className={solidButton} onClick={changeNumber}>
                {text.confirmChange}
              </Button>
              <Button type="button" variant="outline" className={quietButton} onClick={() => setConfirmChange(false)}>
                {text.cancel}
              </Button>
            </div>
          </div>
        ) : null}
```

6. Inside `<main className="intake-chat">`, render the gate instead of the file input and chat while `needsPhone`:

```tsx
        <main className="intake-chat">
          {needsPhone ? (
            <PhoneGate
              copy={text}
              busy={snapshot.busy}
              serverError={snapshot.phoneError}
              onSubmit={(phone) => void controller.initialize(locale, phone)}
            />
          ) : (
            <>
              {/* existing <input id="intake-shots" …/> and <AgentChat …/> unchanged */}
            </>
          )}
        </main>
```

7. Pass the phone to the receipt: `<ReceiptPanel receipt={session.receipt} customerPhone={session.customer_phone} copy={text} />`.

`ReceiptPanel.tsx`:

```tsx
export function ReceiptPanel({ receipt, customerPhone, copy }: { receipt: Receipt; customerPhone: string; copy: IntakeCopy }) {
```

and after the ticket-reference paragraph:

```tsx
      <p>
        {copy.receiptFor} <bdi dir="ltr">{customerPhone}</bdi>
      </p>
```

`intake.css` — append before the `@media (min-width: 800px)` block:

```css
.intake-profile {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.intake-profile-phone {
  font-family: var(--font-latin);
  font-weight: 600;
}
.intake-gate {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: min(420px, 100%);
  margin: auto;
  padding: 24px 16px;
}
.intake-gate-title {
  margin: 0;
  font-size: 1.35rem;
}
.intake-gate-input {
  min-height: 44px;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-latin);
  font-size: 1.05rem;
  text-align: left;
}
.intake-gate-input:focus-visible {
  outline: 2px solid #da3345;
  outline-offset: 2px;
}
.intake-gate-error {
  margin: 0;
  color: #da3345;
}
```

- [ ] **Step 5: Run the whole intake app suite, typecheck and lint**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npx vitest run && npm run typecheck && npm run lint"`
Expected: all tests PASS, no type or lint errors.

- [ ] **Step 6: Commit**

```bash
git add users-frontend/apps/web/src/features/intake
git commit -m "feat(intake-app): add the phone screen and show the customer's number"
```

---

### Task 9: Employee app — required phone, queue identity and search, batch entry

**Files:**
- Create: `employee-frontend/src/lib/phone.ts`, `employee-frontend/src/lib/phone.test.ts`, `employee-frontend/src/lib/test-fixtures.ts`
- Create: `employee-frontend/src/features/queue/TicketIdentity.tsx`, `TicketIdentity.test.tsx`
- Modify: `employee-frontend/src/lib/types.ts:2-14`
- Modify: `employee-frontend/src/features/queue/queue-projection.ts`, `queue-projection.test.ts`
- Modify: `employee-frontend/src/features/queue/QueuePage.tsx:245-263,397`
- Modify: `employee-frontend/src/lib/imports.ts:74-80`, `imports.test.ts`
- Create: `employee-frontend/src/features/runs/pasted-ticket.ts`, `pasted-ticket.test.ts`
- Modify: `employee-frontend/src/features/runs/NewBatchPage.tsx`
- Modify: `employee-frontend/src/lib/api.ts:44-48`, `api.test.ts`
- Modify: `employee-frontend/src/features/review/TicketReviewPage.tsx:321` (drop `display_name` only; the header is redesigned in Task 10)
- Modify: `employee-frontend/src/locales/en.json`, `ar.json`
- Fix fixtures: `employee-frontend/src/features/review/ticket-flow.test.ts:64`, `ticket-flow-view.test.tsx:28`

**Interfaces:**
- Consumes: backend `customer_phone` in result tickets, 422 list errors with `loc` (Tasks 3, 5)
- Produces:
  - `normalizeCustomerPhone(raw: string): string | null`, `customerPath(phone: string): string` → `/customers/<phone>`
  - `TicketInput.customer_phone: string` (required); `Ticket` without `display_name`
  - `resultFixture(id: number, patch?: Partial<Result>, ticket?: Partial<Ticket>): Result`
  - `TicketIdentity({ ticket, index })`
  - `pastedTickets(message: string, channel: TicketInput["channel"], phone: string): TicketInput[]`
  - Copy keys: `batch.phoneInvalid`

- [ ] **Step 1: Write the failing helper tests**

`employee-frontend/src/lib/phone.test.ts`:

```ts
import { expect, it } from "vitest"
import { customerPath, normalizeCustomerPhone } from "./phone"

it.each(["07809876543", "+964 780 987 6543", "٠٧٨٠٩٨٧٦٥٤٣", "7809876543", "00964-780-987-6543"])("accepts %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBe("07809876543")
})

it.each(["", "0780", "07809876543x", "07209876543", "needle"])("rejects %s", (raw) => {
  expect(normalizeCustomerPhone(raw)).toBeNull()
})

it("builds the customer page path", () => {
  expect(customerPath("07809876543")).toBe("/customers/07809876543")
})
```

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run src/lib/phone.test.ts"`
Expected: FAIL (cannot resolve `./phone`)

- [ ] **Step 2: Implement the helper, types and fixture**

`employee-frontend/src/lib/phone.ts`:

```ts
// Same rules as backend/app/customers/phone.py. The server stays authoritative.
const ALLOWED = /^[0-9\s+\-().]*$/
const CANONICAL = /^07[3-9][0-9]{8}$/
const WITHOUT_ZERO = /^7[3-9][0-9]{8}$/

function asciiDigits(value: string) {
  // U+0660–U+0669 and U+06F0–U+06F9 end in the digit value.
  return value.replace(/[\u0660-\u0669\u06f0-\u06f9]/g, (digit) => String(digit.charCodeAt(0) & 0xf))
}

export function normalizeCustomerPhone(raw: string): string | null {
  const text = asciiDigits(raw).trim()
  if (!ALLOWED.test(text)) return null
  let digits = text.replace(/[^0-9]/g, "")
  if (digits.startsWith("00964")) digits = digits.slice(2)
  if (digits.startsWith("964")) digits = `0${digits.slice(3)}`
  else if (WITHOUT_ZERO.test(digits)) digits = `0${digits}`
  return CANONICAL.test(digits) ? digits : null
}

export function customerPath(phone: string) {
  return `/customers/${encodeURIComponent(phone)}`
}
```

`employee-frontend/src/lib/types.ts`:

```ts
export type TicketInput = {
  external_id?: string
  text: string
  received_at?: string
  channel: "app" | "whatsapp" | "call_note"
  customer_phone: string
}
export type Ticket = TicketInput & {
  id: number
  external_id: string
  received_at: string
}
```

Also add (used by Task 10):

```ts
export type CustomerProfile = {
  phone: string
  created_at: string
  ticket_count: number
  results: Result[]
}
```

`employee-frontend/src/lib/test-fixtures.ts`:

```ts
import type { Result, Ticket } from "./types"

export function resultFixture(id: number, patch: Partial<Result> = {}, ticket: Partial<Ticket> = {}): Result {
  return {
    id,
    ticket_id: id,
    run_id: 1,
    ticket: {
      id,
      external_id: `T-${id}`,
      text: `ticket ${id}`,
      received_at: "2026-10-12T10:00:00Z",
      channel: "app",
      customer_phone: "07701234567",
      ...ticket,
    },
    category: "failed_transfer",
    category_confidence: 0.8,
    category_probs: {},
    priority: "P2",
    priority_confidence: null,
    flags: {},
    classifier_path: "jev",
    extracted: {},
    lookup_status: "not_applicable",
    matched_txn_ref: null,
    team: "Payments Ops",
    escalated: false,
    escalation_reasons: [],
    escalation_note: null,
    draft_text: null,
    final_text: null,
    citations: [],
    agent_trace: [],
    status: "pending_review",
    error: null,
    latency_ms: 1,
    cost_usd: 0,
    updated_at: "2026-10-12T10:00:00Z",
    ...patch,
  }
}
```

Replace `customer_phone: null,` with `customer_phone: "07701234567",` in `queue-projection.test.ts:24`, `ticket-flow.test.ts:64` and `ticket-flow-view.test.tsx:28`.

Run Step 1's command. Expected: PASS.

- [ ] **Step 3: Write the failing queue, import, batch and API tests**

`queue-projection.test.ts` — add:

```ts
it("finds a customer's tickets by phone in any accepted format", () => {
  const mine = row(1)
  const rows = [
    { ...mine, ticket: { ...mine.ticket, customer_phone: "07809876543" } },
    row(2),
  ]
  for (const search of ["07809876543", "+964 780 987 6543", "0780987"]) {
    expect(projectQueue(rows, filters({ search }), 0).filtered.map((item) => item.id)).toEqual([1])
  }
})
```

`employee-frontend/src/features/queue/TicketIdentity.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import { TicketIdentity } from "./TicketIdentity"

it("leads with the customer phone and links to the customer page", () => {
  const { ticket } = resultFixture(7, {}, { external_id: "S-001", customer_phone: "07809876543" })
  const html = renderToStaticMarkup(<MemoryRouter><TicketIdentity ticket={ticket} index={0} /></MemoryRouter>)
  expect(html).toContain('href="/customers/07809876543"')
  expect(html.indexOf("07809876543")).toBeLessThan(html.indexOf("S-001"))
})
```

`imports.test.ts`:
- Give existing rows a phone so they still reach the checks they test: CSV header `external_id,text,customer_phone` with row `T-1,"…",07701234567`; JSONL rows `{"message":"مرحبا","customer_phone":"07701234567"}` and `{"text":"سؤال","customer_phone":"07701234567"}`; in the conflicting-ID JSON add `"customer_phone":"07701234567"` to both rows.
- Add:

```ts
  it("requires and normalizes the customer phone", () => {
    expect(() => parseTicketFile('[{"text":"one"}]', "t.json")).toThrow(/Row 1 needs a valid customer phone/)
    expect(() => parseTicketFile('[{"text":"one","customer_phone":"0770"}]', "t.json")).toThrow(/Row 1/)
    expect(parseTicketFile('[{"text":"one","customer_phone":"+964 770 123 4567"}]', "t.json")[0].customer_phone).toBe("07701234567")
  })
```

`api.test.ts`:
- In "starts every new run with Jev classification", pass `{ text: "شكد العمولة", channel: "app", customer_phone: "07701234567" }`.
- Add:

```ts
it("names the ticket row in validation errors", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({
    detail: [{ loc: ["body", "tickets", 1, "customer_phone"], msg: "Value error, Enter a valid ZainCash phone number, for example 07701234567." }],
  }), { status: 422 }))
  await expect(api.startRun([])).rejects.toThrow("Ticket 2: Value error, Enter a valid ZainCash phone number")
})
```

`employee-frontend/src/features/runs/pasted-ticket.test.ts` (the paste tab is not rendered in static markup while the upload tab is active, so the rule is tested as a pure function):

```ts
import { expect, it } from "vitest"
import { pastedTickets } from "./pasted-ticket"

it("builds one ticket only with a message and a valid phone", () => {
  expect(pastedTickets("حولت فلوس", "app", "+964 780 987 6543")).toEqual([
    { text: "حولت فلوس", channel: "app", customer_phone: "07809876543" },
  ])
  expect(pastedTickets("حولت فلوس", "app", "")).toEqual([])
  expect(pastedTickets("حولت فلوس", "app", "0780")).toEqual([])
  expect(pastedTickets("   ", "app", "07809876543")).toEqual([])
})
```

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run src/features/queue src/lib src/features/runs/pasted-ticket.test.ts"`
Expected: FAIL (phone search misses, TicketIdentity and pasted-ticket missing, imports accept no phone, message lacks "Ticket 2:")

- [ ] **Step 4: Implement queue search and identity**

`queue-projection.ts` — import `normalizeCustomerPhone` from `@/lib/phone`; before `const filtered`, add `const phoneQuery = normalizeCustomerPhone(filters.search)`; replace the search clause with:

```ts
      (`${row.ticket.text} ${row.ticket.external_id} ${row.ticket.customer_phone}`
        .toLowerCase()
        .includes(filters.search.toLowerCase()) ||
        (phoneQuery !== null && row.ticket.customer_phone === phoneQuery)),
```

`TicketIdentity.tsx`:

```tsx
import { Link } from "react-router-dom"
import { Smartphone } from "lucide-react"
import { dateLabel, timeLabel } from "@/lib/format"
import { customerPath } from "@/lib/phone"
import type { Ticket } from "@/lib/types"

export function TicketIdentity({ ticket, index }: { ticket: Ticket; index: number }) {
  return (
    <div className="ticket-identity">
      <span className={`ticket-avatar avatar-${index % 4}`}>
        <Smartphone size={17} />
      </span>
      <div>
        <Link to={customerPath(ticket.customer_phone)} className="ticket-id">
          <bdi dir="ltr">{ticket.customer_phone}</bdi>
        </Link>
        <small>
          <bdi dir="ltr">{ticket.external_id}</bdi> · {dateLabel(ticket.received_at)}, {timeLabel(ticket.received_at)}
        </small>
      </div>
    </div>
  )
}
```

`QueuePage.tsx`:
- Replace the first `<TableCell>`'s `<div className="ticket-identity">…</div>` (lines ~246–263) with `<TicketIdentity ticket={row.ticket} index={index} />` and import it from `./TicketIdentity`. Remove now-unused imports (`dateLabel`, `timeLabel`, `Smartphone` if no longer used elsewhere in the file — `Smartphone` is still used for the channel icon, keep it).
- In the attention card, replace `<span>{row.ticket.external_id}</span>` with `<span dir="ltr">{row.ticket.customer_phone}</span>`.

- [ ] **Step 5: Implement import, batch entry and API error changes**

`imports.ts` — import `normalizeCustomerPhone` from `./phone`; replace the returned object:

```ts
    const phone = normalizeCustomerPhone(String(row.customer_phone ?? ""))
    if (!phone)
      throw new Error(`Row ${index + 1} needs a valid customer phone (07XXXXXXXXX).`)
    return {
      external_id: id,
      text: message.trim(),
      channel,
      ...(row.received_at ? { received_at: String(row.received_at) } : {}),
      customer_phone: phone,
    }
```

`employee-frontend/src/features/runs/pasted-ticket.ts`:

```ts
import { normalizeCustomerPhone } from "@/lib/phone"
import type { TicketInput } from "@/lib/types"

export function pastedTickets(message: string, channel: TicketInput["channel"], phone: string): TicketInput[] {
  const customerPhone = normalizeCustomerPhone(phone)
  return message.trim() && customerPhone ? [{ text: message, channel, customer_phone: customerPhone }] : []
}
```

`NewBatchPage.tsx`:
- Import `normalizeCustomerPhone` from `@/lib/phone` and `pastedTickets` from `./pasted-ticket`.
- `exampleTickets`: add `customer_phone: "07501112233"` to the second and `customer_phone: "07734445566"` to the third ticket.
- Replace `selected`:

```tsx
  const customerPhone = normalizeCustomerPhone(phone)
  const selected = tab === "upload" ? tickets : pastedTickets(message, channel, phone)
```

- On the phone `<Input>` add `required`, `aria-required="true"` and `aria-invalid={Boolean(phone.trim() && !customerPhone)}`. After the `<Input …/>` (inside the label) add:

```tsx
                    {phone.trim() && !customerPhone ? (
                      <small className="error-text" role="alert">{text.phoneInvalid}</small>
                    ) : null}
```

`api.ts` `request()` — replace the array branch:

```ts
      else if (Array.isArray(body.detail))
        message = body.detail
          .map((error: { msg: string; loc?: unknown[] }) => {
            const index = error.loc?.[1] === "tickets" ? error.loc?.[2] : undefined
            return typeof index === "number" ? `Ticket ${index + 1}: ${error.msg}` : error.msg
          })
          .join(" ")
```

`TicketReviewPage.tsx:321` — replace `result.ticket.display_name || textCopy.customerTicket` with `textCopy.customerTicket` (Task 10 replaces the whole header).

- [ ] **Step 6: Update the locale strings**

`en.json`: `queue.searchPlaceholder` → `"Search phone, ticket ID or message…"`; `queue.colTicket` → `"Customer / Ticket"`; `batch.phone` → `"Customer phone"`; add `"phoneInvalid": "Enter a valid phone number, for example 07701234567."` after `batch.phonePlaceholder`.

`ar.json`: `queue.searchPlaceholder` → `"ابحث برقم الهاتف أو التذكرة أو الرسالة…"`; `queue.colTicket` → `"الزبون / التذكرة"`; `batch.phone` → `"هاتف الزبون"`; add `"phoneInvalid": "اكتب رقم هاتف صحيحاً، مثل 07701234567."` after `batch.phonePlaceholder`.

- [ ] **Step 7: Run tests, typecheck and lint**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run && npm run typecheck && npm run lint"`
Expected: PASS, no type errors (every `customer_phone: null` and `display_name` use is gone).

- [ ] **Step 8: Commit**

```bash
git add employee-frontend/src
git commit -m "feat(workspace): lead the queue with the customer phone and require it on batches"
```

---

### Task 10: Employee app — customer page and ticket header link

**Files:**
- Create: `employee-frontend/src/features/customers/CustomerPage.tsx`, `CustomerPage.test.tsx`
- Create: `employee-frontend/src/features/review/TicketHeader.tsx`, `TicketHeader.test.tsx`
- Modify: `employee-frontend/src/components/shared/workspace-ui.tsx:57-65` (`PageHeader.title: ReactNode`)
- Modify: `employee-frontend/src/features/review/TicketReviewPage.tsx:319-325`
- Modify: `employee-frontend/src/App.tsx` (lazy route `customers/:phone`)
- Modify: `employee-frontend/src/locales/en.json`, `ar.json`, `employee-frontend/src/styles/workspace.css`

**Interfaces:**
- Consumes: `GET /api/customers/{phone}` (Task 5); `customerPath`, `normalizeCustomerPhone`, `CustomerProfile`, `resultFixture` (Task 9); `request`, `ApiError` (`lib/api.ts`); `useResource` (`hooks/use-resource.ts`)
- Produces: `CustomerPage`, `CustomerProfileView({ customer })`, `TicketHeader({ result })`; copy section `customer`; key `review.customerProfile` (replaces `review.customerTicket`)

- [ ] **Step 1: Write the failing tests**

`employee-frontend/src/features/customers/CustomerPage.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { getLocale, setLocale } from "@/lib/locale"
import { resultFixture } from "@/lib/test-fixtures"
import { WorkspaceContext } from "@/lib/workspace"
import { CustomerPage, CustomerProfileView } from "./CustomerPage"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

it("lists the customer's tickets with links to each review", () => {
  setLocale("en")
  const html = renderToStaticMarkup(
    <MemoryRouter>
      <CustomerProfileView customer={{
        phone: "07809876543",
        created_at: "2026-10-07T09:30:00+03:00",
        ticket_count: 2,
        results: [
          resultFixture(11, {}, { external_id: "S-001", customer_phone: "07809876543" }),
          resultFixture(12, {}, { external_id: "S-009", customer_phone: "07809876543" }),
        ],
      }} />
    </MemoryRouter>,
  )
  expect(html).toContain("07809876543")
  expect(html).toContain("2 tickets")
  expect(html).toContain('href="/tickets/11"')
  expect(html).toContain("S-009")
})

it("shows a localized state for a malformed phone without loading", () => {
  setLocale("ar")
  const html = renderToStaticMarkup(
    <MemoryRouter initialEntries={["/customers/abc"]}>
      <WorkspaceContext.Provider value={{
        revision: 0, refresh: () => {}, health: null, connectionError: null, notify: () => {},
      }}>
        <Routes>
          <Route path="/customers/:phone" element={<CustomerPage />} />
        </Routes>
      </WorkspaceContext.Provider>
    </MemoryRouter>,
  )
  expect(html).toContain("رقم الهاتف غير صحيح")
})
```

`employee-frontend/src/features/review/TicketHeader.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { expect, it } from "vitest"
import { resultFixture } from "@/lib/test-fixtures"
import { TicketHeader } from "./TicketHeader"

it("titles the ticket with the customer phone linked to the customer page", () => {
  const result = resultFixture(5, {}, { external_id: "INTAKE-abc", customer_phone: "07809876543" })
  const html = renderToStaticMarkup(<MemoryRouter><TicketHeader result={result} /></MemoryRouter>)
  expect(html).toMatch(/<h1>.*href="\/customers\/07809876543".*07809876543.*<\/h1>/)
  expect(html).toContain("INTAKE-abc")
})
```

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run src/features/customers src/features/review/TicketHeader.test.tsx"`
Expected: FAIL (modules not found)

- [ ] **Step 2: Add the copy**

`en.json`: in `review`, replace `"customerTicket": "Customer support ticket",` with `"customerProfile": "Open customer profile",`. Add a top-level section after `queue`:

```json
  "customer": {
    "back": "Back to queue",
    "since": "Customer since {date}",
    "ticketCount": "{count} tickets",
    "colTicket": "Ticket",
    "colIssue": "Issue & message",
    "colPriority": "Priority",
    "colStatus": "Status",
    "noTickets": "No tickets yet",
    "noTicketsDetail": "Tickets for this phone number appear here after they are processed.",
    "notFound": "No customer with this number",
    "notFoundDetail": "No ticket has been received from this phone number yet.",
    "invalid": "Not a valid phone number",
    "invalidDetail": "Customer pages use a ZainCash phone number, for example 07701234567."
  },
```

`ar.json`: in `review`, replace `"customerTicket": "تذكرة دعم الزبائن",` with `"customerProfile": "فتح ملف الزبون",`. Add after `queue`:

```json
  "customer": {
    "back": "العودة إلى الطابور",
    "since": "زبون منذ {date}",
    "ticketCount": "{count} تذاكر",
    "colTicket": "التذكرة",
    "colIssue": "المشكلة والرسالة",
    "colPriority": "الأولوية",
    "colStatus": "الحالة",
    "noTickets": "لا توجد تذاكر بعد",
    "noTicketsDetail": "تظهر تذاكر هذا الرقم هنا بعد معالجتها.",
    "notFound": "لا يوجد زبون بهذا الرقم",
    "notFoundDetail": "لم تصل أي تذكرة من هذا الرقم حتى الآن.",
    "invalid": "رقم الهاتف غير صحيح",
    "invalidDetail": "صفحة الزبون تستخدم رقم زين كاش، مثل 07701234567."
  },
```

- [ ] **Step 3: Implement the header**

`workspace-ui.tsx` `PageHeader`: change `title: string` to `title: ReactNode` (`ReactNode` is already imported for `children`).

`employee-frontend/src/features/review/TicketHeader.tsx`:

```tsx
import { Link } from "react-router-dom"
import { PageHeader, PriorityBadge, StatusBadge } from "@/components/shared/workspace-ui"
import { dateLabel, timeLabel } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import { customerPath } from "@/lib/phone"
import type { Result } from "@/lib/types"

export function TicketHeader({ result }: { result: Result }) {
  const text = useCopy().review
  const { customer_phone: phone, external_id, received_at } = result.ticket
  return (
    <PageHeader
      title={
        <Link to={customerPath(phone)} className="customer-title-link" title={text.customerProfile}>
          <bdi dir="ltr">{phone}</bdi>
        </Link>
      }
      description={`${external_id} · ${dateLabel(received_at)}, ${timeLabel(received_at)} ${text.baghdad}`}
    >
      <PriorityBadge priority={result.priority} />
      <StatusBadge status={result.status} />
    </PageHeader>
  )
}
```

`TicketReviewPage.tsx`: replace the `<PageHeader …>…</PageHeader>` block (lines ~319–325) with `<TicketHeader result={result} />`, import it from `./TicketHeader`, and remove imports that become unused (`PageHeader`, `PriorityBadge`, `StatusBadge`, `dateLabel`, `timeLabel` — check each is not used elsewhere in the file first).

`workspace.css` — append after the `.ticket-id:hover` rule:

```css
.customer-title-link {
  color: inherit;
  text-decoration: none;
}
.customer-title-link:hover {
  text-decoration: underline;
  text-underline-offset: 4px;
}
```

- [ ] **Step 4: Implement the customer page and route**

`employee-frontend/src/features/customers/CustomerPage.tsx`:

```tsx
import { Link, useParams } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { ApiError, request } from "@/lib/api"
import { categoryLabel, dateLabel, timeLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import { normalizeCustomerPhone } from "@/lib/phone"
import type { CustomerProfile } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"

async function loadCustomer(path: string, options: RequestInit) {
  try {
    return await request<CustomerProfile>(path, options)
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) return null
    throw error
  }
}

function CustomerMissing({ title, description }: { title: string; description: string }) {
  const text = useCopy().customer
  return (
    <EmptyState title={title} description={description}>
      <Button nativeButton={false} render={<Link to="/" />}>
        {text.back}
      </Button>
    </EmptyState>
  )
}

export function CustomerProfileView({ customer }: { customer: CustomerProfile }) {
  const text = useCopy().customer
  return (
    <>
      <Link to="/" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={<bdi dir="ltr">{customer.phone}</bdi>}
        description={`${fill(text.since, { date: dateLabel(customer.created_at) })} · ${fill(text.ticketCount, { count: customer.ticket_count })}`}
      />
      <Card className="queue-card">
        {customer.results.length ? (
          <Table className="ticket-table">
            <TableHeader>
              <TableRow>
                <TableHead>{text.colTicket}</TableHead>
                <TableHead>{text.colIssue}</TableHead>
                <TableHead>{text.colPriority}</TableHead>
                <TableHead>{text.colStatus}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {customer.results.map((row) => (
                <TableRow key={row.id} className="ticket-row">
                  <TableCell>
                    <div className="ticket-identity">
                      <div>
                        <Link to={`/tickets/${row.id}`} className="ticket-id">
                          <bdi dir="ltr">{row.ticket.external_id}</bdi>
                        </Link>
                        <small>
                          {dateLabel(row.ticket.received_at)}, {timeLabel(row.ticket.received_at)}
                        </small>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="ticket-subject">
                      <strong>{categoryLabel(row.category)}</strong>
                      <p dir="auto" lang="ar">{row.ticket.text}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <PriorityBadge priority={row.priority} />
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={row.status} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <EmptyState title={text.noTickets} description={text.noTicketsDetail} />
        )}
      </Card>
    </>
  )
}

export function CustomerPage() {
  const { phone: raw = "" } = useParams()
  const workspace = useWorkspace()
  const text = useCopy().customer
  const phone = normalizeCustomerPhone(raw)
  const query = useResource<CustomerProfile | null>(
    phone ? `/customers/${phone}` : null,
    workspace.revision,
    0,
    loadCustomer,
  )
  if (!phone) return <CustomerMissing title={text.invalid} description={text.invalidDetail} />
  if (query.error) return <ErrorState message={query.error} retry={query.reload} />
  if (query.loading) return <LoadingState />
  if (!query.data) return <CustomerMissing title={text.notFound} description={text.notFoundDetail} />
  return <CustomerProfileView customer={query.data} />
}
```

`App.tsx` — add with the other lazy imports:

```tsx
const CustomerPage = lazy(() =>
  import("@/features/customers/CustomerPage").then((module) => ({
    default: module.CustomerPage,
  }))
)
```

and the route after `tickets/:id`: `<Route path="customers/:phone" element={<CustomerPage />} />`.

- [ ] **Step 5: Run tests, typecheck, lint and build**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npx vitest run && npm run lint && npm run build"`
Expected: PASS; build succeeds.

- [ ] **Step 6: Commit**

```bash
git add employee-frontend/src
git commit -m "feat(workspace): add the customer page and link it from the ticket header"
```

---

### Task 11: Whole-system verification

**Files:**
- Possibly modify: anything a full-suite run exposes (only to fix regressions caused by this plan)

- [ ] **Step 1: Run every backend check**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/backend -- bash -lc "uv run pytest -q && uv run ruff check app tests"`
Expected: all tests pass, no lint findings. If an untouched test fails because it posts tickets or creates intake sessions without a phone, add the phone (`07701234567`) the same way as in Tasks 3–4.

- [ ] **Step 2: Run every frontend check**

Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/employee-frontend -- bash -lc "npm test && npm run lint && npm run build"`
Run: `wsl -d Ubuntu-24.04 --cd /home/cvzmh_saif/dev/zaincash-support/users-frontend/apps/web -- bash -lc "npm test && npm run lint && npm run build"`
Expected: PASS

- [ ] **Step 3: Manual smoke test on a reset demo database**

1. `docker compose down -v` then `docker compose up --build -d` (from the repo root in WSL).
2. Run `docker/db/cleanup.sql` then `docker/db/seed_demo.sql` against database `support`.
3. Employee workspace (http://localhost:5173): queue rows show phones first; search `+964 780 987 6543` finds RAG-DEMO-FAILED-TRANSFER; clicking a phone opens `/customers/07809876543`; a ticket header shows the phone linked to the same page; `/customers/abc` shows "Not a valid phone number".
4. Customer intake (http://localhost:5174): the phone screen appears; `0770` is rejected; `٠٧٧٠١٢٣٤٥٦٧` is accepted; the header shows `07701234567`; after a submitted report the receipt shows the number; the employee queue shows the intake ticket under `07701234567`.
5. Point the API at a database created before this change (or drop `NOT NULL` on `tickets.customer_phone` in a scratch DB): the API refuses to start with the reset message.

- [ ] **Step 4: Refresh the knowledge graph**

The repo rule `.cursor/rules/graphify.mdc` asks for `graphify update .` after code edits. Run it from the repo root in WSL if `graphify` is installed; otherwise note that it was skipped.

- [ ] **Step 5: Commit any regression fixes**

```bash
git add <only the files you changed in this task>
git commit -m "test: give remaining fixtures a customer phone"
```

(Skip if nothing changed.)
