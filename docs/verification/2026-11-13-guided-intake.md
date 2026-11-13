# Guided intake interview verification — 2026-11-13

Verification of the guided intake interview on `main` (Tasks 1–10: 47288d9, c4c0fcd, 0956fe4, 0306ae1, e3f85d7, cf827ee, d6f83e6, 3c3df40, 2d77ffd, cacf927, 14f8aaf; Task 11 adds the employee label and this record).

What was built: a per-category required and ask-once field plan with one re-ask and `recipient_name` (`backend/app/intake/policy.py`); prompt rules for implied facts (`intake_v1.md` / `review_v1.md`); `SessionView.pending_question` and progress; quick-reply answers via `answer_to` without a model call; `POST /ask`; backend scenario tests (`tests/intake/test_interview_scenarios.py`); a `transfers` mode in `tests/intake/live_probe.py`; customer UI with an instant bubble and typing indicator, reasons, quick-reply chips, composer hints, a progress strip and a grouped review card. The employee app only gains the `recipient_name` label in both locale files.

## Final automated checks

All commands completed successfully. Backend tests ran serially against the guarded `support_test` database; the development `support` database was not reset.

| Working directory | Command | Result |
|---|---|---|
| Repository root | `uv --directory backend run pytest -q --tb=short` | **979 passed**, 111.85s |
| Repository root | `uv --directory backend run ruff check app tests` | `All checks passed!` |
| `users-frontend/` | `npm --workspace web run test` | **141 passed** (8 files) |
| `users-frontend/` | `npm --workspace web run typecheck` | Passed |
| `users-frontend/` | `npm --workspace web run lint` | Passed |
| `users-frontend/` | `npm --workspace web run build` | Passed |
| `employee-frontend/` | `npm run test` | **124 passed** |
| `employee-frontend/` | `npm run typecheck` | Passed |
| `employee-frontend/` | `npm run lint` | Passed |
| `employee-frontend/` | `npm run build` | Passed |

PowerShell invoked these through WSL (`uv` at `/home/cvzmh_saif/.local/bin/uv`). `git stash list` was empty; nothing was stashed or reverted.

## Live transfer probe

Command (paid provider calls, synthetic data; keys are never printed):

```bash
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
uv --directory backend run python -m tests.intake.live_probe transfers
```

One run was needed; the prompt was **not** changed. Model: `anthropic/claude-sonnet-5.5` (the configured model), one provider request per case.

| Case | Outcome | Latency | Cost (provider-reported) |
|---|---|---:|---:|
| Vague ("حولت فلوس وما وصلت") | `category` = `failed_transfer`; `recipient_outcome` known with normalized `no`; `quality` = `collecting`; `next_question.key` = `debited` (not `expected` or `recipient_outcome`) | 2.989s | $0.010836 |
| Complete (50000 IQD to Ali Hussain, phone, date, reference, debited, not received) | `quality` = `sufficient_context`; `next_question` = `null`; facts include `recipient_name` = علي حسين, `recipient_phone` = 07701234567, `txn_ref` = ZC2410000123, `debited` = `yes`, `recipient_outcome` = `no`, plus amount 50000 IQD and date 2026-10-06 | 6.054s | $0.019416 |

Both expectations held. This is a small smoke check on two messages, not a quality benchmark or proof of Iraqi-dialect fluency.

## Existing-test expectation changes from Task 1

The new field plan makes `recipient_phone` required for `failed_transfer` and adds ask-once details (`recipient_name`, `txn_ref`, and others). Tests that treated those fields as absent or unnecessary were updated rather than weakened:

- `tests/intake/test_policy.py::test_unknown_material_fact_is_not_sufficient` and `::test_complete_transfer_is_sufficient`: a "complete" transfer now has to include `recipient_phone`, and the unknown-fact example reflects the new required set.
- `tests/intake/test_review.py` line 52: the expected `fact_keys` now include `recipient_phone`, since the review lists every collected or required key for a transfer.
- `tests/intake/test_handoff.py`: the `_MATERIAL` fixture gains `recipient_phone`, and the opening transcript now records `recipient_phone`, `recipient_name` and `txn_ref` as unknown, because the plan asks for them.

## Remaining limits

- **No live-model browser run yet.** The live-model run on `http://localhost:5174` (Arabic at 390px from the vague message through quick replies and typed answers to submit; English on desktop with the complete message; ticket check in the employee app) is done by the controller after the whole-branch review, and its results are appended here. Until then, UI behavior is covered by automated tests and the backend by the scripted scenarios plus the live probe above.
- Out of scope per the spec:
  - The UI does not switch its language on its own from the model-detected language.
  - Duplicate review invitations after a language switch are not handled.
  - Specific error messages are not provided (errors stay generic).
  - There is no readable ticket reference.
  - The customer does not poll for receipt status.
- Rulings recorded during implementation: while an unsent message is pending, the composer and chips are blocked until "Try again" (Task 8); the welcome bubble stays until the first reply, and outgoing and typing bubbles append after it (Task 8).
