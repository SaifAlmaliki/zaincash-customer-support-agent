# Customer intake

This workspace is the customer conversation for a ZainCash support report. It is separate from the employee review app. A customer describes the problem, can attach screenshots, reviews the summary, and then submits one ticket. Submission does not recover money or close the problem.

From this directory:

```bash
npm ci
npm --workspace web run dev
```

The app is http://localhost:5174 and proxies `/api` to http://127.0.0.1:8000. The employee app uses port 5173.

```bash
npm --workspace web run test
npm --workspace web run typecheck
npm --workspace web run lint
npm --workspace web run build
```
