# Plan 1 — Core Pipeline (LangGraph batch pipeline + CLI): Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working command-line batch pipeline. It reads Iraqi-dialect tickets from JSONL, JSON or CSV, then for each ticket:

1. normalizes the text,
2. classifies it (with Jev, Gemini, or a cascade of the two),
3. extracts the transaction details without inventing values,
4. matches them against mock transactions,
5. applies the routing and escalation rules,
6. persists the results and run summary to Postgres.

**Architecture:**
- **Graph.** A LangGraph `StateGraph` with one node per stage: prepare, jev_classify, gemini_classify, extract, lookup, decide, draft.
- **Routing.** Plain, unit-tested Python functions decide which node runs next.
- **Models.** Jev is reached through `langchain-typesafe`; Gemini through `langchain-google-genai` structured output. Each sits behind its own small protocol, so tests use fakes.
- **Drafting.** Drafting is a `Drafter` protocol. This plan ships `NullDrafter`; Plan 3 replaces it.

**Tech Stack:**

| Area | Tools |
|---|---|
| Language and tooling | Python 3.12 (WSL), uv |
| LangChain | langchain ≥1.0, langgraph ≥1.0, langchain-google-genai, langchain-typesafe 0.0.1a3 |
| Data and storage | pydantic v2, SQLAlchemy 2, psycopg 3, pgvector, Postgres 16 (Docker in WSL) |
| CLI and tests | typer, pytest, pytest-asyncio, ruff |

**Spec:** `docs/superpowers/specs/2026-10-07-support-pipeline-design.md`. Read §4–§6 and §14 before starting.

**This plan is 1 of 5:**

| Plan | Scope |
|---|---|
| **1** | Core pipeline and CLI (this plan) |
| 2 | Synthetic data and the evaluation harness |
| 3 | Knowledge-base RAG, the drafting agent and guardrails |
| 4 | FastAPI and the React review UI |
| 5 | Weekly report, docs, CI and the full docker-compose stack |

## Global Constraints

- **Python:** `requires-python = ">=3.11"`. Develop on Python 3.12 in WSL Ubuntu-24.04.
- **LangChain packages:**
  - `langchain>=1.0,<2.0`
  - `langchain-core>=1.6.2,<2.0`
  - `langgraph>=1.0,<2.0`
  - `langchain-typesafe==0.0.1a3` (alpha, so pinned)
  - `langchain-google-genai>=2.1`
- **Pinned models:**
  - Jev: `JEV_MODEL=jev-1.13.0`. Never use `jev-latest`; thresholds are tuned against a specific version.
  - Gemini: `gemini-2.5-flash` for the pipeline.
- **Threshold defaults:** `T_JEV=0.6`, `T_GEM=0.66`, `JEV_MIN_TOP_PROB=0.60`, `PIPELINE_CONCURRENCY=20`, `MAX_STATE_CHARS=6000`.
- **Never invent a value.** An extracted field is either a substring that occurs in the ticket text (after converting digits) or `null`.
- **Nothing is sent.** No code path sends a message to a customer.
- **Card numbers are masked before storage.** Only the last 4 digits are kept.
- **Git stays local.** Commit after every task. Never push, and do not change git config.
- **Shell:** every command below runs inside WSL in `~/dev/zaincash-support` (the repo root) or in `~/dev/zaincash-support/backend` as stated.

## Review Focus

1. **Arabic-Indic digits next to a phone number.** In `"حولت ٥٠ الف لرقم 0770 123 4567"` the amount candidate must be `50 الف`, and no fragment of the phone number may become an amount. Spans must index correctly into the original text. *Test:* `test_candidates.py::test_arabic_indic_amount_not_confused_with_phone`
2. **Empty or whitespace-only ticket.** It is escalated with reason `empty_ticket` and no model is called. A ticket longer than `MAX_STATE_CHARS` is truncated before it is sent to Jev. *Tests:* `test_graph.py::test_empty_ticket_escalates_without_model_calls` and `test_jev.py::test_state_is_truncated`
3. **A model returns a category that isn't in the taxonomy.** It maps to `other` and is marked uncertain; it is never trusted. *Tests:* `test_jev.py::test_unknown_category_is_other_and_uncertain` and `test_gemini.py::test_invalid_categories_do_not_vote`
4. **The same batch is run twice, or a file repeats an `external_id`.** No duplicate ticket rows and no duplicate result rows. *Tests:* `test_ingest.py::test_duplicate_external_ids_keep_first` and `test_repository.py::test_rerun_is_idempotent`
5. **A CSV exported from Excel.** It has a UTF-8 BOM, Arabic text, and no `channel` or `received_at` columns. It must load with defaults (`app`, the current time in Baghdad). *Test:* `test_ingest.py::test_csv_with_bom_and_missing_columns`

## File Structure

```
.gitignore  .env.example  docker-compose.yml  docker/db/init.sql
data/taxonomy.yaml                       # categories, teams, priorities (single source of truth)
backend/pyproject.toml
backend/app/
  config.py                              # Settings (pydantic-settings), REPO_ROOT
  taxonomy.py                            # Category/Taxonomy, load_taxonomy, priority helpers
  llm.py                                 # StructuredLLM protocol, Sample, LLMUnavailable, GeminiStructuredLLM
  ingest.py                              # load_tickets (jsonl/json/csv), load_jsonl
  cli.py                                 # typer app: init-db, seed-db, run-batch
  db/models.py  db/session.py  db/repository.py
  pipeline/
    contracts.py                         # dataclasses shared by every stage
    state.py                             # PipelineState TypedDict
    normalize.py  candidates.py  dates.py
    classify/base.py  classify/jev.py  classify/gemini.py  classify/cascade.py
    extract.py  lookup.py  rules.py  drafting.py
    graph.py                             # PipelineDeps, build_graph, run_batch, summarize
    serialize.py                         # outcome -> JSON-safe dict
    factory.py                           # build_pipeline(settings, mode, repo)
    prompts/__init__.py  prompts/gemini_classify_v1.md  prompts/gemini_extract_v1.md
backend/tests/
  __init__.py  helpers.py  fakes.py  fixtures/*.jsonl  test_*.py
```

---

### Task 0: Move the repo into WSL and verify the toolchain

No code yet. This task sets up the environment every later task depends on.

- [ ] **Step 1: Clone the repo into WSL.** Run this from Windows PowerShell. The clone keeps every local commit and leaves out the old untracked chatbot code.

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "mkdir -p ~/dev && git clone '/mnt/c/Users/CVZMH/OneDrive - Covestro/Dokumente/Dev/ZainCash-customer support' ~/dev/zaincash-support && cd ~/dev/zaincash-support && git remote remove origin && git log --oneline"
```

Expected: the existing commits are listed, and `git remote -v` prints nothing.

- [ ] **Step 2: Install uv inside WSL.**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.local/bin/env && uv --version
```

If the corporate proxy breaks the curl download, use `sudo apt-get install -y pipx && pipx install uv` instead.

- [ ] **Step 3: Check that Docker works in WSL.**

```bash
docker run --rm hello-world
```

Expected: `Hello from Docker!`. If you get a permission error, run `sudo usermod -aG docker $USER`, then run `wsl --shutdown` from PowerShell and reopen WSL.

---

### Task 1: Backend scaffold and settings

**Files:**
- Create: `.gitignore`, `.env.example`, `backend/pyproject.toml`
- Create: `backend/app/__init__.py`, `backend/app/config.py`
- Test: `backend/tests/__init__.py`, `backend/tests/test_config.py`

**Interfaces:**
- Produces:
  - `app.config.REPO_ROOT: Path`
  - `app.config.Settings` (fields listed below)
  - `app.config.get_settings() -> Settings`

- [ ] **Step 1: Write the repo files**

`.gitignore`:
```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.env
.env.*
!.env.example
node_modules/
dist/
*.log
out/
```

`.env.example`:
```dotenv
GOOGLE_API_KEY=
TYPESAFE_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
GEMINI_STRONG_MODEL=gemini-2.5-pro
GEMINI_EMBED_MODEL=gemini-embedding-001
EMBED_DIM=768
JEV_MODEL=jev-1.13.0
T_JEV=0.6
T_GEM=0.66
JEV_MIN_TOP_PROB=0.60
PIPELINE_CONCURRENCY=20
MAX_STATE_CHARS=6000
AGENT_MAX_TOOL_CALLS=6
AGENT_TIMEOUT_S=30
DATABASE_URL=postgresql+psycopg://support:support@localhost:5432/support
TEST_DATABASE_URL=postgresql+psycopg://support:support@localhost:5432/support_test
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
```

`backend/pyproject.toml`:
```toml
[project]
name = "zaincash-support"
version = "0.1.0"
description = "Topic 06 support pipeline: classify, extract, route and pre-draft Iraqi-dialect tickets"
requires-python = ">=3.11"
dependencies = [
  "langchain>=1.0,<2.0",
  "langchain-core>=1.6.2,<2.0",
  "langgraph>=1.0,<2.0",
  "langchain-google-genai>=2.1",
  "langchain-typesafe==0.0.1a3",
  "pydantic>=2.7",
  "pydantic-settings>=2.3",
  "pyyaml>=6.0",
  "sqlalchemy>=2.0.30",
  "psycopg[binary]>=3.1",
  "typer>=0.12",
]

[project.scripts]
support = "app.cli:app"

[dependency-groups]
dev = ["pytest>=8", "pytest-asyncio>=0.24", "ruff>=0.6"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["."]
markers = ["integration: needs Postgres from `docker compose up -d db`"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["E501"]  # long Arabic literals and prompts; formatting is not a review gate

[tool.ruff.lint.flake8-bugbear]
extend-immutable-calls = ["typer.Option", "typer.Argument"]
```

`backend/app/__init__.py` and `backend/tests/__init__.py` are both empty files.

- [ ] **Step 2: Write the failing test**

`backend/tests/test_config.py`:
```python
from app.config import REPO_ROOT, Settings


def test_repo_root_is_project_root():
    assert (REPO_ROOT / "backend" / "app").is_dir()


def test_defaults():
    s = Settings(_env_file=None)
    assert s.taxonomy_path == str(REPO_ROOT / "data" / "taxonomy.yaml")
    assert s.jev_model == "jev-1.13.0"
    assert s.t_gem == 0.66
    assert s.pipeline_concurrency == 20


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("T_JEV", "0.75")
    monkeypatch.setenv("PIPELINE_CONCURRENCY", "5")
    s = Settings(_env_file=None)
    assert s.t_jev == 0.75
    assert s.pipeline_concurrency == 5
```

- [ ] **Step 3: Install and confirm the test fails**

Run: `cd backend && uv sync && uv run pytest tests/test_config.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'app.config'`.

- [ ] **Step 4: Implement `backend/app/config.py`**

```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """All runtime configuration. Environment variable names are the upper-cased field names."""

    model_config = SettingsConfigDict(env_file=str(REPO_ROOT / ".env"), extra="ignore")

    google_api_key: str = ""
    typesafe_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_strong_model: str = "gemini-2.5-pro"
    gemini_embed_model: str = "gemini-embedding-001"
    embed_dim: int = 768
    jev_model: str = "jev-1.13.0"

    t_jev: float = 0.6
    t_gem: float = 0.66
    jev_min_top_prob: float = 0.60
    pipeline_concurrency: int = 20
    max_state_chars: int = 6000
    agent_max_tool_calls: int = 6
    agent_timeout_s: int = 30

    database_url: str = "postgresql+psycopg://support:support@localhost:5432/support"
    test_database_url: str = "postgresql+psycopg://support:support@localhost:5432/support_test"
    taxonomy_path: str = str(REPO_ROOT / "data" / "taxonomy.yaml")

    # USD per 1M tokens. Check current pricing before reporting costs.
    price_gemini_flash_in: float = 0.30
    price_gemini_flash_out: float = 2.50
    price_gemini_pro_in: float = 1.25
    price_gemini_pro_out: float = 10.0
    price_jev_in: float = 0.042


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 5: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_config.py -v`

Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
cd .. && git add .gitignore .env.example backend && git commit -m "feat(backend): scaffold uv project and settings"
```

---

### Task 2: Taxonomy

**Files:**
- Create: `data/taxonomy.yaml`, `backend/app/taxonomy.py`
- Test: `backend/tests/test_taxonomy.py`

**Interfaces:**
- Produces:
  - `FIELD_NAMES = ("txn_ref", "amount", "phone", "date")`
  - `PRIORITIES = ("P1", "P2", "P3", "P4")`
  - `Category`, a frozen dataclass with fields `id`, `team`, `what_en`, `what_ar`, `not_for`, `examples: tuple[str, ...]`, `required_fields: tuple[str, ...]`, `min_priority`, `needs_transaction: bool`, and the method `.describe() -> str`
  - `Taxonomy`, with `teams: tuple[str, ...]`, `categories: dict[str, Category]`, `.ids`, `.get(id) -> Category` (an unknown id returns `other`), and `.render() -> str`
  - `load_taxonomy(path) -> Taxonomy`
  - `TaxonomyError`
  - `priority_rank(p) -> int`
  - `most_urgent(*ps) -> str`

- [ ] **Step 1: Write `data/taxonomy.yaml`**

```yaml
# Single source of truth for categories, teams and priorities (spec §4).
# Priorities: P1 money at risk now / fraud, P2 money lost or stuck, P3 service blocked, P4 information.
teams:
  - Payments Ops
  - Disputes
  - Account & Security
  - Agent Network
  - Cards
  - Tech Support
  - General Care

categories:
  - id: failed_transfer
    team: Payments Ops
    what_en: A transfer the customer sent failed, is stuck or pending, or left the wallet but did not arrive
    what_ar: تحويل فشل أو معلّق أو انقطع من الرصيد وما وصل
    not_for: Money sent to the wrong number on purpose by mistake (wrong_recipient); bill payments (bill_payment)
    examples:
      - حولت فلوس لاخوي من الصبح وبعده ما وصله شي والفلوس انقصت من حسابي
      - التحويل طلعلي فشل بس الرصيد نازل 50 الف
      - hawalit 25 alf w ma wislat
    required_fields: [amount, date]
    min_priority: P2
    needs_transaction: true

  - id: wrong_recipient
    team: Disputes
    what_en: The customer sent money to the wrong number or person by mistake and wants it back
    what_ar: تحويل لرقم غلط أو شخص غلط بالغلط ويريد يرجع الفلوس
    not_for: A transfer that failed technically (failed_transfer)
    examples:
      - غلطت برقم واحد وحولت 100 الف لغير شخص اريد ارجعهن
      - دزيت الفلوس على رقم غلط شلون ارجعها
    required_fields: [amount]
    min_priority: P2
    needs_transaction: true

  - id: login_access
    team: Account & Security
    what_en: Cannot log in, forgot PIN or password, verification code not arriving, account locked
    what_ar: ما يكدر يدخل للحساب، نسى الرمز، رمز التحقق ما يوصل، الحساب مقفول
    not_for: Someone else accessed the account or stole money (fraud_report)
    examples:
      - ما دا يوصلني رمز التحقق حتى افتح الحساب
      - نسيت الرمز السري وانقفل الحساب
      - ma da ywselni el code mal ta2keed
    required_fields: []
    min_priority: P3
    needs_transaction: false

  - id: agent_dispute
    team: Agent Network
    what_en: Problem with a ZainCash agent or shop - cash-in or cash-out not credited, extra fee charged, service refused
    what_ar: مشكلة مع وكيل زين كاش - شحن أو سحب ما نزل، عمولة زايدة، رفض الخدمة
    not_for: Problems inside the app with no agent involved
    examples:
      - رحت للوكيل وانطيته 200 الف يشحن حسابي وما نزلت
      - الوكيل اخذ مني عمولة زايدة على السحب
    required_fields: [amount]
    min_priority: P2
    needs_transaction: true

  - id: card_issue
    team: Cards
    what_en: ZainCash Mastercard or virtual card - card declined, blocked, not delivered, or charged twice for one purchase
    what_ar: بطاقة زين كاش ماستر كارد - مرفوضة، مقفولة، ما وصلت، أو انسحب مبلغ مرتين
    not_for: Wallet transfers between people (failed_transfer)
    examples:
      - الماستر كارد مالتي ترفض بكل موقع
      - انسحب مني مبلغ مرتين من البطاقة على شراء واحد
    required_fields: []
    min_priority: P3
    needs_transaction: false

  - id: bill_payment
    team: Payments Ops
    what_en: Paying a bill or top-up (electricity, internet, mobile credit, water) failed or was not applied by the biller
    what_ar: دفع فاتورة أو شحن رصيد (كهرباء، انترنت، رصيد موبايل) فشل أو ما انحسب عند الجهة
    not_for: Transfers to a person (failed_transfer)
    examples:
      - دفعت فاتورة الكهرباء وطلعتلي ناجحة بس بعدها الوطنية تكول ما مدفوعة
      - شحنت رصيد اسيا وما وصل
    required_fields: [amount]
    min_priority: P3
    needs_transaction: true

  - id: account_kyc
    team: Account & Security
    what_en: Account verification, upgrading the account level, ID documents, limits reached, changing account details
    what_ar: توثيق الحساب، رفع مستوى الحساب، المستمسكات، الحد الأعلى، تغيير معلومات الحساب
    not_for: Cannot log in (login_access)
    examples:
      - شلون ارفع مستوى الحساب حتى اكدر احول اكثر
      - رفضوا هويتي بالتوثيق
    required_fields: []
    min_priority: P4
    needs_transaction: false

  - id: refund_request
    team: Disputes
    what_en: The customer wants money back from a merchant purchase or a cancelled service
    what_ar: يريد يرجع فلوسه من متجر أو خدمة ملغية
    not_for: Money sent to the wrong person (wrong_recipient); failed transfers (failed_transfer)
    examples:
      - اشتريت من متجر بالزين كاش والغيت الطلب يمته ترجع فلوسي
    required_fields: [amount]
    min_priority: P3
    needs_transaction: true

  - id: fraud_report
    team: Account & Security
    what_en: Scam or fraud - someone asked for the OTP or PIN, unauthorized transactions, hacked account
    what_ar: احتيال أو نصب - واحد طلب الرمز، حركات ما سواها الزبون، الحساب مخترق
    not_for: Simply forgetting the PIN (login_access)
    examples:
      - واحد اتصل بيه يكول من زين كاش وطلب الرمز وبعدها انسحبت فلوسي
      - اكو حركات بحسابي ما سويتها
    required_fields: []
    min_priority: P1
    needs_transaction: false

  - id: app_bug
    team: Tech Support
    what_en: The app crashes, shows errors, or a feature does not work, with no money lost
    what_ar: التطبيق يطفي أو يطلع أخطاء أو ميزة ما تشتغل بدون ضياع فلوس
    not_for: Any case where money is missing (failed_transfer, bill_payment)
    examples:
      - التطبيق يطفي اول ما افتحه بعد التحديث
    required_fields: []
    min_priority: P3
    needs_transaction: false

  - id: general_inquiry
    team: General Care
    what_en: Questions about fees, limits, how to do something, agent locations, or promotions
    what_ar: أسئلة عن العمولة، الحدود، طريقة الاستخدام، أماكن الوكلاء، العروض
    not_for: Reports of a problem that already happened
    examples:
      - شكد عمولة التحويل لحساب بنكي
    required_fields: []
    min_priority: P4
    needs_transaction: false

  - id: other
    team: General Care
    what_en: Anything that does not fit the categories above, including complaints with no clear request
    what_ar: أي شي ما ينطبق على الأصناف الثانية
    not_for: ""
    examples:
      - عندي ملاحظة على الخدمة بشكل عام
    required_fields: []
    min_priority: P4
    needs_transaction: false
```

- [ ] **Step 2: Write the failing tests**

`backend/tests/test_taxonomy.py`:
```python
import pytest

from app.config import REPO_ROOT
from app.taxonomy import TaxonomyError, load_taxonomy, most_urgent, priority_rank

EXPECTED = {
    "failed_transfer", "wrong_recipient", "login_access", "agent_dispute", "card_issue",
    "bill_payment", "account_kyc", "refund_request", "fraud_report", "app_bug",
    "general_inquiry", "other",
}


@pytest.fixture(scope="module")
def taxonomy():
    return load_taxonomy(REPO_ROOT / "data" / "taxonomy.yaml")


def test_loads_all_categories(taxonomy):
    assert set(taxonomy.ids) == EXPECTED
    assert taxonomy.get("failed_transfer").team == "Payments Ops"
    assert taxonomy.get("fraud_report").min_priority == "P1"
    assert taxonomy.get("failed_transfer").required_fields == ("amount", "date")


def test_unknown_id_falls_back_to_other(taxonomy):
    assert taxonomy.get("nope").id == "other"


def test_every_category_is_complete(taxonomy):
    for c in taxonomy.categories.values():
        assert c.examples, c.id
        assert c.team in taxonomy.teams


def test_describe_and_render(taxonomy):
    d = taxonomy.get("failed_transfer").describe()
    assert "Not for:" in d and "Examples:" in d
    assert "- failed_transfer: " in taxonomy.render()


def test_priority_helpers():
    assert priority_rank("P1") < priority_rank("P4")
    assert most_urgent("P3", "P1", "P2") == "P1"


def test_rejects_unknown_team(tmp_path):
    p = tmp_path / "t.yaml"
    p.write_text(
        "teams: [A]\ncategories:\n  - {id: other, team: B, what_en: x, what_ar: y,"
        " examples: [z], min_priority: P4}\n",
        encoding="utf-8",
    )
    with pytest.raises(TaxonomyError):
        load_taxonomy(p)
```

Also create `backend/tests/conftest.py` so later tasks can share the fixture:
```python
import pytest

from app.config import REPO_ROOT
from app.taxonomy import load_taxonomy


@pytest.fixture(scope="session")
def tax():
    return load_taxonomy(REPO_ROOT / "data" / "taxonomy.yaml")
```

- [ ] **Step 3: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_taxonomy.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'app.taxonomy'`.

- [ ] **Step 4: Implement `backend/app/taxonomy.py`**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

PRIORITIES = ("P1", "P2", "P3", "P4")
FIELD_NAMES = ("txn_ref", "amount", "phone", "date")


class TaxonomyError(ValueError):
    """Raised when taxonomy.yaml is inconsistent."""


@dataclass(frozen=True)
class Category:
    id: str
    team: str
    what_en: str
    what_ar: str
    not_for: str
    examples: tuple[str, ...]
    required_fields: tuple[str, ...]
    min_priority: str
    needs_transaction: bool

    def describe(self) -> str:
        """One-line description used by both Jev criteria and Gemini prompts."""
        parts = [f"{self.what_en} ({self.what_ar})"]
        if self.not_for:
            parts.append(f"Not for: {self.not_for}")
        if self.examples:
            parts.append("Examples: " + " | ".join(self.examples))
        return ". ".join(parts)


@dataclass(frozen=True)
class Taxonomy:
    teams: tuple[str, ...]
    categories: dict[str, Category]

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(self.categories)

    def get(self, category_id: str) -> Category:
        return self.categories.get(category_id, self.categories["other"])

    def render(self) -> str:
        return "\n".join(f"- {c.id}: {c.describe()}" for c in self.categories.values())


def priority_rank(priority: str) -> int:
    if priority not in PRIORITIES:
        raise ValueError(f"unknown priority {priority!r}")
    return PRIORITIES.index(priority)


def most_urgent(*priorities: str) -> str:
    return min(priorities, key=priority_rank)


def load_taxonomy(path: str | Path) -> Taxonomy:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    teams = tuple(data["teams"])
    categories: dict[str, Category] = {}
    for raw in data["categories"]:
        cid = raw["id"]
        if cid in categories:
            raise TaxonomyError(f"duplicate category {cid}")
        if raw["team"] not in teams:
            raise TaxonomyError(f"category {cid} uses unknown team {raw['team']!r}")
        if raw["min_priority"] not in PRIORITIES:
            raise TaxonomyError(f"category {cid} has invalid min_priority")
        required = tuple(raw.get("required_fields") or ())
        unknown = set(required) - set(FIELD_NAMES)
        if unknown:
            raise TaxonomyError(f"category {cid} requires unknown fields {sorted(unknown)}")
        categories[cid] = Category(
            id=cid,
            team=raw["team"],
            what_en=str(raw["what_en"]).strip(),
            what_ar=str(raw["what_ar"]).strip(),
            not_for=str(raw.get("not_for") or "").strip(),
            examples=tuple(raw.get("examples") or ()),
            required_fields=required,
            min_priority=raw["min_priority"],
            needs_transaction=bool(raw.get("needs_transaction", False)),
        )
    if "other" not in categories:
        raise TaxonomyError("taxonomy must define an 'other' category")
    return Taxonomy(teams=teams, categories=categories)
```

- [ ] **Step 5: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_taxonomy.py -v`

Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
cd .. && git add data/taxonomy.yaml backend && git commit -m "feat: taxonomy of categories, teams and priorities"
```

---

### Task 3: Shared contracts and normalization

**Files:**
- Create: `backend/app/pipeline/__init__.py` (empty), `backend/app/pipeline/contracts.py`, `backend/app/pipeline/normalize.py`
- Create: `backend/tests/helpers.py`
- Test: `backend/tests/test_normalize.py`

**Interfaces:**
- Produces, in `contracts.py`:
  - constants `FLAG_NAMES`, `FIELD_NAMES`
  - dataclasses `Ticket`, `NormalizedTicket`, `Candidate`, `Candidates`, `FieldPick`, `ClassificationResult`, `ClassifierOutput`, `ExtractedField`, `TxnRecord`, `LookupResult`, `Decision`, `DraftResult`, `TicketOutcome`
  - The fields are exactly as written in the code below. Every later task depends on these names.
- Produces, in `normalize.py`:
  - `to_ascii_digits(s) -> str`
  - `mask_cards(s) -> str`
  - `fold_arabic(s) -> str`
  - `detect_arabizi(s) -> bool`
  - `has_latin_mix(s) -> bool`
  - `normalize(ticket) -> NormalizedTicket`
  - `sanitize_for_storage(text) -> str`
- Produces, in `tests/helpers.py`:
  - `RECEIVED` (2026-10-07 09:30 Baghdad time)
  - `make_ticket(text, **kw) -> Ticket`

- [ ] **Step 1: Write `backend/app/pipeline/contracts.py`**

```python
"""Typed contracts shared by every pipeline stage. Keep this module dependency-free."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.taxonomy import FIELD_NAMES

FLAG_NAMES = (
    "fraud_suspected",
    "money_lost",
    "multi_issue",
    "urgent_or_angry",
    "mentions_specific_transaction",
    "asks_for_human",
)
__all__ = ["FIELD_NAMES", "FLAG_NAMES"]


@dataclass(frozen=True)
class Ticket:
    external_id: str
    text: str
    received_at: datetime
    channel: str = "app"
    customer_phone: str | None = None
    id: int | None = None


@dataclass(frozen=True)
class NormalizedTicket:
    ticket: Ticket
    match_text: str  # ASCII digits; same length as ticket.text, so spans index both
    normalized_text: str  # folded Arabic letters, diacritics removed (for models only)
    is_arabizi: bool
    has_latin_mix: bool


@dataclass(frozen=True)
class Candidate:
    field: str  # one of FIELD_NAMES
    value: str  # canonical value, e.g. "ZC2410000123", "07701234567", "50 الف"
    span: str  # exact substring of match_text
    start: int
    end: int


@dataclass
class Candidates:
    txn_ref: list[Candidate] = field(default_factory=list)
    amount: list[Candidate] = field(default_factory=list)
    phone: list[Candidate] = field(default_factory=list)
    date: list[Candidate] = field(default_factory=list)

    def for_field(self, name: str) -> list[Candidate]:
        return getattr(self, name)


@dataclass(frozen=True)
class FieldPick:
    value: str | None  # jev: the chosen candidate span; gemini: the verified verbatim span
    confidence: float
    method: str  # "jev_pick" | "gemini" | "none"
    normalized: str | None = None  # gemini's normalized value (e.g. "50000" for "خمسين الف")


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    category_confidence: float
    category_probs: dict[str, float]
    priority: str
    priority_confidence: float
    flags: dict[str, float]
    source: str  # "jev" | "gemini"
    uncertain: bool
    model: str


@dataclass(frozen=True)
class ClassifierOutput:
    classification: ClassificationResult
    picks: dict[str, FieldPick]
    path: str  # "jev" | "gemini" | "gemini_fallback" | "disagreement"
    reasons: tuple[str, ...] = ()
    cost_usd: float = 0.0
    degraded: bool = False


@dataclass(frozen=True)
class ExtractedField:
    value: str | int | None  # txn_ref str, amount int, phone "07..", date ISO string
    span: str | None
    start: int | None
    end: int | None
    method: str
    confidence: float
    currency: str | None = None


@dataclass(frozen=True)
class TxnRecord:
    txn_ref: str
    sender_phone: str
    receiver_phone: str | None
    receiver_name: str | None
    amount_iqd: int
    type: str
    status: str
    created_at: datetime
    biller: str | None = None
    agent_id: str | None = None
    failure_reason: str | None = None


@dataclass(frozen=True)
class LookupResult:
    # matched | not_found | ambiguous | amount_mismatch | date_mismatch | not_applicable
    status: str
    txn: TxnRecord | None = None
    candidates_found: int = 0


@dataclass(frozen=True)
class Decision:
    team: str
    priority: str
    escalated: bool
    reasons: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class DraftResult:
    text: str | None = None
    citations: tuple[str, ...] = ()
    trace: tuple[dict, ...] = ()
    reasons: tuple[str, ...] = ()
    cost_usd: float = 0.0


@dataclass(frozen=True)
class TicketOutcome:
    ticket: Ticket
    status: str  # pending_review | escalated | failed
    classifier: ClassifierOutput | None = None
    extracted: dict[str, ExtractedField] = field(default_factory=dict)
    lookup: LookupResult | None = None
    decision: Decision | None = None
    draft: DraftResult | None = None
    latency_ms: int = 0
    cost_usd: float = 0.0
    error: str | None = None
```

- [ ] **Step 2: Write `backend/tests/helpers.py`**

```python
from datetime import datetime, timedelta, timezone

from app.pipeline.contracts import Ticket

BAGHDAD = timezone(timedelta(hours=3))
RECEIVED = datetime(2026, 10, 7, 9, 30, tzinfo=BAGHDAD)  # a Wednesday


def make_ticket(text: str, **kw) -> Ticket:
    return Ticket(
        external_id=kw.pop("external_id", "T-1"),
        text=text,
        received_at=kw.pop("received_at", RECEIVED),
        **kw,
    )
```

- [ ] **Step 3: Write the failing tests**

`backend/tests/test_normalize.py`:
```python
from app.pipeline.normalize import (
    detect_arabizi, fold_arabic, has_latin_mix, mask_cards, normalize, sanitize_for_storage,
    to_ascii_digits,
)
from tests.helpers import make_ticket


def test_ascii_digits_is_length_preserving():
    assert to_ascii_digits("٥٠ الف ۱۲") == "50 الف 12"


def test_mask_card_keeps_last_four():
    assert mask_cards("رقم البطاقة 5123 4567 8901 2346") == "رقم البطاقة **** **** **** 2346"


def test_mask_card_in_arabic_indic_digits():
    assert mask_cards("٥١٢٣٤٥٦٧٨٩٠١٢٣٤٦") == "************٢٣٤٦"


def test_mask_leaves_phones_and_refs():
    for s in ["07701234567", "+9647701234567", "9647701234567", "ZC2410000123"]:
        assert mask_cards(s) == s


def test_fold_arabic():
    assert fold_arabic("أحمد إلى مستشفى") == "احمد الي مستشفي"
    assert fold_arabic("شُكْراً") == "شكرا"


def test_arabizi_detection():
    assert detect_arabizi("hawalit 25 alf w ma wslat")
    assert detect_arabizi("ma da ywselni el code mal ta2keed")
    assert not detect_arabizi("حولت 25 الف")
    assert not detect_arabizi("my app is not working")


def test_latin_mix():
    assert has_latin_mix("التطبيق ما يشتغل after update")
    assert not has_latin_mix("التطبيق ما يشتغل")


def test_normalize_keeps_spans_aligned():
    nt = normalize(make_ticket("حولت ٥٠ الف امس"))
    assert len(nt.match_text) == len(nt.ticket.text)
    assert "50" in nt.match_text
    assert not nt.is_arabizi


def test_sanitize_masks_cards():
    assert sanitize_for_storage(" بطاقتي 5123456789012346 ") == "بطاقتي ************2346"
```

- [ ] **Step 4: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_normalize.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 5: Implement `backend/app/pipeline/normalize.py`**

```python
from __future__ import annotations

import re

from app.pipeline.contracts import NormalizedTicket, Ticket

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
_FOLD = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"})
_DIACRITICS = re.compile(r"[\u064B-\u0652\u0670\u0640]")  # harakat, dagger alef, tatweel
_CARD = re.compile(r"(?<![\w+])\d(?:[ -]?\d){12,18}(?!\w)")
_ARABIC = re.compile(r"[\u0600-\u06FF]")
_LATIN_WORD = re.compile(r"\b[0-9']*[A-Za-z][A-Za-z0-9']*\b")
_DIGIT_IN_WORD = re.compile(r"(?=.*[A-Za-z])(?=.*[235679])[A-Za-z0-9']+")
_ARABIZI_WORDS = frozenset({
    "shlon", "shlonak", "shlonich", "aku", "maku", "mako", "flos", "floos", "hawala",
    "hawalit", "rasid", "ams", "lyom", "alyom", "wallah", "wallahi", "shnu", "shno", "leish",
    "lesh", "ani", "inta", "inti", "ma", "da", "wsl", "wslat", "wislat", "alf", "dinar", "mal",
    "el", "w", "ywselni", "agdar", "akdar",
})


def to_ascii_digits(text: str) -> str:
    """Arabic-Indic and Persian digits to ASCII. Length-preserving."""
    return text.translate(_DIGITS)


def mask_cards(text: str) -> str:
    """Replace all but the last 4 digits of card-like numbers with '*'. Length-preserving."""
    ascii_text = to_ascii_digits(text)
    chars = list(text)
    for m in _CARD.finditer(ascii_text):
        idx = [i for i in range(m.start(), m.end()) if ascii_text[i].isdigit()]
        digits = "".join(ascii_text[i] for i in idx)
        if digits.startswith(("964", "07")) and len(digits) <= 13:
            continue  # Iraqi phone number, not a card
        for i in idx[:-4]:
            chars[i] = "*"
    return "".join(chars)


def fold_arabic(text: str) -> str:
    return _DIACRITICS.sub("", text).translate(_FOLD)


def _latin_words(text: str) -> list[str]:
    return [w.lower() for w in _LATIN_WORD.findall(text)]


def detect_arabizi(text: str) -> bool:
    words = _latin_words(text)
    if len(words) < 2:
        return False
    hits = sum(1 for w in words if w in _ARABIZI_WORDS or _DIGIT_IN_WORD.fullmatch(w))
    return hits >= 2 or hits / len(words) >= 0.3


def has_latin_mix(text: str) -> bool:
    return bool(_ARABIC.search(text)) and len(_latin_words(text)) >= 2


def sanitize_for_storage(text: str) -> str:
    return mask_cards(text).strip()


def normalize(ticket: Ticket) -> NormalizedTicket:
    match_text = to_ascii_digits(ticket.text)
    return NormalizedTicket(
        ticket=ticket,
        match_text=match_text,
        normalized_text=fold_arabic(match_text),
        is_arabizi=detect_arabizi(ticket.text),
        has_latin_mix=has_latin_mix(ticket.text),
    )
```

- [ ] **Step 6: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_normalize.py -v`

Expected: 9 passed.

- [ ] **Step 7: Commit**

```bash
cd .. && git add backend && git commit -m "feat(pipeline): shared contracts and text normalization"
```

---

### Task 4: Regex candidate finders and amount parsing

**Files:**
- Create: `backend/app/pipeline/candidates.py`
- Test: `backend/tests/test_candidates.py`

**Interfaces:**
- Consumes: `Candidate`, `Candidates`, and `to_ascii_digits` (from Task 3)
- Produces:
  - `find_candidates(match_text) -> Candidates`
  - `parse_amount(span) -> tuple[int, str] | None`, where the string is `"IQD"` or `"USD"`
  - `normalize_phone(s) -> str | None`
  - `TXN_FULL`, a compiled regex for `ZC\d{10}`

- [ ] **Step 1: Write the failing tests**

`backend/tests/test_candidates.py`:
```python
from app.pipeline.candidates import find_candidates, normalize_phone, parse_amount
from app.pipeline.normalize import to_ascii_digits


def _values(cands, field):
    return [c.value for c in cands.for_field(field)]


def test_arabic_indic_amount_not_confused_with_phone():
    text = to_ascii_digits("حولت ٥٠ الف لرقم 0770 123 4567 امس ورقم العملية ZC-2410000123")
    c = find_candidates(text)
    assert _values(c, "txn_ref") == ["ZC2410000123"]
    assert _values(c, "phone") == ["07701234567"]
    assert _values(c, "amount") == ["50 الف"]
    assert _values(c, "date") == ["امس"]
    for field in ("txn_ref", "phone", "amount", "date"):
        for cand in c.for_field(field):
            assert text[cand.start : cand.end] == cand.span


def test_small_bare_numbers_are_not_amounts():
    c = find_candidates("صارلي قبل 2 يوم انتظر")
    assert _values(c, "amount") == []
    assert _values(c, "date") == ["قبل 2 يوم"]


def test_amount_forms():
    c = find_candidates("دفعت 25k ومرة ثانية $20 والفاتورة 1,250,000 دينار")
    assert _values(c, "amount") == ["25k", "$20", "1,250,000 دينار"]


def test_parse_amount():
    assert parse_amount("50 الف") == (50000, "IQD")
    assert parse_amount("25k") == (25000, "IQD")
    assert parse_amount("$20") == (20, "USD")
    assert parse_amount("1,250,000 دينار") == (1250000, "IQD")
    assert parse_amount("1.5 مليون") == (1500000, "IQD")
    assert parse_amount("50.000") == (50000, "IQD")
    assert parse_amount("خمسين الف") is None


def test_dates_absolute_and_weekday():
    c = find_candidates("صار يوم الخميس وبعدها 2026-10-05 و 5/10")
    assert _values(c, "date") == ["2026-10-05", "5/10", "يوم الخميس"]


def test_normalize_phone():
    assert normalize_phone("+964 770 123 4567") == "07701234567"
    assert normalize_phone("0770-123-4567") == "07701234567"
    assert normalize_phone("12345") is None


def test_dedupes_repeated_values():
    c = find_candidates("ZC2410000123 و ZC 2410000123")
    assert _values(c, "txn_ref") == ["ZC2410000123"]
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_candidates.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement `backend/app/pipeline/candidates.py`**

```python
"""Recall-tuned regex candidate finders. Jev later picks among these spans (spec §6.3)."""
from __future__ import annotations

import re

from app.pipeline.contracts import Candidate, Candidates
from app.pipeline.normalize import to_ascii_digits

MAX_CANDIDATES_PER_FIELD = 50  # Jev Choice allows at most 255 options
MIN_BARE_AMOUNT = 250  # a number with no unit below this is not treated as an amount

TXN_FULL = re.compile(r"ZC\d{10}")
_TXN_RE = re.compile(r"(?<![A-Za-z0-9])[Zz][Cc][\s-]?(\d{10})(?!\d)")
_PHONE_RE = re.compile(r"(?<![\d+])(?:\+?964[\s-]?|0)(7[3-9]\d)[\s-]?(\d{3})[\s-]?(\d{4})(?!\d)")
_ABS_DATE_RE = re.compile(
    r"(?<![\d/.-])(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}(?:[/-](?:\d{4}|\d{2}))?)(?![\d/-])"
)
_REL_DATE_RE = re.compile(
    r"(?<!\w)(?:و|ب)?("
    r"اليوم|امس|أمس|البارحة|البارحه|امبارح"
    r"|قبل\s?يومين|قبل\s?\d+\s?(?:يوم|ايام|أيام)"
    r"|(?:ال)?[اأ]سبوع\s(?:الماضي|الفات|اللي\sفات)"
    r"|(?:يوم\s)?(?:السبت|الاحد|الأحد|الاثنين|الإثنين|الثلاثاء|الاربعاء|الأربعاء|الخميس|الجمعة|الجمعه)"
    r"|yesterday|today|lyom|ams|embareh"
    r")(?!\w)",
    re.IGNORECASE,
)
_UNITS = r"الف|ألف|آلاف|الاف|الآف|مليون|دينار|دنانير|دولار|IQD|USD|million|alf|dinar|k|د\.ع"
_AMOUNT_RE = re.compile(
    r"(?<![\w.,$])(\$\s?)?(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)(?:\s?(" + _UNITS + r"))?(?!\w)",
    re.IGNORECASE,
)
_NUM_RE = re.compile(r"\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?")
_GROUPED = re.compile(r"\d{1,3}(?:[,.]\d{3})+")
_THOUSANDS_AR = ("الف", "ألف", "آلاف", "الاف", "الآف")


def normalize_phone(text: str) -> str | None:
    digits = re.sub(r"\D", "", to_ascii_digits(text or ""))
    if digits.startswith("964"):
        digits = "0" + digits[3:]
    return digits if re.fullmatch(r"07[3-9]\d{8}", digits) else None


def parse_amount(span: str) -> tuple[int, str] | None:
    s = to_ascii_digits(span or "").strip().lower()
    m = _NUM_RE.search(s)
    if not m:
        return None
    raw = m.group(0)
    number = float(re.sub(r"[,.]", "", raw)) if _GROUPED.fullmatch(raw) else float(raw)
    rest = s[: m.start()] + " " + s[m.end() :]
    if "مليون" in rest or "million" in rest:
        number *= 1_000_000
    elif any(u in rest for u in _THOUSANDS_AR) or re.search(r"(?<![a-z])(k|alf)(?![a-z])", rest):
        number *= 1000
    usd = "$" in s or "دولار" in s or re.search(r"(?<![a-z])usd(?![a-z])", s) is not None
    return int(round(number)), ("USD" if usd else "IQD")


def _overlaps(start: int, end: int, taken: list[tuple[int, int]]) -> bool:
    return any(start < e and s < end for s, e in taken)


def _add(bucket: list[Candidate], cand: Candidate, taken: list[tuple[int, int]]) -> None:
    taken.append((cand.start, cand.end))
    if len(bucket) < MAX_CANDIDATES_PER_FIELD and all(c.value != cand.value for c in bucket):
        bucket.append(cand)


def find_candidates(match_text: str) -> Candidates:
    """Over-collect candidate spans. `match_text` must already have ASCII digits."""
    out = Candidates()
    taken: list[tuple[int, int]] = []
    for m in _TXN_RE.finditer(match_text):
        _add(out.txn_ref, Candidate("txn_ref", "ZC" + m.group(1), m.group(0), m.start(), m.end()), taken)
    for m in _PHONE_RE.finditer(match_text):
        value = "0" + m.group(1) + m.group(2) + m.group(3)
        _add(out.phone, Candidate("phone", value, m.group(0), m.start(), m.end()), taken)
    for rx in (_ABS_DATE_RE, _REL_DATE_RE):
        for m in rx.finditer(match_text):
            if _overlaps(m.start(1), m.end(1), taken):
                continue
            _add(out.date, Candidate("date", m.group(1), m.group(1), m.start(1), m.end(1)), taken)
    for m in _AMOUNT_RE.finditer(match_text):
        if _overlaps(m.start(), m.end(), taken):
            continue
        span = m.group(0)
        parsed = parse_amount(span)
        has_unit = bool(m.group(1) or m.group(3))
        if parsed is None or (not has_unit and parsed[0] < MIN_BARE_AMOUNT):
            continue
        _add(out.amount, Candidate("amount", span, span, m.start(), m.end()), taken)
    return out
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_candidates.py -v`

Expected: 7 passed. If `test_dates_absolute_and_weekday` fails only on ordering, fix the regex, not the test. Absolute dates are found first, then relative ones.

- [ ] **Step 5: Commit**

```bash
cd .. && git add backend && git commit -m "feat(pipeline): regex candidate finders for refs, phones, amounts, dates"
```

---

### Task 5: Resolving relative dates

**Files:**
- Create: `backend/app/pipeline/dates.py`
- Test: `backend/tests/test_dates.py`

**Interfaces:**
- Produces: `resolve_date(span: str, received_at: datetime) -> date | None`

- [ ] **Step 1: Write the failing tests**

`backend/tests/test_dates.py`:
```python
from datetime import date

import pytest

from app.pipeline.dates import resolve_date
from tests.helpers import RECEIVED  # Wednesday 2026-10-07


@pytest.mark.parametrize(
    ("span", "expected"),
    [
        ("اليوم", date(2026, 10, 7)),
        ("امس", date(2026, 10, 6)),
        ("البارحة", date(2026, 10, 6)),
        ("yesterday", date(2026, 10, 6)),
        ("قبل يومين", date(2026, 10, 5)),
        ("قبل 3 ايام", date(2026, 10, 4)),
        ("الاسبوع الماضي", date(2026, 9, 30)),
        ("يوم الخميس", date(2026, 10, 1)),
        ("الاربعاء", date(2026, 10, 7)),
        ("2026-10-05", date(2026, 10, 5)),
        ("5/10", date(2026, 10, 5)),
        ("25/12", date(2025, 12, 25)),
        ("5/10/26", date(2026, 10, 5)),
    ],
)
def test_resolve(span, expected):
    assert resolve_date(span, RECEIVED) == expected


@pytest.mark.parametrize("span", ["32/13", "", "قريب"])
def test_unresolvable_is_none(span):
    assert resolve_date(span, RECEIVED) is None
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `uv run pytest tests/test_dates.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement `backend/app/pipeline/dates.py`**

```python
"""Resolve date phrases against the ticket's received_at. Arithmetic stays in code (Jev docs)."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from app.pipeline.normalize import to_ascii_digits

_TODAY = {"اليوم", "today", "lyom"}
_YESTERDAY = {"امس", "أمس", "البارحة", "البارحه", "امبارح", "yesterday", "ams", "embareh"}
_WEEKDAYS = {
    "الاثنين": 0, "الإثنين": 0, "الثلاثاء": 1, "الاربعاء": 2, "الأربعاء": 2, "الخميس": 3,
    "الجمعة": 4, "الجمعه": 4, "السبت": 5, "الاحد": 6, "الأحد": 6,
}


def _safe_date(y: int, m: int, d: int) -> date | None:
    try:
        return date(y, m, d)
    except ValueError:
        return None


def resolve_date(span: str, received_at: datetime) -> date | None:
    s = to_ascii_digits(span or "").strip().lower()
    if not s:
        return None
    base = received_at.date()
    if s in _TODAY:
        return base
    if s in _YESTERDAY:
        return base - timedelta(days=1)
    if "يومين" in s:
        return base - timedelta(days=2)
    if m := re.fullmatch(r"قبل\s?(\d+)\s?(?:يوم|ايام|أيام)", s):
        return base - timedelta(days=int(m.group(1)))
    if "سبوع" in s:
        return base - timedelta(days=7)
    day_name = s.removeprefix("يوم").strip()
    if day_name in _WEEKDAYS:
        return base - timedelta(days=(base.weekday() - _WEEKDAYS[day_name]) % 7)
    if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s):
        return _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if m := re.fullmatch(r"(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2}|\d{4}))?", s):
        day, month = int(m.group(1)), int(m.group(2))  # Iraq writes day first
        if m.group(3):
            year = int(m.group(3))
            return _safe_date(year + 2000 if year < 100 else year, month, day)
        d = _safe_date(base.year, month, day)
        if d and d > base:
            d = _safe_date(base.year - 1, month, day)
        return d
    return None
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `uv run pytest tests/test_dates.py -v`

Expected: 16 passed.

- [ ] **Step 5: Commit**

```bash
cd .. && git add backend && git commit -m "feat(pipeline): resolve relative and absolute date phrases"
```

Continue with `2026-10-07-plan1-core-pipeline-part2.md` (Tasks 6–11), then `2026-10-07-plan1-core-pipeline-part3.md` (Tasks 12–15).
