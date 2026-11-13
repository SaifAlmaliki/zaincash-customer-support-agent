# Customer phone identity design

Date: 2026-11-13
Status: Approved design, pending implementation plan

## Intent

Every ZainCash customer is identified by their phone number. The phone number is the customer id in the backend, the customer's profile in users-frontend, and the customer identifier employees see and search by in employee-frontend.

Today there is no customer entity. Intake sessions are anonymous, and `tickets.customer_phone` is an optional, unnormalized, free-text value that the chat assistant may or may not collect.

## Decisions

| Topic | Decision |
|---|---|
| How the customer establishes identity | Phone entry gate before chatting. No OTP or verification. |
| Backend model | New `customers` table with the normalized phone as the primary key. |
| Linking | The gate sends the phone when the intake session is created. The session is owned by that customer. |
| Tickets without a phone | Not allowed. A phone is required on every ticket from every source. |
| Existing data | Demo reset. Seed data and fixtures are updated; no in-place migration. |
| Employee app | Phone in queue rows, phone in ticket header, search by phone, new customer profile page. |

## Canonical phone format

- Canonical form: `07[3-9]XXXXXXXX` (11 ASCII digits, Iraqi local format), regex `^07[3-9]\d{8}$`.
- New module `backend/app/customers/phone.py`:
  - `normalize_customer_phone(raw: str) -> str` reuses `normalize_phone()` from `app/pipeline/stage1_normalize/candidates.py` (Arabic/Persian digits to ASCII, strip non-digits, leading `964` to `0`), then requires the canonical regex.
  - Raises `InvalidPhone` when the result is not canonical.
- API layers map `InvalidPhone` to HTTP 422 with `{"code": "invalid_phone", "message": ...}`.
- Accepted inputs include `07701234567`, `+964 770 123 4567`, `9647701234567`, `964-770-123-4567`, and the same with Arabic-Indic digits.
- Text phone extraction (`_PHONE_RE`) and the SQL normalizer `_stored_phone()` in drafting tools stay as they are. They handle phones found in free text.

## Backend

### Data model

- New table `customers`:
  - `phone VARCHAR(11)` primary key.
  - `created_at TIMESTAMPTZ` server default `now()`.
- `tickets.customer_phone`: `VARCHAR(11) NOT NULL`, foreign key to `customers.phone`, indexed.
- `intake_sessions.customer_phone`: new column, `VARCHAR(11) NOT NULL`, foreign key to `customers.phone`, indexed.
- `transactions.sender_phone` and `receiver_phone` are unchanged and have no foreign key. Transactions come from ZainCash systems and can involve people who are not support customers.
- A repository helper `ensure_customer(session, phone) -> str` normalizes the phone, inserts the customer row if missing (`INSERT ... ON CONFLICT DO NOTHING`), and returns the canonical phone. Every write path that stores a phone calls it.

### Existing data

- The schema is created with `create_all` plus `upgrade_workspace_schema`, which cannot tighten existing columns. No in-place migration is written.
- `upgrade_workspace_schema` checks whether `tickets.customer_phone` is nullable or `intake_sessions.customer_phone` is missing. If so, startup fails with a clear message telling the operator to reset the demo database (`docker compose down -v`, then reseed).
- Every ticket in these files gets a valid canonical phone:
  - `docker/db/seed_demo.sql`
  - `backend/tests/fixtures/sample_tickets.jsonl`
  - `data/demo/rag_tickets.jsonl`
- The seed inserts matching `customers` rows first.
- The README documents the reset.

### Ticket write paths

- `TicketInput.customer_phone` in `backend/app/api/schemas.py` becomes a required `str`, validated and normalized. `POST /api/runs` returns 422 for a missing or invalid phone.
- `backend/app/ingest.py` and `upsert_tickets` store the canonical phone via `ensure_customer`. Rows without a valid phone are rejected with the row identified.
- The rerun 409 for a changed phone (`backend/app/api/runs.py`) compares canonical values.
- The exact-match transaction lookup in `backend/app/db/repository.py` keeps working because stored values are canonical.

### Intake

- `POST /api/intake/sessions` body: `{ language, customer_phone }`.
  - Invalid phone: 422 `invalid_phone`.
  - Valid phone: `ensure_customer`, then the session is created with `customer_phone` set.
- `SessionView` includes `customer_phone` on every intake response.
- The chat assistant no longer collects the customer phone:
  - Remove `customer_phone` from the follow-up questions in `backend/app/intake/policy.py` (both languages) and from `PRECISE`.
  - Remove `customer_phone` from the allowed fact keys in `backend/app/intake/prompts/intake_v1.md`. Keep the rule that a recipient number goes to `recipient_phone`.
  - `backend/app/intake/evidence.py` drops any `customer_phone` fact update coming from the model.
- The review snapshot always contains `customer_phone` as a known fact with the session's phone, so the customer confirms "Your account number" before submitting.
- `backend/app/intake/submission.py` sets `Ticket.customer_phone = row.customer_phone` instead of reading the fact.

### Employee API

- `GET /api/results?q=`: when `q` normalizes to a canonical phone, the search also matches `tickets.customer_phone == normalized(q)`. Text and external id substring search is unchanged.
- New router `GET /api/customers/{phone}`:
  - Normalizes the path value first, so any accepted format works.
  - 422 for an invalid phone, 404 for an unknown customer.
  - Response: `{ phone, created_at, ticket_count, results }`. `results` holds the latest result per ticket of that customer, newest first, each in the same shape as `/api/results` items (`result_view`).
- `result_view` already returns `customer_phone` in the ticket payload.

## users-frontend

- New `PhoneGate` screen, shown when no session is stored:
  - A single field, "Your ZainCash phone number" / Arabic equivalent, `dir="ltr"` input within the existing RTL layout.
  - The client checks the canonical regex after the same normalization for instant feedback. The server is authoritative; a 422 is shown inline.
  - On success it creates the session with `customer_phone` and opens the chat.
- `IntakePage` header shows a profile chip with the session's `customer_phone` (from `SessionView`) and a "Change number" action.
- Change number:
  - Asks for confirmation when a conversation is in progress.
  - Clears `zaincash.intake.session` from localStorage and returns to the gate.
  - Server data is not deleted.
- On reload, the stored credentials restore the session and the phone comes from `GET /sessions/{id}`. The phone is not stored separately in localStorage.
- The receipt panel shows the phone the ticket was submitted for.
- New strings in `locales/en.json` and `locales/ar.json`.

## employee-frontend

- `employee-frontend/src/lib/types.ts`:
  - `TicketInput.customer_phone: string` and `Ticket.customer_phone: string` are required.
  - The unused `display_name` is removed.
- Queue rows (`features/queue/QueuePage.tsx`) show the customer phone as the primary label (`dir="ltr"`). The external id and date move to the secondary line.
- Queue search (`features/queue/queue-projection.ts`) also matches the phone using the same client-side normalization.
- Ticket review header (`features/review/TicketReviewPage.tsx`) shows the customer phone as the customer identifier, linked to `/customers/:phone`. It replaces the `display_name` and "Customer support ticket" fallback.
- New route `/customers/:phone` with `CustomerPage`:
  - Shows the phone, "customer since" date, and ticket count.
  - Lists the customer's tickets using the queue row styling, each linking to `/tickets/:id`.
  - Handles 404 and 422 with clear empty and error states.
- `features/runs/NewBatchPage.tsx`:
  - The phone field is required ("Customer phone", placeholder `07…`) with client-side validation.
  - Server 422 errors are shown against the right row.
- `lib/imports.ts` flags rows without a valid phone and blocks the import, showing the row numbers.
- New strings in the employee locale files (en and ar).

## Error handling

| Case | Behaviour |
|---|---|
| Invalid phone at gate | 422 `invalid_phone`, inline error, stay on the gate. |
| Invalid or missing phone in `POST /api/runs` | 422 with the offending ticket index. |
| Invalid phone in `/api/customers/{phone}` | 422; the page shows "Not a valid phone number". |
| Unknown customer | 404; the page shows "No customer with this number". |
| Old database schema at startup | Startup fails with a reset instruction. |

## Testing

TDD for every change.

- Backend:
  - Phone normalization: accepted formats, Arabic digits, rejections.
  - `ensure_customer` is idempotent.
  - Session creation with valid and invalid phone.
  - Submission uses the session phone.
  - Model-extracted `customer_phone` is ignored.
  - `/api/runs` requires a valid phone.
  - `/api/results?q=` matches any phone format.
  - `/api/customers/{phone}`: found, 404, 422.
  - Startup check on an old schema.
  - Existing tests and fixtures updated to canonical phones.
- users-frontend (Vitest):
  - Gate validation, server 422 display, and the gate-to-chat transition.
  - Header phone chip.
  - Change number confirmation and reset.
- employee-frontend (Vitest):
  - Queue shows the phone and searches by it.
  - Header link to the customer page.
  - `CustomerPage` lists tickets and handles 404 and 422.
  - Batch entry and file import require a phone.

## Out of scope

- OTP or any real customer authentication.
- Employee authentication.
- Editing, merging, or deleting customers.
- A "my past tickets" view in users-frontend.
- Foreign keys from transactions to customers.
