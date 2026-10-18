# Customer intake verification — 2026-10-18

Customer intake is a separate conversation. It reviews a report and then creates one normal ticket for the existing employee pipeline. It does not recover money or mark a problem resolved.

## Automated

| Command | Result |
|---|---|
| `uv --directory backend run pytest -q` | **743 passed** in 97.47s |
| `uv --directory backend run ruff check app tests` | Passed |
| `npm --workspace web run test` from `users-frontend/` | **23 passed** |
| `npm --workspace web run typecheck` | Passed |
| `npm --workspace web run lint` | Passed |
| `npm --workspace web run build` | Passed |
| `npm run test` from `employee-frontend/` | **30 passed** |
| `npm run typecheck` | Passed |
| `npm run lint` | Passed |
| `npm run build` | Passed |

`tests/intake/test_handoff.py` covers a failed-transfer conversation with a generated screenshot, an amount correction from 5000 to 50000, an explicit date, and one employee ticket. An English general inquiry does not ask transaction questions. A model failure retries the same request and still creates one submission.

## Not verified live

`INTAKE_MODEL` was empty, so the adapter used `GEMINI_MODEL` (`google/gemini-3.8-flash`). A direct call with `data/demo/intake/fictional-receipt.png` built one image block locally, then failed three times with `ConnectError` in about 1.3 seconds. No extracted reference, amount, latency of a successful call, or provider cost was observed. That is not a live image-understanding result.

The browser check was partial. The customer app on http://127.0.0.1:5174 rendered in dark theme at desktop width and at 390px, in English and Arabic, with the composer visible and Send disabled until there is a message. The process already bound to port 8000 returned 404 for `POST /api/intake/sessions`, so that server does not include this intake build and no live ticket was submitted. A failed session create shows “The conversation could not be updated. Try again.” The employee queue on http://127.0.0.1:5173 still listed the existing tickets, kept their links, and showed a Processing tab at 0.
