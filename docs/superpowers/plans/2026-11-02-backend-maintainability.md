# Backend Maintainability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove reference-verified backend dead code, clarify existing module ownership, repair the recorded baseline, and fix the approved backend defects without changing public compatibility contracts.

**Architecture:** Work cleanup-first: delete only reference-verified dead code, then perform mechanical extractions behind unchanged interfaces, then use TDD for each approved defect fix. Keep pipeline stages, intake orchestration, API transport, and KB transaction behavior separate; no pipeline, API, schema, or migration-framework rewrite is included.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic 2, SQLAlchemy 2/PostgreSQL, LangGraph/LangChain, pytest/pytest-asyncio, Ruff, `uv`.

**Spec:** `docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md` (§§1–5 and 9–10 are the scope of this backend plan).

## Global Constraints

The following constraints are copied exactly from the approved specification and apply to every task:

- No git commits or other git mutations are part of this design.
- This pass does not:
  - Rewrite the pipeline, intake architecture, API, or frontend applications.
  - Change visual styling or user flows.
  - Reformat unrelated files or make stylistic changes without a maintainability purpose.
  - Split cohesive functions merely because of line count; `RagDrafter.draft`, `build_tools`, and `AgentChat` internals remain intact unless required by an approved change.
  - Remove public compatibility fields such as `fallback_rate`, `classifier_paths`, or `ClassifierOutput.degraded`.
  - Broaden JSONL parsing, weaken TypeScript contracts, or add type-suppression comments.
  - Add a runtime schema-validation library to the customer frontend.
  - Perform broad localization consolidation or extract `ReviewEditor` in this pass.
  - Optimize every database N+1 pattern; only the result-list work specified below is included.
  - Delete historical material merely because it mentions retired cascade behavior.
  - Delete generated UI primitive exports solely because they currently lack local consumers.
- Existing HTTP status codes, public messages, optimistic-concurrency protections, idempotency keys, revision rules, and safe secret-free responses remain unchanged unless a defect fix explicitly requires otherwise.
- Model and tool execution limits remain in place. The Jev retry change prevents duplicate paid sibling calls rather than adding another retry layer.
- Database changes are limited to query/initialization behavior; no new schema or migration framework is introduced.
- Frontend runtime validation rejects malformed server or persisted data through the existing error paths rather than allowing invalid typed state to propagate.
- Upload failure behavior remains sequential and stop-on-first-failure; only stale preview handling and identity are corrected.
- Dependency removal must be followed by lockfile regeneration and complete builds to catch transitive or tooling assumptions.
- Until baseline repair, intermediate verification may show only the three documented backend failures and two documented employee TypeScript errors. Any additional failure is a regression and must be resolved before continuing.
- The root `README.md` had a pre-existing user modification. It is not part of this refactor and must not be overwritten.
- Historical specifications, verification records, dated Graphify snapshots, Archify provenance, demo data, and the user's existing root `README.md` modification remain intact.

Commands below run from the repository root unless a step explicitly changes directory. PostgreSQL integration tests require the existing `support_test` database; never point them at the development database.

## Review Focus

1. **Legacy database initialization:** a database with `runs.status VARCHAR(16)` and an existing completed row must be upgraded by both API and CLI entry points without losing that row — owned by `backend/tests/test_db_initialization.py::test_entry_points_upgrade_legacy_run_status` in Task 8.
2. **Partial Jev failure:** a successful paid main request followed by one order-check failure must produce the existing per-ticket failure without repeating either request — owned by `backend/tests/test_graph.py::test_failed_order_check_does_not_repeat_paid_sibling` in Task 10.
3. **Draft cost fallback:** Anthropic usage with missing provider cost must use Anthropic token prices, while an explicit provider cost of zero must remain authoritative — owned by `backend/tests/test_rag_drafter.py::test_anthropic_fallback_prices_and_provider_cost_precedence` in Task 11.
4. **Empty/paginated result views:** an offset beyond the filtered total must return no items with the real total, and list projection must not issue an intake-submission query — owned by `backend/tests/test_workspace_api.py::test_result_list_paginates_filters_and_run_id` and `test_result_list_uses_count_page_and_no_intake_query` in Task 12.
5. **Completed-operation replay after physical failure:** a removal whose first unlink failed must retry the same unlink without adding a revision or operation — owned by `backend/tests/intake/test_attachments.py::test_remove_replays_physical_unlink_without_revision_change` in Task 13.

---

### Task 1: Record the Baseline and Remove Reference-Verified Dead Code

**Files:**
- Create: none.
- Modify: `backend/app/config.py`, `backend/app/taxonomy.py`, `backend/app/intake/submission.py`, `backend/app/services/intake_runtime.py`, `backend/app/intake/model.py`, `backend/tests/test_taxonomy.py`.
- Test: `backend/tests/test_config.py`, `backend/tests/test_taxonomy.py`, `backend/tests/intake/test_model.py`, `backend/tests/intake/test_submission.py`, `backend/tests/intake/test_api.py`.

**Interfaces:**
- Consumes: existing `Settings`, `Taxonomy`, `SubmissionService`, `make_intake_service()`, and `ModelBudget(timeout_s, max_requests)` APIs.
- Produces: the same public runtime interfaces minus the unused settings and `current_session_view()`; `ModelBudget` retains its constructor argument and deadline behavior but has no `timeout_s` instance attribute.

- [ ] **Step 1: Capture the recorded backend baseline before editing**

```bash
cd backend
uv run ruff check app tests
uv run pytest -q
cd ..
```

Expected: Ruff passes. Pytest reports 758 passed and the three documented `sample_tickets.jsonl` failures; any other failure must be resolved before proceeding.

- [ ] **Step 2: Repeat reference searches and confirm the deletion set**

```bash
grep -RInE --include='*.py' 'gemini_strong_model|gemini_embed_model|price_gemini_pro_in|price_gemini_pro_out' backend/app backend/tests
grep -RInE --include='*.py' '\.render\(\)|def render\(' backend/app backend/tests
grep -RInE --include='*.py' 'current_session_view|service\.submission|\.timeout_s' backend/app/intake backend/app/services backend/tests/intake
```

Expected: the four settings occur only in `config.py`; `Taxonomy.render()` has only its test call; `current_session_view` has no caller; `service.submission` occurs only in `intake_runtime.py`; `ModelBudget.timeout_s` is only the unused assignment. Do not remove active timeout uses such as `settings.intake_timeout_s` or `budget.remaining_s()`.

- [ ] **Step 3: Apply the minimal dead-code deletions**

In `backend/app/config.py`, delete the four unused fields and change the validator to cover only the active model:

```python
    gemini_model: str = "google/gemini-3.8-flash"
    anthropic_model: str = ""
```

```python
    @field_validator("gemini_model")
    @classmethod
    def qualify_gemini_model(cls, value: str) -> str:
        """Accept legacy .env model names while recording the OpenRouter model ID."""
        return f"google/{value}" if value.startswith("gemini-") else value
```

In `backend/app/taxonomy.py`, delete `Taxonomy.render()` and retain `describe()` with the corrected ownership comment:

```python
    def describe(self) -> str:
        """One-line description used by Jev category criteria."""
        parts = [f"{self.what_en} ({self.what_ar})"]
        if self.not_for:
            parts.append(f"Not for: {self.not_for}")
        if self.examples:
            parts.append("Examples: " + " | ".join(self.examples))
        return ". ".join(parts)
```

In `backend/tests/test_taxonomy.py`, replace the render assertion test with:

```python
def test_describe(taxonomy):
    description = taxonomy.get("failed_transfer").describe()
    assert "Not for:" in description and "Examples:" in description
```

In `backend/app/intake/submission.py`, delete the complete `current_session_view()` function and remove `session_view` from its repository import. In `backend/app/services/intake_runtime.py`, delete the `SubmissionService` import and `service.submission = SubmissionService(...)`; retain:

```python
    service = IntakeService(repo, turns, graph, store)
    return service
```

In `backend/app/intake/model.py`, retain deadline initialization while deleting only the unused instance attribute:

```python
class ModelBudget:
    def __init__(self, timeout_s: float, max_requests: int) -> None:
        self.max_requests = max_requests
        self.deadline = time.monotonic() + timeout_s
        self.used = 0
        self.trace: list[dict] = []
```

- [ ] **Step 4: Verify cleanup with focused tests and reference searches**

```bash
cd backend
uv run pytest -q tests/test_config.py tests/test_taxonomy.py tests/intake/test_model.py tests/intake/test_submission.py tests/intake/test_api.py
uv run ruff check app/config.py app/taxonomy.py app/intake/submission.py app/services/intake_runtime.py app/intake/model.py tests/test_taxonomy.py
cd ..
grep -RInE --include='*.py' 'gemini_strong_model|gemini_embed_model|price_gemini_pro_in|price_gemini_pro_out|current_session_view|service\.submission' backend/app backend/tests || true
```

Expected: focused tests and Ruff pass; the final search prints no matches. `backend/app/main.py` still constructs the real `app.state.submission` path.

- [ ] **Step 5: Review the cleanup diff without changing git state**

```bash
git diff --check -- backend/app/config.py backend/app/taxonomy.py backend/app/intake/submission.py backend/app/services/intake_runtime.py backend/app/intake/model.py backend/tests/test_taxonomy.py
git diff -- backend/app/config.py backend/app/taxonomy.py backend/app/intake/submission.py backend/app/services/intake_runtime.py backend/app/intake/model.py backend/tests/test_taxonomy.py
```

Expected: only the approved deletions and docstring/test-name correction appear; no compatibility fields or historical documents changed.

### Task 2: Separate Historical Escalation Text from Current Tool Reasons

**Files:**
- Create: none.
- Modify: `backend/app/pipeline/stage5_decide/rules.py`, `backend/app/pipeline/stage6_draft/tools.py`.
- Test: `backend/tests/test_draft_tools.py`, `backend/tests/test_rules.py`.

**Interfaces:**
- Consumes: existing `REASON_TEXT`, `note_for(reasons)`, `build_tools()`, and `DraftToolInputError`.
- Produces: `CURRENT_REASON_TEXT` for current tool validation; `LEGACY_REASON_TEXT` plus unchanged `REASON_TEXT` for historical display. `note_for(("classifier_disagreement",))` retains its existing message.

- [ ] **Step 1: Add failing regression coverage for the retired reason and legacy display**

Add to `backend/tests/test_draft_tools.py`:

```python
async def test_retired_classifier_disagreement_cannot_be_introduced(api, state, sf, settings):
    context, tools, _ = tools_for(api, state, sf, settings)
    with pytest.raises(draft_context.DraftToolInputError, match="Unknown escalation reason"):
        await tools["flag_for_human"].ainvoke({
            "reason": "classifier_disagreement", "note": "historical result only",
        })
    assert context.reasons == ["txn_not_found"]
    assert context.notes == []
    assert context.trace[-1]["error_type"] == "DraftToolInputError"
```

Add to `backend/tests/test_rules.py`:

```python
def test_legacy_classifier_disagreement_note_remains_available():
    assert note_for(("classifier_disagreement",)) == (
        "Escalated: Jev and Gemini disagree on the category."
    )
```

- [ ] **Step 2: Run the new tool test and confirm the behavioral failure**

```bash
cd backend && uv run pytest -q tests/test_draft_tools.py::test_retired_classifier_disagreement_cannot_be_introduced tests/test_rules.py::test_legacy_classifier_disagreement_note_remains_available
```

Expected: the legacy-note test passes; the tool test fails because the retired reason is currently accepted.

- [ ] **Step 3: Split current and legacy reason mappings**

In `backend/app/pipeline/stage5_decide/rules.py`, use:

```python
LEGACY_REASON_TEXT = {
    "classifier_disagreement": "Jev and Gemini disagree on the category",
}
CURRENT_REASON_TEXT = {
    "low_confidence": "the classifier was not confident",
    "fraud_suspected": "possible fraud or scam",
    "multi_issue": "the ticket raises more than one issue",
    "asks_for_human": "the customer asked for a person",
    "missing_required_fields": "required details are missing",
    "txn_not_found": "no matching transaction was found",
    "txn_ambiguous": "several transactions match",
    "amount_mismatch": "the amount differs from the transaction record",
    "date_mismatch": "the date differs from the transaction record",
    "empty_ticket": "the ticket text is empty",
    "llm_unavailable": "the drafting model was unavailable",
    "draft_failed_guardrail": "the draft failed a safety check",
    "no_kb_support": "no policy document supports a reply",
}
REASON_TEXT = CURRENT_REASON_TEXT | LEGACY_REASON_TEXT
```

In `backend/app/pipeline/stage6_draft/tools.py`, import `CURRENT_REASON_TEXT` instead of `REASON_TEXT` and define:

```python
_REASONS = frozenset(CURRENT_REASON_TEXT) | {
    "kb_unavailable", "draft_timeout", "draft_tool_limit", "draft_not_submitted",
}
```

Keep `note_for()` and historical persisted-result behavior unchanged.

- [ ] **Step 4: Run focused drafting and rules tests**

```bash
cd backend
uv run pytest -q tests/test_draft_tools.py tests/test_rules.py tests/test_rag_drafter.py
uv run ruff check app/pipeline/stage5_decide/rules.py app/pipeline/stage6_draft/tools.py tests/test_draft_tools.py tests/test_rules.py
cd ..
```

Expected: all tests and Ruff pass; current tools reject only the retired cascade reason while historical note rendering remains available.

- [ ] **Step 5: Review the reason-separation diff**

```bash
git diff --check -- backend/app/pipeline/stage5_decide/rules.py backend/app/pipeline/stage6_draft/tools.py backend/tests/test_draft_tools.py backend/tests/test_rules.py
git diff -- backend/app/pipeline/stage5_decide/rules.py backend/app/pipeline/stage6_draft/tools.py backend/tests/test_draft_tools.py backend/tests/test_rules.py
```

Expected: no public result fields or existing reason messages were removed.

### Task 3: Move Gemini Gap Extraction and Its Metadata into Stage 3

**Files:**
- Create: `backend/app/pipeline/stage3_extract/base.py`, `backend/app/pipeline/stage3_extract/gemini.py`, `backend/app/pipeline/stage3_extract/prompts/__init__.py`, `backend/app/pipeline/stage3_extract/prompts/gemini_extract_v1.md`.
- Modify: `backend/app/pipeline/stage2_classify/base.py`, `backend/app/pipeline/stage3_extract/extract.py`, `backend/app/pipeline/factory.py`, `backend/app/pipeline/graph.py`, `backend/app/api/runs.py`, `backend/app/cli.py`, `backend/app/intake/submission.py`, `backend/tests/test_gemini.py`.
- Delete: `backend/app/pipeline/stage2_classify/gemini.py`, `backend/app/pipeline/stage2_classify/prompts/__init__.py`, `backend/app/pipeline/stage2_classify/prompts/gemini_extract_v1.md`.
- Test: `backend/tests/test_gemini.py`, `backend/tests/test_extract.py`, `backend/tests/test_factory.py`, `backend/tests/test_graph.py`, `backend/tests/test_cli.py::test_run_batch_defaults_to_jev`, `backend/tests/intake/test_submission.py`.

**Interfaces:**
- Consumes: the existing `GeminiExtractor`, `FieldExtractor`, prompt renderer, `PROMPT_VERSION = "v1"`, and extraction prompt without content changes.
- Produces: `app.pipeline.stage3_extract.base.FieldExtractor`, `app.pipeline.stage3_extract.gemini.GeminiExtractor`, and `app.pipeline.stage3_extract.prompts.PROMPT_VERSION`; Jev remains the only classifier.

- [ ] **Step 1: Record current import consumers before the mechanical move**

```bash
grep -RInE --include='*.py' 'stage2_classify\.gemini|stage2_classify\.prompts|FieldExtractor' backend/app backend/tests
```

Expected consumers are `factory.py`, `graph.py`, `stage3_extract/extract.py`, `api/runs.py`, `cli.py`, `intake/submission.py`, and `tests/test_gemini.py`; no Gemini classifier import is present.

- [ ] **Step 2: Move the implementation and prompt files unchanged**

```bash
cd backend
mkdir -p app/pipeline/stage3_extract/prompts
mv app/pipeline/stage2_classify/gemini.py app/pipeline/stage3_extract/gemini.py
mv app/pipeline/stage2_classify/prompts/__init__.py app/pipeline/stage3_extract/prompts/__init__.py
mv app/pipeline/stage2_classify/prompts/gemini_extract_v1.md app/pipeline/stage3_extract/prompts/gemini_extract_v1.md
cd ..
```

Expected: all four destination files exist, the old prompt source files are gone, and the extraction prompt still renders `<<FIELDS>>`, `<<RECEIVED_AT>>`, and `<<TICKET>>` exactly as before. Leave ignored `__pycache__` directories untouched.

Create `backend/app/pipeline/stage3_extract/base.py`:

```python
from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from app.pipeline.contracts import FieldPick, NormalizedTicket


class FieldExtractor(Protocol):
    async def extract(
        self, nt: NormalizedTicket, fields: Sequence[str]
    ) -> tuple[dict[str, FieldPick], float]: ...
```

Reduce `backend/app/pipeline/stage2_classify/base.py` to the classifier protocol:

```python
from __future__ import annotations

from typing import Protocol

from app.pipeline.contracts import Candidates, ClassifierOutput, NormalizedTicket


class Classifier(Protocol):
    async def classify(self, nt: NormalizedTicket, cands: Candidates) -> ClassifierOutput: ...
```

- [ ] **Step 3: Update every import to the Stage 3 owners**

Use these exact imports:

```python
# backend/app/pipeline/stage3_extract/extract.py
from app.pipeline.stage3_extract.base import FieldExtractor

# backend/app/pipeline/factory.py
from app.pipeline.stage3_extract.gemini import GeminiExtractor

# backend/app/pipeline/graph.py
from app.pipeline.stage2_classify.base import Classifier
from app.pipeline.stage3_extract.base import FieldExtractor

# backend/app/api/runs.py, backend/app/cli.py, backend/app/intake/submission.py
from app.pipeline.stage3_extract.prompts import PROMPT_VERSION

# backend/tests/test_gemini.py
from app.pipeline.stage3_extract.gemini import ExtractedSpan, GeminiExtractor, GeminiFields
```

Leave function bodies, prompt text, graph nodes, and extraction behavior unchanged.

- [ ] **Step 4: Run extraction and wiring tests, then reject stale imports**

```bash
cd backend
uv run pytest -q tests/test_gemini.py tests/test_extract.py tests/test_factory.py tests/test_graph.py tests/test_cli.py::test_run_batch_defaults_to_jev tests/intake/test_submission.py
uv run ruff check app/pipeline app/api/runs.py app/cli.py app/intake/submission.py tests/test_gemini.py
cd ..
grep -RInE --include='*.py' 'stage2_classify\.gemini|stage2_classify\.prompts' backend/app backend/tests || true
```

Expected: all focused tests and Ruff pass; the stale-import search prints no matches and graph tests still show no `gemini_classify` node.

- [ ] **Step 5: Review the mechanical move**

```bash
git diff --check -- backend/app/pipeline backend/app/api/runs.py backend/app/cli.py backend/app/intake/submission.py backend/tests/test_gemini.py
git diff --summary -- backend/app/pipeline backend/app/api/runs.py backend/app/cli.py backend/app/intake/submission.py backend/tests/test_gemini.py
```

Expected: only the approved moves and import changes appear; extraction behavior and Jev-only routing are unchanged.

### Task 4: Extract KB Database Call Mechanics Without Changing Transactions

**Files:**
- Create: `backend/app/kb/database.py`.
- Modify: `backend/app/kb/service.py`.
- Test: `backend/tests/test_kb_service.py`, `backend/tests/test_rag_api.py`.

**Interfaces:**
- Consumes: the complete current `_check_deadline`, `_abandoned`, `_consume`, and `_DatabaseCall` implementations in `kb/service.py`.
- Produces: private `app.kb.database._DatabaseCall` with unchanged methods, plus the same three helpers imported back into `KnowledgeService`; indexing, publication, retrieval, and cancellation orchestration signatures remain unchanged.

- [ ] **Step 1: Confirm the extraction block is private and self-contained**

```bash
grep -RInE --include='*.py' '_DatabaseCall|_check_deadline|_abandoned|_consume' backend/app backend/tests
sed -n '76,211p' backend/app/kb/service.py
```

Expected: all references are inside `kb/service.py`; the reviewed block ends immediately before `KnowledgeService` and contains no indexing or retrieval methods.

- [ ] **Step 2: Move the exact block with assertions rather than reimplementing concurrency code**

Run this deterministic extraction script from the repository root:

```bash
python - <<'PY'
from pathlib import Path

service_path = Path("backend/app/kb/service.py")
database_path = Path("backend/app/kb/database.py")
text = service_path.read_text(encoding="utf-8")
start = text.index("def _check_deadline")
end = text.index("\nclass KnowledgeService")
block = text[start:end].rstrip() + "\n"
assert "class _DatabaseCall:" in block
assert "def commit(self, dbapi_commit)" in block
assert "def abandon(self, loop)" in block

database_path.write_text(
    '"""Borrower-local database deadlines, cancellation, and commit handoff."""\n'
    "from math import ceil\n"
    "from threading import Event, Lock\n"
    "from time import monotonic\n\n\n"
    + block,
    encoding="utf-8",
)
text = text[:start] + text[end:]
text = text.replace("from math import ceil\n", "")
text = text.replace("from threading import Event, Lock\n", "")
needle = "from app.kb.documents import document_view\n"
assert needle in text
text = text.replace(
    needle,
    "from app.kb.database import _DatabaseCall, _abandoned, _check_deadline, _consume\n" + needle,
)
service_path.write_text(text, encoding="utf-8")
PY
```

Expected: `kb/database.py` contains the unchanged helper/class block; `KnowledgeService` and `_error_cost` remain in `service.py`; `monotonic` remains imported by `service.py` because its orchestration still uses it.

- [ ] **Step 3: Run all mandatory KB interleaving and commit-handoff tests**

```bash
cd backend
uv run pytest -q tests/test_kb_service.py
uv run pytest -q tests/test_rag_api.py
uv run ruff check app/kb/database.py app/kb/service.py
cd ..
```

Expected: every deadline, cancellation, publication, concurrent-index, and DBAPI commit-handoff test passes; no transaction semantics changed.

- [ ] **Step 4: Review the extraction diff and import boundary**

```bash
git diff --check -- backend/app/kb/database.py backend/app/kb/service.py
git diff -- backend/app/kb/database.py backend/app/kb/service.py
grep -RInE --include='*.py' '^class KnowledgeService|^class _DatabaseCall|^def _check_deadline' backend/app/kb/service.py backend/app/kb/database.py
```

Expected: `_DatabaseCall` and `_check_deadline` are defined only in `database.py`; `KnowledgeService` remains in `service.py`; the diff contains no query or orchestration rewrite.

### Task 5: Move Shared Text and Datetime Primitives to Neutral Modules

**Files:**
- Create: `backend/app/text.py`, `backend/app/datetime.py`.
- Modify: `backend/app/pipeline/stage1_normalize/normalize.py`, `backend/app/pipeline/stage1_normalize/candidates.py`, `backend/app/pipeline/stage1_normalize/dates.py`, `backend/app/pipeline/stage3_extract/gemini.py`, `backend/app/pipeline/stage4_lookup/lookup.py`, `backend/app/pipeline/stage6_draft/guardrails.py`, `backend/app/pipeline/stage6_draft/investigation.py`, `backend/app/intake/dates.py`, `backend/app/intake/sanitize.py`, `backend/app/ingest.py`, `backend/app/db/repository.py`, `backend/app/api/schemas.py`, `backend/tests/test_normalize.py`, `backend/tests/test_candidates.py`, `backend/tests/helpers.py`.
- Test: `backend/tests/test_normalize.py`, `backend/tests/test_candidates.py`, `backend/tests/test_lookup.py`, `backend/tests/test_ingest.py`, `backend/tests/intake/test_dates.py`, `backend/tests/test_workspace_api.py`.

**Interfaces:**
- Consumes: existing length-preserving digit/card functions and existing `parse_dt()`/Baghdad arithmetic.
- Produces: `app.text.to_ascii_digits(text: str) -> str`, `app.text.mask_cards(text: str) -> str`, `app.datetime.parse_dt(value: Any) -> datetime`, and `app.datetime.BAGHDAD`; Arabic folding, Arabizi detection, ticket normalization, and lookup matching stay in their stages.

- [ ] **Step 1: Create the neutral text module**

Create `backend/app/text.py`:

```python
"""Shared, length-preserving digit and sensitive-card normalization."""
from __future__ import annotations

import re

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
_CARD = re.compile(r"(?<![\w+])\d(?:[ -]?\d){12,18}(?!\w)")


def to_ascii_digits(text: str) -> str:
    """Arabic-Indic and Persian digits to ASCII. Length-preserving."""
    return text.translate(_DIGITS)


def mask_cards(text: str) -> str:
    """Replace all but the last 4 digits of card-like numbers with '*'. Length-preserving."""
    ascii_text = to_ascii_digits(text)
    chars = list(text)
    for match in _CARD.finditer(ascii_text):
        indexes = [i for i in range(match.start(), match.end()) if ascii_text[i].isdigit()]
        digits = "".join(ascii_text[i] for i in indexes)
        if digits.startswith(("964", "07")) and len(digits) <= 13:
            continue
        for index in indexes[:-4]:
            chars[index] = "*"
    return "".join(chars)
```

- [ ] **Step 2: Create the neutral datetime module**

Create `backend/app/datetime.py`:

```python
"""Shared datetime parsing and the pipeline's Baghdad timezone convention."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

BAGHDAD = timezone(timedelta(hours=3))


def parse_dt(value: Any) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(
        str(value).replace("Z", "+00:00")
    )
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=BAGHDAD)
```

This deliberately retains the existing fixed +03:00 convention; no date-resolution rules change.

- [ ] **Step 3: Rewire consumers and remove only the moved definitions**

In `stage1_normalize/normalize.py`, import `mask_cards` and `to_ascii_digits` from `app.text`, delete their local definitions plus `_DIGITS` and `_CARD`, and retain folding/detection/ticket functions. In `stage4_lookup/lookup.py`, import `BAGHDAD` and `parse_dt` from `app.datetime`, delete their local definitions, and remove the now-unused `timezone` import.

Apply these exact import replacements, asserting each old import exists first:

```bash
python - <<'PY'
from pathlib import Path

replacements = {
    "backend/app/pipeline/stage1_normalize/candidates.py": [(
        "from app.pipeline.stage1_normalize.normalize import to_ascii_digits",
        "from app.text import to_ascii_digits",
    )],
    "backend/app/pipeline/stage1_normalize/dates.py": [(
        "from app.pipeline.stage1_normalize.normalize import to_ascii_digits",
        "from app.text import to_ascii_digits",
    )],
    "backend/app/pipeline/stage3_extract/gemini.py": [(
        "from app.pipeline.stage1_normalize.normalize import to_ascii_digits",
        "from app.text import to_ascii_digits",
    )],
    "backend/app/pipeline/stage6_draft/investigation.py": [(
        "from app.pipeline.stage4_lookup.lookup import parse_dt",
        "from app.datetime import parse_dt",
    )],
    "backend/app/intake/sanitize.py": [(
        "from app.pipeline.stage1_normalize.normalize import mask_cards",
        "from app.text import mask_cards",
    )],
    "backend/app/ingest.py": [(
        "from app.pipeline.stage4_lookup.lookup import BAGHDAD, parse_dt",
        "from app.datetime import BAGHDAD, parse_dt",
    )],
    "backend/app/db/repository.py": [(
        "from app.pipeline.stage4_lookup.lookup import parse_dt",
        "from app.datetime import parse_dt",
    )],
    "backend/tests/test_candidates.py": [(
        "from app.pipeline.stage1_normalize.normalize import to_ascii_digits",
        "from app.text import to_ascii_digits",
    )],
}
for filename, edits in replacements.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in edits:
        assert old in text, (filename, old)
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
PY
```

In `guardrails.py`, use separate stage-specific and neutral imports:

```python
from app.pipeline.stage1_normalize.normalize import fold_arabic
from app.text import to_ascii_digits
```

In `intake/dates.py`, remove `ZoneInfo` and its local `BAGHDAD`, then use:

```python
from app.datetime import BAGHDAD
from app.text import to_ascii_digits
```

In `api/schemas.py`, add `from app.datetime import BAGHDAD` at module scope and replace the naive-date branch with:

```python
        if value.tzinfo is None:
            value = value.replace(tzinfo=BAGHDAD)
```

In `tests/test_normalize.py`, import `mask_cards` and `to_ascii_digits` from `app.text` while importing the other helpers from `stage1_normalize.normalize`. In `tests/helpers.py`, use:

```python
from datetime import datetime

from app.datetime import BAGHDAD
from app.pipeline.contracts import Ticket

RECEIVED = datetime(2026, 10, 7, 9, 30, tzinfo=BAGHDAD)
```

- [ ] **Step 4: Run behavior-preserving normalization, date, lookup, and API tests**

```bash
cd backend
uv run pytest -q tests/test_normalize.py tests/test_candidates.py tests/test_lookup.py tests/test_ingest.py tests/intake/test_dates.py tests/test_workspace_api.py tests/test_gemini.py tests/test_extract.py
uv run ruff check app tests/test_normalize.py tests/test_candidates.py tests/helpers.py
cd ..
```

Expected: all tests and Ruff pass; card masks remain length-preserving, naive datetimes still receive +03:00, and ticket lookup behavior is unchanged.

- [ ] **Step 5: Verify no consumer imports the moved primitives from stage modules**

```bash
grep -RInE --include='*.py' 'stage4_lookup\.lookup import BAGHDAD|stage4_lookup\.lookup import parse_dt|stage1_normalize\.normalize import .*to_ascii_digits|stage1_normalize\.normalize import .*mask_cards' backend/app backend/tests || true
git diff --check -- backend/app backend/tests/test_normalize.py backend/tests/test_candidates.py backend/tests/helpers.py
```

Expected: no stale primitive imports and no whitespace errors; only genuinely shared primitives moved.

### Task 6: Replace Review-Service Transport Dependencies with Domain Contracts

**Files:**
- Create: none.
- Modify: `backend/app/services/reviews.py`, `backend/app/api/results.py`.
- Test: `backend/tests/test_workspace_api.py`.

**Interfaces:**
- Consumes: validated API `ReviewInput`, taxonomy teams, and the existing locked `TicketResultRow` update transaction.
- Produces: `ReviewCommand(action, reviewer, final_text, team, expected_updated_at)`, `ReviewNotFound`, `ReviewConflict`, `InvalidReviewTeam`, and `record_review(session, result_id: int, review: ReviewCommand, teams)`; the API alone maps exceptions to existing 404/409/422 messages.

- [ ] **Step 1: Add HTTP characterization tests for every existing service error**

Add to `backend/tests/test_workspace_api.py`:

```python
def review_payload(result, **updates):
    payload = {
        "action": "approve",
        "reviewer": "Reviewer",
        "final_text": "هلا بيك، نراجع استفسارك.",
        "expected_updated_at": result["updated_at"],
    }
    payload.update(updates)
    return payload


def test_review_missing_stale_and_team_errors_keep_http_contract(client):
    missing = {
        "action": "approve", "reviewer": "Reviewer", "final_text": "رد",
        "expected_updated_at": datetime.now(UTC).isoformat(),
    }
    response = client.post("/api/results/99999/reviews", json=missing)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket result not found."

    start_run(client)
    result = client.get("/api/results").json()["items"][0]
    url = f"/api/results/{result['id']}/reviews"
    stale = review_payload(result, expected_updated_at="2000-01-01T00:00:00+00:00")
    response = client.post(url, json=stale)
    assert response.status_code == 409
    assert response.json()["detail"] == "This ticket was updated by another reviewer. Refresh before saving."

    invalid_team = review_payload(result, action="reassign", team="Not a team", final_text=None)
    response = client.post(url, json=invalid_team)
    assert response.status_code == 422
    assert response.json()["detail"] == "Select a valid support team."


@pytest.mark.parametrize("status,message", [
    ("processing", "This ticket is still processing."),
    ("failed", "Processing failed. Run the ticket again before reviewing it."),
])
def test_review_state_errors_keep_http_contract(client, status, message):
    from app.db.models import TicketResultRow

    start_run(client)
    result = client.get("/api/results").json()["items"][0]
    with client.app.state.session_factory.begin() as session:
        session.get(TicketResultRow, result["id"]).status = status
    current = client.get(f"/api/results/{result['id']}").json()
    response = client.post(f"/api/results/{result['id']}/reviews", json=review_payload(current))
    assert response.status_code == 409
    assert response.json()["detail"] == message
```

- [ ] **Step 2: Run characterization tests before refactoring**

```bash
cd backend && uv run pytest -q tests/test_workspace_api.py -k 'review_missing_stale_and_team_errors or review_state_errors or review_requires_text'
```

Expected: all characterization tests pass against the current HTTP contract.

- [ ] **Step 3: Introduce domain command/exceptions and map them only in the API**

Replace `backend/app/services/reviews.py` imports and error definitions with:

```python
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal

from sqlalchemy import select

from app.db.models import ReviewRow, TicketResultRow


@dataclass(frozen=True)
class ReviewCommand:
    action: Literal["approve", "edit_approve", "reject", "reassign"]
    reviewer: str
    final_text: str | None
    team: str | None
    expected_updated_at: datetime


class ReviewNotFound(LookupError):
    pass


class ReviewConflict(RuntimeError):
    pass


class InvalidReviewTeam(ValueError):
    pass
```

Keep the existing locked update body, changing only its signature and raises:

```python
def record_review(session, result_id: int, review: ReviewCommand, teams):
    result = session.scalar(
        select(TicketResultRow).where(TicketResultRow.id == result_id).with_for_update()
    )
    if result is None:
        raise ReviewNotFound("Ticket result not found.")
    if result.updated_at != review.expected_updated_at:
        raise ReviewConflict("This ticket was updated by another reviewer. Refresh before saving.")
    if result.status == "processing":
        raise ReviewConflict("This ticket is still processing.")
    if result.status == "failed":
        raise ReviewConflict("Processing failed. Run the ticket again before reviewing it.")
    final_text = (review.final_text or "").strip() or None
    if review.action == "reassign":
        if review.team not in teams:
            raise InvalidReviewTeam("Select a valid support team.")
        final_text = f"Assigned from {result.team} to {review.team}"
        result.team = review.team
    else:
        result.status = {
            "approve": "approved", "edit_approve": "edited", "reject": "rejected",
        }[review.action]
    session.add(ReviewRow(
        result_id=result.id, reviewer=review.reviewer, action=review.action,
        final_text=final_text, edit_distance=None,
    ))
    result.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(result)
    return result
```

In `backend/app/api/results.py`, import the domain types and replace the review endpoint with:

```python
from app.services.reviews import (
    InvalidReviewTeam,
    ReviewCommand,
    ReviewConflict,
    ReviewNotFound,
    record_review,
)
```

```python
@router.post("/{result_id}/reviews")
def review_result(result_id: int, review: ReviewInput, request: Request, session: SessionDep):
    try:
        result = record_review(
            session, result_id, ReviewCommand(**review.model_dump()), request.app.state.taxonomy.teams,
        )
    except ReviewNotFound as exc:
        raise HTTPException(404, str(exc)) from None
    except ReviewConflict as exc:
        raise HTTPException(409, str(exc)) from None
    except InvalidReviewTeam as exc:
        raise HTTPException(422, str(exc)) from None
    return result_view(session, result, detail=True)
```

- [ ] **Step 4: Re-run HTTP behavior and dependency checks**

```bash
cd backend
uv run pytest -q tests/test_workspace_api.py
uv run ruff check app/services/reviews.py app/api/results.py tests/test_workspace_api.py
cd ..
grep -RInE --include='*.py' 'fastapi|app\.api' backend/app/services/reviews.py || true
```

Expected: all HTTP statuses/messages and optimistic-concurrency tests pass; the service contains no FastAPI or API-schema dependency.

- [ ] **Step 5: Review the transport-boundary diff**

```bash
git diff --check -- backend/app/services/reviews.py backend/app/api/results.py backend/tests/test_workspace_api.py
git diff -- backend/app/services/reviews.py backend/app/api/results.py backend/tests/test_workspace_api.py
```

Expected: `with_for_update()`, commit/refresh ordering, original-draft retention, and every public error message remain unchanged.

### Task 7: Consolidate Attachment Row Projection

**Files:**
- Create: none.
- Modify: `backend/app/intake/repository.py`, `backend/app/intake/attachments.py`.
- Test: `backend/tests/intake/test_attachments.py`, `backend/tests/intake/test_repository.py`.

**Interfaces:**
- Consumes: `IntakeAttachmentRow` and the existing `Attachment` contract.
- Produces: `app.intake.repository.attachment_from_row(row: IntakeAttachmentRow) -> Attachment`, used by both `load_attachments()` and `AttachmentStore`; upload/read/remove signatures remain unchanged.

- [ ] **Step 1: Confirm the two projections are identical**

```bash
sed -n '89,100p' backend/app/intake/repository.py
sed -n '224,229p' backend/app/intake/attachments.py
grep -RInE --include='*.py' '_attachment\(|_public\(' backend/app/intake
```

Expected: both construct `Attachment` from the same eight row fields, and no external caller uses either private name.

- [ ] **Step 2: Expose one projection helper and use it in both locations**

In `backend/app/intake/repository.py`, rename `_attachment` to `attachment_from_row` without changing its body:

```python
def attachment_from_row(row: IntakeAttachmentRow) -> Attachment:
    return Attachment(
        id=row.id,
        filename=row.filename,
        mime_type=row.mime_type,
        size=row.size,
        width=row.width,
        height=row.height,
        message_id=row.message_id,
        removed=row.removed,
    )
```

Change `load_attachments()` to:

```python
    return [attachment_from_row(row) for row in rows]
```

In `backend/app/intake/attachments.py`, add `attachment_from_row` to the repository import, replace both `self._public(stored)` calls with `attachment_from_row(stored)`, and delete the static `_public` method. Do not change upload replay, removal, or file behavior.

- [ ] **Step 3: Run focused projection and attachment lifecycle tests**

```bash
cd backend
uv run pytest -q tests/intake/test_attachments.py tests/intake/test_repository.py tests/intake/test_api.py
uv run ruff check app/intake/repository.py app/intake/attachments.py
cd ..
grep -RInE --include='*.py' '_public\(|_attachment\(' backend/app/intake || true
```

Expected: all tests and Ruff pass; no private duplicate mapper remains.

- [ ] **Step 4: Review the mapper-only diff**

```bash
git diff --check -- backend/app/intake/repository.py backend/app/intake/attachments.py
git diff -- backend/app/intake/repository.py backend/app/intake/attachments.py
```

Expected: only projection naming/imports changed; no attachment persistence or revision logic changed.

### Task 8: Share API/CLI Schema Initialization and Cover Legacy Status Width

**Files:**
- Create: `backend/tests/test_db_initialization.py`.
- Modify: `backend/app/db/session.py`, `backend/app/main.py`, `backend/app/cli.py`.
- Test: `backend/tests/test_db_initialization.py`, `backend/tests/test_cli.py`, `backend/tests/test_rag_api.py`.

**Interfaces:**
- Consumes: `init_db(engine)`, `upgrade_workspace_schema(engine)`, API lifespan startup, and CLI `_sessionmaker()`.
- Produces: `initialize_database(engine: Engine) -> None`, called by both entry points; no migration framework or schema change beyond the existing 32-character upgrade.

- [ ] **Step 1: Write the failing two-entry-point legacy-schema integration test**

Create `backend/tests/test_db_initialization.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from typer.testing import CliRunner

from app import cli
from app.config import Settings
from app.db.session import make_engine, reset_db
from app.main import create_app


@pytest.mark.integration
@pytest.mark.parametrize("entrypoint", ["api", "cli"])
def test_entry_points_upgrade_legacy_run_status(entrypoint, monkeypatch, tmp_path):
    settings = Settings(
        _env_file=None,
        database_url=Settings(_env_file=None).test_database_url,
        openrouter_api_key="",
        typesafe_api_key="",
        intake_upload_dir=str(tmp_path),
    )
    assert make_url(settings.database_url).database == "support_test"
    engine = make_engine(settings.database_url)
    reset_db(engine)
    try:
        with engine.begin() as connection:
            run_id = connection.execute(text(
                "INSERT INTO runs (mode, prompt_version, model_ids, degraded, counts, "
                "total_cost_usd, status) VALUES ('jev', 'v1', CAST('{}' AS jsonb), false, "
                "CAST('{}' AS jsonb), 0, 'completed') RETURNING id"
            )).scalar_one()
            connection.execute(text("ALTER TABLE runs ALTER COLUMN status TYPE VARCHAR(16)"))

        if entrypoint == "cli":
            monkeypatch.setattr(cli, "get_settings", lambda: settings)
            result = CliRunner().invoke(cli.app, ["init-db"])
            assert result.exit_code == 0, result.output
        else:
            with TestClient(create_app(settings)) as client:
                assert client.get("/api/health").status_code == 200

        with engine.begin() as connection:
            length = connection.scalar(text(
                "SELECT character_maximum_length FROM information_schema.columns "
                "WHERE table_schema = current_schema() AND table_name = 'runs' "
                "AND column_name = 'status'"
            ))
            connection.execute(
                text("UPDATE runs SET status = 'completed_with_errors' WHERE id = :run_id"),
                {"run_id": run_id},
            )
            preserved = connection.execute(
                text("SELECT mode, status FROM runs WHERE id = :run_id"), {"run_id": run_id},
            ).one()
        assert length == 32
        assert preserved == ("jev", "completed_with_errors")
    finally:
        engine.dispose()
```

- [ ] **Step 2: Run the test before sharing initialization**

```bash
cd backend && uv run pytest -q tests/test_db_initialization.py
```

Expected: the API case passes and the CLI case fails because CLI initialization leaves the 16-character column unchanged.

- [ ] **Step 3: Add one initialization function and call it from both entry points**

In `backend/app/db/session.py`, add:

```python
def initialize_database(engine: Engine) -> None:
    from app.db.workspace_schema import upgrade_workspace_schema

    init_db(engine)
    upgrade_workspace_schema(engine)
```

In `backend/app/main.py`, import `initialize_database` instead of the two separate functions and replace startup initialization with:

```python
                engine = make_engine(settings.database_url)
                initialize_database(engine)
                app.state.session_factory = make_sessionmaker(engine)
```

In `backend/app/cli.py`, import `initialize_database` and change `_sessionmaker()` to:

```python
def _sessionmaker(settings: Settings):
    engine = make_engine(settings.database_url)
    initialize_database(engine)
    return make_sessionmaker(engine)
```

Keep `reset_db()` unchanged so test teardown/recreation behavior is unaffected.

- [ ] **Step 4: Verify both entry points and existing startup/CLI behavior**

```bash
cd backend
uv run pytest -q tests/test_db_initialization.py tests/test_rag_api.py::test_startup_recovers_even_with_injected_sessions tests/test_cli.py::test_run_batch_defaults_to_jev
uv run ruff check app/db/session.py app/main.py app/cli.py tests/test_db_initialization.py
cd ..
```

Expected: both legacy-schema cases pass, the existing row accepts `completed_with_errors`, and the selected startup/CLI tests pass. The complete CLI suite runs after the fixture repair in Task 9.

- [ ] **Step 5: Review initialization calls and diff**

```bash
grep -RInE --include='*.py' 'init_db\(|initialize_database\(|upgrade_workspace_schema\(' backend/app/main.py backend/app/cli.py backend/app/db/session.py
git diff --check -- backend/app/db/session.py backend/app/main.py backend/app/cli.py backend/tests/test_db_initialization.py
```

Expected: both entry points call `initialize_database`; only `reset_db()` continues to call plain `init_db()` for fresh test schemas.

### Task 9: Repair the Five-Record JSONL Baseline Fixture

**Files:**
- Create: none.
- Modify: `backend/tests/fixtures/sample_tickets.jsonl`.
- Test: `backend/tests/test_cli.py`, `backend/tests/test_ingest.py`.

**Interfaces:**
- Consumes: unchanged `load_jsonl()` requiring one complete JSON object per nonblank line.
- Produces: the same five ticket values (`S-001` through `S-005`) in valid JSONL; no parser changes.

- [ ] **Step 1: Add a direct fixture-contract check and reproduce the baseline failure**

```bash
cd backend
python - <<'PY'
import json
from pathlib import Path

path = Path("tests/fixtures/sample_tickets.jsonl")
records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(records) == 5
assert [record["external_id"] for record in records] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
PY
```

Expected: `json.decoder.JSONDecodeError` on the pretty-printed first record; do not broaden `load_jsonl()`.

- [ ] **Step 2: Replace the fixture with exactly five complete JSON lines**

Set `backend/tests/fixtures/sample_tickets.jsonl` to:

```jsonl
{"external_id":"S-001","text":"حولت ٥٠ الف لاخوي على رقم 07701234567 امس وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123","channel":"app","customer_phone":"07809876543","received_at":"2026-10-07T09:30:00+03:00"}
{"external_id":"S-002","text":"واحد اتصل بيه يكول انه موظف زين كاش وطلب الرمز اللي وصلني، انطيته وبعدها انسحب من حسابي 200 الف!! الحكوني","channel":"whatsapp","customer_phone":"07501112233","received_at":"2026-10-07T10:05:00+03:00"}
{"external_id":"S-003","text":"ma da ywselni el code mal ta2keed, ma agdar afta7 el 7isab","channel":"app","customer_phone":"07712223344","received_at":"2026-10-07T11:00:00+03:00"}
{"external_id":"S-004","text":"دفعت فاتورة الكهرباء 35,000 دينار يوم الخميس وطلعت ناجحة بس بعدها جاني اشعار انها ما مدفوعة","channel":"app","customer_phone":"07723334455","received_at":"2026-10-07T12:15:00+03:00"}
{"external_id":"S-005","text":"شكد عمولة التحويل لحساب بنكي؟","channel":"whatsapp","received_at":"2026-10-07T13:00:00+03:00"}
```

- [ ] **Step 3: Verify record fidelity and the repaired CLI baseline**

```bash
cd backend
python - <<'PY'
from app.ingest import load_jsonl, load_tickets

records = load_jsonl("tests/fixtures/sample_tickets.jsonl")
tickets = load_tickets("tests/fixtures/sample_tickets.jsonl")
assert len(records) == len(tickets) == 5
assert [ticket.external_id for ticket in tickets] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
assert tickets[0].customer_phone == "07809876543"
assert tickets[4].customer_phone is None
assert tickets[3].text.startswith("دفعت فاتورة الكهرباء 35,000")
PY
uv run pytest -q tests/test_cli.py tests/test_ingest.py
cd ..
```

Expected: direct assertions and all CLI/ingest tests pass; the three documented baseline failures are gone.

- [ ] **Step 4: Review that only fixture formatting changed**

```bash
git diff --check -- backend/tests/fixtures/sample_tickets.jsonl
git diff --word-diff=plain -- backend/tests/fixtures/sample_tickets.jsonl
```

Expected: five records and all original values remain; `backend/app/ingest.py` has no JSONL parser change beyond Task 5's neutral import.

### Task 10: Disable Paid Whole-Node Retry for Jev Classification

**Files:**
- Create: none.
- Modify: `backend/app/pipeline/graph.py`.
- Test: `backend/tests/test_graph.py`, `backend/tests/test_jev.py`.

**Interfaces:**
- Consumes: existing `JevClassifier.classify()`, LangGraph node failure propagation, and `run_batch()` per-ticket failure outcomes.
- Produces: `jev_classify` with `RetryPolicy(max_attempts=1)`; extraction retains the injected retry policy and drafting retains its existing no-retry policy.

- [ ] **Step 1: Add the failing main-success/order-failure regression fake and test**

Add to `backend/tests/test_graph.py`:

```python
async def test_failed_order_check_does_not_repeat_paid_sibling(tax):
    class OrderCheckFailsOnce(FakeJevRunnable):
        def __init__(self):
            super().__init__()
            self.main_attempts = 0
            self.order_attempts = 0

        async def ainvoke(self, request):
            if list(request["questions"]) == ["category"]:
                self.order_attempts += 1
                if self.order_attempts == 1:
                    raise httpx.ConnectError("order check unavailable")
            else:
                self.main_attempts += 1
            return await super().ainvoke(request)

    runnable = OrderCheckFailsOnce()
    jev = JevClassifier(
        runnable, tax, model_id="jev-1.13.0", t_jev=0.6,
        min_top_prob=0.6, price_in_per_m=0.042, max_state_chars=6000,
    )
    [outcome], _ = await _run(_deps(tax, jev=jev), [make_ticket("حوالة")], concurrency=1)
    assert outcome.status == "failed"
    assert "ConnectError" in outcome.error
    assert runnable.main_attempts == 1
    assert runnable.order_attempts == 1
```

- [ ] **Step 2: Verify the old whole-node retry repeats the paid sibling**

```bash
cd backend && uv run pytest -q tests/test_graph.py::test_failed_order_check_does_not_repeat_paid_sibling
```

Expected: FAIL because the order-check is retried, the main request is attempted twice, and the outcome no longer follows the asserted first-failure path.

- [ ] **Step 3: Disable retry only on the Jev node**

In `backend/app/pipeline/graph.py`, change one node registration:

```python
    b.add_node("jev_classify", n.jev_classify, retry_policy=RetryPolicy(max_attempts=1))
```

Do not add another retry layer or change `_Nodes.jev_classify`, extraction retry, batch exception handling, or model limits.

- [ ] **Step 4: Run focused graph/Jev tests**

```bash
cd backend
uv run pytest -q tests/test_graph.py tests/test_jev.py tests/test_factory.py
uv run ruff check app/pipeline/graph.py tests/test_graph.py
cd ..
```

Expected: all tests pass; the regression reports one main attempt, one order attempt, and a failed ticket isolated by `run_batch()`.

- [ ] **Step 5: Review the retry-only diff**

```bash
git diff --check -- backend/app/pipeline/graph.py backend/tests/test_graph.py
git diff -- backend/app/pipeline/graph.py backend/tests/test_graph.py
```

Expected: exactly the Jev node retry policy and its regression test changed.

### Task 11: Use Draft-Model-Specific Fallback Token Prices

**Files:**
- Create: none.
- Modify: `backend/app/config.py`, `backend/app/pipeline/stage6_draft/agent.py`.
- Test: `backend/tests/test_rag_drafter.py`, `backend/tests/test_config.py`, `backend/tests/test_draft_model.py`.

**Interfaces:**
- Consumes: `Settings.draft_model`, existing Gemini price fields, provider-reported response cost, and `_ModelUsage`.
- Produces: `price_anthropic_in/out` settings and `Settings.draft_token_prices -> tuple[float, float]`; `_ModelUsage` uses those prices only when provider cost is absent.

- [ ] **Step 1: Add failing Anthropic fallback and provider-precedence coverage**

Add to `backend/tests/test_rag_drafter.py`:

```python
@pytest.mark.parametrize("reported,expected", [(None, 0.0006), (0.0, 0.0), (0.25, 0.25)])
async def test_anthropic_fallback_prices_and_provider_cost_precedence(reported, expected):
    from uuid import uuid4

    from langchain_core.outputs import ChatGeneration, LLMResult

    from app.pipeline.stage6_draft.agent import _ModelUsage
    from app.pipeline.stage6_draft.context import DraftContext

    settings = Settings(
        _env_file=None, anthropic_model="anthropic/claude-sonnet-5.5",
    )
    ledger = _ModelUsage(DraftContext(draft_state()), settings)
    response = LLMResult(generations=[[ChatGeneration(message=answer(cost=reported))]])
    await ledger.on_llm_end(response, run_id=uuid4())
    assert ledger.cost_usd == pytest.approx(expected)
```

The fallback expectation is `(100 input × $3 + 20 output × $15) / 1,000,000 = 0.0006`; explicit zero and nonzero provider costs remain authoritative.

- [ ] **Step 2: Confirm Gemini prices are incorrectly used for Anthropic fallback**

```bash
cd backend && uv run pytest -q tests/test_rag_drafter.py::test_anthropic_fallback_prices_and_provider_cost_precedence
```

Expected: the missing-cost case fails with `0.00015` instead of `0.0006`; provider-cost cases pass.

- [ ] **Step 3: Add model-aware price selection**

In `backend/app/config.py`, add beside the existing Gemini prices:

```python
    # Fallback estimate for Anthropic drafting when OpenRouter omits cost.
    price_anthropic_in: float = Field(default=3.0, ge=0, allow_inf_nan=False)
    price_anthropic_out: float = Field(default=15.0, ge=0, allow_inf_nan=False)
```

Add this property beside `draft_model`:

```python
    @property
    def draft_token_prices(self) -> tuple[float, float]:
        if self.anthropic_model:
            return self.price_anthropic_in, self.price_anthropic_out
        return self.price_gemini_flash_in, self.price_gemini_flash_out
```

In `_ModelUsage._record_response` in `backend/app/pipeline/stage6_draft/agent.py`, replace the hard-coded pair with:

```python
        price_in, price_out = self.settings.draft_token_prices
        cost = (
            _number(usage.get("input_tokens")) * price_in
            + _number(usage.get("output_tokens")) * price_out
        ) / 1e6
```

Retain the existing provider-cost override unchanged.

- [ ] **Step 4: Run pricing, configuration, and real-provider response tests**

```bash
cd backend
uv run pytest -q tests/test_rag_drafter.py tests/test_config.py tests/test_draft_model.py tests/test_llm.py
uv run ruff check app/config.py app/pipeline/stage6_draft/agent.py tests/test_rag_drafter.py
cd ..
```

Expected: Anthropic fallback is `0.0006`, provider zero/nonzero costs take precedence, and all existing Gemini estimates remain unchanged.

- [ ] **Step 5: Review the pricing-only diff**

```bash
git diff --check -- backend/app/config.py backend/app/pipeline/stage6_draft/agent.py backend/tests/test_rag_drafter.py
git diff -- backend/app/config.py backend/app/pipeline/stage6_draft/agent.py backend/tests/test_rag_drafter.py
```

Expected: no model ID, request path, provider precedence, or execution limit changed.

### Task 12: Apply SQL Pagination and Skip Intake Projection for Result Lists

**Files:**
- Create: none.
- Modify: `backend/app/api/results.py`, `backend/app/services/workspace_queries.py`.
- Test: `backend/tests/test_workspace_api.py`.

**Interfaces:**
- Consumes: existing filtered `Select` query, `offset`/`limit` query parameters, `result_view(..., detail=False)`, and response shape `{"items": ..., "total": ...}`.
- Produces: a separate count query plus SQL `OFFSET`/`LIMIT`; `result_view()` queries intake only when `detail=True`; public filters, ordering, and response fields remain unchanged.

- [ ] **Step 1: Add pagination/filter/run-ID and statement-count regressions**

Add to `backend/tests/test_workspace_api.py`:

```python
def test_result_list_paginates_filters_and_run_id(client):
    first_run = start_run(client, [
        {"external_id": "needle-a", "text": "needle alpha"},
        {"external_id": "needle-b", "text": "needle beta"},
        {"external_id": "other", "text": "unrelated"},
    ])
    second_run = start_run(client, [{"external_id": "second-run", "text": "needle second"}])
    assert second_run != first_run
    query = (
        f"/api/results?run_id={first_run}&status=pending_review&team=General%20Care"
        "&category=general_inquiry&priority=P4&q=needle&offset=1&limit=1"
    )
    page = client.get(query).json()
    assert page["total"] == 2
    assert len(page["items"]) == 1
    assert page["items"][0]["run_id"] == first_run
    assert "needle" in page["items"][0]["ticket"]["text"]
    empty = client.get(query.replace("offset=1", "offset=99")).json()
    assert empty == {"items": [], "total": 2}


def test_result_list_uses_count_page_and_no_intake_query(client):
    from sqlalchemy import event

    start_run(client)
    engine = client.app.state.session_factory.kw["bind"]
    statements = []

    def observe(_conn, _cursor, statement, _parameters, _context, _many):
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", observe)
    try:
        response = client.get("/api/results?offset=0&limit=1")
        assert response.status_code == 200, response.text
    finally:
        event.remove(engine, "before_cursor_execute", observe)
    assert len([sql for sql in statements if "ticket_results" in sql]) == 2
    assert not [sql for sql in statements if "intake_submissions" in sql]
```

- [ ] **Step 2: Confirm the old list implementation fails the database-work regression**

```bash
cd backend && uv run pytest -q tests/test_workspace_api.py -k 'result_list_paginates_filters_and_run_id or result_list_uses_count_page_and_no_intake_query'
```

Expected: output pagination assertions pass, but the statement-count test fails because there is no separate count query and intake projection is queried for a list.

- [ ] **Step 3: Move count/page work into SQL and gate intake projection on detail**

In `backend/app/api/results.py`, import `func` and replace the end of `list_results()` with:

```python
from sqlalchemy import func, select
```

```python
    total = session.scalar(
        select(func.count()).select_from(query.order_by(None).subquery())
    ) or 0
    rows = session.scalars(
        query.order_by(TicketResultRow.priority.asc().nullslast(), TicketResultRow.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return {"items": [result_view(session, row) for row in rows], "total": total}
```

In `backend/app/services/workspace_queries.py`, replace the projection tail with:

```python
    if detail:
        value.update(draft_evidence(result.agent_trace, result.citations))
        value["reviews"] = [columns(review) for review in session.scalars(
            select(ReviewRow).where(ReviewRow.result_id == result.id).order_by(ReviewRow.id.desc())
        )]
        txn = session.get(TransactionRow, result.matched_txn_ref) if result.matched_txn_ref else None
        value["transaction"] = columns(txn) if txn else None
        intake = intake_result_view(session, result.ticket_id)
        if intake is not None:
            for attachment in intake["attachments"]:
                attachment["download_url"] = (
                    f"/api/results/{result.id}/intake/attachments/{attachment['id']}"
                )
        value["intake"] = intake
    else:
        value["intake"] = None
    return value
```

Remove the old unconditional `intake_result_view()` call; do not alter ticket/approval projection or the detail attachment URLs.

- [ ] **Step 4: Run result-list, detail, review, and intake-evidence tests**

```bash
cd backend
uv run pytest -q tests/test_workspace_api.py tests/test_rag_api.py -k 'result or review or persisted_actual_trace or intake'
uv run ruff check app/api/results.py app/services/workspace_queries.py tests/test_workspace_api.py
cd ..
```

Expected: SQL count/page behavior, filters, run-ID selection, empty pages, detail intake evidence, and statement-count assertions all pass.

- [ ] **Step 5: Review the query-only diff**

```bash
git diff --check -- backend/app/api/results.py backend/app/services/workspace_queries.py backend/tests/test_workspace_api.py
git diff -- backend/app/api/results.py backend/app/services/workspace_queries.py backend/tests/test_workspace_api.py
```

Expected: no unrelated N+1 optimization, response-shape change, or intake detail behavior change.

### Task 13: Finish Physical Unlink on Completed Attachment-Removal Replay

**Files:**
- Create: none.
- Modify: `backend/app/intake/attachments.py`.
- Test: `backend/tests/intake/test_attachments.py`.

**Interfaces:**
- Consumes: existing operation fingerprint/idempotency checks, `IntakeAttachmentRow.storage_key`, `Path.unlink(missing_ok=True)`, and session revision rules.
- Produces: completed removal replay that performs the same physical unlink before returning, without changing revision or creating an operation.

- [ ] **Step 1: Add the failing first-unlink-failure/replay test**

Add to `backend/tests/intake/test_attachments.py`:

```python
def test_remove_replays_physical_unlink_without_revision_change(store, repo, tmp_path, monkeypatch):
    from pathlib import Path

    from app.intake.db_models import IntakeOperationRow

    owner, view = repo.create("ar")
    attachment, view = store.upload(owner, uuid4(), view.revision, "shot.png", png_bytes())
    request_id = uuid4()
    original_unlink = Path.unlink
    attempts = 0

    def fail_first_unlink(path, missing_ok=False):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OSError("simulated unlink failure")
        return original_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", fail_first_unlink)
    with pytest.raises(OSError, match="simulated unlink failure"):
        store.remove(owner, attachment.id, request_id, view.revision)

    after_failure = repo.get(owner)
    assert after_failure.revision == view.revision + 1
    assert after_failure.attachments[0].removed is True
    replayed = store.remove(owner, attachment.id, request_id, after_failure.revision)
    assert replayed.revision == after_failure.revision
    assert attempts == 2
    assert not list(tmp_path.rglob("*.png"))

    with store._sf() as session:
        from sqlalchemy import func, select
        count = session.scalar(select(func.count()).select_from(IntakeOperationRow).where(
            IntakeOperationRow.request_id == request_id
        ))
    assert count == 1
```

- [ ] **Step 2: Verify the existing replay leaves the file behind**

```bash
cd backend && uv run pytest -q tests/intake/test_attachments.py::test_remove_replays_physical_unlink_without_revision_change
```

Expected: FAIL because replay returns without a second unlink attempt and the PNG remains.

- [ ] **Step 3: Route replay through the same post-commit unlink path**

In `AttachmentStore.remove()`, replace the early replay return and the post-session return with this structure:

```python
            if existing is not None:
                assert_same_operation(existing.fingerprint, fingerprint)
                attachment = session.get(IntakeAttachmentRow, attachment_id)
                if attachment is not None and attachment.session_id == row.id:
                    path = self.root / attachment.storage_key
                view = session_view(session, row)
            else:
                self._ensure_mutable(row, expected_revision)
                attachment = session.get(IntakeAttachmentRow, attachment_id)
                if attachment is None or attachment.session_id != row.id:
                    raise NotOwned("Conversation not found.")
                now = datetime.now(UTC)
                session.add(IntakeOperationRow(
                    id=uuid.uuid4(), session_id=row.id, request_id=request_id, kind="remove",
                    fingerprint=fingerprint, status="completed", attempt_id=uuid.uuid4(),
                    claimed_revision=row.revision + 1,
                    request_json={"attachment_id": str(attachment_id)},
                    result_json={"removed": True}, error_code=None, usage=[],
                    created_at=now, updated_at=now,
                ))
                attachment.removed = True
                state = remove_attachment_evidence(IntakeState.model_validate(row.state), attachment_id)
                row.state = state.model_dump(mode="json")
                row.review = None
                row.phase = "collecting" if row.phase != "submitted" else row.phase
                row.revision += 1
                row.updated_at = now
                path = self.root / attachment.storage_key
                session.commit()
                view = session_view(session, row)
        if path is not None:
            path.unlink(missing_ok=True)
        return view
```

The existing fingerprint check still runs first; the replay branch performs no revision mutation or commit.

- [ ] **Step 4: Run attachment and idempotency tests**

```bash
cd backend
uv run pytest -q tests/intake/test_attachments.py tests/intake/test_api.py tests/intake/test_recovery_regressions.py
uv run ruff check app/intake/attachments.py tests/intake/test_attachments.py
cd ..
```

Expected: the first failure remains visible to the caller, successful replay removes the file, revision/operation counts stay unchanged, and all existing idempotency tests pass.

- [ ] **Step 5: Review the replay-only diff**

```bash
git diff --check -- backend/app/intake/attachments.py backend/tests/intake/test_attachments.py
git diff -- backend/app/intake/attachments.py backend/tests/intake/test_attachments.py
```

Expected: only completed-removal replay control flow and its regression test changed; no upload or submission behavior changed.

### Task 14: Preserve Safe Knowledge 503s and Log Only Unexpected Diagnostic Types

**Files:**
- Create: none.
- Modify: `backend/app/api/knowledge.py`.
- Test: `backend/tests/test_rag_api.py`.

**Interfaces:**
- Consumes: `EmbeddingError`, `KnowledgeError`, `KnowledgeExecutionError`, `TimeoutError`, and the existing public 503 detail.
- Produces: explicit expected-failure handling plus warning logs containing only safe exception type names for unexpected faults; response status/messages and cancellation behavior remain unchanged.

- [ ] **Step 1: Add expected-failure contract tests and failing unexpected-diagnostic coverage**

Add these module-level imports to `backend/tests/test_rag_api.py`:

```python
from app.kb.embeddings import EmbeddingError
from app.kb.service import KnowledgeError, KnowledgeExecutionError
```

Then add the tests:

```python
@pytest.mark.parametrize("error", [
    EmbeddingError("PRIVATE-provider-secret"),
    KnowledgeError("PRIVATE-provider-secret"),
    TimeoutError("PRIVATE-provider-secret"),
])
def test_search_expected_failures_keep_safe_503(client, monkeypatch, error):
    async def fail_search(*args, **kwargs):
        raise error

    monkeypatch.setattr(client.app.state.knowledge, "search", fail_search)
    response = client.post("/api/knowledge/search", json={"query": "policy"})
    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Knowledge search unavailable; check the provider and index, then retry."
    )
    assert "PRIVATE-provider-secret" not in response.text


def test_search_unexpected_fault_logs_only_safe_type(client, monkeypatch, caplog):
    async def fail_search(*args, **kwargs):
        raise KnowledgeExecutionError(RuntimeError("PRIVATE-provider-secret"))

    monkeypatch.setattr(client.app.state.knowledge, "search", fail_search)
    with caplog.at_level("WARNING", logger="app.api.knowledge"):
        response = client.post("/api/knowledge/search", json={"query": "policy"})
    assert response.status_code == 503
    assert "PRIVATE-provider-secret" not in response.text
    assert "RuntimeError" in caplog.text
    assert "PRIVATE-provider-secret" not in caplog.text
```

- [ ] **Step 2: Verify the missing diagnostic behavior**

```bash
cd backend && uv run pytest -q tests/test_rag_api.py -k 'search_expected_failures_keep_safe_503 or search_unexpected_fault_logs_only_safe_type'
```

Expected: safe 503 assertions pass, but the unexpected-fault test fails because no safe `RuntimeError` diagnostic is logged.

- [ ] **Step 3: Catch expected failures explicitly and sanitize unexpected logs**

In `backend/app/api/knowledge.py`, add `logging`, import `EmbeddingError`, and extend the existing `DocumentNotFoundError` service import rather than duplicating it:

```python
import logging

from app.kb.embeddings import EmbeddingError
from app.kb.service import DocumentNotFoundError, KnowledgeError, KnowledgeExecutionError

logger = logging.getLogger(__name__)
```

Replace only the search exception handler with:

```python
    except (EmbeddingError, KnowledgeError, TimeoutError):
        raise HTTPException(
            503, "Knowledge search unavailable; check the provider and index, then retry.",
        ) from None
    except Exception as exc:
        diagnostic_type = (
            exc.diagnostic_type if isinstance(exc, KnowledgeExecutionError) else type(exc).__name__
        )
        logger.warning("Knowledge search failed with %s", diagnostic_type)
        raise HTTPException(
            503, "Knowledge search unavailable; check the provider and index, then retry.",
        ) from None
```

Do not log exception strings, request queries, API keys, or tracebacks, and do not catch `asyncio.CancelledError`.

- [ ] **Step 4: Run knowledge diagnostics and lifecycle tests**

```bash
cd backend
uv run pytest -q tests/test_rag_api.py tests/test_kb_service.py tests/test_embeddings.py
uv run ruff check app/api/knowledge.py tests/test_rag_api.py
cd ..
```

Expected: all expected failures retain the same safe 503, unexpected logs contain only `RuntimeError`, and all KB lifecycle tests pass.

- [ ] **Step 5: Review diagnostics for accidental secret propagation**

```bash
git diff --check -- backend/app/api/knowledge.py backend/tests/test_rag_api.py
git diff -- backend/app/api/knowledge.py backend/tests/test_rag_api.py
grep -RInE --include='*.py' 'logger\.(warning|error|exception).*exc|str\(exc\)' backend/app/api/knowledge.py || true
```

Expected: no exception-text logging and no public-response change.

### Task 15: Run Complete Backend Verification and Review the Final Diff

**Files:**
- Create: none.
- Modify: none; return to the owning task if verification exposes a defect.
- Test: the complete `backend/tests` suite and Ruff over `backend/app` plus `backend/tests`.

**Interfaces:**
- Consumes: every interface produced by Tasks 1–14.
- Produces: a verified backend tree with no known baseline failures and only approved changes.

- [ ] **Step 1: Run focused acceptance coverage across all required defect areas**

```bash
cd backend
uv run pytest -q \
  tests/test_graph.py::test_failed_order_check_does_not_repeat_paid_sibling \
  tests/test_rag_drafter.py::test_anthropic_fallback_prices_and_provider_cost_precedence \
  tests/test_gemini.py tests/test_factory.py tests/test_kb_service.py \
  tests/test_workspace_api.py tests/intake/test_attachments.py \
  tests/test_db_initialization.py tests/test_rag_api.py tests/test_cli.py
cd ..
```

Expected: all focused acceptance tests pass, including Jev retries, draft pricing, extraction/factory wiring, KB interleavings, result pagination, attachment replay, API/CLI schema initialization, review HTTP behavior, and knowledge-search diagnostics.

- [ ] **Step 2: Run the complete backend acceptance matrix**

```bash
cd backend
uv run pytest -q
uv run ruff check app tests
cd ..
```

Expected: zero test failures and Ruff success. The original 761-test repaired baseline plus all newly added regression tests pass; no JSONL failures remain.

- [ ] **Step 3: Verify cleanup and interface consistency with reference searches**

```bash
grep -RInE --include='*.py' 'stage2_classify\.gemini|stage2_classify\.prompts|gemini_strong_model|gemini_embed_model|price_gemini_pro_in|price_gemini_pro_out|current_session_view|service\.submission' backend/app backend/tests || true
grep -RInE --include='*.py' 'fastapi|app\.api' backend/app/services/reviews.py || true
grep -RInE --include='*.py' 'classifier_disagreement' backend/app/pipeline/stage6_draft/tools.py backend/app/pipeline/stage5_decide/rules.py
```

Expected: the first two searches print no matches; the final search shows legacy text in `rules.py` only, not current drafting-tool validation.

- [ ] **Step 4: Perform the final status/diff review without git mutations**

```bash
git diff --check
git status --short
git diff --stat
git diff -- backend/app backend/tests
```

Expected: only the approved backend source/test changes, fixture repair, and this plan are new. The user's pre-existing root `README.md` modification remains untouched; historical records, Graphify snapshots, demo data, public compatibility fields, and unrelated user changes are absent from the backend diff. No commits, staging, resets, or other git mutations are performed.
