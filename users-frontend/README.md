# Customer intake

This workspace is the customer conversation for a ZainCash support report. It is separate from the employee review app. A customer describes the problem, can attach screenshots, reviews the summary, and then submits one ticket. Submission does not recover money or close the problem.

From this directory:

```bash
npm ci
npm --workspace web run dev
```

The app is http://localhost:5174 and proxies `/api` to http://127.0.0.1:8000. The employee app uses port 5173.

Both ports are strict. For an isolated API during verification, use `API_PROXY_TARGET=http://127.0.0.1:8001 npm --workspace web run dev`. This changes the development proxy only; customer requests still use relative `/api` URLs. Configure the backend's tested vision model with `INTAKE_MODEL=google/gemini-2.5-flash` and restart the API.

```bash
npm --workspace web run test
npm --workspace web run typecheck
npm --workspace web run lint
npm --workspace web run build
```
