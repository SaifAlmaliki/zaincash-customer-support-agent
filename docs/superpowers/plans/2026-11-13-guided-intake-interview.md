# Guided Intake Interview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The customer intake agent keeps interviewing until a transfer report is as complete as "حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123". The chat shows why each question is asked, quick replies, progress and a clear review card.

**Architecture:** Fixed per-category rules in `backend/app/intake/policy.py` choose every question and decide readiness. Each question carries a reason, an answer kind and choices. Quick replies are recorded without a model call. `SessionView` gains `pending_question` and `progress`, and a new `/ask` operation lets the customer pick a missing detail. The React intake screen renders these with an optimistic customer bubble, a typing indicator, quick-reply chips, a progress strip and a grouped review card.

**Tech Stack:** Python 3.12 + FastAPI + Pydantic v2 + LangGraph + SQLAlchemy/Postgres (pytest against `support_test`); React 19 + TypeScript 6 + Vite + Vitest + Testing Library.

**Spec:** `docs/superpowers/specs/2026-11-13-guided-intake-interview-design.md`

## Global Constraints

- Run every command from Windows PowerShell through WSL. Never use bare `pytest`/`npm` on Windows.
  - Backend tests: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short <paths>"`
  - Backend lint: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run ruff check app tests"`
  - Customer frontend: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test -- <file>"`. Same pattern for `typecheck`, `lint` and `build`.
  - Employee frontend: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/employee-frontend && npm run test"`. Same pattern for `typecheck`, `lint` and `build`.
- If you work in a git worktree, replace `~/dev/zaincash-support` with the worktree path in every command.
- Backend tests use the guarded `support_test` database only. Never reset the development `support` database.
- Commit only the files your task lists, with `git add <exact paths>`.
  - Never run `git add -A`, `git add .` or `git commit -a`.
  - Never touch `graphify-out/**` or the user's uncommitted files under `employee-frontend/src/features/review/**`.
- Fact keys are machine keys: `recipient_name` is the new key, and `recipient_phone` is the recipient's number. Never use `receiver_name` in intake code.
- The Arabic customer text and the employee summary stay identical (`review.py::build_review`). Do not break this.
- Never ask for a PIN, OTP, password or full card number. `asks_for_secret` stays in force for model-suggested questions.
- Locale files (`users-frontend/apps/web/src/features/intake/locales/*.json`): add keys only. Do not reword existing keys. Every key added to `IntakeCopy` in `copy.ts` must exist in both `ar.json` and `en.json`.
- Match the surrounding style. Backend: no new comments except for non-obvious behavior. Frontend: no semicolons, double quotes, 2-space indent.

## Review Focus

1. **The customer types an answer instead of tapping a chip** (for example "اي انقطعت"). It must go through the model exactly as before. Pinned in Task 6: the scenario mixes typed and tapped answers.
2. **A stale tab taps a chip after the question changed.** Expected: 409 `revision_conflict`, no customer message stored, and the screen reloads. Pinned in Task 4.
3. **The page reloads while a quick reply or an `/ask` is in flight.** The saved pending operation (with `answer_to`, or kind `ask`) must survive `parseSavedSession` and be retried with the same request ID. Pinned in Task 7.
4. **Sessions stored before this change** have `QuestionRecord`s without `reason`/`attempt`. Expected: they still load, and the screen hides an empty "why we ask" line. Pinned in Task 3 (backend) and Task 8 (frontend).
5. **An ask-once detail answered "I don't know"** must not keep the report partial or be asked again. A required detail answered "I don't know" keeps it partial. Pinned in Tasks 1 and 6.

---

### Task 1: Field plan, question choice and readiness

**Files:**
- Modify: `backend/app/intake/contracts.py` (add `AnswerKind`, `Choice`, `AskedQuestion`; extend `QuestionRecord`)
- Replace: `backend/app/intake/policy.py`
- Modify: `backend/app/intake/review.py:10,14-23,88-91`
- Create: `backend/tests/intake/test_interview_policy.py`
- Modify (existing expectations only): `backend/tests/intake/test_policy.py`, `backend/tests/intake/test_review.py:52`, `backend/tests/intake/test_handoff.py:17,29-36`

**Interfaces:**
- Produces, in `app.intake.contracts`:
  - `AnswerKind = Literal["yes_no", "amount", "phone", "reference", "date", "text"]`
  - `Choice = Literal["yes", "no", "unknown", "attach"]`
  - `class AskedQuestion(Question)` with `answer_kind: AnswerKind = "text"`, `choices: list[Choice] = []`, `attempt: int = 1`
  - `QuestionRecord` gains `reason: str = ""` and `attempt: int = 1`
- Produces, in `app.intake.policy`:
  - `material_keys(category, taxonomy=None) -> list[str]`: the required keys
  - `ask_once_keys(category) -> list[str]`
  - `optional_keys(state, taxonomy=None) -> list[str]`: ask-once plus HIGH_VALUE `additional_needed`
  - `answer_kind(key) -> AnswerKind`
  - `answer_choices(key) -> list[Choice]`
  - `asked_count(state, key) -> int`
  - `choose_question(state, suggested, revision, taxonomy=None) -> AskedQuestion | None`
  - `ask_for(state, key, revision) -> AskedQuestion`
  - `assess_readiness(state, taxonomy, *, allow_partial=False) -> Readiness`
  - Unchanged: `field_needs_question`, `field_is_resolved`, `canonical_category`, `asks_for_secret`, `HIGH_VALUE`, `PRECISE`.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/intake/test_interview_policy.py`:

```python
from uuid import uuid4

import pytest

from app.config import Settings
from app.intake.contracts import EvidenceRef, Fact, Question, QuestionRecord
from app.intake.policy import (
    answer_choices,
    answer_kind,
    ask_for,
    ask_once_keys,
    assess_readiness,
    choose_question,
    material_keys,
)
from app.taxonomy import load_taxonomy
from tests.intake.helpers import context, fact, message


@pytest.fixture
def taxonomy():
    return load_taxonomy(Settings(_env_file=None).taxonomy_path)


def asked(key, times=1):
    return [QuestionRecord(key=key, basis_revision=1, message_id=uuid4(), outcome="asked") for _ in range(times)]


def unknown(key, source):
    return Fact(key=key, status="unknown", evidence=[EvidenceRef(kind="message", source_id=source.id, quote=source.text)])


def complete_transfer(source, *extra):
    return [
        fact("issue", source.text, source),
        fact("amount", "50000", source, normalized="50000"),
        fact("date", "2026-10-06", source, normalized="2026-10-06"),
        fact("debited", "yes", source, normalized="yes"),
        fact("recipient_outcome", "no", source, normalized="no"),
        fact("recipient_phone", "07701234567", source, normalized="07701234567"),
        *extra,
    ]


@pytest.mark.parametrize(("category", "required", "optional"), [
    ("failed_transfer", ["issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"], ["recipient_name", "txn_ref"]),
    ("wrong_recipient", ["issue", "amount", "date", "recipient_phone"], ["recipient_name", "txn_ref"]),
    ("bill_payment", ["issue", "biller", "amount", "date"], ["txn_ref", "debited"]),
    ("agent_dispute", ["issue", "amount", "agent_location", "date"], ["txn_ref"]),
    ("refund_request", ["issue", "merchant", "amount", "date"], ["txn_ref"]),
    ("app_bug", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("login_access", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("card_issue", ["issue", "card_symptom", "expected"], ["exact_error"]),
    ("account_kyc", ["issue", "kyc_step", "expected"], ["exact_error"]),
    ("fraud_report", ["issue", "date"], ["amount", "recipient_phone", "txn_ref"]),
    ("general_inquiry", ["issue"], []),
    ("other", ["issue", "desired_outcome"], []),
    ("login", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("something_new", ["issue", "desired_outcome"], []),
])
def test_field_plan(taxonomy, category, required, optional):
    assert material_keys(category, taxonomy) == required
    assert ask_once_keys(category) == optional


def test_money_problems_do_not_ask_what_was_expected(taxonomy):
    source = message("حولت فلوس وما وصلت")
    state = context([source], [fact("issue", source.text, source)], category="failed_transfer").state
    question = choose_question(state, None, 1, taxonomy)
    assert question is not None and question.key == "amount"
    readiness = assess_readiness(state, taxonomy)
    assert "expected" not in readiness.missing and "actual" not in readiness.missing


def test_question_carries_reason_kind_choices_and_attempt(taxonomy):
    source = message("حولت 50000 بتاريخ 2026-10-06 وما وصلت")
    known = [
        fact("issue", source.text, source),
        fact("amount", "50000", source, normalized="50000"),
        fact("date", "2026-10-06", source, normalized="2026-10-06"),
    ]
    question = choose_question(context([source], known, category="failed_transfer").state, None, 3, taxonomy)
    assert question.key == "debited"
    assert question.text == "انخصم المبلغ من محفظتك؟"
    assert question.reason == "حتى نعرف إذا الفلوس طلعت من محفظتك."
    assert question.answer_kind == "yes_no"
    assert question.choices == ["yes", "no", "unknown"]
    assert question.attempt == 1
    assert question.basis_revision == 3


@pytest.mark.parametrize(("key", "kind", "choices"), [
    ("debited", "yes_no", ["yes", "no", "unknown"]),
    ("recipient_outcome", "yes_no", ["yes", "no", "unknown"]),
    ("repeats", "yes_no", ["yes", "no", "unknown"]),
    ("amount", "amount", ["unknown"]),
    ("recipient_phone", "phone", ["unknown"]),
    ("txn_ref", "reference", ["unknown", "attach"]),
    ("date", "date", ["unknown"]),
    ("recipient_name", "text", ["unknown"]),
])
def test_answer_kind_comes_from_the_key(key, kind, choices):
    assert answer_kind(key) == kind
    assert answer_choices(key) == choices


def test_required_detail_is_asked_again_once_after_the_first_round(taxonomy):
    source = message("حولت فلوس وما وصلت")
    known = [fact("issue", source.text, source), fact("amount", "50000", source, normalized="50000")]
    state = context([source], known, category="failed_transfer").state
    state = state.model_copy(update={"questions": [*asked("amount"), *asked("date")]})
    first = choose_question(state, None, 4, taxonomy)
    assert first.key == "debited" and first.attempt == 1
    rest = ["debited", "recipient_outcome", "recipient_phone", "recipient_name", "txn_ref"]
    state = state.model_copy(update={"questions": [*state.questions, *[item for key in rest for item in asked(key)]]})
    again = choose_question(state, None, 5, taxonomy)
    assert again.key == "date" and again.attempt == 2
    assert again.text == "بس حتى نكمل التقرير: متى صارت هالمشكلة؟"
    state = state.model_copy(update={"questions": [*state.questions, *asked("date")]})
    after = choose_question(state, None, 6, taxonomy)
    assert after is not None and after.key == "debited" and after.attempt == 2


def test_ask_once_detail_is_never_asked_twice(taxonomy):
    source = message("x")
    state = context([source], complete_transfer(source), category="failed_transfer").state
    state = state.model_copy(update={"questions": [*asked("recipient_name"), *asked("txn_ref")]})
    assert choose_question(state, None, 9, taxonomy) is None
    assert assess_readiness(state, taxonomy).quality == "sufficient_context"


def test_unasked_ask_once_detail_keeps_collecting(taxonomy):
    source = message("x")
    readiness = assess_readiness(context([source], complete_transfer(source), category="failed_transfer").state, taxonomy)
    assert readiness.quality == "collecting"
    assert readiness.missing == []
    assert readiness.next_key == "recipient_name"


def test_unknown_reference_still_gives_a_complete_report(taxonomy):
    source = message("ما عندي رقم")
    facts = complete_transfer(source, fact("recipient_name", "علي حسين", source), unknown("txn_ref", source))
    assert assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy).quality == "sufficient_context"


def test_unknown_required_detail_is_partial(taxonomy):
    source = message("ما أعرف")
    facts = [
        *complete_transfer(source)[:-1], unknown("recipient_phone", source),
        fact("recipient_name", "علي", source), fact("txn_ref", "ZC1", source, normalized="ZC1"),
    ]
    readiness = assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy)
    assert readiness.quality == "partial_context"


def test_customer_chosen_question_ignores_the_ask_limit():
    source = message("x")
    state = context([source], [fact("issue", source.text, source), unknown("txn_ref", source)], category="failed_transfer").state
    state = state.model_copy(update={"questions": asked("txn_ref")})
    question = ask_for(state, "txn_ref", 7)
    assert question.key == "txn_ref" and question.attempt == 2
    assert question.text == "عدك رقم عملية أو مرجع؟"
    assert question.choices == ["unknown", "attach"]


def test_model_suggestion_is_used_within_the_current_round(taxonomy):
    source = message("حولت فلوس وما وصلت")
    state = context([source], [fact("issue", source.text, source)], category="failed_transfer").state
    suggested = Question(key="recipient_phone", text="على أي رقم حولت؟", reason="حتى نلگه التحويل.", basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question.key == "recipient_phone"
    assert question.text == "على أي رقم حولت؟"
    assert question.reason == "حتى نلگه التحويل."
    assert question.answer_kind == "phone"
```

Append to `backend/tests/intake/test_review.py`:

```python
def test_review_lists_ask_once_details_for_the_employee():
    source = message("Transfer failed")
    ctx = context([source], [fact("issue", "transfer failed", source)], category="failed_transfer")
    text = ReviewText(customer_text="Transfer failed", employee_text_ar="فشل التحويل",
                      fact_keys=["issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"])
    review = build_review(ctx, ctx.state, text, publication=1, language="en")
    assert review.facts["recipient_name"].status == "missing"
    assert "- اسم المستلم: غير متوفر" in review.ticket_text_ar
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_interview_policy.py tests/intake/test_review.py"`
Expected: FAIL. The collection error `ImportError: cannot import name 'answer_choices'` is expected.

- [ ] **Step 3: Extend the contracts**

In `backend/app/intake/contracts.py`:
- Add the two literals after `ProcessingStatus = ...`:

```python
AnswerKind = Literal["yes_no", "amount", "phone", "reference", "date", "text"]
Choice = Literal["yes", "no", "unknown", "attach"]
```

- Replace the `QuestionRecord` class:

```python
class QuestionRecord(IntakeModel):
    key: str
    basis_revision: int
    message_id: UUID
    outcome: Literal["asked", "answered", "unknown"]
    reason: str = ""
    attempt: int = 1
```

- Directly after the `Question` class, add:

```python
class AskedQuestion(Question):
    answer_kind: AnswerKind = "text"
    choices: list[Choice] = Field(default_factory=list)
    attempt: int = 1
```

`Analysis.suggested_question` stays `Question | None`, so the model's output schema does not change.

- [ ] **Step 4: Replace `backend/app/intake/policy.py`**

```python
"""Field plan, question choice and readiness. Unknown answers never count as a complete report."""
from __future__ import annotations

import re

from app.intake.contracts import AnswerKind, AskedQuestion, Choice, Fact, IntakeState, Question, Readiness
from app.taxonomy import Taxonomy

HIGH_VALUE = ("txn_ref", "exact_error", "repeats", "attempted_steps", "app_version")
PRECISE = {"amount", "recipient_phone", "date", "txn_ref"}
REQUIRED_ASKS = 2
OPTIONAL_ASKS = 1
_ALIASES = {
    "login": "login_access",
    "card": "card_issue",
    "kyc": "account_kyc",
    "fraud": "fraud_report",
    "refund": "refund_request",
}
# category -> (required keys, ask-once keys)
_PLAN: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "failed_transfer": (
        ("issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"), ("recipient_name", "txn_ref"),
    ),
    "wrong_recipient": (("issue", "amount", "date", "recipient_phone"), ("recipient_name", "txn_ref")),
    "bill_payment": (("issue", "biller", "amount", "date"), ("txn_ref", "debited")),
    "agent_dispute": (("issue", "amount", "agent_location", "date"), ("txn_ref",)),
    "refund_request": (("issue", "merchant", "amount", "date"), ("txn_ref",)),
    "app_bug": (("issue", "failed_step", "expected"), ("exact_error", "device", "app_version")),
    "login_access": (("issue", "failed_step", "expected"), ("exact_error", "device", "app_version")),
    "card_issue": (("issue", "card_symptom", "expected"), ("exact_error",)),
    "account_kyc": (("issue", "kyc_step", "expected"), ("exact_error",)),
    "fraud_report": (("issue", "date"), ("amount", "recipient_phone", "txn_ref")),
    "general_inquiry": (("issue",), ()),
    "other": (("issue", "desired_outcome"), ()),
}
_KINDS: dict[str, AnswerKind] = {
    "debited": "yes_no", "recipient_outcome": "yes_no", "repeats": "yes_no",
    "amount": "amount", "recipient_phone": "phone", "txn_ref": "reference", "date": "date",
}
_CHOICES: dict[str, list[Choice]] = {"yes_no": ["yes", "no", "unknown"], "reference": ["unknown", "attach"]}
_SECRET = re.compile(
    r"\b(pin|otp|password|passcode|cvv|cvc)\b|card[\s-]*(number|details)|رمز\s*(السر|التحقق|التأكيد)|كلمة\s*(السر|المرور)|رقم\s*البطاقة",
    re.IGNORECASE,
)
_ASK = {
    "en": {
        "issue": "What happened?",
        "actual": "What actually happened?",
        "expected": "What did you expect to happen?",
        "date": "When did this happen?",
        "amount": "What amount was involved?",
        "debited": "Was the amount taken from your wallet?",
        "recipient_outcome": "Did the other person receive the money?",
        "recipient_phone": "What number did you send the money to?",
        "recipient_name": "What is the recipient's name?",
        "txn_ref": "Do you have a transaction or reference number?",
        "exact_error": "What exact error appeared?",
        "failed_step": "Which step failed?",
        "device": "Which phone were you using?",
        "agent_location": "Where was the agent or shop?",
        "biller": "Which bill or company was this for?",
        "merchant": "Which shop was this?",
        "card_symptom": "What happened with the card?",
        "kyc_step": "Which verification step is stuck?",
        "desired_outcome": "What would you like us to do?",
        "attempted_steps": "What have you already tried?",
        "repeats": "Has this happened more than once?",
        "app_version": "Which app version is installed?",
        "currency": "Which currency was the amount in?",
    },
    "ar": {
        "issue": "شنو صار بالضبط؟",
        "actual": "شنو اللي صار فعلياً؟",
        "expected": "شنو كنت تتوقع يصير؟",
        "date": "متى صارت هالمشكلة؟",
        "amount": "شكد المبلغ؟",
        "debited": "انخصم المبلغ من محفظتك؟",
        "recipient_outcome": "وصلت الفلوس للشخص الثاني؟",
        "recipient_phone": "على أي رقم حولت الفلوس؟",
        "recipient_name": "شنو اسم الشخص اللي حولتله؟",
        "txn_ref": "عدك رقم عملية أو مرجع؟",
        "exact_error": "شنو نص الخطأ اللي طلع؟",
        "failed_step": "بأي خطوة صار الفشل؟",
        "device": "شنو نوع الهاتف اللي تستخدمه؟",
        "agent_location": "وين موقع الوكيل أو المحل؟",
        "biller": "لفائدة أي جهة أو فاتورة؟",
        "merchant": "شنو اسم المتجر؟",
        "card_symptom": "شنو اللي صار ويا البطاقة؟",
        "kyc_step": "بأي خطوة توقف التوثيق؟",
        "desired_outcome": "شنو تحب نسوي؟",
        "attempted_steps": "شنو جربت لحد هسة؟",
        "repeats": "تكررت المشكلة أكثر من مرة؟",
        "app_version": "شنو إصدار التطبيق؟",
        "currency": "المبلغ بالدينار لو بعملة ثانية؟",
    },
}
_WHY = {
    "en": {
        "issue": "It helps us understand the problem.",
        "actual": "It tells us what went wrong.",
        "expected": "It tells us what should have happened.",
        "date": "It helps us find the transaction.",
        "amount": "It helps us find the transaction.",
        "debited": "It tells us whether the money left your wallet.",
        "recipient_outcome": "It tells us whether the money arrived.",
        "recipient_phone": "It helps us find the transfer.",
        "recipient_name": "It helps us confirm the right transfer.",
        "txn_ref": "It lets us find the transaction directly.",
        "exact_error": "The exact message points to the cause.",
        "failed_step": "It shows where the problem happens.",
        "device": "Some problems only happen on certain phones.",
        "agent_location": "It helps us identify the agent.",
        "biller": "It helps us find the payment.",
        "merchant": "It helps us find the payment.",
        "card_symptom": "It tells us what is wrong with the card.",
        "kyc_step": "It shows where verification stopped.",
        "desired_outcome": "It tells us how to help.",
        "attempted_steps": "It saves you repeating steps.",
        "repeats": "It shows whether the problem is ongoing.",
        "app_version": "Some problems only affect certain versions.",
        "currency": "It helps us read the amount correctly.",
    },
    "ar": {
        "issue": "حتى نفهم المشكلة.",
        "actual": "حتى نعرف شنو اللي صار غلط.",
        "expected": "حتى نعرف شنو المفروض يصير.",
        "date": "يساعدنا نلگه العملية.",
        "amount": "يساعدنا نلگه العملية.",
        "debited": "حتى نعرف إذا الفلوس طلعت من محفظتك.",
        "recipient_outcome": "حتى نعرف إذا الفلوس وصلت.",
        "recipient_phone": "يساعدنا نلگه التحويل.",
        "recipient_name": "يساعدنا نتأكد من التحويل الصحيح.",
        "txn_ref": "بيه نلگه العملية مباشرة.",
        "exact_error": "نص الخطأ يدلنا على السبب.",
        "failed_step": "حتى نعرف وين تصير المشكلة.",
        "device": "بعض المشاكل تصير بس على أجهزة معينة.",
        "agent_location": "حتى نعرف الوكيل.",
        "biller": "يساعدنا نلگه الدفعة.",
        "merchant": "يساعدنا نلگه الدفعة.",
        "card_symptom": "حتى نعرف شنو مشكلة البطاقة.",
        "kyc_step": "حتى نعرف وين وگف التوثيق.",
        "desired_outcome": "حتى نعرف شلون نساعدك.",
        "attempted_steps": "حتى ما تعيد نفس الخطوات.",
        "repeats": "حتى نعرف إذا المشكلة مستمرة.",
        "app_version": "بعض المشاكل تخص إصدارات معينة.",
        "currency": "حتى نقرأ المبلغ صح.",
    },
}
_REASK = {"en": "Just so we can complete the report: ", "ar": "بس حتى نكمل التقرير: "}
_GENERIC = {
    "en": ("Could you tell us more about this?", "This detail is needed to understand the report."),
    "ar": ("ممكن توضح هالنقطة أكثر؟", "هالتفصيلة ضرورية حتى نفهم المشكلة."),
}


def field_needs_question(item: Fact | None) -> bool:
    return item is None or item.status in {"missing", "conflicting"}


def field_is_resolved(item: Fact | None) -> bool:
    return item is not None and item.status in {"known", "not_applicable"}


def canonical_category(category: str) -> str:
    return _ALIASES.get(category, category)


def _plan(category: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return _PLAN.get(canonical_category(category), _PLAN["other"])


def material_keys(category: str, taxonomy: Taxonomy | None = None) -> list[str]:
    cid = canonical_category(category)
    keys = list(_plan(cid)[0])
    if taxonomy is not None and cid in getattr(taxonomy, "categories", {}):
        for name in taxonomy.get(cid).required_fields:
            if name == "phone":
                if cid == "wrong_recipient":
                    keys.append("recipient_phone")
            elif name in {"date", "amount"}:
                keys.append(name)
    return list(dict.fromkeys(keys))


def ask_once_keys(category: str) -> list[str]:
    required = set(material_keys(category))
    return [key for key in _plan(category)[1] if key not in required]


def optional_keys(state: IntakeState, taxonomy: Taxonomy | None = None) -> list[str]:
    required = set(material_keys(state.category, taxonomy))
    extra = [key for key in state.additional_needed if key in HIGH_VALUE]
    return [key for key in dict.fromkeys([*ask_once_keys(state.category), *extra]) if key not in required]


def answer_kind(key: str) -> AnswerKind:
    return _KINDS.get(key, "text")


def answer_choices(key: str) -> list[Choice]:
    return list(_CHOICES.get(answer_kind(key), ["unknown"]))


def asks_for_secret(text: str) -> bool:
    return _SECRET.search(text or "") is not None


def _needs_precision(item: Fact | None) -> bool:
    return item is not None and item.status == "known" and item.key in PRECISE and not item.normalized


def asked_count(state: IntakeState, key: str) -> int:
    return sum(1 for item in state.questions if item.key == key and item.outcome == "asked")


def _limit(state: IntakeState, key: str, taxonomy: Taxonomy | None) -> int:
    item = state.facts.get(key)
    if item is not None and item.status == "conflicting":
        return REQUIRED_ASKS
    return REQUIRED_ASKS if key in material_keys(state.category, taxonomy) else OPTIONAL_ASKS


def _can_ask(state: IntakeState, key: str, taxonomy: Taxonomy | None = None) -> bool:
    item = state.facts.get(key)
    if item is not None and item.status in {"unknown", "not_applicable"}:
        return False
    if not field_needs_question(item) and not _needs_precision(item):
        return False
    return asked_count(state, key) < _limit(state, key, taxonomy)


def _candidates(state: IntakeState, taxonomy: Taxonomy | None) -> list[str]:
    keys = list(dict.fromkeys([*material_keys(state.category, taxonomy), *optional_keys(state, taxonomy)]))
    # First asks come before any re-ask; plan order is kept inside each round.
    return sorted((key for key in keys if _can_ask(state, key, taxonomy)), key=lambda key: asked_count(state, key))


def _language(state: IntakeState) -> str:
    return state.language if state.language in _ASK else "ar"


def _question(key: str, text: str, reason: str, revision: int, attempt: int) -> AskedQuestion:
    return AskedQuestion(
        key=key, text=text, reason=reason, basis_revision=revision,
        answer_kind=answer_kind(key), choices=answer_choices(key), attempt=attempt,
    )


def _template(state: IntakeState, key: str, revision: int, attempt: int, *, reword: bool) -> AskedQuestion:
    language = _language(state)
    generic_text, generic_reason = _GENERIC[language]
    text = _ASK[language].get(key, generic_text)
    if reword and attempt > 1:
        text = _REASK[language] + text
    return _question(key, text, _WHY[language].get(key, generic_reason), revision, attempt)


def choose_question(state: IntakeState, suggested: Question | None, revision: int,
                    taxonomy: Taxonomy | None = None) -> AskedQuestion | None:
    candidates = _candidates(state, taxonomy)
    if not candidates:
        return None
    current_round = asked_count(state, candidates[0])
    eligible = [key for key in candidates if asked_count(state, key) == current_round]
    if suggested is not None and suggested.key in eligible:
        if asks_for_secret(suggested.text):
            return _template(state, suggested.key, revision, current_round + 1, reword=True)
        fallback = _template(state, suggested.key, revision, current_round + 1, reword=False)
        return _question(suggested.key, suggested.text, suggested.reason.strip() or fallback.reason,
                         revision, current_round + 1)
    return _template(state, candidates[0], revision, current_round + 1, reword=True)


def ask_for(state: IntakeState, key: str, revision: int) -> AskedQuestion:
    """The customer chose this detail, so the ask limits do not apply."""
    return _template(state, key, revision, asked_count(state, key) + 1, reword=False)


def assess_readiness(state: IntakeState, taxonomy: Taxonomy, *, allow_partial: bool = False) -> Readiness:
    keys = material_keys(state.category, taxonomy)
    missing = [key for key in keys if field_needs_question(state.facts.get(key)) or _needs_precision(state.facts.get(key))]
    conflicts = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "conflicting"]
    unknowns = [key for key in keys if (item := state.facts.get(key)) is not None and item.status == "unknown"]
    optional_open = [key for key in optional_keys(state, taxonomy) if _can_ask(state, key, taxonomy)]
    issues_unclear = any(item.status not in {"known", "not_applicable"} for item in state.additional_issues)
    resolved = all(
        field_is_resolved(state.facts.get(key)) and not _needs_precision(state.facts.get(key)) for key in keys
    )
    if resolved and not conflicts and not unknowns and not optional_open and not issues_unclear:
        return Readiness(
            quality="sufficient_context", missing=[], conflicts=[], reason="The report has the material context.", next_key=None
        )
    candidates = _candidates(state, taxonomy)
    next_key = candidates[0] if candidates else None
    if (not candidates or allow_partial) and field_is_resolved(state.facts.get("issue")):
        return Readiness(
            quality="partial_context",
            missing=missing,
            conflicts=conflicts,
            reason="Some details are still unknown. The customer can review what we have.",
            next_key=next_key,
        )
    return Readiness(
        quality="collecting", missing=missing, conflicts=conflicts, reason="More context is needed.", next_key=next_key
    )
```

- [ ] **Step 5: Show the ask-once details in the review**

In `backend/app/intake/review.py`:
- Change the import to `from app.intake.policy import ask_once_keys, material_keys`.
- Add `"recipient_name": "اسم المستلم",` to `_LABELS`, after `"recipient_phone": "رقم المستلم",`.
- In `build_review`, replace `ordered = list(dict.fromkeys([*required, *state.facts, *state.additional_needed]))` with:

```python
    ordered = list(dict.fromkeys([*required, *ask_once_keys(state.category), *state.facts, *state.additional_needed]))
```

- [ ] **Step 6: Update the existing tests whose expectations the new field plan changes**

1. `backend/tests/intake/test_policy.py::test_unknown_material_fact_is_not_sufficient`: the transfer now also needs the recipient number, and the ask-once details must be settled for the report to be partial.
   - Build a second `Fact` the same way as `unknown`, for each of `recipient_name` and `txn_ref`.
   - Add `fact("recipient_phone", "07701234567", source, normalized="07701234567")` and those two unknown facts to the fact list.
   - The assertions stay the same.
2. `backend/tests/intake/test_policy.py::test_complete_transfer_is_sufficient`: replace the body after `source = ...` with:

```python
    facts = [
        fact("issue", source.text, source), fact("date", "أمس", source, normalized="2026-10-17"),
        fact("amount", "50000", source, normalized="50000"), fact("debited", "yes", source),
        fact("recipient_outcome", "not received", source),
        fact("recipient_phone", "07701234567", source, normalized="07701234567"),
        fact("recipient_name", "علي", source), fact("txn_ref", "ZC1", source, normalized="ZC1"),
    ]
    readiness = assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy)
    assert readiness.quality == "sufficient_context"
    assert readiness.missing == []
```

3. `backend/tests/intake/test_review.py:52`: add `"recipient_phone"` to the `fact_keys` list.
4. `backend/tests/intake/test_handoff.py`:
   - Line 17 becomes `_MATERIAL = ["issue", "actual", "expected", "date", "amount", "debited", "recipient_outcome", "recipient_phone"]`.
   - In `_opening`, after `fact("recipient_outcome", "", source, status="unknown"),`, add:

```python
            fact("recipient_phone", "", source, status="unknown"),
            fact("recipient_name", "", source, status="unknown"),
            fact("txn_ref", "", source, status="unknown"),
```

- [ ] **Step 7: Run the intake suite**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake"`
Expected: PASS.
- If another existing intake test fails **only** because the new field plan changes which keys are required or asked, update that expectation the same way as Step 6, and list each change in your report.
- Any other failure is a bug in your change. Fix the code, not the test.

- [ ] **Step 8: Lint and commit**

Run the backend lint command (Global Constraints). Expected: no errors.

```bash
git add backend/app/intake/contracts.py backend/app/intake/policy.py backend/app/intake/review.py backend/tests/intake/test_interview_policy.py backend/tests/intake/test_policy.py backend/tests/intake/test_review.py backend/tests/intake/test_handoff.py
git commit -m "feat(intake): plan required and ask-once details per problem type"
```

---

### Task 2: Prompt rules and the `recipient_name` vocabulary

**Files:**
- Modify: `backend/app/intake/prompts/intake_v1.md`
- Modify: `backend/app/intake/prompts/review_v1.md`
- Create: `backend/tests/intake/test_prompts.py`

**Interfaces:**
- Consumes: the fact key `recipient_name` from Task 1.
- Produces: prompt text only. No code interfaces.

- [ ] **Step 1: Write the failing test**

Create `backend/tests/intake/test_prompts.py`:

```python
from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[2] / "app" / "intake" / "prompts"


def test_intake_prompt_knows_the_recipient_name_and_implied_answers():
    text = (PROMPTS / "intake_v1.md").read_text(encoding="utf-8")
    vocabulary = next(line for line in text.splitlines() if line.startswith("- Fact keys in updates:"))
    assert "recipient_name" in vocabulary
    assert "ما وصلت" in text and "انقطعت" in text
    assert "reason" in text and "why" in text.lower()


def test_review_prompt_asks_for_a_narrative_not_a_field_list():
    text = (PROMPTS / "review_v1.md").read_text(encoding="utf-8")
    assert "narrative" in text
    assert "label: value" in text
```

- [ ] **Step 2: Run it to verify it fails**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_prompts.py"`
Expected: FAIL on `assert "recipient_name" in vocabulary`.

- [ ] **Step 3: Update `intake_v1.md`**

1. In the line starting `- Fact keys in updates:`, insert `recipient_name, ` directly after `recipient_phone, `.
2. Replace the line `- The customer's own phone (customer_phone) is already known from sign-in. Never send a customer_phone update. Map a recipient number to recipient_phone.` with:

```markdown
- The customer's own phone (customer_phone) is already known from sign-in. Never send a customer_phone update. Map a recipient number to recipient_phone and a recipient's name to recipient_name. Never put a name in recipient_phone.
- Record what the customer already implied, quoting their words: "ما وصلت", "ما وصلتله", "ما وصل" or "didn't arrive" means recipient_outcome is known with normalized "no"; "انقطعت من رصيدي", "انخصمت" or "was deducted" means debited is known with normalized "yes". Never ask about a detail the customer already stated.
- For a money problem (transfer, wrong recipient, bill, agent, refund) the expected outcome is implied. Do not ask what they expected.
- If questions shows a key was asked once and is still missing, you may ask it once more with different wording.
- suggested_question.reason is one short sentence in the customer's language that tells the customer why this detail helps, for example "حتى نعرف إذا الفلوس طلعت من محفظتك.".
```

- [ ] **Step 4: Update `review_v1.md`**

Append these rules after the last line:

```markdown
- customer_text is a short neutral narrative of what happened, two or three sentences. Do not list fields as label: value pairs, because the application shows the details list separately. Do not address the customer as "you"; the same Arabic text is the employee summary.
```

- [ ] **Step 5: Run the prompt tests and the model tests**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_prompts.py tests/intake/test_model.py"`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/intake/prompts/intake_v1.md backend/app/intake/prompts/review_v1.md backend/tests/intake/test_prompts.py
git commit -m "feat(intake): teach the intake prompt implied answers and the recipient name"
```

---

### Task 3: Session projection — pending question, progress, question metadata

**Files:**
- Modify: `backend/app/intake/contracts.py` (add `PendingQuestion` and `ProgressItem`; extend `SessionView`)
- Modify: `backend/app/intake/policy.py` (add `progress` and `pending_question`)
- Modify: `backend/app/intake/graph.py` (`_merge` sets `next_key`; `_ask` stores the reason and the attempt)
- Modify: `backend/app/intake/repository.py::session_view`
- Create: `backend/tests/intake/test_interview_api.py`

**Interfaces:**
- Consumes (from Task 1): `AskedQuestion`, `answer_kind`, `answer_choices`, `material_keys`, `optional_keys`.
- Produces, in contracts:
  - `class PendingQuestion(IntakeModel)` with fields `key: str`, `message_id: UUID`, `text: str`, `reason: str`, `answer_kind: AnswerKind`, `choices: list[Choice]`, `attempt: int`.
  - `class ProgressItem(IntakeModel)` with fields `key: str`, `tier: Literal["required", "ask_once"]`, `status: FactStatus`, `display: str | None = None`.
  - `SessionView.pending_question: PendingQuestion | None = None`
  - `SessionView.progress: list[ProgressItem] = []`
- Produces, in policy:
  - `progress(state, taxonomy=None) -> list[ProgressItem]`
  - `pending_question(state, messages, phase) -> PendingQuestion | None`

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/intake/test_interview_api.py`:

```python
"""Guided interview over the real intake API with the scripted model."""
from __future__ import annotations

from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, QuestionRecord
from tests.intake.helpers import fact

pytestmark = pytest.mark.integration

VAGUE = "حولت فلوس وما وصلت"


def user_message(turn):
    return next(item for item in reversed(turn.messages) if item.role == "user")


def opening(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[
        fact("issue", source.text, source),
        fact("recipient_outcome", "ما وصلت", source, normalized="no"),
    ])


def start(client, text=VAGUE):
    created = client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
    case = {
        "sid": created["credentials"]["session_id"],
        "headers": {"Authorization": f"Bearer {created['credentials']['token']}"},
        "view": created["session"],
    }
    send(client, case, text)
    return case


def send(client, case, text, answer_to=None, status=200):
    body = {
        "request_id": str(uuid4()), "expected_revision": case["view"]["revision"],
        "text": text, "language": "ar", "attachment_ids": [],
    }
    if answer_to is not None:
        body["answer_to"] = answer_to
    response = client.post(f"/api/intake/sessions/{case['sid']}/messages", headers=case["headers"], json=body)
    assert response.status_code == status, response.text
    if status == 200:
        case["view"] = response.json()
    return response


def analyze_calls(client):
    return sum(1 for call in client.model.calls if call[0] == "analyze")


def test_new_session_has_no_question_or_progress(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
    assert created["session"]["pending_question"] is None
    assert created["session"]["progress"] == []


def test_session_exposes_the_pending_question_and_progress(intake_client):
    intake_client.model.analyses = [opening]
    view = start(intake_client)["view"]
    pending = view["pending_question"]
    assert pending == {
        "key": "amount", "message_id": view["messages"][-1]["id"], "text": "شكد المبلغ؟",
        "reason": "يساعدنا نلگه العملية.", "answer_kind": "amount", "choices": ["unknown"], "attempt": 1,
    }
    assert view["readiness"]["next_key"] == "amount"
    progress = {item["key"]: item for item in view["progress"]}
    assert list(progress) == [
        "issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone", "recipient_name", "txn_ref",
    ]
    assert progress["issue"] == {"key": "issue", "tier": "required", "status": "known", "display": VAGUE}
    assert progress["recipient_outcome"]["display"] == "no"
    assert progress["amount"] == {"key": "amount", "tier": "required", "status": "missing", "display": None}
    assert progress["txn_ref"]["tier"] == "ask_once"


def test_review_has_no_pending_question(reviewed):
    assert reviewed["view"]["pending_question"] is None


def test_records_from_before_question_metadata_still_load():
    record = QuestionRecord.model_validate(
        {"key": "amount", "basis_revision": 1, "message_id": str(uuid4()), "outcome": "asked"}
    )
    assert record.reason == "" and record.attempt == 1
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_interview_api.py"`
Expected: FAIL with `KeyError: 'pending_question'`.

- [ ] **Step 3: Add the contracts**

In `backend/app/intake/contracts.py`, add these after the `Readiness` class:

```python
class PendingQuestion(IntakeModel):
    key: str
    message_id: UUID
    text: str
    reason: str
    answer_kind: AnswerKind
    choices: list[Choice] = Field(default_factory=list)
    attempt: int = 1


class ProgressItem(IntakeModel):
    key: str
    tier: Literal["required", "ask_once"]
    status: FactStatus
    display: str | None = None
```

In `SessionView`, add after `error_code: str | None = None`:

```python
    pending_question: PendingQuestion | None = None
    progress: list[ProgressItem] = Field(default_factory=list)
```

- [ ] **Step 4: Add `progress` and `pending_question` to the policy**

In `backend/app/intake/policy.py`, extend the contracts import to:

```python
from app.intake.contracts import (
    AnswerKind,
    AskedQuestion,
    Choice,
    Fact,
    IntakeState,
    Message,
    PendingQuestion,
    ProgressItem,
    Question,
    Readiness,
)
```

Append to the end of the file:

```python
def progress(state: IntakeState, taxonomy: Taxonomy | None = None) -> list[ProgressItem]:
    if not any(key != "customer_phone" for key in state.facts):
        return []
    items: list[ProgressItem] = []
    tiers = (("required", material_keys(state.category, taxonomy)), ("ask_once", optional_keys(state, taxonomy)))
    for tier, keys in tiers:
        for key in keys:
            item = state.facts.get(key)
            known = item is not None and item.status == "known"
            items.append(ProgressItem(
                key=key, tier=tier, status=item.status if item is not None else "missing",
                display=(item.normalized or item.value) if known else None,
            ))
    return items


def pending_question(state: IntakeState, messages: list[Message], phase: str) -> PendingQuestion | None:
    if phase != "collecting" or not state.questions or not messages:
        return None
    record = state.questions[-1]
    latest = messages[-1]
    if latest.role != "assistant" or latest.id != record.message_id:
        return None
    return PendingQuestion(
        key=record.key, message_id=record.message_id, text=latest.text, reason=record.reason,
        answer_kind=answer_kind(record.key), choices=answer_choices(record.key), attempt=record.attempt,
    )
```

- [ ] **Step 5: Store the question metadata and the real next key in the graph**

In `backend/app/intake/graph.py`:

Replace `_merge` with:

```python
    def _merge(self, state: dict) -> dict:
        merged = merge_analysis(state["context"], state["analysis"], visible_image_ids=state["visible_image_ids"])
        readiness = assess_readiness(merged, self.taxonomy)
        question = choose_question(
            merged, state["analysis"].suggested_question, state["context"].revision + 1, self.taxonomy
        )
        readiness = readiness.model_copy(update={"next_key": question.key if question is not None else None})
        return {**state, "state": merged.model_copy(update={"readiness": readiness}), "question": question}
```

Replace `_ask` with:

```python
    @staticmethod
    def _ask(state: dict) -> dict:
        question = state["question"]
        record = QuestionRecord(
            key=question.key, basis_revision=question.basis_revision, message_id=uuid4(), outcome="asked",
            reason=question.reason, attempt=getattr(question, "attempt", 1),
        )
        updated = state["state"].model_copy(update={"questions": [*state["state"].questions, record]})
        return {**state, "state": updated, "assistant_text": question.text, "review": None}
```

- [ ] **Step 6: Project the new fields**

In `backend/app/intake/repository.py`:
- Add the import `from app.intake.policy import pending_question, progress`.
- Replace `session_view` with:

```python
def session_view(session: Session, row: IntakeSessionRow) -> SessionView:
    state = IntakeState.model_validate(row.state)
    messages = load_messages(session, row.id)
    return SessionView(
        id=row.id,
        revision=row.revision,
        phase=row.phase,
        language=row.language,
        customer_phone=row.customer_phone,
        turn_status=row.turn_status,
        active_request_id=row.active_request_id,
        messages=messages,
        attachments=load_attachments(session, row.id),
        readiness=state.readiness,
        review=customer_review(row.review),
        receipt=receipt_for(session, row),
        error_code=row.error_code,
        pending_question=pending_question(state, messages, row.phase),
        progress=progress(state),
    )
```

- [ ] **Step 7: Run the intake suite**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake"`
Expected: PASS.

- [ ] **Step 8: Lint and commit**

```bash
git add backend/app/intake/contracts.py backend/app/intake/policy.py backend/app/intake/graph.py backend/app/intake/repository.py backend/tests/intake/test_interview_api.py
git commit -m "feat(intake): expose the pending question and interview progress"
```

---

### Task 4: Quick-reply answers without a model call

**Files:**
- Create: `backend/app/intake/answers.py`
- Modify: `backend/app/intake/graph.py` (`advance` accepts `answer`)
- Modify: `backend/app/intake/service.py::_execute`
- Modify: `backend/app/intake/turns.py` (validate `answer_to` in `claim`)
- Modify: `backend/app/api/intake_schemas.py` (`AnswerTo`, `MessageInput.answer_to`)
- Modify: `backend/app/api/intake.py::post_message`
- Test: `backend/tests/intake/test_interview_api.py`

**Interfaces:**
- Consumes (from Task 3): `pending_question(state, messages, phase)`.
- Produces:
  - `app.intake.answers.quick_answer(context: TurnContext, key: str, choice: str) -> Analysis`
  - `IntakeGraph.advance(context, answer: dict | None = None)`. `answer` has the keys `message_id`, `key` and `choice`.
- HTTP: `POST /messages` accepts an optional `answer_to: {message_id: UUID, key: str, choice: "yes" | "no" | "unknown"}`.

- [ ] **Step 1: Write the failing tests**

Append to `backend/tests/intake/test_interview_api.py`:

```python
def opening_with_amount(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[
        fact("issue", source.text, source),
        fact("amount", "50000", source),
        fact("date", "2026-10-06", source),
        fact("recipient_outcome", "ما وصلت", source, normalized="no"),
    ])


def test_quick_reply_is_recorded_without_the_model(intake_client):
    intake_client.model.analyses = [opening_with_amount]
    case = start(intake_client, "حولت 50000 بتاريخ 2026-10-06 وما وصلت")
    pending = case["view"]["pending_question"]
    assert pending["key"] == "debited"
    before = analyze_calls(intake_client)
    send(intake_client, case, "اي", answer_to={"message_id": pending["message_id"], "key": "debited", "choice": "yes"})
    assert analyze_calls(intake_client) == before
    progress = {item["key"]: item for item in case["view"]["progress"]}
    assert progress["debited"]["status"] == "known"
    assert progress["debited"]["display"] == "yes"
    assert case["view"]["messages"][-2]["text"] == "اي"
    assert case["view"]["pending_question"]["key"] == "recipient_phone"


def test_quick_unknown_marks_the_detail_unknown(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    send(intake_client, case, "ما أعرف", answer_to={"message_id": pending["message_id"], "key": "amount", "choice": "unknown"})
    progress = {item["key"]: item for item in case["view"]["progress"]}
    assert progress["amount"]["status"] == "unknown"
    assert case["view"]["pending_question"]["key"] == "date"


def test_quick_reply_for_another_question_is_rejected(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    messages = len(case["view"]["messages"])
    response = send(intake_client, case, "اي", answer_to={
        "message_id": pending["message_id"], "key": "debited", "choice": "yes",
    }, status=409)
    assert response.json()["detail"]["code"] == "revision_conflict"
    stale = send(intake_client, case, "ما أعرف", answer_to={
        "message_id": str(uuid4()), "key": "amount", "choice": "unknown",
    }, status=409)
    assert stale.json()["detail"]["code"] == "revision_conflict"
    current = intake_client.get(f"/api/intake/sessions/{case['sid']}", headers=case["headers"]).json()
    assert len(current["messages"]) == messages


def test_attach_is_not_a_message_answer(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    pending = case["view"]["pending_question"]
    send(intake_client, case, "x", answer_to={"message_id": pending["message_id"], "key": "amount", "choice": "attach"}, status=422)
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_interview_api.py"`
Expected: FAIL. The quick-reply tests return 422 because `answer_to` is an extra field and the body forbids extra fields.

- [ ] **Step 3: Accept `answer_to` over HTTP**

In `backend/app/api/intake_schemas.py`, add before `MessageInput`:

```python
class AnswerTo(IntakeBody):
    message_id: UUID
    key: str = Field(min_length=1, max_length=64)
    choice: Literal["yes", "no", "unknown"]
```

Add this field to `MessageInput`, after `attachment_ids`:

```python
    answer_to: AnswerTo | None = None
```

In `backend/app/api/intake.py::post_message`, change `body.model_dump()` to `body.model_dump(exclude_none=True)`. This keeps the request fingerprint of a plain message identical to its fingerprint before this change.

- [ ] **Step 4: Validate the answer when the turn is claimed**

In `backend/app/intake/turns.py`:
- Add the imports `from app.intake.contracts import IntakeState` (merge it into the existing contracts import) and `from app.intake.policy import pending_question`. Add `load_messages` to the existing `from app.intake.repository import (...)` list.
- In `claim`, replace:

```python
            if kind == "message":
                customer_message = self._append_customer_message(session, row, payload, now)
```

with:

```python
            if kind == "message":
                if payload.get("answer_to") is not None:
                    self._check_answer(session, row, payload["answer_to"])
                customer_message = self._append_customer_message(session, row, payload, now)
```

- Add this method to `TurnStore`, just before `_locked_attempt`:

```python
    @staticmethod
    def _check_answer(session, row: IntakeSessionRow, answer: dict) -> None:
        state = IntakeState.model_validate(row.state)
        pending = pending_question(state, load_messages(session, row.id), row.phase)
        choice = answer.get("choice")
        if (
            pending is None or str(pending.message_id) != str(answer.get("message_id"))
            or pending.key != answer.get("key") or choice not in pending.choices or choice == "attach"
        ):
            raise RevisionConflict("Reload the current conversation.")
```

- [ ] **Step 5: Record the answer without the model**

Create `backend/app/intake/answers.py`:

```python
"""Record a tapped quick reply without asking the model to interpret it."""
from __future__ import annotations

from app.intake.contracts import Analysis, EvidenceRef, Fact, TurnContext
from app.intake.errors import InvalidEvidence


def quick_answer(context: TurnContext, key: str, choice: str) -> Analysis:
    source = next(
        (item for item in context.messages if item.id == context.current_message_id and item.role == "user"), None
    )
    if source is None or not source.text.strip():
        raise InvalidEvidence("Send the answer as a message.")
    evidence = [EvidenceRef(kind="message", source_id=source.id, quote=source.text)]
    if choice == "unknown":
        update = Fact(key=key, status="unknown", evidence=evidence)
    elif choice in {"yes", "no"}:
        update = Fact(key=key, status="known", value=source.text, normalized=choice, evidence=evidence)
    else:
        raise InvalidEvidence("Choose one of the offered answers.")
    return Analysis(language=source.language, category=context.state.category, updates=[update])
```

In `backend/app/intake/graph.py`:
- Add the import `from app.intake.answers import quick_answer`.
- Replace `advance` with:

```python
    async def advance(self, context: TurnContext, answer: dict | None = None) -> TurnResult:
        budget = await self._budget(context)
        try:
            if answer is not None:
                outcome = await self._answer(context, answer, budget)
            else:
                outcome = await self._compiled.ainvoke({
                    "context": context,
                    "images": self._images(context, [item for item in context.messages if item.id == context.current_message_id]),
                    "budget": budget,
                    "trace": [],
                })
        except IntakeError as exc:
            exc.trace = list(budget.trace or exc.trace)
            raise
        return TurnResult(outcome["state"], outcome.get("assistant_text"), outcome.get("review"), outcome.get("trace", []))

    async def _answer(self, context: TurnContext, answer: dict, budget: ModelBudget) -> dict:
        analysis = quick_answer(context, answer["key"], answer["choice"])
        state = self._merge({
            "context": context, "analysis": analysis, "visible_image_ids": set(), "budget": budget, "trace": [],
        })
        if self._route(state) == "review":
            return await self._review(state)
        return self._ask(state)
```

In `backend/app/intake/service.py::_execute`, replace `result = await self.graph.advance(claim.context)` with:

```python
                result = await self.graph.advance(claim.context, answer=claim.payload.get("answer_to"))
```

- [ ] **Step 6: Run the intake suite**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake"`
Expected: PASS.

- [ ] **Step 7: Lint and commit**

```bash
git add backend/app/intake/answers.py backend/app/intake/graph.py backend/app/intake/service.py backend/app/intake/turns.py backend/app/api/intake_schemas.py backend/app/api/intake.py backend/tests/intake/test_interview_api.py
git commit -m "feat(intake): record quick-reply answers without a model call"
```

---

### Task 5: Let the customer choose a detail to answer (`/ask`)

**Files:**
- Modify: `backend/app/intake/graph.py` (add `ask`)
- Modify: `backend/app/intake/service.py` (add `ask`; dispatch kind `ask`)
- Modify: `backend/app/intake/turns.py` (accept kind `ask`; add `_check_ask`)
- Modify: `backend/app/api/intake_schemas.py` (`AskInput`)
- Modify: `backend/app/api/intake.py` (route `POST /sessions/{id}/ask`)
- Test: `backend/tests/intake/test_interview_api.py`

**Interfaces:**
- Consumes: `ask_for(state, key, revision)` (Task 1) and `progress(state)` (Task 3).
- Produces:
  - `IntakeGraph.ask(context, key) -> TurnResult`
  - `IntakeService.ask(credentials, command) -> SessionView`
  - HTTP `POST /api/intake/sessions/{id}/ask` with body `{request_id, expected_revision, key}`. It returns a `SessionView`.

- [ ] **Step 1: Write the failing tests**

Change the contracts import at the top of `backend/tests/intake/test_interview_api.py` to `from app.intake.contracts import Analysis, QuestionRecord, ReviewText`.

The scripted model's default summary only lists `issue`. A transfer review needs every required key, so these tests script their own summary.

Append to the same file:

```python
COMPLETE = "حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123"


def summary(state, language):
    return ReviewText(customer_text="التحويل ما وصل.", employee_text_ar="التحويل ما وصل.", fact_keys=list(state.facts))


def complete_without_reference(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[
        fact("issue", source.text, source), fact("amount", "50000", source), fact("date", "2026-10-06", source),
        fact("debited", "انقطعت من رصيدي", source, normalized="yes"),
        fact("recipient_outcome", "ما وصلتله", source, normalized="no"),
        fact("recipient_phone", "07701234567", source), fact("recipient_name", "علي حسين", source),
        fact("txn_ref", "", source, status="unknown"),
    ])


def reference_answer(turn):
    source = user_message(turn)
    return Analysis(language="ar", category="failed_transfer", updates=[fact("txn_ref", "ZC2410000123", source)])


def ask(client, case, key, status=200):
    response = client.post(f"/api/intake/sessions/{case['sid']}/ask", headers=case["headers"], json={
        "request_id": str(uuid4()), "expected_revision": case["view"]["revision"], "key": key,
    })
    assert response.status_code == status, response.text
    if status == 200:
        case["view"] = response.json()
    return response


def test_customer_can_answer_a_detail_from_the_review(intake_client):
    intake_client.model.analyses = [complete_without_reference, reference_answer]
    intake_client.model.reviews = [summary, summary]
    case = start(intake_client, COMPLETE.replace(" رقم العملية ZC2410000123", ""))
    assert case["view"]["review"]["quality"] == "sufficient_context"
    calls = len(intake_client.model.calls)
    ask(intake_client, case, "txn_ref")
    assert len(intake_client.model.calls) == calls
    view = case["view"]
    assert view["review"] is None and view["phase"] == "collecting"
    assert view["messages"][-1]["text"] == "عدك رقم عملية أو مرجع؟"
    assert view["pending_question"]["key"] == "txn_ref"
    assert view["pending_question"]["choices"] == ["unknown", "attach"]
    send(intake_client, case, "ZC2410000123")
    assert case["view"]["review"]["facts"]["txn_ref"]["normalized"] == "ZC2410000123"


def test_ask_rejects_a_detail_outside_the_plan(intake_client):
    intake_client.model.analyses = [opening]
    case = start(intake_client)
    response = ask(intake_client, case, "card_symptom", status=422)
    assert response.json()["detail"]["code"] == "invalid_evidence"
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_interview_api.py -k ask"`
Expected: FAIL with 404 (no route).

- [ ] **Step 3: Add the HTTP surface**

In `backend/app/api/intake_schemas.py`, add after `ReviewInput`:

```python
class AskInput(IntakeBody):
    request_id: UUID
    expected_revision: int = Field(ge=0)
    key: str = Field(min_length=1, max_length=64)
```

In `backend/app/api/intake.py`:
- Add `AskInput` to the schema import.
- Add this route after `request_review`:

```python
@router.post("/sessions/{session_id}/ask")
async def ask_question(session_id: UUID, body: AskInput, request: Request):
    view = await request.app.state.intake.ask(_credentials(request, session_id), body.model_dump())
    return JSONResponse(_dump(view), status_code=_status(view, body.request_id))
```

- [ ] **Step 4: Claim and run the operation**

In `backend/app/intake/turns.py`:
- Add `progress` to the policy import: `from app.intake.policy import pending_question, progress`.
- In `claim`, replace `elif kind != "review":` with:

```python
            elif kind == "ask":
                self._check_ask(row, payload.get("key"))
            elif kind != "review":
```

- Add this method next to `_check_answer`:

```python
    @staticmethod
    def _check_ask(row: IntakeSessionRow, key) -> None:
        state = IntakeState.model_validate(row.state)
        if not key or key not in {item.key for item in progress(state)}:
            raise InvalidEvidence("That detail cannot be asked here.")
```

In `backend/app/intake/graph.py`:
- Add `ask_for` to the policy import.
- Add this method after `review`:

```python
    def ask(self, context: TurnContext, key: str) -> TurnResult:
        question = ask_for(context.state, key, context.revision + 1)
        readiness = assess_readiness(context.state, self.taxonomy).model_copy(update={"next_key": key})
        outcome = self._ask({"state": context.state.model_copy(update={"readiness": readiness}), "question": question})
        return TurnResult(outcome["state"], outcome["assistant_text"], None, [])
```

In `backend/app/intake/service.py`:
- Add after `review`:

```python
    async def ask(self, credentials: Credentials, command: dict) -> SessionView:
        return await self._perform(credentials, "ask", command)
```

- In `_execute`, add a branch between the `review` branch and the `else`:

```python
            elif claim.kind == "ask":
                result = self.graph.ask(claim.context, claim.payload["key"])
```

- [ ] **Step 5: Run the intake suite**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake"`
Expected: PASS.

- [ ] **Step 6: Lint and commit**

```bash
git add backend/app/intake/graph.py backend/app/intake/service.py backend/app/intake/turns.py backend/app/api/intake_schemas.py backend/app/api/intake.py backend/tests/intake/test_interview_api.py
git commit -m "feat(intake): let the customer choose a missing detail to answer"
```

---

### Task 6: Backend acceptance scenarios

**Files:**
- Create: `backend/tests/intake/test_interview_scenarios.py`
- Modify: `backend/tests/intake/live_probe.py` (add a `transfers` mode)

**Interfaces:**
- Consumes: everything from Tasks 1–5 through HTTP.
- Produces: tests only, plus the opt-in live probe mode `python -m tests.intake.live_probe transfers`.

- [ ] **Step 1: Write the scenario tests**

Create `backend/tests/intake/test_interview_scenarios.py`:

```python
"""The vague-to-complete transfer interview from the design, end to end."""
from __future__ import annotations

from uuid import uuid4

import pytest

from app.intake.contracts import Analysis, ReviewText
from tests.intake.helpers import fact

pytestmark = pytest.mark.integration

VAGUE = "حولت فلوس وما وصلت"
COMPLETE = "حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123"
REQUIRED = ["issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"]


def source_of(turn):
    return next(item for item in reversed(turn.messages) if item.role == "user")


def updates(*builders):
    def analyze(turn):
        source = source_of(turn)
        return Analysis(language="ar", category="failed_transfer", updates=[build(source) for build in builders])
    return analyze


def summary(state, language):
    return ReviewText(customer_text="التحويل ما وصل للمستلم.", employee_text_ar="التحويل ما وصل للمستلم.",
                      fact_keys=[*REQUIRED, *state.facts])


class Chat:
    def __init__(self, client):
        self.client = client
        created = client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07809876543"}).json()
        self.sid = created["credentials"]["session_id"]
        self.headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
        self.view = created["session"]

    def say(self, text, answer_to=None):
        body = {"request_id": str(uuid4()), "expected_revision": self.view["revision"], "text": text,
                "language": "ar", "attachment_ids": []}
        if answer_to is not None:
            body["answer_to"] = answer_to
        response = self.client.post(f"/api/intake/sessions/{self.sid}/messages", headers=self.headers, json=body)
        assert response.status_code == 200, response.text
        self.view = response.json()
        return self.view

    def tap(self, text, choice):
        pending = self.view["pending_question"]
        return self.say(text, {"message_id": pending["message_id"], "key": pending["key"], "choice": choice})

    def asked(self):
        return self.view["pending_question"]["key"] if self.view["pending_question"] else None


def analyze_calls(client):
    return sum(1 for call in client.model.calls if call[0] == "analyze")


def test_vague_report_is_interviewed_into_a_complete_ticket(intake_client):
    intake_client.model.analyses = [
        updates(lambda s: fact("issue", s.text, s), lambda s: fact("recipient_outcome", "ما وصلت", s, normalized="no")),
        updates(lambda s: fact("amount", "50000", s)),
        updates(lambda s: fact("date", "2026-10-06", s)),
        updates(lambda s: fact("recipient_phone", "07701234567", s)),
        updates(lambda s: fact("recipient_name", "علي حسين", s)),
        updates(lambda s: fact("txn_ref", "ZC2410000123", s)),
    ]
    intake_client.model.reviews = [summary]
    chat = Chat(intake_client)
    asked = []
    chat.say(VAGUE)
    asked.append(chat.asked())
    chat.say("50000 دينار")
    asked.append(chat.asked())
    chat.say("2026-10-06")
    asked.append(chat.asked())
    chat.tap("اي", "yes")
    asked.append(chat.asked())
    chat.say("07701234567")
    asked.append(chat.asked())
    chat.say("علي حسين")
    asked.append(chat.asked())
    view = chat.say("ZC2410000123")
    assert asked == ["amount", "date", "debited", "recipient_phone", "recipient_name", "txn_ref"]
    assert analyze_calls(intake_client) == 6
    review = view["review"]
    assert review["quality"] == "sufficient_context"
    facts = review["facts"]
    assert facts["amount"]["normalized"] == "50000"
    assert facts["date"]["normalized"] == "2026-10-06"
    assert facts["debited"]["normalized"] == "yes"
    assert facts["recipient_outcome"]["normalized"] == "no"
    assert facts["recipient_phone"]["normalized"] == "07701234567"
    assert facts["recipient_name"]["value"] == "علي حسين"
    assert facts["txn_ref"]["normalized"] == "ZC2410000123"
    questions = [item["text"] for item in view["messages"] if item["role"] == "assistant"][:-1]
    assert len(questions) == len(set(questions)) == 6


def test_complete_report_goes_straight_to_review(intake_client):
    intake_client.model.analyses = [updates(
        lambda s: fact("issue", s.text, s), lambda s: fact("amount", "50000", s), lambda s: fact("date", "2026-10-06", s),
        lambda s: fact("debited", "انقطعت من رصيدي", s, normalized="yes"),
        lambda s: fact("recipient_outcome", "ما وصلتله", s, normalized="no"),
        lambda s: fact("recipient_phone", "07701234567", s), lambda s: fact("recipient_name", "علي حسين", s),
        lambda s: fact("txn_ref", "ZC2410000123", s),
    )]
    intake_client.model.reviews = [summary]
    view = Chat(intake_client).say(COMPLETE)
    assert view["review"]["quality"] == "sufficient_context"
    assert view["pending_question"] is None
    assert [item["role"] for item in view["messages"]] == ["user", "assistant"]
    assert view["messages"][-1]["text"] == "راجع التفاصيل قبل الإرسال."


def test_no_reference_number_still_gives_a_complete_report(intake_client):
    intake_client.model.analyses = [updates(
        lambda s: fact("issue", s.text, s), lambda s: fact("amount", "50000", s), lambda s: fact("date", "2026-10-06", s),
        lambda s: fact("debited", "انقطعت من رصيدي", s, normalized="yes"),
        lambda s: fact("recipient_outcome", "ما وصلتله", s, normalized="no"),
        lambda s: fact("recipient_phone", "07701234567", s), lambda s: fact("recipient_name", "علي حسين", s),
    )]
    intake_client.model.reviews = [summary]
    chat = Chat(intake_client)
    chat.say(COMPLETE.replace(" رقم العملية ZC2410000123", ""))
    assert chat.asked() == "txn_ref"
    view = chat.tap("ما عندي رقم", "unknown")
    assert view["review"]["quality"] == "sufficient_context"
    assert view["review"]["facts"]["txn_ref"]["status"] == "unknown"
    assert analyze_calls(intake_client) == 1
```

- [ ] **Step 2: Run the scenarios**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short tests/intake/test_interview_scenarios.py"`
Expected: PASS. Tasks 1–5 already implement the behavior.
- If a scenario fails, that is a real defect in Tasks 1–5. Use superpowers:systematic-debugging, fix the production code and keep the test unchanged.
- Report the defect and the fix.

- [ ] **Step 3: Add the live `transfers` probe**

In `backend/tests/intake/live_probe.py`, add after `main()`:

```python
VAGUE = "حولت فلوس وما وصلت"
COMPLETE = "حولت 50000 دينار لعلي حسين على رقم 07701234567 بتاريخ 2026-10-06 وانقطعت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123"


async def transfers():
    settings = Settings()
    model = IntakeModel(settings)
    taxonomy = load_taxonomy(settings.taxonomy_path)
    for name, text in (("vague", VAGUE), ("complete", COMPLETE)):
        ctx = context([message(text)])
        budget = ModelBudget(settings.intake_timeout_s, settings.intake_max_model_requests)
        report = {"case": name, "model": settings.intake_model or settings.gemini_model}
        started = time.monotonic()
        try:
            result = await model.analyze(ctx, [], budget)
            merged = merge_analysis(ctx, result.value)
            merged = merged.model_copy(update={"readiness": assess_readiness(merged, taxonomy)})
            question = choose_question(merged, result.value.suggested_question, 1, taxonomy)
            report["category"] = merged.category
            report["facts"] = {key: {"status": item.status, "value": item.value, "normalized": item.normalized}
                               for key, item in merged.facts.items()}
            report["quality"] = merged.readiness.quality
            report["next_question"] = None if question is None else {
                "key": question.key, "text": question.text, "reason": question.reason,
            }
        except Exception as error:
            report["error_type"] = type(error).__name__
        report["latency_s"] = round(time.monotonic() - started, 3)
        report["trace"] = budget.trace
        print(json.dumps(report, ensure_ascii=False))
```

Replace the `if __name__ == "__main__":` block with:

```python
if __name__ == "__main__":
    import sys

    asyncio.run(transfers() if sys.argv[1:] == ["transfers"] else main())
```

Also update the module docstring's first line to: `"""Opt-in live checks: uv run python -m tests.intake.live_probe [transfers].`. Do **not** run the live probe in this task; it makes paid calls. Task 11 runs it.

- [ ] **Step 4: Run the whole backend suite and lint**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short"`
Expected: PASS.

Run the backend lint command. Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add backend/tests/intake/test_interview_scenarios.py backend/tests/intake/live_probe.py
git commit -m "test(intake): pin the vague-to-complete transfer interview"
```

---

### Task 7: Customer frontend data layer

**Files:**
- Modify: `users-frontend/apps/web/src/features/intake/types.ts`
- Modify: `users-frontend/apps/web/src/features/intake/contracts.ts`
- Modify: `users-frontend/apps/web/src/features/intake/api.ts`
- Modify: `users-frontend/apps/web/src/features/intake/controller.ts`
- Modify: `users-frontend/apps/web/src/features/intake/test/fixtures.ts`
- Test: `users-frontend/apps/web/src/features/intake/controller.test.ts`, `users-frontend/apps/web/src/features/intake/contracts.test.ts`

**Interfaces:**
- Consumes: the HTTP contract from Tasks 3–5.
- Produces, in `types.ts`:
  - `AnswerKind`, `Choice`, `PendingQuestion`, `ProgressItem`, `AnswerTo`, `AskCommand`
  - `SessionView.pending_question: PendingQuestion | null` and `SessionView.progress: ProgressItem[]`
  - `MessageCommand.answer_to?: AnswerTo`
  - `PendingOperation` gains `{ kind: "ask"; payload: AskCommand }`
- Produces, in `controller.ts`:
  - `export type Activity = "message" | "review" | "ask" | "upload" | "remove" | "submit"`
  - `ControllerState.activity: Activity | null` and `ControllerState.outgoing: MessageCommand | null`
  - `send(text, language, attachmentIds, answerTo?)` and `ask(key: string)`
- Produces, in `api.ts`: `IntakeApi.ask(credentials, command: AskCommand, signal?) => Promise<SessionView>`

- [ ] **Step 1: Write the failing tests**

Append inside the `describe("intake controller", ...)` block in `controller.test.ts`:

```ts
  it("sends a quick reply with the question it answers", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.send("اي", "ar", [], { message_id: "q1", key: "debited", choice: "yes" })
    expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({
      text: "اي",
      attachment_ids: [],
      answer_to: { message_id: "q1", key: "debited", choice: "yes" },
    })
  })

  it("asks for a chosen detail through the ask operation", async () => {
    const api = fakeApi()
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("ar", CUSTOMER_PHONE)
    await controller.ask("txn_ref")
    expect(vi.mocked(api.ask).mock.calls[0]?.[1]).toMatchObject({ key: "txn_ref", expected_revision: 1 })
  })

  it("exposes the outgoing message and the activity while it is in flight", async () => {
    const api = fakeApi()
    let release!: (view: SessionView) => void
    vi.mocked(api.message).mockImplementation(() => new Promise((resolve) => { release = resolve }))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    const sent = controller.send("hello", "en", [])
    await vi.waitFor(() => expect(controller.getSnapshot().busy).toBe(true))
    expect(controller.getSnapshot()).toMatchObject({ activity: "message", outgoing: { text: "hello" } })
    release(emptySession({ revision: 2 }))
    await sent
    expect(controller.getSnapshot()).toMatchObject({ busy: false, outgoing: null })
  })

  it("keeps an unsent message after a lost connection and resends it", async () => {
    const api = fakeApi()
    vi.mocked(api.message).mockRejectedValueOnce(new TypeError("offline"))
    vi.mocked(api.get).mockRejectedValueOnce(new TypeError("offline"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en", CUSTOMER_PHONE)
    await controller.send("hello", "en", [])
    expect(controller.getSnapshot().outgoing?.text).toBe("hello")
    expect(controller.getSnapshot().error).toBeTruthy()
    await controller.retry()
    const calls = vi.mocked(api.message).mock.calls
    expect(calls[1]?.[1].text).toBe("hello")
    expect(calls[1]?.[1].request_id).toBe(calls[0]?.[1].request_id)
  })
```

Append to `contracts.test.ts`:
- Add `parseSavedSession` to the `./contracts` import.
- Add these malformed cases to the `malformed` array:

```ts
  ["pending question kind", { ...populated, pending_question: { key: "amount", message_id: "m1", text: "?", reason: "", answer_kind: "money", choices: [], attempt: 1 } }],
  ["pending question choice", { ...populated, pending_question: { key: "amount", message_id: "m1", text: "?", reason: "", answer_kind: "amount", choices: ["maybe"], attempt: 1 } }],
  ["progress tier", { ...populated, progress: [{ key: "amount", tier: "later", status: "known", display: null }] }],
  ["progress status", { ...populated, progress: [{ key: "amount", tier: "required", status: "done", display: null }] }],
```

- Add these tests inside the describe block:

```ts
  it("fills the interview fields for an older server", () => {
    const older: Record<string, unknown> = { ...populated }
    delete older.pending_question
    delete older.progress
    expect(parseSession(older)).toMatchObject({ pending_question: null, progress: [] })
  })

  it("restores a saved quick reply and a saved ask", () => {
    const credentials = { session_id: "session-1", token: "token" }
    const answer = { request_id: "r1", expected_revision: 2, text: "اي", language: "ar", attachment_ids: [], answer_to: { message_id: "q1", key: "debited", choice: "yes" } }
    expect(parseSavedSession({ credentials, pending: { kind: "message", payload: answer } })?.pending).toEqual({ kind: "message", payload: answer })
    const ask = { request_id: "r2", expected_revision: 2, key: "txn_ref" }
    expect(parseSavedSession({ credentials, pending: { kind: "ask", payload: ask } })?.pending).toEqual({ kind: "ask", payload: ask })
    expect(parseSavedSession({ credentials, pending: { kind: "message", payload: { ...answer, answer_to: { key: "debited" } } } })).toBeNull()
  })
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test -- src/features/intake/controller.test.ts src/features/intake/contracts.test.ts"`
Expected: FAIL (`api.ask` is undefined; `activity` is missing).

- [ ] **Step 3: Extend the types**

In `types.ts`, add after `ProcessingStatus`:

```ts
export type AnswerKind = "yes_no" | "amount" | "phone" | "reference" | "date" | "text"
export type Choice = "yes" | "no" | "unknown" | "attach"
```

Add after the `Readiness` type:

```ts
export type PendingQuestion = {
  key: string
  message_id: string
  text: string
  reason: string
  answer_kind: AnswerKind
  choices: Choice[]
  attempt: number
}

export type ProgressItem = {
  key: string
  tier: "required" | "ask_once"
  status: Fact["status"]
  display: string | null
}

export type AnswerTo = {
  message_id: string
  key: string
  choice: "yes" | "no" | "unknown"
}
```

Then:
- Add `pending_question: PendingQuestion | null` and `progress: ProgressItem[]` to `SessionView`, after `error_code`.
- Add `answer_to?: AnswerTo` to `MessageCommand`.
- Add this type after `ReviewCommand`:

```ts
export type AskCommand = {
  request_id: string
  expected_revision: number
  key: string
}
```

- Add `| { kind: "ask"; payload: AskCommand }` to `PendingOperation`.

- [ ] **Step 4: Validate the new fields**

In `contracts.ts`:
- Add `AnswerTo`, `AskCommand`, `PendingQuestion` and `ProgressItem` to the type import.
- Add after `validReview`:

```ts
const ANSWER_KINDS = ["yes_no", "amount", "phone", "reference", "date", "text"]
const CHOICES = ["yes", "no", "unknown", "attach"]
const FACT_STATUSES = ["known", "missing", "unknown", "conflicting", "not_applicable"]

function validPendingQuestion(value: unknown): value is PendingQuestion {
  return isRecord(value) &&
    typeof value.key === "string" &&
    typeof value.message_id === "string" &&
    typeof value.text === "string" &&
    typeof value.reason === "string" &&
    ANSWER_KINDS.includes(String(value.answer_kind)) &&
    Array.isArray(value.choices) && value.choices.every((choice) => CHOICES.includes(String(choice))) &&
    typeof value.attempt === "number" && Number.isInteger(value.attempt) && value.attempt >= 1
}

function validProgressItem(value: unknown): value is ProgressItem {
  return isRecord(value) &&
    typeof value.key === "string" &&
    (value.tier === "required" || value.tier === "ask_once") &&
    FACT_STATUSES.includes(String(value.status)) &&
    nullableString(value.display)
}

function validAnswerTo(value: unknown): value is AnswerTo {
  return isRecord(value) &&
    typeof value.message_id === "string" && !!value.message_id &&
    typeof value.key === "string" && !!value.key &&
    (value.choice === "yes" || value.choice === "no" || value.choice === "unknown")
}
```

- In `parseSession`, add these conditions to the big `if`, right before `!nullableString(value.error_code)`:

```ts
      (value.pending_question !== undefined && value.pending_question !== null &&
        !validPendingQuestion(value.pending_question)) ||
      (value.progress !== undefined &&
        (!Array.isArray(value.progress) || !value.progress.every(validProgressItem))) ||
```

- Replace the final `return value as unknown as SessionView` with:

```ts
  const session = value as unknown as SessionView
  return { ...session, pending_question: session.pending_question ?? null, progress: session.progress ?? [] }
```

- Replace `validMessageCommand` with the version below, and add `validAskCommand`:

```ts
function validMessageCommand(value: unknown): value is MessageCommand {
  return requestIdentity(value) && typeof value.text === "string" &&
    language(value.language) && stringList(value.attachment_ids) &&
    (value.answer_to === undefined || validAnswerTo(value.answer_to))
}

function validAskCommand(value: unknown): value is AskCommand {
  return requestIdentity(value) && typeof value.key === "string" && !!value.key
}
```

- In `parsePendingOperation`, add before `return null`:

```ts
  if (value.kind === "ask" && validAskCommand(value.payload)) {
    return { kind: "ask", payload: value.payload }
  }
```

- [ ] **Step 5: Add `ask` to the API**

In `api.ts`:
- Add `AskCommand` to the type import.
- Add `ask(credentials: Credentials, command: AskCommand, signal?: AbortSignal): Promise<SessionView>` to `IntakeApi`.
- Add this implementation after `review`:

```ts
    async ask(credentials, command, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, "/ask"), {
        method: "POST",
        headers: authHeaders(credentials, true),
        body: JSON.stringify(command),
        signal,
      })
      return parseSession(await parseJson(response))
    },
```

- [ ] **Step 6: Update the fixtures**

In `test/fixtures.ts`:
- Add `pending_question: null,` and `progress: [],` to `emptySession`, before `...overrides`.
- Add `ask: vi.fn(async () => session),` to `fakeApi`, after `review`.

- [ ] **Step 7: Extend the controller**

In `controller.ts`:
- Add `AnswerTo` and `AskCommand` to the type import.
- Export the type `Activity`:

```ts
export type Activity = "message" | "review" | "ask" | "upload" | "remove" | "submit"
```

- Add `activity: Activity | null` and `outgoing: MessageCommand | null` to `ControllerState`. Add `activity: null, outgoing: null,` to `emptyState()`.
- Change `send` and `sendNow` to take `answerTo?: AnswerTo`:

```ts
  async send(text: string, language: Language, attachmentIds: string[], answerTo?: AnswerTo) {
    if (this.sendFlight) return this.sendFlight
    this.sendFlight = this.enqueue(async () => {
      if (this.unreconciled()) return
      await this.sendNow(text, language, attachmentIds, answerTo)
    }).finally(() => { this.sendFlight = null })
    return this.sendFlight
  }

  async ask(key: string) {
    return this.enqueue(async () => {
      if (this.unreconciled()) return
      await this.askNow(key)
    })
  }
```

- In `sendNow(text, language, attachmentIds, answerTo?: AnswerTo)`, build the new command as:

```ts
      : {
          request_id: crypto.randomUUID(),
          expected_revision: session.revision,
          text,
          language,
          attachment_ids: attachmentIds,
          ...(answerTo ? { answer_to: answerTo } : {}),
        }
```

  and pass `"message"` as a new third argument to `this.dispatch(...)`.
- Pass `"review"` as the third `dispatch` argument in `reviewNow`.
- Add `askNow` after `reviewNow`:

```ts
  private async askNow(key: string) {
    const session = this.requireSession()
    if (!session || session.turn_status === "processing") return
    const generation = this.generation
    const command: AskCommand = this.pending?.kind === "ask"
      ? this.pending.payload
      : { request_id: crypto.randomUUID(), expected_revision: session.revision, key }
    if (this.pending?.kind !== "ask") {
      this.pending = { kind: "ask", payload: command }
      this.persist()
    }
    await this.dispatch(generation, () => this.api.ask(this.credentials!, command, this.nextSignal()), "ask")
  }
```

- In `retryNow`:
  - Change the message branch to `return this.sendNow(command.text, command.language, command.attachment_ids, command.answer_to)`.
  - Add `if (this.pending?.kind === "ask") return this.askNow(this.pending.payload.key)` before the review branch.
  - Pass `"message"` as the retry dispatch's third argument (`this.dispatch(generation, () => this.api.retry(...), "message")`).
- Change `dispatch` to `private async dispatch(generation: number, run: () => Promise<SessionView>, activity: Activity)`. Its first `replace` becomes `this.replace({ ...this.snapshot, busy: true, activity, error: null, pollingExhausted: false })`.
- Set `activity` wherever `busy: true` is set directly:
  - `submitNow`: `{ ...this.snapshot, busy: true, activity: "submit", error: null }`
  - `uploadNow`: add `activity: "upload"`
  - `removeNow`: add `activity: "remove"`
  - `bootNow`: leave it unchanged, so `activity` stays `null`.
- Replace `replace` with:

```ts
  private replace(next: ControllerState) {
    this.snapshot = { ...next, outgoing: this.pending?.kind === "message" ? this.pending.payload : null }
    for (const listener of this.listeners) listener()
  }
```

- [ ] **Step 8: Run the frontend tests, typecheck and lint**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test && npm --workspace web run typecheck && npm --workspace web run lint"`
Expected: PASS. Fix any type errors in other test files that construct `SessionView` literals by adding `pending_question: null, progress: []`.

- [ ] **Step 9: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/types.ts users-frontend/apps/web/src/features/intake/contracts.ts users-frontend/apps/web/src/features/intake/api.ts users-frontend/apps/web/src/features/intake/controller.ts users-frontend/apps/web/src/features/intake/test/fixtures.ts users-frontend/apps/web/src/features/intake/controller.test.ts users-frontend/apps/web/src/features/intake/contracts.test.ts
```

Also add any other test file you changed in Step 8. Then commit:

```bash
git commit -m "feat(intake-app): carry quick replies, asks and interview state in the client"
```

---

### Task 8: Chat screen — instant bubble, typing, reasons, quick replies, composer hints

**Files:**
- Modify: `users-frontend/apps/web/src/components/ui/agent-chat.tsx`
- Modify: `users-frontend/apps/web/src/components/ui/agent-chat.test.tsx`
- Create: `users-frontend/apps/web/src/features/intake/composer.ts`
- Create: `users-frontend/apps/web/src/features/intake/QuestionExtras.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/copy.ts`, `locales/ar.json`, `locales/en.json`, `intake.css`
- Test: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`

**Interfaces:**
- Consumes (Task 7): `snapshot.activity`, `snapshot.outgoing`, `session.pending_question`, `controller.send(..., answerTo)`, `controller.retry()`.
- Produces:
  - `AgentChatProps.inputMode?: "text" | "tel" | "numeric"`
  - `AgentMessage.pending?: boolean`
  - `MessagePart` adds `{ type: "typing"; label: string }`
  - `composerHint(kind: AnswerKind | null, copy: IntakeCopy): { placeholder: string; inputMode: "text" | "tel" | "numeric" }`
  - `choiceLabel(choice: Choice, kind: AnswerKind, copy: IntakeCopy): string`
  - `<QuestionExtras question copy interactive attachInputId attachDisabled onAnswer />`
- New `IntakeCopy` keys: `whyPrefix`, `quickReplies`, `choiceYes`, `choiceNo`, `choiceUnknown`, `choiceNoReference`, `choiceAttach`, `hintPhone`, `hintAmount`, `hintReference`, `hintDate`, `typing`, `sending`, `uploading`, `removing`, `submitting`, `notSent`, `resend`. Plus `fieldLabels.recipient_name`.

- [ ] **Step 1: Write the failing tests**

Append to `agent-chat.test.tsx`:

```tsx
describe("AgentChat interview parts", () => {
  it("renders a typing indicator, a pending user bubble and the input mode", () => {
    render(
      <AgentChat
        inputMode="tel"
        messages={[
          { id: "u", role: "user", pending: true, parts: [{ type: "text", text: "hello" }] },
          { id: "t", role: "assistant", parts: [{ type: "typing", label: "Support is typing…" }] },
        ]}
      />
    )
    expect(screen.getByRole("img", { name: "Support is typing…" })).toBeVisible()
    expect(screen.getByText("hello")).toHaveClass("opacity-60")
    expect(screen.getByRole("textbox")).toHaveAttribute("inputmode", "tel")
  })
})
```

Append to `IntakePage.test.tsx`:
- Add `import type { Choice, PendingQuestion } from "./types"` next to the existing type import.
- Add these tests:

```tsx
function asking(question: PendingQuestion): Partial<SessionView> {
  return {
    messages: [{ id: question.message_id, role: "assistant", text: question.text, language: "ar", created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }],
    pending_question: question,
  }
}

const debited: PendingQuestion = {
  key: "debited", message_id: "q1", text: "انخصم المبلغ من محفظتك؟", reason: "حتى نعرف إذا الفلوس طلعت من محفظتك.",
  answer_kind: "yes_no", choices: ["yes", "no", "unknown"] as Choice[], attempt: 1,
}

it("shows why a question is asked and answers it with one tap", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("ar", asking(debited))
  render(<IntakePage controller={controller} />)
  expect(await screen.findByText("ليش نسأل: حتى نعرف إذا الفلوس طلعت من محفظتك.")).toBeVisible()
  await user.click(screen.getByRole("button", { name: "اي" }))
  expect(vi.mocked(api.message).mock.calls[0]?.[1]).toMatchObject({
    text: "اي", attachment_ids: [], answer_to: { message_id: "q1", key: "debited", choice: "yes" },
  })
})

it("hides an empty reason from older conversations", async () => {
  const { controller } = await collectingController("ar", asking({ ...debited, reason: "" }))
  render(<IntakePage controller={controller} />)
  expect(await screen.findByRole("button", { name: "ما أعرف" })).toBeVisible()
  expect(screen.queryByText(/ليش نسأل/)).not.toBeInTheDocument()
})

it("offers the receipt upload for a reference question", async () => {
  const { controller } = await collectingController("ar", asking({
    ...debited, key: "txn_ref", text: "عدك رقم عملية أو مرجع؟", answer_kind: "reference", choices: ["unknown", "attach"],
  }))
  render(<IntakePage controller={controller} />)
  expect(await screen.findByRole("button", { name: "ما عندي رقم" })).toBeVisible()
  expect(screen.getByText("أرفق لقطة الوصل").closest("label")).toHaveAttribute("for", "intake-shots")
})

it("adapts the composer to the expected answer", async () => {
  const { controller } = await collectingController("ar", asking({
    ...debited, key: "recipient_phone", text: "على أي رقم حولت الفلوس؟", answer_kind: "phone", choices: ["unknown"],
  }))
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "رسالتك" })
  expect(input).toHaveAttribute("placeholder", "07XXXXXXXXX")
  expect(input).toHaveAttribute("inputmode", "tel")
})

it("shows the sent message and a typing indicator while the reply is pending", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en")
  vi.mocked(api.message).mockImplementation(() => new Promise(() => undefined))
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  await user.type(input, "hello")
  await user.click(screen.getByRole("button", { name: "Send" }))
  expect(await screen.findByText("hello")).toBeVisible()
  expect(screen.getByRole("img", { name: "Support is typing…" })).toBeVisible()
  expect(input).toHaveValue("")
  expect(screen.getByRole("status")).toHaveTextContent("Sending…")
})

it("marks an unsent message and resends it", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en")
  vi.mocked(api.message).mockRejectedValueOnce(new TypeError("offline"))
  vi.mocked(api.get).mockRejectedValueOnce(new TypeError("offline"))
  render(<IntakePage controller={controller} />)
  await user.type(await screen.findByRole("textbox", { name: "Your message" }), "hello")
  await user.click(screen.getByRole("button", { name: "Send" }))
  expect(await screen.findByText("Not sent")).toBeVisible()
  await user.click(screen.getByRole("button", { name: "Try again" }))
  await waitFor(() => expect(api.message).toHaveBeenCalledTimes(2))
})
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test -- src/features/intake/IntakePage.test.tsx src/components/ui/agent-chat.test.tsx"`
Expected: FAIL (no reason text, no typing indicator, no `inputmode`).

- [ ] **Step 3: Extend `AgentChat`**

In `agent-chat.tsx`:
- Change `MessagePart` and `AgentMessage`:

```tsx
export type MessagePart =
  | { type: "text"; text: string }
  | { type: "error"; title?: string; message: string }
  | { type: "typing"; label: string }

export type AgentMessage = {
  id: string
  role: "user" | "assistant"
  parts: MessagePart[]
  pending?: boolean
}
```

- Add `inputMode?: "text" | "tel" | "numeric"` to `AgentChatProps`. Destructure it in `AgentChat` and pass `inputMode={inputMode}` to `<InputBar>`. Add it to `InputBar`'s props and type, and add `inputMode={inputMode}` to the `<textarea>`.
- In the textarea class, change `text-[14px]` to `text-[16px]`.
- Replace `UserBubble`:

```tsx
function UserBubble({ text, speaker, pending }: { text: string; speaker?: string; pending?: boolean }) {
  return (
    <div className="flex justify-end">
      <div
        dir="auto"
        className={cn(
          "max-w-[80%] rounded-2xl bg-[color-mix(in_oklch,#da3345_10%,var(--card))] px-3.5 py-2 text-sm break-words whitespace-pre-wrap text-foreground",
          pending && "opacity-60"
        )}
      >
        {speaker ? <span className="sr-only">{speaker}</span> : null}
        {text}
      </div>
    </div>
  )
}
```

- Add after `ErrorBubble`:

```tsx
function TypingBubble({ label }: { label: string }) {
  return (
    <div className="flex justify-start">
      <div role="img" aria-label={label} className="inline-flex items-center gap-1 rounded-2xl bg-muted px-3 py-2.5">
        {[0, 150, 300].map((delay) => (
          <span
            key={delay}
            className="size-1.5 animate-bounce rounded-full bg-muted-foreground motion-reduce:animate-none"
            style={{ animationDelay: `${delay}ms` }}
          />
        ))}
      </div>
    </div>
  )
}
```

- In `MessageList`'s part mapping, add `if (part.type === "typing") return <TypingBubble key={index} label={part.label} />` after the error branch. Pass `pending={message.pending}` to `UserBubble`.

- [ ] **Step 4: Add the copy**

In `copy.ts`, add to `IntakeCopy`:

```ts
  whyPrefix: string
  quickReplies: string
  choiceYes: string
  choiceNo: string
  choiceUnknown: string
  choiceNoReference: string
  choiceAttach: string
  hintPhone: string
  hintAmount: string
  hintReference: string
  hintDate: string
  typing: string
  sending: string
  uploading: string
  removing: string
  submitting: string
  notSent: string
  resend: string
```

Add these keys to `locales/ar.json`, before `"empty"`:

```json
  "whyPrefix": "ليش نسأل:",
  "quickReplies": "ردود سريعة",
  "choiceYes": "اي",
  "choiceNo": "لا",
  "choiceUnknown": "ما أعرف",
  "choiceNoReference": "ما عندي رقم",
  "choiceAttach": "أرفق لقطة الوصل",
  "hintPhone": "07XXXXXXXXX",
  "hintAmount": "مثلاً 50000",
  "hintReference": "مثلاً ZC2410000123",
  "hintDate": "مثلاً 2026-10-06 أو امس",
  "typing": "الدعم يكتب…",
  "sending": "جاري الإرسال…",
  "uploading": "جاري رفع اللقطة…",
  "removing": "جاري إزالة اللقطة…",
  "submitting": "جاري إرسال التذكرة…",
  "notSent": "ما انرسلت",
  "resend": "أعد الإرسال",
```

Add `"recipient_name": "اسم المستلم",` to `fieldLabels`, after `"recipient_phone"`.

Add the same keys to `locales/en.json`, before `"empty"`:

```json
  "whyPrefix": "Why we ask:",
  "quickReplies": "Quick replies",
  "choiceYes": "Yes",
  "choiceNo": "No",
  "choiceUnknown": "I don't know",
  "choiceNoReference": "I don't have the number",
  "choiceAttach": "Attach the receipt",
  "hintPhone": "07XXXXXXXXX",
  "hintAmount": "For example 50000",
  "hintReference": "For example ZC2410000123",
  "hintDate": "For example 2026-10-06 or yesterday",
  "typing": "Support is typing…",
  "sending": "Sending…",
  "uploading": "Uploading the screenshot…",
  "removing": "Removing the screenshot…",
  "submitting": "Submitting the ticket…",
  "notSent": "Not sent",
  "resend": "Try again",
```

Add `"recipient_name": "Recipient name",` to `fieldLabels`, after `"recipient_phone"`.

- [ ] **Step 5: Add the composer helpers and the question extras**

Create `features/intake/composer.ts`:

```ts
import type { Activity } from "./controller"
import type { IntakeCopy } from "./copy"
import type { AnswerKind, Choice } from "./types"

export type ComposerHint = { placeholder: string; inputMode: "text" | "tel" | "numeric" }

export function composerHint(kind: AnswerKind | null, copy: IntakeCopy): ComposerHint {
  switch (kind) {
    case "phone":
      return { placeholder: copy.hintPhone, inputMode: "tel" }
    case "amount":
      return { placeholder: copy.hintAmount, inputMode: "numeric" }
    case "reference":
      return { placeholder: copy.hintReference, inputMode: "text" }
    case "date":
      return { placeholder: copy.hintDate, inputMode: "text" }
    default:
      return { placeholder: copy.placeholder, inputMode: "text" }
  }
}

export function choiceLabel(choice: Choice, kind: AnswerKind, copy: IntakeCopy): string {
  if (choice === "yes") return copy.choiceYes
  if (choice === "no") return copy.choiceNo
  if (choice === "attach") return copy.choiceAttach
  return kind === "reference" ? copy.choiceNoReference : copy.choiceUnknown
}

export function activityText(activity: Activity | null, busy: boolean, processing: boolean, copy: IntakeCopy) {
  if (busy) {
    const text: Record<Activity, string> = {
      message: copy.sending,
      ask: copy.sending,
      review: copy.processing,
      upload: copy.uploading,
      remove: copy.removing,
      submit: copy.submitting,
    }
    return text[activity ?? "message"]
  }
  return processing ? copy.processing : null
}
```

Create `features/intake/QuestionExtras.tsx`:

```tsx
import { Button, buttonVariants } from "@workspace/ui/components/button"
import { quietButton } from "./buttons"
import { choiceLabel } from "./composer"
import type { IntakeCopy } from "./copy"
import type { AnswerTo, PendingQuestion } from "./types"

export function QuestionExtras({
  question,
  copy,
  interactive,
  attachInputId,
  attachDisabled,
  onAnswer,
}: {
  question: PendingQuestion
  copy: IntakeCopy
  interactive: boolean
  attachInputId: string
  attachDisabled: boolean
  onAnswer: (text: string, answer: AnswerTo) => void
}) {
  return (
    <div className="intake-question-extras">
      {question.reason ? (
        <p className="intake-why" dir="auto">
          {copy.whyPrefix} {question.reason}
        </p>
      ) : null}
      {interactive && question.choices.length ? (
        <div className="intake-choices" role="group" aria-label={copy.quickReplies}>
          {question.choices.map((choice) => {
            const label = choiceLabel(choice, question.answer_kind, copy)
            if (choice === "attach") {
              return (
                <label
                  key={choice}
                  htmlFor={attachInputId}
                  aria-disabled={attachDisabled}
                  className={`${buttonVariants({ variant: "outline", size: "sm" })} ${quietButton} intake-choice${attachDisabled ? " is-disabled" : ""}`}
                >
                  {label}
                </label>
              )
            }
            return (
              <Button
                key={choice}
                type="button"
                variant="outline"
                size="sm"
                className={`${quietButton} intake-choice`}
                onClick={() => onAnswer(label, { message_id: question.message_id, key: question.key, choice })}
              >
                {label}
              </Button>
            )
          })}
        </div>
      ) : null}
    </div>
  )
}
```

- [ ] **Step 6: Wire the chat into `IntakePage.tsx`**

1. Add the imports `import { QuestionExtras } from "./QuestionExtras"`, `import { activityText, composerHint } from "./composer"` and `import type { AnswerTo, Language } from "./types"` (replacing the existing `Language` import).
2. After `const inProgress = ...`, add:

```tsx
  const pending = session?.pending_question ?? null
  const interactive = Boolean(
    pending &&
    session?.phase === "collecting" &&
    session.turn_status === "idle" &&
    !snapshot.busy
  )
  const hint = composerHint(interactive && pending ? pending.answer_kind : null, text)
  const outgoing = snapshot.outgoing
  const showOutgoing = Boolean(
    outgoing?.text &&
    session &&
    session.phase !== "submitted" &&
    session.revision === outgoing.expected_revision
  )
  const outgoingFailed = showOutgoing && !snapshot.busy && Boolean(snapshot.error)
  const typing =
    (snapshot.busy && (snapshot.activity === "message" || snapshot.activity === "ask")) ||
    session?.turn_status === "processing"
```

3. Replace the `chatMessages` `useMemo` body's final `return history.map(...)` with:

```tsx
    const items: AgentMessage[] = history.map((message) => ({
      id: message.id,
      role: message.role,
      parts: [{ type: "text" as const, text: message.text }],
    }))
    if (showOutgoing && outgoing) {
      items.push({ id: "outgoing", role: "user", pending: !outgoingFailed, parts: [{ type: "text", text: outgoing.text }] })
    }
    if (typing) items.push({ id: "typing", role: "assistant", parts: [{ type: "typing", label: text.typing }] })
    return items
```

   Extend the dependency list to `[session?.messages, session?.receipt, session?.review, text.empty, text.typing, showOutgoing, outgoing, outgoingFailed, typing]`.
4. Replace `send`:

```tsx
  async function send(content: string) {
    if (!canSend) return
    const attachmentIds = unsent.map((item) => item.id)
    setDraft("")
    await controller.send(content, locale, attachmentIds)
    const after = controller.getSnapshot()
    if (after.error && !after.outgoing) {
      setDraft((current) => current || content)
      return
    }
    if (!after.error) {
      clearPreviews()
      document.getElementById("intake-message")?.focus()
    }
  }

  function answer(label: string, answerTo: AnswerTo) {
    void controller.send(label, locale, [], answerTo)
  }
```

5. Replace `const showTyping = snapshot.busy || session?.turn_status === "processing"` with:

```tsx
  const statusText = activityText(snapshot.activity, snapshot.busy, session?.turn_status === "processing", text)
```

   In the `toolbar` condition, replace `showTyping` with `statusText`. Replace the typing paragraph with:

```tsx
                        {statusText ? (
                          <p role="status" className="intake-typing">
                            {statusText}
                          </p>
                        ) : null}
```

6. On `<AgentChat>`, set `placeholder={hint.placeholder}` and add `inputMode={hint.inputMode}`.
7. At the start of the `renderAfter` callback, before the existing user-attachment logic, add:

```tsx
                    if (message.id === "outgoing") {
                      return outgoingFailed ? (
                        <div className="intake-outgoing-failed">
                          <span>{text.notSent}</span>
                          <Button type="button" variant="outline" size="sm" className={quietButton} onClick={() => void controller.retry()}>
                            {text.resend}
                          </Button>
                        </div>
                      ) : null
                    }
                    if (pending && message.id === pending.message_id && message.role === "assistant") {
                      return (
                        <QuestionExtras
                          question={pending}
                          copy={text}
                          interactive={interactive}
                          attachInputId="intake-shots"
                          attachDisabled={Boolean(attachingDisabled)}
                          onAnswer={answer}
                        />
                      )
                    }
```

8. Add to `intake.css`, after `.intake-typing`:

```css
.intake-question-extras {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.intake-why {
  margin: 0;
  color: var(--muted-foreground);
  font-size: 0.8125rem;
}
.intake-choices {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.intake-choice {
  min-height: 36px;
  border-radius: 999px;
}
.intake-choice.is-disabled {
  pointer-events: none;
  opacity: 0.5;
}
.intake-outgoing-failed {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  color: #da3345;
  font-size: 0.8125rem;
}
```

- [ ] **Step 7: Run all frontend checks**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test && npm --workspace web run typecheck && npm --workspace web run lint"`
Expected: PASS. The existing test "retains text typed while the previous message is in flight" must still pass unchanged.

- [ ] **Step 8: Commit**

```bash
git add users-frontend/apps/web/src/components/ui/agent-chat.tsx users-frontend/apps/web/src/components/ui/agent-chat.test.tsx users-frontend/apps/web/src/features/intake/composer.ts users-frontend/apps/web/src/features/intake/QuestionExtras.tsx users-frontend/apps/web/src/features/intake/IntakePage.tsx users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/copy.ts users-frontend/apps/web/src/features/intake/locales/ar.json users-frontend/apps/web/src/features/intake/locales/en.json users-frontend/apps/web/src/features/intake/intake.css
git commit -m "feat(intake-app): show reasons, quick replies and a live chat while the agent works"
```

---

### Task 9: Progress strip

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/ProgressStrip.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx` (move "Review what I have" from the header into the strip)
- Modify: `users-frontend/apps/web/src/features/intake/copy.ts`, `locales/ar.json`, `locales/en.json`, `intake.css`
- Test: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`

**Interfaces:**
- Consumes: `session.progress` (Task 7) and `controller.requestReview(true, locale)`.
- Produces:
  - `<ProgressStrip items copy reviewDisabled onReviewNow />`
  - `displayValue(item: ProgressItem, copy: IntakeCopy): string | null`, exported for Task 10.
- New `IntakeCopy` keys: `progressLabel`, `stillNeeded`, `notKnown`.

- [ ] **Step 1: Write the failing tests**

Append to `IntakePage.test.tsx`:
- Add `ProgressItem` to the `./types` type import.
- Add these tests:

```tsx
const transferProgress: ProgressItem[] = [
  { key: "issue", tier: "required", status: "known", display: "Transfer failed" },
  { key: "amount", tier: "required", status: "known", display: "50000" },
  { key: "debited", tier: "required", status: "known", display: "yes" },
  { key: "recipient_phone", tier: "required", status: "missing", display: null },
  { key: "txn_ref", tier: "ask_once", status: "unknown", display: null },
]
const firstMessage = { id: "m1", role: "user" as const, text: "Transfer failed", language: "en" as const, created_at: "2026-10-18T09:00:00Z", attachment_ids: [] }

it("shows interview progress with the collected values", async () => {
  const user = userEvent.setup()
  const { controller } = await collectingController("en", { progress: transferProgress, messages: [firstMessage] })
  render(<IntakePage controller={controller} />)
  await user.click(await screen.findByRole("button", { name: "Details: 3 of 4" }))
  const list = screen.getByRole("list", { name: "Details: 3 of 4" })
  expect(within(list).getByText("Amount · 50000")).toBeVisible()
  expect(within(list).getByText("Funds deducted · Yes")).toBeVisible()
  expect(within(list).getByText("Recipient number")).toBeVisible()
  expect(within(list).getByText("Reference · Not known")).toBeVisible()
})

it("requests an early review from the progress strip", async () => {
  const user = userEvent.setup()
  const { controller, api } = await collectingController("en", { progress: transferProgress, messages: [firstMessage] })
  render(<IntakePage controller={controller} />)
  expect(within(screen.getByRole("banner")).queryByRole("button", { name: "Review what I have" })).not.toBeInTheDocument()
  await user.click(screen.getByRole("button", { name: "Review what I have" }))
  expect(vi.mocked(api.review).mock.calls[0]?.[1]).toMatchObject({ allow_partial: true, language: "en" })
})
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test -- src/features/intake/IntakePage.test.tsx"`
Expected: FAIL (no "Details: 3 of 4" button).

- [ ] **Step 3: Add the copy**

Add `progressLabel: string`, `stillNeeded: string` and `notKnown: string` to `IntakeCopy`.

`ar.json`:

```json
  "progressLabel": "التفاصيل: {done} من {total}",
  "stillNeeded": "بعده مطلوب",
  "notKnown": "ما معروف",
```

`en.json`:

```json
  "progressLabel": "Details: {done} of {total}",
  "stillNeeded": "still needed",
  "notKnown": "Not known",
```

- [ ] **Step 4: Create `ProgressStrip.tsx`**

```tsx
import { useState } from "react"
import { Button } from "@workspace/ui/components/button"
import { quietButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import type { ProgressItem } from "./types"

export function displayValue(item: ProgressItem, copy: IntakeCopy): string | null {
  if (item.display === "yes") return copy.choiceYes
  if (item.display === "no") return copy.choiceNo
  return item.display
}

function wideScreen() {
  return typeof window.matchMedia === "function" && window.matchMedia("(min-width: 721px)").matches
}

export function ProgressStrip({
  items,
  copy,
  reviewDisabled,
  onReviewNow,
}: {
  items: ProgressItem[]
  copy: IntakeCopy
  reviewDisabled: boolean
  onReviewNow: () => void
}) {
  const [open, setOpen] = useState(wideScreen)
  const required = items.filter((item) => item.tier === "required")
  const done = required.filter((item) => item.status === "known" || item.status === "not_applicable").length
  const label = copy.progressLabel.replace("{done}", String(done)).replace("{total}", String(required.length))
  return (
    <div className="intake-progress-strip">
      <div className="intake-progress-head">
        {items.length ? (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            aria-expanded={open}
            aria-controls="intake-progress-list"
            onClick={() => setOpen((value) => !value)}
          >
            {label}
          </Button>
        ) : null}
        <Button type="button" variant="outline" size="sm" className={quietButton} disabled={reviewDisabled} onClick={onReviewNow}>
          {copy.reviewNow}
        </Button>
      </div>
      {open && items.length ? (
        <ul id="intake-progress-list" className="intake-progress-list" aria-label={label}>
          {items.map((item) => {
            const name = copy.fieldLabels[item.key] || item.key
            const value = displayValue(item, copy)
            const known = item.status === "known" || item.status === "not_applicable"
            const mark = known ? "✓" : item.status === "unknown" ? "–" : "○"
            const shown = known && value ? `${name} · ${value}` : item.status === "unknown" ? `${name} · ${copy.notKnown}` : name
            return (
              <li key={item.key} data-status={item.status} className={item.tier === "ask_once" ? "is-optional" : undefined}>
                <span aria-hidden="true" className="intake-progress-mark">{mark}</span>
                {shown}
                {!known && item.status !== "unknown" ? <span className="sr-only"> {copy.stillNeeded}</span> : null}
              </li>
            )
          })}
        </ul>
      ) : null}
    </div>
  )
}
```

- [ ] **Step 5: Use it in `IntakePage.tsx`**

1. Import `ProgressStrip`.
2. Delete the header `{showReviewNow && hasContent ? (<Button ...>{text.reviewNow}</Button>) : null}` block. Keep `showReviewNow`.
3. Add `const showProgress = Boolean(showReviewNow && (session?.progress.length || hasContent))`.
4. In the `toolbar` condition, add `showProgress ||`. Render this as the first child of the toolbar fragment:

```tsx
                        {showProgress && session ? (
                          <ProgressStrip
                            items={session.progress}
                            copy={text}
                            reviewDisabled={snapshot.busy || session.turn_status === "processing"}
                            onReviewNow={() => {
                              reviewRequest.current = true
                              void controller.requestReview(true, locale)
                            }}
                          />
                        ) : null}
```

5. Add to `intake.css`:

```css
.intake-progress-strip {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.intake-progress-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.intake-progress-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.intake-progress-list li {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  font-size: 0.8125rem;
}
.intake-progress-list li[data-status="known"] {
  background: color-mix(in oklch, #16a34a 10%, var(--card));
}
.intake-progress-list li.is-optional {
  opacity: 0.75;
}
```

- [ ] **Step 6: Run all frontend checks**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test && npm --workspace web run typecheck && npm --workspace web run lint"`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/ProgressStrip.tsx users-frontend/apps/web/src/features/intake/IntakePage.tsx users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/copy.ts users-frontend/apps/web/src/features/intake/locales/ar.json users-frontend/apps/web/src/features/intake/locales/en.json users-frontend/apps/web/src/features/intake/intake.css
git commit -m "feat(intake-app): show what the agent has collected and what is still needed"
```

---

### Task 10: Grouped review card with answer buttons

**Files:**
- Replace: `users-frontend/apps/web/src/features/intake/ReviewPanel.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/IntakePage.tsx` (review actions move into the card; the card stays visible while submitting)
- Modify: `users-frontend/apps/web/src/features/intake/copy.ts`, `locales/ar.json`, `locales/en.json`, `intake.css`
- Test: `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`

**Interfaces:**
- Consumes: `controller.ask(key)` and `controller.submit()` (Task 7), and `session.progress`.
- Produces: `ReviewPanel` props `{ review, attachments, credentials, api, copy, headingRef, askable: string[], busy: boolean, submitting: boolean, onAsk: (key: string) => void, onSubmit: () => void, onContinue: () => void }`.
- New `IntakeCopy` keys: `complete`, `missingList`, `listSeparator`, `groupKnown`, `groupMissing`, `groupUnknown`, `answer`, `answerRemembered`.

- [ ] **Step 1: Write the failing tests**

Append to `IntakePage.test.tsx`:

```tsx
const groupedReview = {
  ...review,
  facts: {
    customer_phone: { key: "customer_phone", status: "known" as const, value: CUSTOMER_PHONE, normalized: CUSTOMER_PHONE, evidence: [] },
    amount: { key: "amount", status: "known" as const, value: "50000", normalized: "50000", evidence: [] },
    recipient_phone: { key: "recipient_phone", status: "missing" as const, value: null, normalized: null, evidence: [] },
    txn_ref: { key: "txn_ref", status: "unknown" as const, value: null, normalized: null, evidence: [] },
  },
  unknown_keys: ["recipient_phone", "txn_ref"],
}
const groupedProgress: ProgressItem[] = [
  { key: "amount", tier: "required", status: "known", display: "50000" },
  { key: "recipient_phone", tier: "required", status: "missing", display: null },
  { key: "txn_ref", tier: "ask_once", status: "unknown", display: null },
]

it("groups review details and asks for a missing one", async () => {
  const user = userEvent.setup()
  const api = fakeApi({ phase: "review_ready", review: groupedReview, progress: groupedProgress })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize("en", CUSTOMER_PHONE)
  render(<IntakePage controller={controller} />)
  expect(await screen.findByText("Missing: Recipient number")).toBeVisible()
  expect(screen.getByRole("heading", { name: "What we know" })).toBeVisible()
  expect(screen.getByRole("heading", { name: "Missing" })).toBeVisible()
  expect(screen.getByRole("heading", { name: "Not known" })).toBeVisible()
  expect(screen.queryByText("Your account number")).not.toBeInTheDocument()
  expect(screen.getByRole("button", { name: "Remembered? Answer: Reference" })).toBeVisible()
  await user.click(screen.getByRole("button", { name: "Answer: Recipient number" }))
  expect(vi.mocked(api.ask).mock.calls[0]?.[1]).toMatchObject({ key: "recipient_phone" })
})

it("marks a complete review", async () => {
  const api = fakeApi({ phase: "review_ready", review: { ...review, quality: "sufficient_context", facts: { amount: groupedReview.facts.amount }, unknown_keys: [] } })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize("en", CUSTOMER_PHONE)
  render(<IntakePage controller={controller} />)
  expect(await screen.findByText("Details complete")).toBeVisible()
})

it("keeps the review visible while the ticket is submitting", async () => {
  const user = userEvent.setup()
  const { controller, api } = await readyController("en")
  vi.mocked(api.submit).mockImplementation(() => new Promise(() => undefined))
  render(<IntakePage controller={controller} />)
  const submit = await screen.findByRole("button", { name: "Submit ticket" })
  await user.click(submit)
  expect(screen.getByRole("heading", { name: "Review your report" })).toBeVisible()
  expect(submit).toBeDisabled()
  expect(submit).toHaveAttribute("aria-busy", "true")
  expect(screen.getByRole("status")).toHaveTextContent("Submitting the ticket…")
})
```

- [ ] **Step 2: Run them to verify they fail**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test -- src/features/intake/IntakePage.test.tsx"`
Expected: FAIL (no "Missing: Recipient number").

- [ ] **Step 3: Add the copy**

Add `complete`, `missingList`, `listSeparator`, `groupKnown`, `groupMissing`, `groupUnknown`, `answer` and `answerRemembered` (all `string`) to `IntakeCopy`.

`ar.json`:

```json
  "complete": "التفاصيل كاملة",
  "missingList": "ناقص: {items}",
  "listSeparator": "، ",
  "groupKnown": "اللي عرفناه",
  "groupMissing": "ناقص",
  "groupUnknown": "ما معروف",
  "answer": "جاوب",
  "answerRemembered": "تذكرت؟ جاوب",
```

`en.json`:

```json
  "complete": "Details complete",
  "missingList": "Missing: {items}",
  "listSeparator": ", ",
  "groupKnown": "What we know",
  "groupMissing": "Missing",
  "groupUnknown": "Not known",
  "answer": "Answer",
  "answerRemembered": "Remembered? Answer",
```

- [ ] **Step 4: Replace `ReviewPanel.tsx`**

```tsx
import { Button } from "@workspace/ui/components/button"
import type { IntakeApi } from "./api"
import { quietButton, solidButton } from "./buttons"
import type { IntakeCopy } from "./copy"
import type { Attachment, Credentials, CustomerReview, Fact } from "./types"
import { OwnedImage } from "./OwnedImage"

function factText(fact: Fact, copy: IntakeCopy) {
  if (fact.status === "unknown" || fact.status === "missing") return copy.unknown
  if (fact.status === "not_applicable") return copy.notApplicable
  if (fact.status === "conflicting") return `${copy.conflicting}: ${fact.value || copy.unknown}`
  if (fact.normalized === "yes") return copy.choiceYes
  if (fact.normalized === "no") return copy.choiceNo
  return fact.normalized || fact.value || copy.unknown
}

function statusSuffix(fact: Fact, copy: IntakeCopy) {
  if (fact.status === "known") return ""
  if (fact.status === "conflicting") return ` (${copy.conflicting})`
  if (fact.status === "not_applicable") return ` (${copy.notApplicable})`
  return ` (${copy.unknown})`
}

export function ReviewPanel({
  review,
  attachments,
  credentials,
  api,
  copy,
  headingRef,
  askable,
  busy,
  submitting,
  onAsk,
  onSubmit,
  onContinue,
}: {
  review: CustomerReview
  attachments: Attachment[]
  credentials: Credentials | null
  api: IntakeApi
  copy: IntakeCopy
  headingRef: (node: HTMLHeadingElement | null) => void
  askable: string[]
  busy: boolean
  submitting: boolean
  onAsk: (key: string) => void
  onSubmit: () => void
  onContinue: () => void
}) {
  const selected = attachments.filter((item) => !item.removed && review.attachment_ids.includes(item.id))
  const facts = Object.values(review.facts).filter((fact) => fact.key !== "customer_phone")
  const known = facts.filter((fact) => fact.status === "known" || fact.status === "not_applicable")
  const missing = facts.filter((fact) => fact.status === "missing" || fact.status === "conflicting")
  const unknown = facts.filter((fact) => fact.status === "unknown")
  const label = (key: string) => copy.fieldLabels[key] || key
  const banner = review.quality === "sufficient_context"
    ? null
    : missing.length
      ? copy.missingList.replace("{items}", missing.map((fact) => label(fact.key)).join(copy.listSeparator))
      : copy.partial
  return (
    <section className="intake-review" aria-labelledby="intake-review-heading">
      <h2 id="intake-review-heading" tabIndex={-1} ref={headingRef}>
        {copy.review}
      </h2>
      {review.quality === "sufficient_context" ? (
        <p className="intake-complete">{copy.complete}</p>
      ) : (
        <p className="intake-partial">{banner}</p>
      )}
      <p dir="auto" lang={review.language}>
        {review.text}
      </p>
      {known.length ? (
        <>
          <h3>{copy.groupKnown}</h3>
          <dl>
            {known.map((fact) => (
              <div key={fact.key}>
                <dt>{label(fact.key)}</dt>
                <dd>
                  <bdi dir="auto">{factText(fact, copy)}</bdi>
                </dd>
              </div>
            ))}
          </dl>
        </>
      ) : null}
      {missing.length ? (
        <>
          <h3>{copy.groupMissing}</h3>
          <ul className="intake-gaps">
            {missing.map((fact) => (
              <li key={fact.key}>
                <span>{label(fact.key)}</span>
                {fact.status === "conflicting" ? <bdi dir="auto">{factText(fact, copy)}</bdi> : null}
                {askable.includes(fact.key) ? (
                  <Button type="button" variant="outline" size="sm" className={quietButton} disabled={busy}
                    aria-label={`${copy.answer}: ${label(fact.key)}`} onClick={() => onAsk(fact.key)}>
                    {copy.answer}
                  </Button>
                ) : null}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {unknown.length ? (
        <>
          <h3>{copy.groupUnknown}</h3>
          <ul className="intake-gaps">
            {unknown.map((fact) => (
              <li key={fact.key}>
                <span>{label(fact.key)}</span>
                <span className="intake-muted">{copy.unknown}</span>
                {askable.includes(fact.key) ? (
                  <Button type="button" variant="outline" size="sm" className={quietButton} disabled={busy}
                    aria-label={`${copy.answerRemembered}: ${label(fact.key)}`} onClick={() => onAsk(fact.key)}>
                    {copy.answerRemembered}
                  </Button>
                ) : null}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {review.additional_issues.length ? (
        <>
          <h3>{copy.issues}</h3>
          <ul>
            {review.additional_issues.map((issue) => (
              <li key={issue.key} dir="auto">
                {issue.value || copy.unknown}
                {statusSuffix(issue, copy)}
              </li>
            ))}
          </ul>
        </>
      ) : null}
      {selected.length ? (
        <div>
          <h3>{copy.screenshots}</h3>
          {selected.map((attachment) => (
            <OwnedImage
              key={attachment.id}
              attachment={attachment}
              credentials={credentials}
              api={api}
              alt={attachment.filename}
              unavailable={copy.imageUnavailable}
            />
          ))}
        </div>
      ) : null}
      <div className="intake-actions intake-review-actions">
        <Button type="button" variant="outline" className={quietButton} disabled={busy} onClick={onContinue}>
          {copy.continueChat}
        </Button>
        <Button type="button" className={solidButton} disabled={busy} aria-busy={submitting} onClick={onSubmit}>
          {submitting ? <span className="intake-spinner" aria-hidden="true" /> : null}
          {copy.submit}
        </Button>
      </div>
    </section>
  )
}
```

- [ ] **Step 5: Wire the card in `IntakePage.tsx`**

1. Replace `showReview` with:

```tsx
  const submitting = snapshot.busy && snapshot.activity === "submit"
  const showReview = Boolean(
    session?.review &&
    !session.receipt &&
    session.turn_status === "idle" &&
    (!snapshot.busy || submitting)
  )
```

2. Pass these props to `<ReviewPanel>`:

```tsx
          askable={session.progress.map((item) => item.key)}
          busy={snapshot.busy}
          submitting={submitting}
          onAsk={(key) => void controller.ask(key)}
          onSubmit={() => void controller.submit()}
          onContinue={() => document.getElementById("intake-message")?.focus()}
```

3. Delete the toolbar block `{showReview ? (<div className="intake-actions">…Continue…Submit…</div>) : null}`, and remove `showReview ||` from the toolbar condition. `ReviewPanel` now owns these actions.
4. Add to `intake.css`:

```css
.intake-complete {
  margin: 0;
  padding: 10px 12px;
  border-radius: 12px;
  background: color-mix(in oklch, #16a34a 12%, var(--card));
}
.intake-gaps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.intake-gaps li {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.intake-review-actions {
  justify-content: flex-end;
}
.intake-spinner {
  width: 14px;
  height: 14px;
  margin-inline-end: 6px;
  border: 2px solid currentColor;
  border-inline-end-color: transparent;
  border-radius: 999px;
  animation: intake-spin 0.8s linear infinite;
}
@keyframes intake-spin {
  to {
    transform: rotate(360deg);
  }
}
@media (prefers-reduced-motion: reduce) {
  .intake-spinner {
    animation: none;
  }
}
```

- [ ] **Step 6: Run all frontend checks, including the build**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test && npm --workspace web run typecheck && npm --workspace web run lint && npm --workspace web run build"`
Expected: PASS. The existing review tests ("requires explicit submission", "submits once…", "shows unknown facts in a partial review", "labels conflicting and inapplicable facts") must pass unchanged.

- [ ] **Step 7: Commit**

```bash
git add users-frontend/apps/web/src/features/intake/ReviewPanel.tsx users-frontend/apps/web/src/features/intake/IntakePage.tsx users-frontend/apps/web/src/features/intake/IntakePage.test.tsx users-frontend/apps/web/src/features/intake/copy.ts users-frontend/apps/web/src/features/intake/locales/ar.json users-frontend/apps/web/src/features/intake/locales/en.json users-frontend/apps/web/src/features/intake/intake.css
git commit -m "feat(intake-app): group the review card and let the customer answer gaps"
```

---

### Task 11: Employee label, full gates, live probe and verification record

**Files:**
- Modify: `employee-frontend/src/locales/en.json` and `employee-frontend/src/locales/ar.json` (add `recipient_name` to the reported-details `fields` block, around line 266)
- Create: `docs/verification/2026-11-13-guided-intake.md`

**Interfaces:**
- Consumes: everything above.
- Produces: the employee label and a verification record.

- [ ] **Step 1: Add the employee label**

In the `fields` object that contains `"recipient_phone"` (around line 276):
- `en.json`: add `"recipient_name": "Recipient name",` after `"recipient_phone": "Recipient phone",`.
- `ar.json`: add `"recipient_name": "اسم المستلم",` after `"recipient_phone": "هاتف المستلم",`.

Do not modify any other employee-frontend file.

- [ ] **Step 2: Run every gate**

Run each command and record its exact summary line. Each must exit 0.
1. `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run pytest -q --tb=short"`
2. `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && ~/.local/bin/uv --directory backend run ruff check app tests"`
3. `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/users-frontend && npm --workspace web run test && npm --workspace web run typecheck && npm --workspace web run lint && npm --workspace web run build"`
4. `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support/employee-frontend && npm run test && npm run typecheck && npm run lint && npm run build"`

If the employee checks fail because of the user's own uncommitted changes in `employee-frontend/src/features/review/**`, do not fix them. Run `git stash list` to confirm you did not create any stash, then report the failure as pre-existing with the failing test names.

- [ ] **Step 3: Run the live transfer probe (paid, synthetic data)**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd ~/dev/zaincash-support && SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt ~/.local/bin/uv --directory backend run python -m tests.intake.live_probe transfers"`

Expected:
- **vague:** `category` is `failed_transfer`; `recipient_outcome` is known with normalized `no`; `next_question.key` is not `expected` or `recipient_outcome`.
- **complete:** `quality` is `sufficient_context` or `collecting` with `next_question` `null`; facts include `recipient_name`, `recipient_phone`, `txn_ref`, `debited` = yes and `recipient_outcome` = no.

If the live model misses the implied facts:
1. Tighten only the new rules in `intake_v1.md`.
2. Re-run the probe, at most three times.
3. Re-run `tests/intake/test_prompts.py`.

Record every run's output (latency, cost and the outcome) in the verification record. Never print or record API keys.

- [ ] **Step 4: Write `docs/verification/2026-11-13-guided-intake.md`**

Follow the structure of `docs/verification/2026-10-18-customer-intake.md`:
- a table of gate commands with their pass counts
- the live probe results
- any existing-test expectation changes from Task 1 Step 6 / Step 7, with the reason for each
- the remaining limits: no live-model browser run yet, which the controller does after the whole-branch review; and the out-of-scope items from the spec.

- [ ] **Step 5: Commit**

```bash
git add employee-frontend/src/locales/en.json employee-frontend/src/locales/ar.json docs/verification/2026-11-13-guided-intake.md
```

If Step 3 changed the prompt, also add `backend/app/intake/prompts/intake_v1.md`. Then commit:

```bash
git commit -m "docs: verify the guided intake interview"
```

---

## After all tasks (controller)

1. Run the whole-branch review required by superpowers:subagent-driven-development.
2. Run the browser check on `http://localhost:5174` with the live model, after restarting or reloading the backend that serves it:
   - Arabic at 390px: the vague message, through quick replies and typed answers, to a complete review and submit.
   - English on desktop: the complete message goes straight to review.
   - Confirm the ticket appears in the employee app with the recipient name and number.
3. Append the browser results to the verification record.
