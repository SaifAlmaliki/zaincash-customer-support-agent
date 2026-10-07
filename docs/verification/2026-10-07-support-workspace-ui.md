# Support workspace verification — 2026-10-07

## Scope

Implemented the approved UI/live API plan in `customer-support-ui/` and `backend/app/api/` / `backend/app/services/`. The current backend provider migration uses OpenRouter for Gemini; UI setup instructions match that configuration.

## Automated checks observed

| Check | Result |
|---|---|
| `npm run build` | Passed; route-split production build, no oversized-chunk warning |
| `npm run lint` | Passed |
| `npm test` | 6 passed |
| `uv run pytest -q` in backend | 134 passed, including PostgreSQL integration tests |
| `uv run ruff check app tests` | Passed |

## Browser checks observed

- Preview queue: status filter, text search, 8-row pagination, blank approval disabled, edited response approved locally.
- Preview review actions produced zero live POST requests.
- Real one-ticket Jev run through the browser: batch 5 completed with 1/1 processed.
- Its synthetic UI-verification ticket was manually reviewed through the UI; the saved reply survived a page reload, and the original generated draft remained null.
- Live Markdown upload stored a document with `awaiting_indexing`; download/deletion paths verified. The temporary test document was deleted.
- Evaluation initially displayed no metrics. A labelled, two-sample UI-test report imported successfully; this was not a model evaluation and was not persisted.
- Stage dialog dismissed with Escape; source paths displayed correctly.
- At 390 px width, queue, run history, new batch, knowledge, insights, evaluation and ticket review stayed within the page width.
- Final live queue loaded and `/api/docs` returned 200; no browser console errors during that check.

## Independent review and fixes

All five important findings from the independent code review were addressed:

1. **Concurrent conflicting ticket IDs:** added a failing interleaved-insert regression test. The API now re-reads durable rows after upsert, rejects conflicting content, and executes the graph against persisted ticket text/timestamps.
2. **Preview document uploads:** reproduced the enabled hidden file input. Both the input and mutation handler now enforce live mode; browser verification confirmed preview uploads are disabled.
3. **Lost unsaved reply after reassignment:** reproduced in the browser. The editor remains mounted across version updates, preserving unsaved text while adopting the current concurrency token. Verified after the fix.
4. **Failed-save summary counts:** a failing persistence-injection test reproduced counts exceeding saved rows. Summaries now include only committed outcomes, and progress checkpoints include cost and degraded status.
5. **Queues larger than 500:** added tests for a 501-ticket queue and inconsistent pagination. The client fetches all result pages before filtering or exporting, rather than silently limiting the queue to its first page.

## Implementation decisions

- Reused the existing shadcn **base-nova / Base UI** components rather than introducing another component library.
- Expanded the existing `runs.status` column from 16 to 32 characters with a non-destructive startup upgrade, because `completed_with_errors` does not fit the original column.
- Kept live operation and illustrative preview state separate. No preview-only data is represented as measured model output.
- Used the existing compiled graph and outcome/summary/repository functions for processing. New stage events describe actual graph updates; planned tool names remain reference material, not fabricated tool calls.

## Capability boundaries

The current `NullDrafter` does not generate replies. Document storage does not yet embed/index files into pgvector. The evaluation screen views imported reports; it does not run a held-out evaluator. Those limitations are visible in the UI and documented in `customer-support-ui/README.md`.
