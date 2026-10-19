# Customer Conversation Intake Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn incomplete customer complaints into evidence-backed, customer-approved tickets that employees can understand quickly.

**Architecture:** Add a durable, turn-based intake graph to the existing FastAPI backend. LangChain/OpenRouter interprets text and screenshots; application rules validate evidence, select missing context, and enforce review-before-submission. A transactional adapter creates a normal pipeline ticket and a processing result, while separate customer and employee UIs present the appropriate views.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic 2, SQLAlchemy 2/Postgres, LangGraph 1.x, LangChain 1.x, langchain-openrouter, Pillow for image validation, React/TypeScript/Vite 8, existing shadcn components, pytest, Vitest 5 and React Testing Library.

**Spec:** `docs/superpowers/specs/2026-10-18-customer-intake-design.md` (approved 2026-10-18).

## Completion audit — 2026-10-18

Audited and repaired on `feat/customer-intake`. Current verification: **781 backend tests, 40 customer tests, 31 employee tests**, Ruff, both frontend type/lint/build checks. See [the verification record](../../verification/2026-10-18-customer-intake.md) for findings, commands, browser evidence and measured live vision results.

- [x] Task 1 — Durable session contracts, ownership, operation identities and configuration.
- [x] Task 2 — Grounded evidence, corrections, role-specific phones, conservative dates and readiness.
- [x] Task 3 — Validated attachments, bounded vision calls, structured-output repair and usage accounting.
- [x] Task 4 — Graph turns, recovery fencing, current reviews and customer API.
- [x] Task 5 — Exactly-once submission, frozen employee evidence and durable failure reconciliation.
- [x] Task 6 — Resumable client, pending-operation recovery, initialization and polling guards.
- [x] Task 7 — Bilingual chat, multiple screenshots, corrections, partial review and receipt.
- [x] Task 8 — Employee evidence/status presentation and review availability.
- [x] Task 9 — Automated handoff, browser handoff, reproducible live image probe and runbook.

Browser handoff used real HTTP/Postgres with scripted models. Separate live image-and-review checks passed with `INTAKE_MODEL=google/gemini-2.5-flash` (now the example configuration). The former `google/gemini-3.8-flash` fallback was unreliable in this check. End-to-end live-provider linguistic quality is not established by the scripted browser run. One minor documentation enhancement remains deferred: explicit success-response declarations in OpenAPI.

## Global Constraints

- A ticket becomes visible to employees only after the customer reviews its summary and submits it.
- Direct demo access without customer sign-in; a browser can resume its own saved draft.
- Iraqi Arabic and English conversations, including mixed-language messages.
- Screenshot uploads that the AI can read and use for follow-up questions.
- Intake gathers customer-provided context. Transaction, incident, and policy investigation stays in the existing submitted-ticket pipeline.
- Employees receive an Iraqi Arabic summary, alongside the original conversation and screenshots.
- Adaptive questioning continues until the issue is sufficiently understood, rather than ending after a fixed number of questions.
- Customers can review and submit the information they have, with unknowns explicitly recorded.
- Initial configurable limits: 5 MiB and 20 megapixels per image, three images per message, ten per session.
- Default execution limits are a 60-second deadline and at most three provider requests per turn or review-generation operation, including retries and output repair; make these limits configurable.
- Keep the employee development UI on port 5173 and use port 5174 for the customer UI, with strict port selection to prevent accidental switching.
- The assistant must not request PINs, OTPs, passwords, or full payment-card numbers.
- The database is authoritative. Persist messages and the structured state after each completed turn; do not rely on process-local memory or browser message history.
- Submitted evidence is immutable. Intake never sends a final support response or performs transaction/incident/KB investigation.

## Review Focus

1. A reused operation ID with changed text, image bytes, or review ID must conflict rather than replay an unrelated success (Tasks 1, 3, 4, 5).
2. StrictMode must not duplicate session initialization; refresh/two tabs and interrupted requests must not duplicate accepted turns, screenshots, or submissions (Tasks 4, 6, 7).
3. A late model response after recovery or attachment removal must not restore stale facts or a superseded review (Tasks 3, 4).
4. Arabic/Persian digits, receipt/reference numbers, relative dates across Baghdad midnight, and recipient/customer phone roles must survive summarization without being mixed together (Tasks 2, 4).
5. A crash after submission commits but before scheduling, or a persistence error during processing, must leave a visible, non-reviewable failed result with intact evidence (Task 5).

---

## Execution conventions and repository baseline

- The detailed step checkboxes below preserve the original execution recipe, including creation-time red checks. They are not a retroactive claim about the first implementation session. The completion audit above and linked measured verification record are the current delivery status.
- Obtain plan approval and an execution-method choice before implementation. Use the appropriate execution and isolation skills then.
- Commands below use Linux paths inside the repository's WSL checkout. Run them with the stated working directory; PowerShell callers can use `wsl -d Ubuntu-24.04 --cd <absolute-directory> <command>`. Run dependent commands separately and check their exit status.
- Use `apply_patch` for file edits. Install dependencies only during the owning implementation task, updating the corresponding lockfile.
- Before any database reset, assert the database name is exactly `support_test`. Tests must not reset the development `support` database. Existing Postgres tests are serial; do not add parallel pytest workers.
- Before implementing, inspect `git status` and diffs in the root and `users-frontend/`. Preserve the existing clickable-row changes in `QueuePage.tsx`, `RunsPage.tsx`, and `workspace.css`.
- `users-frontend/` is presently an untracked nested repository. Preserve its `.git` metadata. An isolated checkout must deliberately include the approved documents, starter UI, and current intended baseline; an ordinary root worktree does not contain those untracked files.
- Do not stage an embedded gitlink, remove the nested `.git`, commit, or push without explicit user instruction. End each task with its tests and a local diff review. Resolve repository integration with the user if they request commits.
- Keep Python intake modules under `backend/app/intake/`; do not fold customer chat into the employee RAG drafting agent.
- Reuse the current backend dependency floors and the frontend's npm workspaces. Add Pillow only for image decoding, and frontend test dependencies only for interaction testing. No new database service, queue service, or agent deployment platform is needed.

## File map and dependency order

| Task | Files / responsibility |
| --- | --- |
| 1 | `app/intake/contracts.py`, `db_models.py`, `repository.py`, `errors.py`: typed state, session ownership, durable operation identities |
| 2 | `app/intake/evidence.py`, `policy.py`, `dates.py`: supported facts, corrections, readiness, category-specific questions |
| 3 | `app/intake/attachments.py`, `model.py`, `prompts/intake_v1.md`, `prompts/review_v1.md`: safe local images and bounded multimodal adapter |
| 4 | `app/intake/graph.py`, `review.py`, `turns.py`, `service.py`, `api/intake.py`, `api/intake_schemas.py`, `services/intake_runtime.py`: resumable turns and customer review API |
| 5 | `app/intake/submission.py`, `projection.py`, `services/intake_recovery.py`: exactly-once ticket creation, employee evidence and processing lifecycle |
| 6 | `users-frontend/apps/web/src/features/intake/{types,api,session,controller}.ts`: customer API/state transport and test setup |
| 7 | `users-frontend/apps/web/src/features/intake/` components, copy and styles: customer chat, upload, review and receipt |
| 8 | `employee-frontend/src/features/review/IntakeEvidence.tsx` and processing-state support: employee handoff presentation |
| 9 | `backend/tests/intake/test_handoff.py`, demo fixtures and runbook: whole-flow evidence and live vision verification |

Tasks 1–5 build the backend in order. Task 6 consumes the frozen HTTP contract below; Task 7 uses its controller. Task 8 consumes Task 5's result projection. Task 9 verifies all paths together.

## Shared contracts (implement in Task 1; extend only through explicit edits here)

Use Pydantic models with `extra="forbid"`, UUID identifiers serialized as strings, and timezone-aware datetimes. Store JSON with `model_dump(mode="json")`; create new values when changing JSONB state so SQLAlchemy observes the update.

| Type | Fields |
| --- | --- |
| `EvidenceRef` | `kind: Literal["message", "image"]`, `source_id: UUID`, `quote: str` |
| `Fact` | `key: str`, `status: Literal["known", "missing", "unknown", "conflicting", "not_applicable"]`, `value: str \| None`, `normalized: str \| None`, `evidence: list[EvidenceRef]`, `supersedes: list[EvidenceRef]` |
| `Question` | `key: str`, `text: str`, `reason: str`, `basis_revision: int` |
| `QuestionRecord` | `key: str`, `basis_revision: int`, `message_id: UUID`, `outcome: Literal["asked", "answered", "unknown"]` |
| `Message` | `id: UUID`, `role: Literal["user", "assistant"]`, `text: str`, `language: Literal["ar", "en"]`, `created_at: datetime`, `attachment_ids: list[UUID]` |
| `Attachment` | `id: UUID`, `filename: str`, `mime_type: str`, `size: int`, `width: int`, `height: int`, `message_id: UUID \| None`, `removed: bool` |
| `Readiness` | `quality: Literal["collecting", "sufficient_context", "partial_context"]`, `missing: list[str]`, `conflicts: list[str]`, `reason: str`, `next_key: str \| None` |
| `IntakeState` | `language: Literal["ar", "en"] = "ar"`, `category: str = "other"`, `facts: dict[str, Fact]`, `additional_issues: list[Fact]`, `additional_needed: list[str]`, `questions: list[QuestionRecord]`, `readiness: Readiness` |
| `Analysis` | `language: Literal["ar", "en"]`, `category: str`, `updates: list[Fact]`, `additional_issues: list[Fact]`, `suggested_question: Question \| None`, `additional_needed: list[str]`, `reinspect_images: list[UUID]` |
| `ReviewText` | `customer_text: str`, `employee_text_ar: str`, `fact_keys: list[str]` |
| `ReviewSnapshot` | `id: UUID`, `revision: int`, `language: Literal["ar", "en"]`, `quality: Literal["sufficient_context", "partial_context"]`, `facts: dict[str, Fact]`, `additional_issues: list[Fact]`, `unknown_keys: list[str]`, `customer_text: str`, `employee_text_ar: str`, `ticket_text_ar: str`, `attachment_ids: list[UUID]` |
| `Receipt` | `ticket_reference: str`, `submitted_at: datetime`, `processing_status: Literal["processing", "ready_for_employee", "needs_attention"]` |
| `SessionView` | `id: UUID`, `revision: int`, `phase: Literal["collecting", "review_ready", "submitted"]`, `language: Literal["ar", "en"]`, `turn_status: Literal["idle", "processing", "retryable_failure"]`, `active_request_id: UUID \| None`, `messages: list[Message]`, `attachments: list[Attachment]`, `readiness: Readiness`, `review: CustomerReview \| None`, `receipt: Receipt \| None`, `error_code: str \| None` |
| `CustomerReview` | `id: UUID`, `revision: int`, `language: Literal["ar", "en"]`, `quality: Literal["sufficient_context", "partial_context"]`, `text: str`, `facts: dict[str, Fact]`, `additional_issues: list[Fact]`, `unknown_keys: list[str]`, `attachment_ids: list[UUID]` (projection of `ReviewSnapshot`; omit internal/provider fields) |
| `Credentials` | `session_id: UUID`, `token: str` (returned only from create; never stored in plaintext in Postgres) |

Python-only dataclasses: `ImageInput(id: UUID, mime_type: str, data: bytes)`; `TurnContext(session_id: UUID, revision: int, state: IntakeState, messages: list[Message], attachments: list[Attachment], current_message_id: UUID | None)`; `TurnResult(state: IntakeState, assistant_text: str | None, review: ReviewSnapshot | None, trace: list[dict])`; `ModelCall(value: Analysis | ReviewText, trace: list[dict])`; `OperationClaim(session_id: UUID, request_id: UUID, attempt_id: UUID, revision: int, context: TurnContext)`. Give all collection fields independent default factories. `ModelUnavailable` carries an optional `trace` list for failed-call accounting.

Completion-audit amendment: `TurnContext` also carries `needs_analysis: bool = False`, derived from the latest customer message's durable operation status. Explicit review interprets an accepted-but-unprocessed message (and unbound uploads) before summarizing, within the same operation budget. This flag is internal and does not change the HTTP contract.

Use these fact keys: `issue`, `expected`, `actual`, `date`, `exact_error`, `repeats`, `attempted_steps`, `desired_outcome`, `txn_ref`, `amount`, `currency`, `customer_phone`, `recipient_phone`, `debited`, `recipient_outcome`, `device`, `app_version`, `failed_step`, `agent_location`, `merchant`, `biller`, `card_symptom`, `kyc_step`. Additional distinct issues are evidence-backed `Fact` objects in `additional_issues`; they do not overwrite the primary issue's amount/reference.

## HTTP contract (implemented in Tasks 4–5)

All owned routes use `Authorization: Bearer <token>`. Wrong/missing ownership returns 404/401 without exposing session existence. A 409 has `{detail: {code: "revision_conflict" | "operation_conflict" | "turn_busy" | "stale_review", message: string}}`; provider failure details remain server-side. Use `expected_revision` and a client UUID `request_id` on every session mutation.

| Method/path | Input | Success |
| --- | --- | --- |
| `POST /api/intake/sessions` | `{language: "ar" | "en"}` | 201 `{credentials: Credentials, session: SessionView}` |
| `GET /api/intake/sessions/{sid}` | authorization | 200 `SessionView` |
| `POST /api/intake/sessions/{sid}/messages` | `{request_id, expected_revision, text, language, attachment_ids}`; text max 6000 chars, text or image required | 200 updated `SessionView`; 202 if identical request still running |
| `POST /api/intake/sessions/{sid}/operations/{request_id}/retry` | `{expected_revision}`; same request identity, new server attempt | 200/202 `SessionView` |
| `POST /api/intake/sessions/{sid}/attachments` | multipart `file`, `request_id`, `expected_revision` | 201 `{attachment: Attachment, session: SessionView}` |
| `GET /api/intake/sessions/{sid}/attachments/{aid}` | authorization | validated image bytes, `Cache-Control: no-store` |
| `DELETE /api/intake/sessions/{sid}/attachments/{aid}` | JSON `{request_id, expected_revision}` | 200 `SessionView` |
| `POST /api/intake/sessions/{sid}/review` | `{request_id, expected_revision, allow_partial: boolean, language}` | 200 `SessionView` with current review |
| `POST /api/intake/sessions/{sid}/submit` | `{request_id, expected_revision, review_id, confirmed: true}` | 200 `Receipt` for both first submit and replay |
| `GET /api/results/{rid}/intake/attachments/{aid}` | existing local employee access model | bytes only if linked to that result's submitted snapshot |

Completed operation replay is checked before revision rejection, but only after authentication and fingerprint comparison. Operation fingerprints include endpoint kind and payload content except `expected_revision`, allowing a recovery retry against the current version without permitting changed content under the same ID. Submitted-session replay validates the accepted review ID and confirmation; a stale different review is not accepted merely because the session was submitted.

Replay returns the current session projection plus the same durable message/attachment identity, not an old `SessionView` that could roll back the UI. Receipt identity is stable while its processing status may advance. Creation has no accepted customer content until its response supplies credentials; a lost create response can leave an empty inaccessible session, but never loses or duplicates an accepted report. The client single-flight guard prevents duplicate initialization during remounts.

### Task 1: Durable intake sessions and ownership

**Files:**
- Create: `backend/app/intake/__init__.py`, `contracts.py`, `errors.py`, `db_models.py`, `repository.py`.
- Modify: `backend/app/db/session.py` (register intake models before `create_all`/`drop_all`), `backend/app/config.py`.
- Create: `backend/tests/intake/__init__.py`, `conftest.py`, `helpers.py`, `test_repository.py`.

**Interfaces:**
- `IntakeRepository(session_factory)` exposes `create(language: str) -> tuple[Credentials, SessionView]`, `get(credentials: Credentials) -> SessionView`, `authenticate(session: Session, credentials: Credentials, *, lock: bool = False) -> IntakeSessionRow`.
- `operation_fingerprint(kind: str, payload: dict) -> str`; `assert_same_operation(stored: str, incoming: str) -> None` raises `OperationConflict`.
- Domain errors in `errors.py`: `IntakeError`, `NotOwned`, `RevisionConflict`, `OperationConflict`, `TurnBusy`, `InvalidEvidence`, `ImageRejected`, `ModelUnavailable`, `StaleReview`; each has a stable `code` and safe public message.

- [ ] **Step 1: Establish the real Postgres fixture and failing ownership/replay tests.** In `tests/intake/conftest.py`, define `intake_db` yielding `(Settings, sessionmaker)` with the same `support_test` guard/reset/disposal pattern as `tests/test_workspace_api.py`. Create the repository fixture in `test_repository.py`. Include:

```python
def test_only_token_owner_can_resume(repo):
    from app.intake.contracts import Credentials
    from app.intake.errors import NotOwned
    owner, original = repo.create("ar")
    stranger, _ = repo.create("en")
    assert repo.get(owner).id == original.id
    with pytest.raises(NotOwned):
        repo.get(Credentials(session_id=owner.session_id, token=stranger.token))

def test_changed_payload_cannot_reuse_operation_identity():
    from app.intake.errors import OperationConflict
    from app.intake.repository import operation_fingerprint, assert_same_operation
    old = operation_fingerprint("message", {"text": "50000", "expected_revision": 1})
    same = operation_fingerprint("message", {"text": "50000", "expected_revision": 2})
    changed = operation_fingerprint("message", {"text": "5000", "expected_revision": 1})
    assert_same_operation(old, same)
    with pytest.raises(OperationConflict):
        assert_same_operation(old, changed)
```

- [ ] **Step 2: Run the red check from repository root.** `uv --directory backend run pytest tests/intake/test_repository.py -q`. Expect missing intake modules, not a connection error; start the existing test database if needed.

- [ ] **Step 3: Implement the shared models and schema.** Use the field table above. Persist five tables: `intake_sessions` (UUID PK, token hash, revision, phase, turn status, JSON state/review, current operation ID, timestamps); `intake_messages` (UUID PK, session FK, sequence, role/text/language, operation FK, timestamps); `intake_attachments` (UUID PK, session/message FKs, server storage key, hash/MIME/size/dimensions, tombstone); `intake_operations` (UUID PK plus unique session/request ID, kind, fingerprint, status, attempt UUID, claimed revision, request JSON, safe result JSON, error/usage); `intake_submissions` (UUID PK, unique session FK, unique ticket FK, initial run/result FKs, accepted review ID, immutable JSON snapshot, submitted timestamp). Use foreign keys and unique `(session_id, sequence)` for message ordering. Store attachment ownership with a session FK and operation identity so upload replay can recover the same row. All fields containing provider/raw state stay outside `SessionView`.

```python
def operation_fingerprint(kind: str, payload: dict) -> str:
    stable = {key: value for key, value in payload.items() if key != "expected_revision"}
    raw = json.dumps([kind, stable], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def new_access_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    return token, hashlib.sha256(token.encode("utf-8")).hexdigest()
```

Import `hashlib`, `json`, `secrets`, and use `secrets.compare_digest` to check hashes. `create` inserts a default `collecting` state and commits before returning. `get` reads the same state through a new session, proving it is not cached. Do not return token hashes, storage paths, operation request JSON, or model traces.

- [ ] **Step 4: Add configuration and minimal test builders.** Add settings `intake_model: str = ""` (effective value falls back to `gemini_model`), `intake_timeout_s=60`, `intake_max_model_requests=3`, `intake_upload_dir` rooted at repo `data/intake-uploads`, and the four image limits from the spec. Validate positive limits and nonblank configured model IDs. `helpers.py` defines `message(text, *, language="ar", at=None, attachments=()) -> Message`, `fact(key, value, source: Message, *, normalized=None, status="known") -> Fact`, and `context(messages=(), facts=(), *, category="other", revision=0, attachments=()) -> TurnContext`, all using these real models. `fact` uses the supplied source text as its quote; `context` initializes explicit collecting readiness and a new UUID session.

- [ ] **Step 5: Verify schema and durable round trips.** Add tests for token hash storage, messages ordering, Unicode JSON, timezone enforcement, rejected extra contract keys, uniqueness, and repeated `init_db` without dropping existing tickets. Run `uv --directory backend run pytest tests/intake/test_repository.py tests/test_workspace_api.py -q` and `uv --directory backend run ruff check app/intake app/db/session.py app/config.py tests/intake`. Review only this task's diff.

### Task 2: Evidence merging and adaptive readiness

**Files:** Create `backend/app/intake/evidence.py`, `policy.py`, `dates.py`, `backend/tests/intake/test_policy.py`, `test_evidence.py`, `test_dates.py`.

**Interfaces:**
- `merge_analysis(context: TurnContext, analysis: Analysis) -> IntakeState` validates source references and corrections.
- `assess_readiness(state: IntakeState, taxonomy: Taxonomy, *, allow_partial: bool = False) -> Readiness`.
- `choose_question(state: IntakeState, suggested: Question | None, revision: int) -> Question | None`.
- `normalize_reported_date(value: str, source_time: datetime) -> str | None`; `canonical_digits(value: str) -> str`.
- `remove_attachment_evidence(state: IntakeState, attachment_id: UUID) -> IntakeState` invalidates unsupported facts and readiness.

- [ ] **Step 1: Write source-grounding and gap tests using Task 1's helpers.** Include the actual branches below and parameterize the category requirements in Step 3.

```python
def test_known_answer_is_not_asked_again(taxonomy):
    from app.intake.policy import assess_readiness
    from tests.intake.helpers import context, fact, message
    m = message("حولت ٥٠ ألف أمس وما وصلت")
    ctx = context([m], [fact("issue", m.text, m), fact("amount", "٥٠ ألف", m, normalized="50000")],
                  category="failed_transfer")
    readiness = assess_readiness(ctx.state, taxonomy)
    assert "amount" not in readiness.missing
    assert readiness.quality == "collecting"

def test_foreign_message_cannot_ground_fact():
    from app.intake.contracts import Analysis
    from app.intake.evidence import merge_analysis
    from app.intake.errors import InvalidEvidence
    from tests.intake.helpers import context, fact, message
    local, foreign = message("فشل التحويل"), message("المبلغ 50000")
    proposal = Analysis(language="ar", category="failed_transfer",
                        updates=[fact("amount", "50000", foreign)], additional_issues=[],
                        suggested_question=None, additional_needed=[], reinspect_images=[])
    with pytest.raises(InvalidEvidence):
        merge_analysis(context([local]), proposal)
```

- [ ] **Step 2: Run the red checks.** `uv --directory backend run pytest tests/intake/test_policy.py tests/intake/test_evidence.py tests/intake/test_dates.py -q`. Expect missing functions until implementation exists.

- [ ] **Step 3: Implement a material-field policy, not a numeric score.** All categories require a grounded `issue`. Problem reports also need `actual`, `expected`, and `date`, unless evidence establishes a field is genuinely not applicable. Category-specific material sets: failed transfer → `amount`, `debited`, `recipient_outcome`; wrong recipient → `amount`, `recipient_phone`; agent dispute → `amount`, `agent_location`; bill payment → `amount`, `biller`; refund → `amount`, `merchant`; app bug → `failed_step`, `device`; login → `failed_step`; card → `card_symptom`; KYC → `kyc_step`; fraud → `actual`; general inquiry → `issue`; other → `issue`, `desired_outcome`. Map taxonomy `date`/`amount` directly and its ambiguous `phone` to `recipient_phone` for wrong-recipient reports; never auto-map it to the customer's phone. `txn_ref`, error text, retries and app version are high-value conditional follow-ups, not universally mandatory fields.

```python
def field_needs_question(item: Fact | None) -> bool:
    return item is None or item.status in {"missing", "conflicting"}

def field_is_resolved(item: Fact | None) -> bool:
    return item is not None and item.status in {"known", "not_applicable"}
```

Readiness is sufficient only when all material fields are resolved, no material conflicts/additional issues are unclear, and `additional_needed` has no validated high-value gaps. An explicit unknown never produces sufficient readiness. After alternative questions are exhausted, return partial readiness and a review invitation; `allow_partial=True` also permits that path. `choose_question` uses the highest-value unresolved key, rejects a suggestion for an answered/unknown key, and uses a localized field-specific fallback if the model suggestion is unusable. Record why the question matters. Re-asking after a genuinely new contradiction is allowed; identical questions at unchanged evidence are not.

- [ ] **Step 4: Implement evidence and correction rules.** Message evidence must belong to this session and quote an actual substring of the stored sanitized source. Image evidence must reference an attached, nonremoved image visible to the model. A `known` fact needs nonblank value and evidence; missing/unknown/not-applicable values remain null. Evidence for unknown/not-applicable must explain the customer's answer or applicability decision. Corrections replace values only when supported by a newer explicit correction; otherwise mark conflicting and ask. Preserve superseded evidence. Retain unchanged facts when the model omits them; category changes only alter applicability. Persist validated `additional_needed` into the state. An assistant's own prior assertion cannot ground a new customer fact.

For transaction references, amounts, phones and exact errors, require the reported value to be present in supporting text after digit normalization, rather than accepting an unrelated value next to a valid quote. Compute normalized amount/phone with `parse_amount` and `normalize_phone` from `app.pipeline.stage1_normalize.candidates` where their input is supported; compute dates using this task's date helper. Reject a provider-normalized value that disagrees with deterministic normalization. When parsing cannot establish a precise value, preserve the report and ask for clarification. Do not accept the amount parser's default IQD as explicit currency evidence. Image values remain observed rather than system-verified; customer review confirms them. Test a valid quote containing 50000 paired with a hallucinated normalized 500000 is rejected.

- [ ] **Step 5: Normalize dates and identifiers conservatively.** Reuse `Asia/Baghdad` and existing Arabic digit normalization where suitable; add Persian digits. Resolve only unambiguous English `today`/`yesterday`, Iraqi equivalents, or explicit dates. Keep broad times broad; never synthesize an hour. Use the source message date, not submission time. Test:

```python
def test_yesterday_is_anchored_to_message_in_baghdad():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from app.intake.dates import normalize_reported_date, canonical_digits
    sent = datetime(2026, 10, 18, 0, 5, tzinfo=ZoneInfo("Asia/Baghdad"))
    assert normalize_reported_date("yesterday", sent) == "2026-10-17"
    assert normalize_reported_date("أمس", sent) == "2026-10-17"
    assert canonical_digits("٥٠٠٠٠ / ۵۰۰۰۰") == "50000 / 50000"
```

Also test ambiguous `10/11` returns no fabricated date, screenshot removal clears image-only facts, recipient-phone evidence never populates `customer_phone`, and general inquiries are not forced through incident questions.

- [ ] **Step 6: Verify this decision boundary.** `uv --directory backend run pytest tests/intake/test_policy.py tests/intake/test_evidence.py tests/intake/test_dates.py -q`; `uv --directory backend run ruff check app/intake tests/intake`. Inspect tests for both unknown and conflicting facts and for an initially complete complaint reaching sufficient readiness without extra questions.

### Task 3: Validated attachments and bounded multimodal interpretation

**Files:** Create `backend/app/intake/attachments.py`, `model.py`, `prompts/intake_v1.md`, `prompts/review_v1.md`, `backend/tests/intake/test_attachments.py`, `test_model.py`; modify `backend/pyproject.toml`, `backend/uv.lock`, `.env.example`, `.gitignore`.

**Interfaces:**
- `AttachmentStore(settings, session_factory)` exposes `upload(credentials, request_id: UUID, expected_revision: int, filename: str, content: bytes) -> tuple[Attachment, SessionView]`, `read(credentials, attachment_id: UUID) -> ImageInput`, `remove(credentials, attachment_id: UUID, request_id: UUID, expected_revision: int) -> SessionView`.
- `IntakeModel.analyze(context: TurnContext, images: list[ImageInput], budget: ModelBudget) -> ModelCall` and `IntakeModel.summarize(state: IntakeState, language: str, budget: ModelBudget) -> ModelCall` are async methods.
- `ModelBudget(timeout_s: float, max_requests: int)` exposes `remaining_s() -> float`, `consume() -> None`, and `trace: list[dict]`; `consume` atomically checks deadline and increments its request counter or raises `ModelUnavailable`. `OpenRouterIntakeModel(settings, *, runnable_factory=None)` implements the two methods. Tests use `ScriptedIntakeModel(analyses: list[Analysis | Exception | Callable[[TurnContext], Analysis]], reviews: list[ReviewText | Exception | Callable[[IntakeState, str], ReviewText]])` in `tests/intake/helpers.py`, recording calls and returning `ModelCall` values. Callables generate source references from real current message IDs; default HTTP fixtures use a callable that asks for context from the current message rather than invented IDs.

- [ ] **Step 1: Write failing image ownership/content tests.** Generate small valid images in memory with Pillow in tests, and verify that a filename/MIME lie cannot become a stored image.

```python
def test_image_bytes_are_decoded_not_trusted(store, repo):
    from uuid import uuid4
    from app.intake.errors import ImageRejected
    credentials, view = repo.create("ar")
    with pytest.raises(ImageRejected):
        store.upload(credentials, uuid4(), view.revision, "receipt.png", b"<svg>not a PNG</svg>")
    assert repo.get(credentials).attachments == []
```

Add tests for byte/pixel limits, forged extension, animation/multiple frames rejection, corrupt/truncated images, ten-image concurrency, cross-session reads, removed attachments, upload replay, changed bytes with same request ID, and path-like filenames. An upload replay must not increment revision or write a second file.

- [ ] **Step 2: Install the decoder and run red tests during execution.** From `backend/`, run `uv add pillow`, then `uv run pytest tests/intake/test_attachments.py tests/intake/test_model.py -q`. Image-construction imports should now work; missing implementation should be the failure.

- [ ] **Step 3: Implement storage with a recoverable database/filesystem boundary.** Decode with `Image.open(BytesIO(content))`, inspect actual format/dimensions, run `verify()`, reopen and `load()`, rejecting frames other than one and formats outside JPEG/PNG/WebP. Check byte size before decoding and pixel dimensions before full load. Derive MIME/extension from detected format. Store original accepted bytes under `<session_uuid>/<attachment_uuid>.<extension>`; never use customer paths. Write to a unique staging path and atomically replace before committing metadata. If the transaction fails, remove the unreferenced new file. Startup cleanup removes stale staging/unreferenced files only after checking their metadata and age; never delete a referenced image.

```python
with Image.open(BytesIO(content)) as image:
    if image.format not in {"JPEG", "PNG", "WEBP"}:
        raise ImageRejected("Unsupported image format")
    if image.width * image.height > settings.intake_max_image_pixels:
        raise ImageRejected("Image resolution is too large")
    if getattr(image, "n_frames", 1) != 1:
        raise ImageRejected("Upload a single screenshot")
    image.verify()
```

Authenticate and lock session for count/revision/operation checks. Uploads invalidate review. Removal uses a tombstone, unlinks the file after commit, calls `remove_attachment_evidence`, clears review, and advances revision; do not allow removal/upload during an active turn or after submission. Retain a transcript marker for removed attachments. Read checks session ownership and tombstone before opening the server-generated path.

- [ ] **Step 4: Implement the multimodal adapter using the existing SDK conventions.** Follow `app/llm.py` for timeout milliseconds and disabling SDK retries. Each operation shares one `ModelBudget`; every provider request, including repairs and reinspection, consumes it. Keep the wrapper separate from `GeminiStructuredLLM` so existing classification behavior is unaffected.

```python
chat = ChatOpenRouter(
    model=settings.intake_model or settings.gemini_model,
    api_key=settings.openrouter_api_key,
    timeout=int(settings.intake_timeout_s * 1000),
    max_retries=0,
    model_kwargs={"retries": None},
)
runnable = chat.with_structured_output(Analysis, method="json_schema", include_raw=True)
blocks = [{"type": "text", "text": serialized_context}]
for image in images:
    encoded = base64.b64encode(image.data).decode("ascii")
    blocks.append({"type": "text", "text": f"Attachment ID: {image.id}"})
    blocks.append({"type": "image_url", "image_url": {
        "url": f"data:{image.mime_type};base64,{encoded}"}})
result = await runnable.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=blocks)])
```

Use `ReviewText` for summarize. Serialize facts, pending gaps, relevant quoted evidence, current message, and recent history; preserve original source UUIDs. Bound prompt size explicitly and return a recoverable context-budget error if mandatory evidence cannot fit. No transaction/KB tools are bound. Record model/usage/cost metadata for every executed call, including malformed output and transient failures; absent cost remains null/unknown. Sanitize public errors. Retry transport/408/429/5xx only inside remaining budget, and allow at most one structured-output repair. Configure prompt/system instructions to return evidence-backed updates, one question, never credential requests, and no claim of verified transaction status.

- [ ] **Step 5: Pin actual wire payload and limits with a fake runnable.** Implement `CapturingRunnable` in `test_model.py` with `async ainvoke(messages)` recording messages and returning a constructed raw `AIMessage` plus parsed `Analysis`. Inject it through a model constructor `runnable_factory(schema)` test seam. Assert an `image_url` data URI with the decoded image's true MIME and attachment ID is present; assert no image is sent for text-only turns. Use a failing runnable to prove three requests exhaust the shared budget and that elapsed deadline prevents another call. Test invalid JSON schema output, absent usage/cost, and prompt-injection text inside image observations.

- [ ] **Step 6: Verify and document configuration.** Add `.env.example` entries for effective intake model, timeout/request limits and upload path; ignore `data/intake-uploads/`. Run `uv --directory backend run pytest tests/intake/test_attachments.py tests/intake/test_model.py -q` and `uv --directory backend run ruff check app/intake tests/intake`. Do not declare the configured provider vision-capable based solely on these fake tests; Task 9 verifies it live.

### Task 4: Resumable graph turns, review and customer API

**Files:** Create `backend/app/intake/graph.py`, `review.py`, `turns.py`, `service.py`, `backend/app/api/intake.py`, `intake_schemas.py`, `backend/app/services/intake_runtime.py`, `backend/tests/intake/test_graph.py`, `test_review.py`, `test_turns.py`, `test_api.py`; modify `backend/app/main.py` and `backend/tests/intake/conftest.py`.

**Interfaces:**
- `IntakeGraph(model: IntakeModel, taxonomy: Taxonomy, store: AttachmentStore, settings)` exposes async `advance(context: TurnContext) -> TurnResult` and `review(context: TurnContext, *, allow_partial: bool, language: str) -> TurnResult`.
- `build_review(context: TurnContext, state: IntakeState, text: ReviewText) -> ReviewSnapshot` checks language/number/evidence consistency and creates frozen ticket text.
- `TurnStore(session_factory)` exposes `claim(credentials, kind, request_id, expected_revision, payload) -> OperationClaim | SessionView`, `finish(claim, result: TurnResult) -> SessionView`, `fail(claim, error_code: str, trace: list[dict]) -> SessionView`, `retry(credentials, request_id, expected_revision) -> OperationClaim | SessionView`, `recover_interrupted() -> int`.
- `IntakeService(repo, turns, graph, store)` exposes async `message(credentials, command)`, `review(credentials, command)`, `retry(credentials, request_id, expected_revision)` returning `SessionView`; sync `create/get` delegate to repository. Routes use these methods and Task 3's attachment store.
- `make_intake_service(session_factory, settings, taxonomy) -> IntakeService`; extend the app signature to `create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None, intake_builder=None)` for fake-model injection using this signature.

- [ ] **Step 1: Write failing operation-recovery tests.** Define `intake_client` in the new test conftest with real test DB, `ScriptedIntakeModel`, `AttachmentStore(tmp_path)`, and the existing fake-pipeline pattern. Expose service/model through fixture attributes rather than real provider calls.

```python
def test_message_replay_is_single_turn(intake_client):
    from uuid import uuid4
    created = intake_client.post("/api/intake/sessions", json={"language": "en"}).json()
    sid, token = created["credentials"]["session_id"], created["credentials"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    url = f"/api/intake/sessions/{sid}/messages"
    body = {"request_id": str(uuid4()), "expected_revision": 0,
            "text": "My transfer failed", "language": "en", "attachment_ids": []}
    first = intake_client.post(url, headers=headers, json=body)
    second = intake_client.post(url, headers=headers, json=body)
    assert first.status_code == second.status_code == 200
    assert [m["id"] for m in first.json()["messages"]] == [m["id"] for m in second.json()["messages"]]
    changed = intake_client.post(url, headers=headers, json=body | {"text": "Different issue"})
    assert changed.status_code == 409
```

Add an async barrier test: claim a turn, recover it, claim retry with new attempt UUID, then release the old model response. `finish(old_claim, result)` must refuse it; current facts/review must reflect only the retry. Test resume through a new service instance, stale revision conflict, missing token, image-only message, repeated question suppression, and review after a failed model call.

```python
def test_recovered_attempt_cannot_publish_stale_output(repo, turns):
    from uuid import uuid4
    from app.intake.contracts import TurnResult
    from app.intake.errors import RevisionConflict
    owner, view = repo.create("en")
    request_id = uuid4()
    old = turns.claim(owner, "message", request_id, view.revision,
                      {"text": "Transfer failed", "language": "en", "attachment_ids": []})
    turns.recover_interrupted()
    fresh = turns.retry(owner, request_id, repo.get(owner).revision)
    with pytest.raises(RevisionConflict):
        turns.finish(old, TurnResult(old.context.state, "Stale question", None, []))
    saved = turns.finish(fresh, TurnResult(fresh.context.state, "Current question", None, []))
    assert "Stale question" not in [m.text for m in saved.messages]
    assert [m.text for m in saved.messages].count("Transfer failed") == 1
```

- [ ] **Step 2: Run red checks.** `uv --directory backend run pytest tests/intake/test_turns.py tests/intake/test_api.py tests/intake/test_graph.py tests/intake/test_review.py -q`.

- [ ] **Step 3: Implement transactional turn claiming and completion.** `claim` authenticates/locks session, checks replay fingerprint before expected revision, rejects another active operation, appends the customer message exactly once, binds owned unbound attachments, clears stale review, increments revision, records attempt ID, and commits. It rejects duplicate attachment IDs, more than three images, foreign/removed images, and already-bound images from another message. `finish` compares session active request, attempt ID and claimed revision, then atomically saves facts, one assistant reply, question history, review, completed operation result, and next revision. `fail` clears executing state but retains the failed request ID for retry, without deleting the customer message; append usage audit with its attempt ID. `retry` reuses request payload/message identity but generates a new attempt ID. Restart recovery fences interrupted attempts and leaves them retryable. Block user mutations while processing rather than allowing concurrent image removal.

Revision invariant: `OperationClaim.revision` is the committed revision after claiming. Publication advances to `claim.revision + 1`; `build_review` uses that same publication revision. Therefore `SessionView.review.revision == SessionView.revision` on successful review, and submission compares against that value. Test this invariant explicitly. Retried/replayed operations must not roll back newer session projections. Preserve cost/usage audit even when stale-attempt fencing rejects its state output.

```python
with session_factory.begin() as session:
    row = repo.authenticate(session, credentials, lock=True)
    operation = session.scalar(select(IntakeOperationRow).where(
        IntakeOperationRow.session_id == row.id,
        IntakeOperationRow.request_id == request_id,
    ))
    if operation is not None:
        assert_same_operation(operation.fingerprint, incoming_fingerprint)
        # Return the current projection for completed replay;
        # return current processing state for an identical active request.
    if row.revision != expected_revision:
        raise RevisionConflict("Reload the current conversation")
```

Put the replay return before the final revision branch; do not hold this transaction while awaiting the model. Use `run_in_threadpool` around synchronous database/file methods called by async routes, returning detached DTOs rather than sessions across thread boundaries.

- [ ] **Step 4: Implement the graph and snapshot builder.** Build a `StateGraph` with analyze → merge/evaluate → ask or review → END. Each invocation processes exactly one turn. Only pass current attached images initially; if `reinspect_images` names an owned, nonremoved historical image, perform one bounded reanalysis with it. All calls share the same deadline/request budget. The service saves nothing from an invalid proposal. `advance` produces review when sufficient or when all useful questions are exhausted with partial context. Explicit `review` verifies that at least one customer message/image exists and never silently turns unknowns into known facts.

```python
def validate_review_numbers(state: IntakeState, text: ReviewText) -> None:
    allowed = {canonical_digits(part) for fact in state.facts.values()
               for value in (fact.value, fact.normalized) if value
               for part in re.findall(r"[\w]*\d[\w:/.,+\-]*", canonical_digits(value))}
    for rendered in (text.customer_text, text.employee_text_ar):
        observed = set(re.findall(r"[\w]*\d[\w:/.,+\-]*", canonical_digits(rendered)))
        if not observed.issubset(allowed):
            raise InvalidEvidence("Summary contains an unsupported identifier or number")
```

Use the numeric check as one guard, not as proof of semantic translation. Require all material fact keys in `ReviewText.fact_keys`, then render explicit fact rows from canonical facts alongside prose, so missing/altered amounts, dates and references cannot hide in translation. Preserve exact error quotes. Ensure natural number formatting is normalized consistently (group separators and Arabic digits) in both extraction and validation; test `50,000` against `50000` rather than rejecting equivalent amounts. Label any conflicting/unknown values separately. `ticket_text_ar` is rendered from these reviewed rows and Arabic narrative, contains absolute confirmed dates, and must be at most 6000 characters. A failed consistency/length check produces a recoverable review error without saving a ready review. Reuse the same Arabic text when the customer language is Arabic.

- [ ] **Step 5: Expose the routes and wire startup.** Implement the HTTP table except submit/employee attachment routes, which belong to Task 5. Use separate response DTOs and exception mapping. CORS allows exact development hosts for ports 5173/5174 and `Authorization`/`Content-Type`; include DELETE. The customer Vite proxy also supports relative API URLs. Initialize service once per app, recover interrupted turns at startup, and leave the existing provider initialization lazy so unconfigured tests can create sessions. When a turn fails, return the saved `SessionView` with `turn_status="retryable_failure"` and a safe error code; do not cause the client to resend it as a new message.

- [ ] **Step 6: Verify review freshness and translation.** Include code-level tests for English-to-Arabic summary number changes, Persian digits, midnight date anchoring, removed screenshot invalidation, and local credential-question fallback. The credential guard rejects generated requests for secrets and uses a known-safe localized question for that field; do not block a customer's report merely for mentioning OTP fraud. Run `uv --directory backend run pytest tests/intake -q` and `uv --directory backend run ruff check app/intake app/api/intake.py app/api/intake_schemas.py app/services/intake_runtime.py app/main.py tests/intake`. Review FastAPI OpenAPI models against the HTTP table.

### Task 5: Exactly-once submission and durable employee visibility

**Files:** Create `backend/app/intake/submission.py`, `projection.py`, `backend/app/services/intake_recovery.py`, `backend/tests/intake/test_submission.py`, `test_processing.py`; modify `backend/app/api/intake.py`, `api/results.py`, `services/workspace_queries.py`, `services/batch_jobs.py`, `services/reviews.py`, `main.py`, and the intake test fixtures.

**Interfaces:**
- `SubmissionService(session_factory, settings).submit(credentials, request_id: UUID, expected_revision: int, review_id: UUID, confirmed: bool) -> SubmissionResult`.
- `SubmissionResult` dataclass: `receipt: Receipt`, `run_id: int`, `ticket: Ticket`, `mode: str`, `dispatch: bool`.
- `intake_result_view(session: Session, ticket_id: int) -> dict | None`; `employee_attachment(session: Session, result_id: int, attachment_id: UUID, store: AttachmentStore) -> ImageInput`.
- `fail_intake_placeholders(session: Session, run_id: int, reason: str) -> int`; `recover_intake_processing(session_factory) -> int`.
- `dispatch_intake(app, submission: SubmissionResult) -> None` invokes existing `run_job` only for a newly committed submission. Extend the app signature to `create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None, intake_builder=None, intake_dispatcher=None)` for no-op/failing-dispatch tests.

- [ ] **Step 1: Add a reviewed-session fixture and failing submission tests.** `reviewed` creates a session, scripts a grounded general inquiry plus matching summaries, sends the customer text through the API and requests review if not already ready. It returns `{sid, headers, view}`. The fixture uses the real intake graph/DB and fake model; configure dispatch as a no-op so tests can observe the initial placeholder.

```python
def test_submission_replay_creates_one_ticket(intake_client, reviewed):
    from uuid import uuid4
    url = f"/api/intake/sessions/{reviewed['sid']}/submit"
    view = reviewed["view"]
    payload = {"request_id": str(uuid4()), "expected_revision": view["revision"],
               "review_id": view["review"]["id"], "confirmed": True}
    first = intake_client.post(url, headers=reviewed["headers"], json=payload)
    replay = intake_client.post(url, headers=reviewed["headers"], json=payload)
    assert first.status_code == replay.status_code == 200
    assert replay.json() == first.json()
    rows = intake_client.get("/api/results").json()["items"]
    assert len(rows) == 1
    assert rows[0]["status"] == "processing"
    assert rows[0]["ticket"]["external_id"] == first.json()["ticket_reference"]
    run = intake_client.get(f"/api/runs/{rows[0]['run_id']}").json()
    assert run["processed"] == 0 and run["total"] == 1
```

Add a true two-connection concurrency test with a barrier and the same reviewed session; require one ticket/run/result and one `dispatch=True`. Also test two different request IDs submitting the same approved review return the same ticket. A different review ID or changed confirmation must conflict, and unsubmitted sessions must be absent from all employee queries.

- [ ] **Step 2: Run red checks.** `uv --directory backend run pytest tests/intake/test_submission.py tests/intake/test_processing.py -q`.

- [ ] **Step 3: Implement the single transaction and frozen snapshot.** Lock session and authenticate. Check completed request fingerprint and existing submission before checking the stale pre-submit revision; preserve accepted-review validation on replay. Require `confirmed is True`, current ready review, matching revision, no active turn, and only session-owned nonremoved attachments. Create a stable external ID `INTAKE-<session_uuid_hex>`, frozen `Ticket`, `RunRow`, and `TicketResultRow(status="processing")` in the same transaction as the submission row and phase change. Use `upsert_tickets`, `create_run`, and existing model-ID/prompt-version helpers. Mode is existing `cascade` by default; tests use injected pipeline and settings. If provider setup is incomplete, retain the accepted ticket and let dispatch record a failed processing result rather than undoing submission.

```python
placeholder = TicketResultRow(
    run_id=run_id,
    ticket_id=ticket.id,
    status="processing",
    category_probs={}, flags={}, extracted={}, escalation_reasons=[],
    citations=[], agent_trace=[],
)
session.add(placeholder)
session.flush()
run.counts = {"expected_total": 1, "total": 0, "by_status": {}}
```

Persist full submitted transcript and fact/evidence snapshots, not access tokens or model secrets. `customer_phone` is populated only from its own known/confirmed fact. Use frozen `ticket_text_ar`, absolute dates, submission UTC `received_at`, and immutable start/message timestamps. Only return `dispatch=True` after commit. The API schedules `dispatch_intake` with BackgroundTasks once; repeating submit does not schedule again.

- [ ] **Step 4: Fix the result lifecycle and count/review boundaries.** `save_outcomes` already upserts `(run_id, ticket_id)` and will replace the placeholder. Change `run_view` processed-count query to exclude `status="processing"`. Add a guard in `record_review` before all actions so processing results cannot be approved, rejected or reassigned. Ensure top-level `run_job` failure, per-ticket persistence failure, and startup interrupted-run recovery each call `fail_intake_placeholders` in their durable recovery transaction. Preserve completed outcomes, costs, and existing non-intake batch semantics. Startup recovery must handle a committed intake run that never reached the scheduler.

```python
def test_processing_ticket_rejects_review(intake_client, reviewed):
    # Submit using the fixture's current review, then fetch its only result.
    from uuid import uuid4
    view = reviewed["view"]
    intake_client.post(f"/api/intake/sessions/{reviewed['sid']}/submit",
        headers=reviewed["headers"], json={"request_id": str(uuid4()),
        "expected_revision": view["revision"], "review_id": view["review"]["id"], "confirmed": True})
    row = intake_client.get("/api/results").json()["items"][0]
    response = intake_client.post(f"/api/results/{row['id']}/reviews", json={
        "action": "approve", "reviewer": "Agent", "final_text": "رد",
        "expected_updated_at": row["updated_at"]})
    assert response.status_code == 409
```

Failure reconciliation counts a now-durable failed intake result as processed, while preserving existing tests where a non-intake outcome was never saved. Recompute counts from durable results after replacing placeholders, preserving `expected_total` and actual saved costs; do not count an in-memory outcome whose save failed. Do not make `run.counts.total`, `processed`, and status counts disagree after recovery. Add tests for crash-before-dispatch, dispatch exceptions, failure to save an outcome, and a successful outcome replacing the same placeholder ID. `recover_intake_processing` covers running runs and already-failed runs that still have processing placeholders; call it after the existing generic startup recovery.

```python
def test_committed_but_unscheduled_ticket_survives_recovery(intake_client, reviewed):
    from uuid import uuid4
    from app.services.intake_recovery import recover_intake_processing
    view = reviewed["view"]
    intake_client.post(f"/api/intake/sessions/{reviewed['sid']}/submit",
        headers=reviewed["headers"], json={"request_id": str(uuid4()),
        "expected_revision": view["revision"], "review_id": view["review"]["id"], "confirmed": True})
    assert recover_intake_processing(intake_client.app.state.session_factory) == 1
    row = intake_client.get("/api/results").json()["items"][0]
    assert row["status"] == "failed"
    detail = intake_client.get(f"/api/results/{row['id']}").json()
    assert detail["intake"]["messages"]
    assert recover_intake_processing(intake_client.app.state.session_factory) == 0
```

- [ ] **Step 5: Add employee and receipt projections.** Detail responses receive `intake: null | {summary_ar, quality, facts, additional_issues, unknown_keys, messages, attachments, submitted_at}`. Each attachment contains metadata plus `download_url` for the employee result-linked route; no token/path/provider state appears. Query `intake_submissions` by ticket ID so a new processing run still displays the original evidence. Employee download requires both the result/ticket association and membership in the frozen snapshot; draft UUIDs are never served. Customer receipt status is a coarse mapping of latest result (`processing` → processing; `failed` → needs_attention; other saved outcomes → ready_for_employee), never “resolved” merely because a response was approved.

- [ ] **Step 6: Verify compatibility and transaction boundaries.** Run `uv --directory backend run pytest tests/intake tests/test_workspace_api.py tests/test_repository.py -q`, then `uv --directory backend run ruff check app tests/intake`. Confirm both the submitted employee detail and customer receipt can be read after constructing a new app instance. Existing `/api/runs` duplicate-ID safeguards must still pass.

### Task 6: Customer API client and resumable UI state

**Files:** Create `users-frontend/apps/web/src/features/intake/types.ts`, `api.ts`, `session.ts`, `controller.ts`, `api.test.ts`, `controller.test.ts`, `users-frontend/apps/web/vitest.config.ts`, `src/test/setup.ts`; modify user `apps/web/package.json`, root `package-lock.json`, `apps/web/vite.config.ts`, and `employee-frontend/vite.config.ts` for strict ports.

**Interfaces:**
- `types.ts` mirrors the public HTTP models, converting UUID/datetime to strings and excluding server-only fields.
- `createIntakeApi(baseUrl = "/api/intake") -> IntakeApi` with `create`, `get`, `message`, `review`, `retry`, `submit`, `upload`, `remove`, `image` methods corresponding exactly to the HTTP table; every method accepts an optional `AbortSignal`.
- `SessionStorage` interface: `load(): SavedSession | null`, `save(value: SavedSession): void`, `clear(): void`; `SavedSession={credentials, pending: PendingOperation | null}`. `PendingOperation={kind:"message"|"review"|"submit", request_id:string, payload:object}` keeps the exact replay payload. Token and pending draft are browser-local, not logged or placed in URLs.
- `IntakeController(api: IntakeApi, storage: SessionStorage)` exposes `initialize(language)`, `send(text, language, attachmentIds)`, `requestReview(allowPartial, language)`, `submit()`, `retry()`, `upload(file)`, `remove(attachmentId)`, `startNew(language)`, `refresh()`, `subscribe(listener)`, `getSnapshot()`, and `dispose()` for cancelling owned polling/network work.
- `ControllerState={session: SessionView | null, busy:boolean, error:string | null, uploads:Record<string,number>}`. Controller owns a single-flight initialization promise, client operation IDs, and current revision. Components subscribe using `useSyncExternalStore`.

- [ ] **Step 1: Add the test harness and a failing single-flight test.** From `users-frontend/`, install `npm install --save-dev --workspace web vitest@^5 @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom`; update the lockfile. Add web script `"test": "vitest run"`. Merge the existing Vite config in `vitest.config.ts`, with `environment:"jsdom"` and setup file `src/test/setup.ts`; setup imports `@testing-library/jest-dom/vitest` and calls RTL `cleanup` after each test.

```ts
it("creates one session when initialized twice", async () => {
  const api = fakeApi()
  const storage = memoryStorage()
  const controller = new IntakeController(api, storage)
  await Promise.all([controller.initialize("ar"), controller.initialize("ar")])
  expect(api.create).toHaveBeenCalledTimes(1)
  expect(storage.load()?.credentials.session_id).toBe("session-1")
})
```

Define `fakeApi` and `memoryStorage` in `controller.test.ts`; fake API returns a full empty `SessionView` matching the schema, has `vi.fn` methods, and issues controlled deferred promises for race cases. No live network is used.

- [ ] **Step 2: Run the red check from `users-frontend/`.** `npm --workspace web run test -- src/features/intake/controller.test.ts src/features/intake/api.test.ts`.

- [ ] **Step 3: Implement the typed client and persistence.** All owned requests attach Authorization. Use `fetch` for JSON and authorized image blobs; use `XMLHttpRequest` for uploads to expose real upload progress. Upload fingerprint identity is stable across transport retries, including the same file bytes. Do not manually set multipart Content-Type. Validate parsed responses enough to reject missing `id/revision/phase` or an invalid receipt rather than rendering undefined state. Handle JSON and non-JSON errors with a localized safe fallback.

```ts
const response = await fetch(`${baseUrl}/sessions/${credentials.session_id}/messages`, {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${credentials.token}` },
  body: JSON.stringify(command),
  signal,
})
```

The storage implementation handles unavailable/quota-exceeded localStorage without losing the in-memory session; display that resume is unavailable rather than pretending it was persisted. A pending JSON operation is saved before dispatch and cleared only after reconciling success. Image blobs stay in memory; after a refresh, fetch server attachment metadata and request reselection only for uploads that never reached the server.

- [ ] **Step 4: Implement the controller state transitions.** `initialize` resumes stored credentials with GET; it does not create sessions inside a render/effect loop. The shared controller instance lives outside remounting components. Single-flight all mutations, pass the latest revision after each completed upload, and generate an operation ID only when creating a new logical action. After a network error, retain pending payload and GET session state before retrying. On 409, load current state and show a conflict; do not automatically overwrite another tab's change. On a saved retryable model failure, use the retry endpoint instead of a new message ID. Poll an in-flight turn every two seconds for up to 70 seconds, cancelling timers on disposal/state completion; exhaustion offers manual refresh/retry and preserves data.

```ts
it("retries a lost submission response with the original request ID", async () => {
  const api = fakeApi({ phase: "review_ready" })
  const controller = new IntakeController(api, memoryStorage())
  await controller.initialize("en")
  api.submit.mockRejectedValueOnce(new TypeError("connection lost"))
  await controller.submit()
  const original = api.submit.mock.calls[0][1].request_id
  await controller.retry()
  expect(api.submit.mock.calls[1][1].request_id).toBe(original)
})
```

Pin replay after reload, stale-tab review, changed body under reused ID, upload completion before message send, and storage exceptions. `startNew` requires a deliberate UI action, leaves the old server report intact, and fences late responses from the previous session.

- [ ] **Step 5: Configure relative API URLs and distinct dev ports.** In user Vite config add `server: {host:"0.0.0.0", port:5174, strictPort:true, proxy:{"/api":"http://127.0.0.1:8000"}}`; configure preview proxy too. Add `port:5173, strictPort:true` to the existing employee server config while retaining its proxy. Both frontend clients use relative `/api` URLs by default.

- [ ] **Step 6: Verify the client layer.** From `users-frontend/`, run `npm --workspace web run test -- src/features/intake/api.test.ts src/features/intake/controller.test.ts`, `npm --workspace web run typecheck`, and `npm --workspace web run lint`. Check no API token appears in logged errors, DOM links, or upload paths. Run employee `npm run build` only if its config modification causes a build concern; the full frontend checks are Task 9.

### Task 7: Bilingual customer chat, screenshots and reviewed submission

**Files:** Create under `users-frontend/apps/web/src/features/intake/`: `IntakePage.tsx`, `ChatTranscript.tsx`, `MessageComposer.tsx`, `ScreenshotPicker.tsx`, `OwnedImage.tsx`, `ReviewPanel.tsx`, `ReceiptPanel.tsx`, `copy.ts`, `intake.css`, `IntakePage.test.tsx`; modify `apps/web/src/App.tsx`, `apps/web/index.html`, and `apps/web/src/main.tsx` only as needed for title/style imports.

**Interfaces:**
- `IntakePage({controller: IntakeController})` is the composed screen; default App provides one shared controller.
- Presentational components consume `SessionView`, `CustomerReview`, or `Receipt`, plus explicit callbacks; none reads localStorage or calls backend endpoints directly except `OwnedImage` through the injected API.
- `OwnedImage({attachment, credentials, api})` retrieves an authorized blob, creates/revokes a local object URL, and aborts stale fetches. It never puts a bearer token in `<img src>`.
- `copy` exports `Record<"ar"|"en", IntakeCopy>` with identical translation keys.

- [ ] **Step 1: Load frontend-design at execution and translate the approved workflow into a focused screen.** Use the existing user-frontend theme provider/button and Arabic-capable system fonts. Layout: branded header with language switch; centered conversation column; screenshot strip and composer; adjacent context/review panel on wide screens, stacked on mobile. Keep the ZainCash identity consistent with the employee app while keeping the customer surface simpler. Use semantic labels and text, not a made-up confidence meter.

- [ ] **Step 2: Write failing interaction tests.** Use the real controller with fake HTTP transport or a controller test double implementing the same public interface. Test observable behavior, not CSS snapshots.

```tsx
it("requires explicit submission after summary review", async () => {
  const { controller, api } = readyController("en")
  render(<IntakePage controller={controller} />)
  expect(await screen.findByRole("heading", { name: "Review your report" })).toBeVisible()
  expect(api.submit).not.toHaveBeenCalled()
  await userEvent.click(screen.getByRole("button", { name: "Submit ticket" }))
  expect(await screen.findByText("INTAKE-demo")).toBeVisible()
  expect(api.submit).toHaveBeenCalledTimes(1)
})

it("keeps an unsent draft when a screenshot upload fails", async () => {
  const { controller, api } = collectingController("en")
  api.upload.mockRejectedValueOnce(new Error("Upload failed"))
  render(<IntakePage controller={controller} />)
  const input = await screen.findByRole("textbox", { name: "Your message" })
  await userEvent.type(input, "This error appeared yesterday")
  await userEvent.upload(screen.getByLabelText("Attach screenshots"),
    new File([new Uint8Array([1, 2])], "error.png", { type: "image/png" }))
  expect(await screen.findByRole("alert")).toHaveTextContent("Upload failed")
  expect(input).toHaveValue("This error appeared yesterday")
})
```

Define `readyController` and `collectingController` fixtures locally with schema-valid sessions and deterministic fake transport. Additional tests: double-click submission, switch language while review is displayed, correct a reviewed amount, image-only message, remove uploaded screenshot, unknown facts shown in partial review, IME composition/Shift+Enter, refresh of an in-flight turn, and old-session late replies after start-new.

- [ ] **Step 3: Run the red check from `users-frontend/`.** `npm --workspace web run test -- src/features/intake/IntakePage.test.tsx`.

- [ ] **Step 4: Implement chat and uploads with a stable controller.** Subscribe using `useSyncExternalStore(controller.subscribe, controller.getSnapshot)`. Compose plain React components and the existing shared Button; add only small local inputs/panels actually needed. Use `dir="auto"` on messages and `bdi dir="ltr"` for identifiers; page controls follow the selected locale. Keep text and selected files until the server confirms message acceptance. Upload files sequentially against updated revisions; preserve successful uploads when a later file fails. Disable sending during active upload/turn and support retry/remove. Show real upload progress and local thumbnail fallback. Revoke blob URLs on replacement/unmount.

```tsx
<section aria-label={t.conversation} role="log" aria-live="polite" aria-relevant="additions">
  {session.messages.map((message) => (
    <article key={message.id} dir="auto" lang={message.language}>
      <p>{message.text}</p>
    </article>
  ))}
</section>
```

Render message text as text, never raw HTML. Announce new assistant replies and errors without repeatedly reading the entire transcript. Enter sends only outside IME composition; Shift+Enter adds a newline. Keep focus on the composer after sending and move focus to the review heading only when review opens intentionally.

- [ ] **Step 5: Implement review, corrections and receipt.** Review shows customer-language prose plus canonical fact rows, additional issues, unknowns and selected screenshots. Corrections are ordinary explicit customer messages sent through the existing evidence path; invalidate the displayed review while updating. Continue-conversation returns to the composer without submitting. Submit uses exactly the current review ID/revision, disables duplicate clicks, and shows the durable receipt. A language switch while viewing review requests a fresh review in that language rather than relabelling old text. The employee Arabic summary remains based on the same facts. Start-new is a deliberate action with a small confirmation if the current report has content.

```ts
const ar = {
  review: "راجع تفاصيل المشكلة", submit: "إرسال التذكرة",
  partial: "بعض التفاصيل بعدها مو معروفة", message: "رسالتك",
  reviewNow: "راجع المعلومات الحالية", unknown: "غير معروف",
}
const en = {
  review: "Review your report", submit: "Submit ticket",
  partial: "Some details are still unknown", message: "Your message",
  reviewNow: "Review what I have", unknown: "Unknown",
}
```

Expand these keys for every actual control/error in `IntakeCopy`; both dictionaries must satisfy the same type. Receipt says submitted/processing/needs attention, never claims money was recovered or a problem resolved. Keyboard/mobile layouts must keep the composer visible without hiding the latest question.

- [ ] **Step 6: Verify interaction and rendering.** From `users-frontend/`, run `npm --workspace web run test`, `npm --workspace web run typecheck`, `npm --workspace web run lint`, `npm --workspace web run build`. In the browser check 390px and desktop widths, both locales, dark theme, screenshots, and a keyboard-only review/submission path.

### Task 8: Employee evidence panel and processing state

**Files:** Create `employee-frontend/src/features/review/IntakeEvidence.tsx`, `intake-evidence.test.tsx`, `review-availability.ts`, `review-availability.test.ts`; modify `src/lib/types.ts`, `src/features/review/TicketReviewPage.tsx`, `src/components/shared/workspace-ui.tsx`, `src/features/queue/QueuePage.tsx`, and `src/styles/workspace.css`. Touch `src/features/runs/RunsPage.tsx` only where processing rows need a label or pending-detail refresh.

**Interfaces:**
- `Result.intake?: IntakeEvidenceData | null` mirrors Task 5's projection; `IntakeEvidence({intake: IntakeEvidenceData | null | undefined})` renders nothing for old tickets.
- `canReview(status: string): boolean` returns false for processing/failed and true only for the existing reviewable saved-result states.

- [ ] **Step 1: Write failing presentation and reviewability tests using existing static-render conventions.**

```tsx
it("shows unknowns and original transcript alongside Arabic summary", () => {
  const html = renderToStaticMarkup(<IntakeEvidence intake={intakeFixture} />)
  expect(html).toContain("ملخص المشكلة")
  expect(html).toContain("Unknown")
  expect(html).toContain("The transfer failed yesterday")
  expect(html).toContain("/api/results/1/intake/attachments/")
  expect(html).not.toContain("Bearer")
})
it("has no intake panel for historical tickets", () => {
  expect(renderToStaticMarkup(<IntakeEvidence intake={null} />)).toBe("")
})
it.each(["processing", "failed"])("prevents review while %s", (status) => {
  expect(canReview(status)).toBe(false)
})
```

Build `intakeFixture` with a partial summary, one unknown amount, English source message and a result-linked screenshot. Add rendering tests for long mixed-direction references and escaped `<script>` customer text; no raw HTML rendering is allowed.

- [ ] **Step 2: Run the red check from `employee-frontend/`.** `npm run test -- src/features/review/intake-evidence.test.tsx src/features/review/review-availability.test.ts`.

- [ ] **Step 3: Implement the evidence component.** Display the Iraqi Arabic summary in a labelled RTL section, the context-quality badge, known facts, additional issues and unknowns/contradictions, expandable original transcript, and attachment thumbnails linking to the submitted employee image endpoint. Show source message/image references for facts. Keep original English messages LTR/auto. Unknowns must read as unknown, not an empty field or a zero amount. Load images lazily and show an unavailable-image message when retrieval fails.

```tsx
if (!intake) return null
return (
  <section aria-labelledby="intake-heading">
    <h2 id="intake-heading">Customer intake</h2>
    <div lang="ar" dir="rtl"><h3>ملخص المشكلة</h3><p>{intake.summary_ar}</p></div>
    <details><summary>Original conversation</summary>
      {intake.messages.map((message) => <p key={message.id} dir="auto">{message.text}</p>)}
    </details>
  </section>
)
```

The final component also includes facts/unknowns/images above; split helpers inside this feature if the component becomes large. Do not reuse the employee RAG citation UI for intake screenshots: their source identities and meaning differ.

- [ ] **Step 4: Integrate processing behavior into existing pages.** Add `processing:"Processing"` to status labels, a queue processing count/tab, and a pending-state block in ticket detail. Use `canReview` for all editor actions and suppress misleading “no draft/check unavailable” warnings during processing. Poll processing detail until a saved outcome is available, then render the existing response workspace. Queue rows remain clickable using the user's current implementation; retain their direct links and keyboard access. Preserve existing run-row clickable behavior and append CSS rather than replacing unrelated styles.

- [ ] **Step 5: Verify existing review compatibility.** From `employee-frontend/`, run `npm run test`, `npm run typecheck`, `npm run lint`, `npm run build`. In the browser open an old ticket, a submitted processing ticket, a failed processing ticket, and a completed intake ticket; confirm original employee approval/edit/reassignment flows remain available only for reviewable outcomes.

### Task 9: End-to-end handoff, live vision evidence and runbook

**Files:** Create `backend/tests/intake/test_handoff.py`, `data/demo/intake/README.md`, `docs/verification/2026-10-18-customer-intake.md`; update `README.md`, `users-frontend/README.md`, `docs/demo-readiness.md`, and `.env.example` if execution discovered a configuration correction. Generate synthetic PNG receipts/errors inside test fixtures; keep any live-demo screenshot under `data/demo/intake/` explicitly fictional.

**Interfaces:** Consumes the real API, Task 4 fake-model seam, Task 5 pipeline dispatch, and both UI builds. Produces a reproducible runbook and honest verification record.

- [ ] **Step 1: Add a failing whole-flow regression with real graph and DB.** Use `intake_client` with actual dispatch enabled and the existing fake pipeline. Script a vague complaint, screenshot-supplied error, follow-up about date/amount, a correction, and final partial or sufficient review. Before submission assert no employee result; after submission assert one ticket, preserved transcript/image evidence, same corrected facts in customer review/Arabic summary, and an existing pipeline result.

```python
def test_review_to_employee_handoff(intake_client, complete_conversation):
    # complete_conversation performs the text/image/correction steps through HTTP
    # with the scripted model and returns the live current review.
    from uuid import uuid4
    case = complete_conversation
    assert intake_client.get("/api/results").json()["items"] == []
    view = case["view"]
    response = intake_client.post(f"/api/intake/sessions/{case['sid']}/submit",
        headers=case["headers"], json={"request_id": str(uuid4()),
        "expected_revision": view["revision"], "review_id": view["review"]["id"], "confirmed": True})
    assert response.status_code == 200
    row = intake_client.get("/api/results").json()["items"][0]
    detail = intake_client.get(f"/api/results/{row['id']}").json()
    assert detail["intake"]["facts"]["amount"]["normalized"] == "50000"
    assert detail["intake"]["messages"]
    assert detail["intake"]["attachments"]
    assert detail["ticket"]["external_id"] == response.json()["ticket_reference"]
```

Define `complete_conversation` in this test file: first text reports a failed transfer; attach a Pillow-generated receipt; scripted analysis asks amount; answer `5000`; correction says `I meant 50000 IQD`; provide an explicit date; scripted review covers all remaining known/unknown facts. Build model outputs from current context IDs so their evidence references are real. Add a second case for English general inquiry with no transaction questions and a third for model failure → restart → retry → one submission.

- [ ] **Step 2: Run the focused integration check.** `uv --directory backend run pytest tests/intake/test_handoff.py -q`. Resolve failures at their owning boundaries before broadening tests.

- [ ] **Step 3: Run final automated verification once the feature stabilizes.** From repository root: `uv --directory backend run pytest -q`, then `uv --directory backend run ruff check app tests`. From `users-frontend/`: `npm --workspace web run test`, `npm --workspace web run typecheck`, `npm --workspace web run lint`, `npm --workspace web run build`. From `employee-frontend/`: `npm run test`, `npm run typecheck`, `npm run lint`, `npm run build`. Capture commands, exit codes and counts in the verification record. Do not label baseline failures as feature regressions without checking the baseline; report unresolved failures explicitly.

- [ ] **Step 4: Exercise real browser handoff.** Start the existing Postgres/API using README commands and both Vite servers on strict ports. Use Playwright browser tools to send an English complaint and an Iraqi Arabic complaint, upload a synthetic screenshot, correct an amount, refresh mid-conversation, review and submit. In the employee UI open the ticket reference and inspect summary, facts, transcript, screenshot, and processing/failure state. Check mobile 390px and desktop widths, console errors, keyboard navigation, and language changes. Verify ticket invisibility before submission and one ticket after double-click/retry.

- [ ] **Step 5: Verify the configured live vision model with synthetic data.** Set `INTAKE_MODEL` to an available OpenRouter model that supports both vision and structured output. Keep API keys server-side. Use a readable synthetic image containing reference `DEMO-2410000123`, amount `50000 IQD`, and a clearly fictional error; repeat with one deliberately unreadable value. Record exact model ID, settings, extracted observations, follow-up behavior, latency, and provider cost when available. Confirm the model actually received image blocks, not merely a caption containing the answer. Never present fake-provider or text-only success as a live image-understanding result.

- [ ] **Step 6: Update the documentation and review the final diff.** Explain the two UI URLs, optional `INTAKE_MODEL` override, upload directory persistence, model prerequisites, customer summary/submission flow, partial-context behavior, and operator retry through the existing batch API with unchanged stored ticket fields. Update README's original “not a chatbot” description to distinguish the new customer intake from the employee pipeline. Replace the user project's starter README with its actual workspace commands. Record any unavailable live check as unverified, and save measured outcomes only after running them.

## Spec coverage and acceptance map

| Approved spec section | Owning tasks |
| --- | --- |
| 1 Outcome, customer choices | Global constraints; Tasks 2, 7, 8, 9 |
| 2 Current integration | Tasks 1, 4, 5, 8 |
| 3 Guided graph and boundaries | Tasks 2, 3, 4 |
| 4 Durable state and concurrency | Tasks 1, 4, 6 |
| 5 Facts, evidence, readiness | Task 2; summary guards in Task 4 |
| 6 Language and screenshots | Tasks 2, 3, 7, 8; live check in Task 9 |
| 7 Review, submission, processing | Tasks 4, 5, 7 |
| 8 API and both UIs | Tasks 4–8 |
| 9 Failures, execution limits, usage | Tasks 1, 3, 4, 5, 6 |
| 10 Verification | Each task's red/green checks and Task 9 |
| 11 Delivery and repository handling | Execution conventions and handoff below |

## Plan review and execution handoff

Status: Implemented, audited and repaired on `feat/customer-intake`; see the completion audit and verification record above. Changes from the completion audit are local and uncommitted.

Recommended execution method: **Native**, because the graph, operation ledger, summary revision, and submission transaction share tightly coupled interfaces; maintaining one implementation context reduces handoff overhead. Follow the selected execution skill and its review process. Subagent-driven execution remains available if the user prefers a separate implementer/reviewer gate for every task.

Before implementation, the user reviews this written plan and chooses Native or Subagent-driven. Approval of this plan does not authorize deleting nested Git metadata, staging unrelated changes, or committing/pushing.
