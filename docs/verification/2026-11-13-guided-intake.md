# Guided intake interview verification — 2026-11-13

Verification of the guided intake interview on `main` (Tasks 1–10: 47288d9, c4c0fcd, 0956fe4, 0306ae1, e3f85d7, cf827ee, d6f83e6, 3c3df40, 2d77ffd, cacf927, 14f8aaf; Task 11 adds the employee label and this record).

What was built: a per-category required and ask-once field plan with one re-ask and `recipient_name` (`backend/app/intake/policy.py`); prompt rules for implied facts (`intake_v1.md` / `review_v1.md`); `SessionView.pending_question` and progress; quick-reply answers via `answer_to` without a model call; `POST /ask`; backend scenario tests (`tests/intake/test_interview_scenarios.py`); a `transfers` mode in `tests/intake/live_probe.py`; customer UI with an instant bubble and typing indicator, reasons, quick-reply chips, composer hints, a progress strip and a grouped review card. The employee app only gains the `recipient_name` label in both locale files.

## Final automated checks

Each command was run through WSL from PowerShell with its exit code captured explicitly. The exit codes came from a temporary script (`/tmp/gi-gates.sh`, outside the repository); the script and its logs were **not preserved**. Per gate the pattern was:

```bash
<command> > /tmp/gi-<name>.log 2>&1; echo "<NAME>_EXIT=$?"; tail -1 /tmp/gi-<name>.log
```

for example `~/.local/bin/uv --directory backend run pytest -q --tb=short > /tmp/gi-pytest.log 2>&1; echo "PYTEST_EXIT=$?"`. Putting this in a script file stops PowerShell from rewriting `$?` before WSL sees it. An earlier pass that piped output through `tail` was not reliable for exit codes; the table below is from the re-run with explicit codes. Summary lines come from the run's output. The intake test fixtures assert the database is `support_test` (`backend/tests/intake/conftest.py`), so those tests do not run against the development `support` database.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| Repository root | `uv --directory backend run pytest -q --tb=short` | 0 | `979 passed in 111.04s (0:01:51)` |
| Repository root | `uv --directory backend run ruff check app tests` | 0 | `All checks passed!` |
| `users-frontend/` | `npm --workspace web run test` | 0 | `Test Files 8 passed (8)`, `Tests 141 passed (141)` |
| `users-frontend/` | `npm --workspace web run typecheck` | 0 | no errors |
| `users-frontend/` | `npm --workspace web run lint` | 0 | no errors |
| `users-frontend/` | `npm --workspace web run build` | 0 | built |
| `employee-frontend/` | `npm run test` | 0 | `Test Files 24 passed (24)`, `Tests 124 passed (124)` |
| `employee-frontend/` | `npm run typecheck` | 0 | no errors |
| `employee-frontend/` | `npm run lint` | 0 | no errors |
| `employee-frontend/` | `npm run build` | 0 | built |

`git stash list` was empty (0 entries); nothing was stashed or reverted. The first pass (before the re-run) showed the same counts: 979, 141 and 124 passed.

## Live transfer probe

Command (paid provider calls; the names, phone number and reference in the probe messages are synthetic test fixtures; keys are never printed):

```bash
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
uv --directory backend run python -m tests.intake.live_probe transfers
```

One run was needed; the prompt was **not** changed. Model, as printed by the probe: `anthropic/claude-sonnet-5.5`; one provider request per case (one trace entry each).

| Case | Outcome | Latency | Cost (provider-reported) |
|---|---|---:|---:|
| Vague ("حولت فلوس وما وصلت") | `category` = `failed_transfer`; `recipient_outcome` known with normalized `no`; `quality` = `collecting`; `next_question.key` = `debited` (not `expected` or `recipient_outcome`) | 2.989s | $0.010836 |
| Complete (50000 IQD to Ali Hussain, phone, date, reference, debited, not received) | `quality` = `sufficient_context`; `next_question` = `null`; facts include `recipient_name` = علي حسين, `recipient_phone` = 07701234567, `txn_ref` = ZC2410000123, `debited` = `yes`, `recipient_outcome` = `no`, plus amount 50000 IQD and date 2026-10-06 | 6.054s | $0.019416 |

### Live probe output (facts only)

Copied from the probe's printed JSON for the single run above, with `trace` (usage, cost, latency details) and all other fields omitted. The `facts` objects list `status`, `value` and `normalized` per key exactly as printed.

**vague**

```json
{"category": "failed_transfer", "quality": "collecting",
 "next_question": {"key": "debited", "text": "المبلغ انقطع من رصيدك بمحفظة زين كاش؟", "reason": "حتى نعرف إذا الفلوس طلعت من محفظتك."},
 "facts": {
  "issue": {"status": "known", "value": "حولت فلوس وما وصلت", "normalized": null},
  "recipient_outcome": {"status": "known", "value": "ما وصلت", "normalized": "no"}}}
```

**complete**

```json
{"category": "failed_transfer", "quality": "sufficient_context", "next_question": null,
 "facts": {
  "issue": {"status": "known", "value": "حولت 50000 دينار لعلي حسين وانقطعت من رصيدي بس ما وصلتله", "normalized": null},
  "actual": {"status": "known", "value": "انقطعت من رصيدي بس ما وصلتله", "normalized": null},
  "expected": {"status": "known", "value": "توصل الفلوس للمستلم", "normalized": null},
  "amount": {"status": "known", "value": "50000", "normalized": "50000"},
  "currency": {"status": "known", "value": "دينار", "normalized": "IQD"},
  "recipient_name": {"status": "known", "value": "علي حسين", "normalized": null},
  "recipient_phone": {"status": "known", "value": "07701234567", "normalized": "07701234567"},
  "date": {"status": "known", "value": "2026-10-06", "normalized": "2026-10-06"},
  "debited": {"status": "known", "value": "انقطعت من رصيدي", "normalized": "yes"},
  "recipient_outcome": {"status": "known", "value": "ما وصلتله", "normalized": "no"},
  "txn_ref": {"status": "known", "value": "ZC2410000123", "normalized": "ZC2410000123"}}}
```

Both expectations held. This is a small smoke check on two messages, not a quality benchmark or proof of Iraqi-dialect fluency.

## Existing-test expectation changes from Task 1

Stated from the diff of commit 47288d9 (`git show 47288d9 -- backend/tests/intake/test_policy.py test_review.py test_handoff.py`). The stated reason for all of them is that the new field plan makes `recipient_phone` required for `failed_transfer` and adds ask-once details (`recipient_name`, `txn_ref`); this reason is from the task plan and the commit's intent ("plan required and ask-once details per problem type"), not separately re-derived.

- `tests/intake/test_policy.py::test_unknown_material_fact_is_not_sufficient`: the fixture now supplies a known `recipient_phone` and adds unknown `recipient_name` and `txn_ref` facts alongside the unknown `amount`.
- `tests/intake/test_policy.py::test_complete_transfer_is_sufficient`: the fact set was rewritten to `issue`, `date`, `amount`, `debited`, `recipient_outcome`, `recipient_phone`, `recipient_name` and `txn_ref`; the earlier `actual` and `expected` facts are no longer in the fixture.
- `tests/intake/test_review.py` (line 52): the `fact_keys` list gains `recipient_phone`. The same commit also adds `test_review_lists_ask_once_details_for_the_employee`, which expects `recipient_name` to appear as missing in the employee ticket text.
- `tests/intake/test_handoff.py`: `_MATERIAL` gains `recipient_phone`, and the opening facts add unknown `recipient_phone`, `recipient_name` and `txn_ref`.

## Remaining limits

- **Live-model browser run.** The run happened after the whole-branch review and its fix wave (`3a92530`, `45c4cc7`; backend 984 passed, customer app 157 passed). See "Live browser run" below.
- Out of scope per the spec:
  - The UI does not switch its language on its own from the model-detected language.
  - Duplicate review invitations after a language switch are not handled.
  - Specific error messages are not provided (errors stay generic).
  - There is no readable ticket reference.
  - The customer does not poll for receipt status.
- Rulings recorded during implementation: while an unsent message is pending, the composer and chips are blocked until "Try again" (Task 8); the welcome bubble stays until the first reply, and outgoing and typing bubbles append after it (Task 8). After the final review, a saved unsent message or ask is replayed automatically, with the same request ID, after a reload or when polling ends.
- Known minor issues, deliberately left after the final review:
  - **Restored text can be dropped in one rare case.** A 409 on an automatic replay restores the customer's text to the composer, but only once per page view; a second restore in the same view is ignored. This needs a poll-triggered replay that fails with a 409 after an earlier restore. Normal sends restore the text themselves.
  - **A brief misleading label after a reload.** "Not sent · Try again" can show for one network round trip while the automatic replay reloads.

## Live browser run

The run took place on 2026-11-13 after the final fix wave, against the code at `45c4cc7`.

**Setup.** The user's Docker API on 8000 runs a pre-feature build without auto-reload, and it was left untouched. A separate API ran from the repository on `127.0.0.1:8001`, against the same development database, with the configured live intake model. A second customer Vite server ran on `5175` with `API_PROXY_TARGET=http://127.0.0.1:8001`. All names, numbers and the reference are synthetic.

### Arabic at 390×844, starting from the vague message

The customer started with the vague message `حولت فلوس وما وصلت` ("I sent money and it didn't arrive").

| Turn | Customer | Agent |
|---|---|---|
| 1 | `حولت فلوس وما وصلت` | `المبلغ انقطع من رصيدك بعد ما حولت؟` (was the amount taken from your balance?), with the reason "ليش نسأل: حتى نعرف إذا الفلوس طلعت من محفظتك." and the chips اي / لا / ما أعرف. The progress strip showed "التفاصيل: 2 من 6" (details: 2 of 6): the model had already recorded that the money did not arrive. It did not ask "what did you expect?". |
| 2 | Tapped **اي** (yes) | `شكد المبلغ؟` (how much?) in about 2 s, with no model call. The composer hint changed to "مثلاً 50000". |
| 3 | Typed `50000 دينار`, then **reloaded the page immediately** | After the reload the message appeared once and processing continued. The next question was `شنو رقم المستلم اللي حولتله؟` (the recipient's number) with the hint `07XXXXXXXXX`. There was no stuck composer and no "Not sent". |
| 4 | `07701234567` | `متى صار التحويل تقريباً؟` (when did it happen?) |
| 5 | `2026-10-06` | Asked for the reference, offering the receipt screenshot as an alternative. |
| 6 | `ZC2410000123` | `شنو اسم الشخص اللي حولتله؟` (the recipient's name) |
| 7 | `علي حسين` | Review: **التفاصيل كاملة** (details complete). |

- **Typed turns** took about 4–7 s each.
- **Review card**: one "اللي عرفناه" (what we know) group with:
  - amount 50000
  - date 2026-10-06
  - debited اي (yes)
  - received لا (no)
  - recipient number 07701234567
  - recipient name علي حسين
  - reference ZC2410000123
  - currency IQD

  Submit and Continue sit inside the card.
- **Submit** produced receipt `INTAKE-f874f4f2eb2a4211b09b3dbeff74635f`.
- **Employee API** (same database): the result is `pending_review`, with the following facts:
  - amount 50000
  - date 2026-10-06
  - debited yes
  - recipient_outcome no
  - recipient_phone 07701234567
  - recipient_name علي حسين
  - txn_ref ZC2410000123

  The ticket text includes the recipient name, and the pipeline matched transaction `ZC2410000123`.
- **Screenshot**: `.playwright-mcp/guided-intake-review-390.png`.

### English at 1280×900, with the complete message

The customer sent: "I sent 50000 IQD to Ali Hussein on 07701234567 on 2026-10-06. It was deducted from my balance but he did not receive it. Reference ZC2410000123".

- It went **straight to "Details complete" with zero questions**, in 9.4 s.
- The facts matched the Arabic run, with `Funds deducted: Yes`, `Recipient outcome: No` and `Recipient name: Ali Hussein`.
- This report was left unsubmitted.
- **Screenshot**: `.playwright-mcp/guided-intake-complete-desktop.png`.

### Observations

- The model sometimes asks in a different order from the template plan, for example debited before amount. That is allowed: a model suggestion within the current round is accepted.
- On a 390px screen the header (new report, phone, language) wraps onto three rows. This predates the feature and is out of scope.
