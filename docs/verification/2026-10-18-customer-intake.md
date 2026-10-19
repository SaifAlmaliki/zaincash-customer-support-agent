# Customer intake verification — 2026-10-18

Completion audit of `feat/customer-intake`, starting at `d6de663`. The initial intake suite had 54 passing tests, but several planned boundaries were missing. The audit added **38 backend, 17 customer, and 1 employee regression tests** and repaired the findings below. Changes are local and uncommitted.

## Final automated checks

All commands below exited **0**. Backend tests ran serially against guarded `support_test`; the development `support` database was not reset.

| Working directory | Command | Result |
|---|---|---|
| Repository root | `uv --directory backend run pytest -q --tb=short` | **781 passed**, 116.51s |
| Repository root | `uv --directory backend run ruff check app tests` | Passed |
| `users-frontend/` | `npm --workspace web run test` | **40 passed** |
| `users-frontend/` | `npm --workspace web run typecheck` | Passed |
| `users-frontend/` | `npm --workspace web run lint` | Passed, no warnings |
| `users-frontend/` | `npm --workspace web run build` | Passed, including project-reference TypeScript checks |
| `employee-frontend/` | `npm run test` | **31 passed** |
| `employee-frontend/` | `npm run typecheck` | Passed |
| `employee-frontend/` | `npm run lint` | Passed |
| `employee-frontend/` | `npm run build` | Passed |

PowerShell invoked these through WSL; `uv` was located at `/home/cvzmh_saif/.local/bin/uv` and npm through the WSL login shell. Intermediate failures included the newly written regression cases, two build-only TypeScript errors and one over-broad test selector; all were resolved before these final checks.

## Repaired gaps and regression evidence

- **Evidence:** dates now reach deterministic normalization and use the source's Baghdad date; ambiguous relative dates remain unresolved. Amounts are parsed from the supported value instead of an earlier reference in the quote. Precise values cannot borrow unrelated normalizations or substrings of longer identifiers. Customer and recipient phone roles are checked even when both occur in one message. Explicit corrections retain superseded evidence; ordinary contradictions remain conflicts. Additional issues merge by identity. Removing a screenshot invalidates all unsupported fact statuses.
- **Images/model:** historical images cannot supply new facts until seen; reinspection includes current images and retains first-pass facts. Changed image bytes conflict before decoding a replay. Decoder failures are safe rejections. Calls enforce the remaining deadline, record latency, avoid duplicate usage entries and perform one bounded evidence/schema repair. Prompts now contain the actual category/fact vocabulary and required review keys. Relative upload paths resolve under the repository, matching the ignored persistent directory.
- **Review:** all collected facts, exact errors and missing material fields survive into canonical review/ticket rows. Arabic customer/employee prose is identical. Number punctuation is handled without dropping reference prefixes. Explicit review reinterprets accepted-but-unprocessed messages. Invalid proposals retain their provider usage audit.
- **Durability:** fingerprints use original request content before sanitization; labelled receipt references survive sanitization. Customer messages link to their operation. Failed/superseded operations cannot reopen submitted sessions. Publication failures become retryable. Attempt-tagged costs survive stale-result fencing. Actual application startup reconciles failed placeholders and counts, including unscheduled submissions; failed outcome persistence is covered too.
- **Customer UI:** single-flight initialization/sending, unavailable browser storage (including the theme wrapper), failed initialization retry, lost-response/model retry, stale-tab conflicts, pending uploads/removals and late polls are covered. A new draft cannot silently replay an old body. Multiple selected files survive native FileList clearing; reattachment gets a new operation identity. Text typed during an in-flight request survives. Submitted reports stop accepting edits. Arabic defaults, localized facts/errors, explicit status labels and authorized thumbnails are displayed.
- **Employee UI:** conflicts and inapplicable details are labelled, evidence links lead to source messages/images, and unavailable screenshots show a fallback. Processing and failed outcomes remain non-reviewable.

The real-DB handoff tests also cover concurrent exactly-once submission, corrected amounts, frozen transcript/images, general inquiries and recovery into one submission. New regressions were first observed failing at their intended boundary, then passing. The persistence-failure test also pins an already-correct batch recovery path.

## Browser handoff

Playwright exercised the real HTTP API/graph/Postgres through a disposable `support_test` server on **8001**, with scripted intake and pipeline models. The existing developer server on 8000 was left running. The customer Vite server on **5174** used `API_PROXY_TARGET=http://127.0.0.1:8001`; employee **5173** reads were routed to that test API by Playwright.

- English complaint + `data/demo/intake/fictional-receipt.png`, refresh/resume, amount 5000, partial review, correction to 50000, new review, keyboard submission.
- Before submission, the draft reference was absent from employee results. Afterwards exactly one `pending_review` result existed for `INTAKE-52e4655a9c7e40619103ead71618f475`.
- Employee ticket detail showed Arabic summary, amount **50000**, `DEMO-2410000123`, explicit unknowns, the original correction/transcript and a linked screenshot.
- Iraqi Arabic complaint and partial-review submission produced `INTAKE-c43bfe1c379d4512a533be8e538327e0` at **390×844**, including dark theme and readable RTL controls/receipt. Measured document width was 375 CSS pixels, within the 390-pixel viewport. Desktop English and mobile Arabic surfaces were inspected.
- The successful submission hid the composer. Duplicate submissions, IME/Shift+Enter, concurrent uploads and interrupted requests are also pinned by automated tests.

Initial diagnostic runs hit the stale 8000 server, and an interception-based multipart forwarding attempt lost image bytes; native Vite proxy upload then succeeded. Resetting the disposable database between regression runs caused an expected old-session 404; starting a deliberate new report succeeded. These are recorded separately from successful handoffs. Browser model prose is **scripted evidence**, not live vision or linguistic-quality evidence.

## Live vision and paired review

Reproduce from the repository root (makes paid provider calls with synthetic data):

```bash
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
INTAKE_MODEL=google/gemini-2.5-flash \
uv --directory backend run python -m tests.intake.live_probe
```

The probe generates readable and deliberately unreadable **900×340** fictional receipts. Each analyze request contains one `image_url` data block with the PNG's true MIME. The accompanying message contains no reference, amount or error answers. Observations, source UUIDs, follow-up selection, paired summaries, actual usage and provider-reported costs are printed; keys are never printed.

Final measured run, **60-second / 3-request shared budget** per image plus review:

| Case | Observations and review | Analyze latency | Total latency | Provider-reported cost |
|---|---|---:|---:|---:|
| Readable | `DEMO-2410000123`, `50000`, `IQD`, `DEMO TRANSFER FAILED`; evidence validated; English and Arabic reviews retained the reference/amount/error; partial context | 4.959s | 6.762s | $0.002274 analyze + $0.0007312 review |
| Unreadable amount | Reference/error retained; amount **missing**, no fabricated number; both reviews validated, missing amount explicitly present in canonical unknowns | 3.356s | 4.987s | $0.002040 analyze + $0.000563 review |

Both completed in two provider requests. The policy selected “What actually happened?” as the next unresolved material question; the unreadable amount remained an unresolved field. These are small smoke checks, not quality benchmarks or proof of Iraqi-dialect fluency.

Earlier diagnostics: the inherited `google/gemini-3.8-flash` selection returned unsupported/ungrounded observations, then timed out or failed bounded repair. An `openai/gpt-4.1-mini` probe returned provider bad-request errors. Missing costs on errors/timeouts remain **unknown**, not free. `.env.example` now selects the successfully checked `google/gemini-2.5-flash`; existing local `.env` files must explicitly adopt that override if still falling back to the former model.

## Review decisions and remaining limits

- Worked in the user's existing feature checkout and retained the implementation, rather than recreating original task files. The detailed original red-check recipe is historical; this record and the plan's audit checklist are delivery evidence.
- Added internal `TurnContext.needs_analysis`, derived from durable message-operation state, so review after model failure cannot omit accepted content. It does not alter the public HTTP contract; the trade-off is a bounded analysis call for an unprocessed message.
- One independent read-only whole-feature review was performed; Important findings were repaired with regression tests. Verification declined by the reviewer (provider, database concurrency, UI) was handled through the checks above where applicable. Full live-provider browser-to-employee conversation quality remains unmeasured; the browser handoff and live model smoke are separate checks.
- **Deferred minor:** explicit success-response declarations in the generated intake OpenAPI schema. Runtime responses still use the existing DTO projections.
