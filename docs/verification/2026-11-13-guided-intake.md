# Guided intake interview verification — 2026-11-13

Verification of the guided intake interview on `main` (Tasks 1–10: 47288d9, c4c0fcd, 0956fe4, 0306ae1, e3f85d7, cf827ee, d6f83e6, 3c3df40, 2d77ffd, cacf927, 14f8aaf; Task 11 adds the employee label and this record).

What was built: a per-category required and ask-once field plan with one re-ask and `recipient_name` (`backend/app/intake/policy.py`); prompt rules for implied facts (`intake_v1.md` / `review_v1.md`); `SessionView.pending_question` and progress; quick-reply answers via `answer_to` without a model call; `POST /ask`; backend scenario tests (`tests/intake/test_interview_scenarios.py`); a `transfers` mode in `tests/intake/live_probe.py`; customer UI with an instant bubble and typing indicator, reasons, quick-reply chips, composer hints, a progress strip and a grouped review card. The employee app only gains the `recipient_name` label in both locale files.

## Final automated checks

Each command was run through WSL from PowerShell with its exit code captured explicitly (`cmd > log 2>&1; echo EXIT=$?` in a script file, so PowerShell could not rewrite `$?`). An earlier pass that piped output through `tail` was not reliable for exit codes; the table below is from the re-run with explicit codes. Exit codes are in the table; summary lines come from the saved logs. The intake test fixtures assert the database is `support_test` (`backend/tests/intake/conftest.py`), so those tests do not run against the development `support` database.

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

Both expectations held. This is a small smoke check on two messages, not a quality benchmark or proof of Iraqi-dialect fluency.

## Existing-test expectation changes from Task 1

Stated from the diff of commit 47288d9 (`git show 47288d9 -- backend/tests/intake/test_policy.py test_review.py test_handoff.py`). The stated reason for all of them is that the new field plan makes `recipient_phone` required for `failed_transfer` and adds ask-once details (`recipient_name`, `txn_ref`); this reason is from the task plan and the commit's intent ("plan required and ask-once details per problem type"), not separately re-derived.

- `tests/intake/test_policy.py::test_unknown_material_fact_is_not_sufficient`: the fixture now supplies a known `recipient_phone` and adds unknown `recipient_name` and `txn_ref` facts alongside the unknown `amount`.
- `tests/intake/test_policy.py::test_complete_transfer_is_sufficient`: the fact set was rewritten to `issue`, `date`, `amount`, `debited`, `recipient_outcome`, `recipient_phone`, `recipient_name` and `txn_ref`; the earlier `actual` and `expected` facts are no longer in the fixture.
- `tests/intake/test_review.py` (line 52): the `fact_keys` list gains `recipient_phone`. The same commit also adds `test_review_lists_ask_once_details_for_the_employee`, which expects `recipient_name` to appear as missing in the employee ticket text.
- `tests/intake/test_handoff.py`: `_MATERIAL` gains `recipient_phone`, and the opening facts add unknown `recipient_phone`, `recipient_name` and `txn_ref`.

## Remaining limits

- **No live-model browser run yet.** The live-model run on `http://localhost:5174` (Arabic at 390px from the vague message through quick replies and typed answers to submit; English on desktop with the complete message; ticket check in the employee app) is done by the controller after the whole-branch review, and its results are appended here. Until then, UI behavior is covered by automated tests and the backend by the scripted scenarios plus the live probe above.
- Out of scope per the spec:
  - The UI does not switch its language on its own from the model-detected language.
  - Duplicate review invitations after a language switch are not handled.
  - Specific error messages are not provided (errors stay generic).
  - There is no readable ticket reference.
  - The customer does not poll for receipt status.
- Rulings recorded during implementation: while an unsent message is pending, the composer and chips are blocked until "Try again" (Task 8); the welcome bubble stays until the first reply, and outgoing and typing bubbles append after it (Task 8).
