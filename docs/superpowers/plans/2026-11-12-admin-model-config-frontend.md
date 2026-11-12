# Admin model configuration — employee frontend implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** An **Admin → Models** page in the employee workspace where an admin, after entering the admin token, can see and change the model behind every pipeline step (with a live test before saving and a guarded embedding switch), plus a read-only **AI: Local / Cloud / Mixed** chip for every employee.

**Architecture:** A token kept in `sessionStorage` is sent as `X-Admin-Token` by a small `adminRequest` wrapper around the existing `request`. Pure helpers (`model-choice.ts`, `admin-errors.ts`, `run-models.ts`, `run-start-error.ts`) hold all decision logic so it can be unit tested with Vitest in Node; components stay thin and reuse the existing shadcn/Base UI primitives and `useResource`.

**Tech Stack:** React 19, TypeScript 6 (`erasableSyntaxOnly`, `verbatimModuleSyntax`), Vite 8, react-router-dom 7, Tailwind 4 + `src/styles/workspace.css`, shadcn on `@base-ui/react`, lucide-react, Vitest 5 (`renderToStaticMarkup`, Node environment).

**Spec:** `docs/superpowers/specs/2026-11-12-admin-model-config-design.md` (sections 5 and 6)

**Depends on:** `docs/superpowers/plans/2026-11-12-admin-model-config-backend.md` (the API contract below). The frontend tests do not need the backend running.

## Global Constraints

- Every user-facing string lives in both `src/locales/en.json` and `src/locales/ar.json` with the same keys; `ar.json` must type-check against `typeof en`.
- No TypeScript parameter properties or enums (`erasableSyntaxOnly`); type-only imports use `import type`.
- The admin token is stored only in `sessionStorage` under `zaincash-admin-token` (with the admin's name), never in `localStorage`, and is sent only as the `X-Admin-Token` header to `/api/admin/*`.
- A `401` or `403` from any admin request clears the stored session, returning the page to its locked state.
- Save is enabled only after a passing test of the exact current selection (provider, model, temperature, thinking).
- Thinking is offered only when the model reports the `thinking` capability or its capabilities are unknown, and defaults to off.
- Model IDs and provider names render with `dir="ltr"` so `qwen3:4b` reads correctly in Arabic.
- Commands run from `employee-frontend/`: `npm test`, `npm run lint`, `npm run build`.

### Backend API contract used here

| Call | Response |
| --- | --- |
| `GET /api/health` | adds `ai: { locality: "local" \| "cloud" \| "mixed", steps: { [step]: { provider, model, locality, status } } }` |
| `GET /api/runs/{id}` | includes `model_ids: { [step]: "provider:model" }` (older runs: `{ jev, gemini, drafting, embedding }` with bare model IDs) |
| `POST /api/runs` | `409 { detail: "knowledge_switch_in_progress" }` during an embedding switch |
| `POST /api/admin/session` | `204`; `401 "invalid_admin_token"`; `403 "admin_disabled"` |
| `GET /api/admin/models` | `{ steps: StepModel[] }` |
| `GET /api/admin/models/catalog?step=&refresh=` | `{ step, providers: CatalogProvider[] }` |
| `POST /api/admin/models/test` | `{ ok, latency_ms, error }` |
| `PUT /api/admin/models/{step}` | `StepModel`; `422 "Model test failed: …"` |
| `POST /api/admin/models/embed/switch` | `EmbeddingSwitch` (`202`); `409 "run_in_progress" \| "switch_in_progress"` |
| `GET /api/admin/models/embed/switch` | `EmbeddingSwitch \| null` |
| `GET /api/admin/models/audit?limit=50` | `{ items: AuditEntry[] }` |

## Review Focus

1. **The token is rejected mid-session (admin changed `ADMIN_TOKEN`).** Expected: the page returns to the locked form, not a stuck error. Test: Task 1 `sends the admin token and locks the session when it is rejected`.
2. **One provider's catalog fails or is offline while the other works.** Expected: the failing tab shows its own message; the other tab still lists models; a typed model ID still works. Test: Task 3 `catalogView reports provider problems without hiding the custom model field`.
3. **The admin edits the selection after a passing test.** Expected: Save is disabled again until a new test passes. Test: Task 3 `enables saving only after a passing test of the exact selection`.
4. **The page opens while an embedding switch is already running.** Expected: progress shows, and the embed card's Change button is disabled. Test: Task 4 `disables the embed change button while a switch runs`.
5. **Older runs recorded legacy `model_ids`.** Expected: the run page still shows them under the right step. Test: Task 2 `maps legacy run model ids to steps`.

---

## File structure

| File | Responsibility |
| --- | --- |
| `src/lib/types.ts` | API types for models, catalog, audit, switch; `Health.ai`; `Run.model_ids` |
| `src/lib/model-steps.ts` | `MODEL_STEPS` order |
| `src/lib/admin-session.ts` | Session-scoped admin token + name store |
| `src/lib/api.ts` | `ApiError`, `adminRequest`, `adminApi` |
| `src/components/layout/AiLocalityChip.tsx` | Read-only AI locality chip |
| `src/features/runs/run-start-error.ts` | Readable batch start errors |
| `src/features/runs/run-models.ts` | Run `model_ids` → display rows |
| `src/features/admin/admin-errors.ts` | Admin API errors → localized messages |
| `src/features/admin/model-choice.ts` | Selection, options, save gating, filtering, prices, catalog view |
| `src/features/admin/ChangeModelDialog.tsx` | Provider tabs, model list, custom ID, options, test, save / switch |
| `src/features/admin/AdminUnlock.tsx` | Token + name form |
| `src/features/admin/ModelStepCard.tsx` | One step's current model |
| `src/features/admin/AuditList.tsx` | Change history |
| `src/features/admin/EmbeddingSwitchStatus.tsx` | Switch progress / result |
| `src/features/admin/ModelsPage.tsx` | The page |

---

### Task 1: API types, admin session and admin requests

**Files:**
- Modify: `employee-frontend/src/lib/types.ts`, `employee-frontend/src/lib/api.ts`
- Create: `employee-frontend/src/lib/model-steps.ts`, `employee-frontend/src/lib/admin-session.ts`
- Test: `employee-frontend/src/lib/api.test.ts` (append)

**Interfaces:**
- Produces:
  - Types `ModelStep`, `ModelLocality`, `ProviderState`, `ModelCapability`, `ModelOptions`, `ModelChoiceInput`, `StepModel`, `CatalogModel`, `CatalogProvider`, `ProbeResult`, `AuditEntry`, `EmbeddingSwitch`, `AiSummary`; `Health.ai?: AiSummary`; `Run.model_ids?: Record<string, string>`.
  - `MODEL_STEPS: ModelStep[]`.
  - `AdminSession = { token: string; name: string }`, `getAdminSession()`, `setAdminSession(next | null)`, `useAdminSession()`.
  - `class ApiError extends Error { status: number }` (thrown by `request` for every non-OK response).
  - `adminRequest<T>(path, options?)` (path relative to `/api/admin`), and `adminApi.{verify, models, catalog, test, save, startEmbeddingSwitch, embeddingSwitch, audit}`.

- [ ] **Step 1: Write the failing tests**

Append to `employee-frontend/src/lib/api.test.ts` (and extend its imports):

```ts
import { ApiError, adminApi, api, loadQueue } from "./api"
import { getAdminSession, setAdminSession } from "./admin-session"
```

```ts
it("sends the admin token and locks the session when it is rejected", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: "invalid_admin_token" }), { status: 401 }),
  )
  await expect(adminApi.models()).rejects.toMatchObject({ status: 401, message: "invalid_admin_token" })
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe("/api/admin/models")
  expect((options?.headers as Record<string, string>)["X-Admin-Token"]).toBe("secret")
  expect(getAdminSession()).toBeNull()
})

it("keeps the admin session on other errors and reports the status", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: "Model test failed: no tool call" }), { status: 422 }),
  )
  const error = await adminApi
    .save("draft", { provider: "ollama", model: "qwen3:4b", options: {} }, "Sara")
    .catch((e: unknown) => e)
  expect(error).toBeInstanceOf(ApiError)
  expect((error as ApiError).status).toBe(422)
  expect((error as ApiError).message).toBe("Model test failed: no tool call")
  expect(getAdminSession()).not.toBeNull()
  setAdminSession(null)
})

it("saves with the admin name and sends model options", async () => {
  setAdminSession({ token: "secret", name: "Sara" })
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } }),
  )
  await adminApi.save("draft", { provider: "ollama", model: "qwen3:4b", options: { think: false } }, "Sara")
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe("/api/admin/models/draft")
  expect(options?.method).toBe("PUT")
  expect(JSON.parse(String(options?.body))).toEqual({
    provider: "ollama", model: "qwen3:4b", options: { think: false }, changed_by: "Sara",
  })
  setAdminSession(null)
})
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `npm test -- src/lib/api.test.ts`
Expected: FAIL with `Failed to resolve import "./admin-session"`.

- [ ] **Step 3: Add the types**

Append to `employee-frontend/src/lib/types.ts`:

```ts
export type ModelStep = "intake" | "classify" | "extract" | "draft" | "embed"
export type ModelLocality = "local" | "cloud"
export type ProviderState = "ready" | "missing_key" | "unreachable"
export type ModelCapability =
  | "structured_output"
  | "tools"
  | "vision"
  | "embedding"
  | "thinking"
  | "classifier"
export type ModelOptions = { temperature?: number; think?: boolean }
export type ModelChoiceInput = { provider: string; model: string; options: ModelOptions }
export type StepModel = {
  step: ModelStep
  provider: string
  model: string
  options: ModelOptions
  source: "env" | "admin"
  updated_at: string | null
  updated_by: string | null
  locality: ModelLocality
  status: ProviderState
  status_detail: string | null
  requirements: ModelCapability[]
  providers: string[]
}
export type CatalogModel = {
  id: string
  name: string
  capabilities: ModelCapability[] | null
  price_in_per_m: number | null
  price_out_per_m: number | null
  context_length: number | null
  eligibility: "eligible" | "unknown"
}
export type CatalogProvider = {
  provider: string
  locality: ModelLocality
  status: ProviderState
  status_detail: string | null
  entries: CatalogModel[]
  error: string | null
}
export type ProbeResult = { ok: boolean; latency_ms: number; error: string | null }
export type AuditEntry = {
  id: number
  step: ModelStep
  previous: ModelChoiceInput | null
  current: ModelChoiceInput
  changed_by: string
  changed_at: string
  test_latency_ms: number
}
export type EmbeddingSwitch = {
  id: number
  status: "running" | "completed" | "completed_with_errors" | "failed"
  total: number
  done: number
  failed_document_ids: number[]
  error: string | null
  target: ModelChoiceInput
  previous: ModelChoiceInput
  started_by: string
  started_at: string
  finished_at: string | null
}
export type AiSummary = {
  locality: ModelLocality | "mixed"
  steps: Partial<
    Record<ModelStep, { provider: string; model: string; locality: ModelLocality; status: ProviderState }>
  >
}
```

In the existing `Run` type add `model_ids?: Record<string, string>` (after `total_cost_usd`), and in `Health` add `ai?: AiSummary` (after `drafting?`).

Create `employee-frontend/src/lib/model-steps.ts`:

```ts
import type { ModelStep } from "./types"

export const MODEL_STEPS: ModelStep[] = ["intake", "classify", "extract", "draft", "embed"]
```

- [ ] **Step 4: Add the admin session store**

Create `employee-frontend/src/lib/admin-session.ts`:

```ts
import { useSyncExternalStore } from "react"

export type AdminSession = { token: string; name: string }

const storageKey = "zaincash-admin-token"
const listeners = new Set<() => void>()

function read(): AdminSession | null {
  try {
    const raw = sessionStorage.getItem(storageKey)
    if (!raw) return null
    const value = JSON.parse(raw) as Partial<AdminSession>
    return typeof value.token === "string" && value.token && typeof value.name === "string" && value.name
      ? { token: value.token, name: value.name }
      : null
  } catch {
    /* No storage (tests, private browsing): start locked. */
    return null
  }
}

let session: AdminSession | null = read()

export function getAdminSession() {
  return session
}

export function setAdminSession(next: AdminSession | null) {
  session = next
  try {
    if (next) sessionStorage.setItem(storageKey, JSON.stringify(next))
    else sessionStorage.removeItem(storageKey)
  } catch {
    /* The session still applies until the page reloads. */
  }
  listeners.forEach((listener) => listener())
}

function subscribe(listener: () => void) {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export function useAdminSession() {
  return useSyncExternalStore(subscribe, getAdminSession, getAdminSession)
}
```

- [ ] **Step 5: Add `ApiError`, `adminRequest` and `adminApi`**

In `employee-frontend/src/lib/api.ts`:

1. Extend the type import with `AuditEntry, CatalogProvider, EmbeddingSwitch, ModelChoiceInput, ModelStep, ProbeResult, StepModel` and add `import { getAdminSession, setAdminSession } from "./admin-session"`.
2. Add above `request`:

```ts
export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}
```

3. In `request`, replace `throw new Error(message)` with `throw new ApiError(message, response.status)`.
4. Append at the end of the file:

```ts
export async function adminRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  try {
    return await request<T>(`/admin${path}`, {
      ...options,
      headers: {
        ...(options.headers as Record<string, string> | undefined),
        "X-Admin-Token": getAdminSession()?.token ?? "",
      },
    })
  } catch (error) {
    // A changed or disabled token must return the page to its locked state.
    if (error instanceof ApiError && (error.status === 401 || error.status === 403))
      setAdminSession(null)
    throw error
  }
}

export const adminApi = {
  verify: (token: string) =>
    request<void>("/admin/session", { method: "POST", headers: { "X-Admin-Token": token } }),
  models: (options?: RequestInit) => adminRequest<{ steps: StepModel[] }>("/models", options),
  catalog: (step: ModelStep, refresh = false) =>
    adminRequest<{ step: ModelStep; providers: CatalogProvider[] }>(
      `/models/catalog?step=${step}&refresh=${refresh}`,
    ),
  test: (step: ModelStep, choice: ModelChoiceInput) =>
    adminRequest<ProbeResult>("/models/test", {
      method: "POST",
      body: JSON.stringify({ step, ...choice }),
    }),
  save: (step: ModelStep, choice: ModelChoiceInput, changedBy: string) =>
    adminRequest<StepModel>(`/models/${step}`, {
      method: "PUT",
      body: JSON.stringify({ ...choice, changed_by: changedBy }),
    }),
  startEmbeddingSwitch: (choice: ModelChoiceInput, changedBy: string) =>
    adminRequest<EmbeddingSwitch>("/models/embed/switch", {
      method: "POST",
      body: JSON.stringify({ ...choice, changed_by: changedBy }),
    }),
  embeddingSwitch: (options?: RequestInit) =>
    adminRequest<EmbeddingSwitch | null>("/models/embed/switch", options),
  audit: (options?: RequestInit) => adminRequest<{ items: AuditEntry[] }>("/models/audit?limit=50", options),
}
```

- [ ] **Step 6: Run the tests and type-check**

Run: `npm test -- src/lib/api.test.ts`
Expected: PASS.

Run: `npm run typecheck`
Expected: exit code 0.

- [ ] **Step 7: Commit**

```bash
git add src/lib
git commit -m "feat(admin): add admin session, admin API client and model types"
```

---

### Task 2: Strings, the AI locality chip, run models and the batch switch message

**Files:**
- Modify: `employee-frontend/src/locales/en.json`, `employee-frontend/src/locales/ar.json`, `employee-frontend/src/components/layout/WorkspaceLayout.tsx`, `employee-frontend/src/features/runs/NewBatchPage.tsx:90-92`, `employee-frontend/src/features/runs/RunDetailPage.tsx`, `employee-frontend/src/styles/workspace.css`
- Create: `employee-frontend/src/components/layout/AiLocalityChip.tsx`, `employee-frontend/src/features/runs/run-start-error.ts`, `employee-frontend/src/features/runs/run-models.ts`
- Test: `employee-frontend/src/components/layout/AiLocalityChip.test.tsx`, `employee-frontend/src/features/runs/run-start-error.test.ts`, `employee-frontend/src/features/runs/run-models.test.ts`

**Interfaces:**
- Consumes: Task 1 types, `MODEL_STEPS`.
- Produces: copy keys `nav.models`, `layout.adminSection`, `ai.*`, `models.*`, `batch.switchInProgress` (used by Tasks 3–4); `AiLocalityChip`; `runStartError(error, text)`; `runModelRows(modelIds) -> { step: ModelStep; provider: string | null; model: string }[]`.

- [ ] **Step 1: Add the strings**

In `employee-frontend/src/locales/en.json`:
- In `"nav"`, after `"evaluation"`, add `"models": "AI models"`.
- In `"layout"`, after `"newBatch"`, add `"adminSection": "Admin"`.
- In `"batch"`, after `"submitted"`, add `"switchInProgress": "The knowledge base is switching embedding models. Start the batch when it finishes."`.
- Add these top-level keys before the final `}`:

```json
  "ai": {
    "local": "AI: Local",
    "cloud": "AI: Cloud",
    "mixed": "AI: Mixed",
    "tooltip": "Where each AI step runs"
  },
  "models": {
    "title": "AI models",
    "description": "Choose the model behind each step of the support pipeline. Changes apply to new batches and new customer conversations.",
    "lock": "Lock admin settings",
    "unlockTitle": "Unlock admin settings",
    "unlockDescription": "Enter the admin token from the backend .env file and your name for the change history.",
    "nameLabel": "Your name",
    "tokenLabel": "Admin token",
    "unlock": "Unlock",
    "unlocking": "Checking…",
    "wrongToken": "That admin token is not correct.",
    "disabled": "Admin settings are turned off. Set ADMIN_TOKEN in the backend .env file and restart the API.",
    "genericError": "Something went wrong. Please retry.",
    "steps": {
      "intake": "Customer intake",
      "classify": "Classification (Jev)",
      "extract": "Field extraction",
      "draft": "Reply drafting",
      "embed": "Knowledge search embeddings"
    },
    "stepHelp": {
      "intake": "Talks with customers in the intake app and reads their screenshots. Needs vision and structured output.",
      "classify": "Sorts each ticket into a category, priority and flags. Runs on TypeSafe.",
      "extract": "Fills in missing transaction details from the ticket text. Needs structured output.",
      "draft": "Writes the Arabic reply using tools and the knowledge base. Needs tool calling.",
      "embed": "Turns knowledge documents and questions into 768-number vectors for search."
    },
    "locality": { "local": "Local", "cloud": "Cloud" },
    "status": { "ready": "Ready", "missing_key": "API key missing", "unreachable": "Not reachable" },
    "providers": { "openrouter": "OpenRouter · cloud", "ollama": "Ollama · local", "typesafe": "TypeSafe · cloud" },
    "capabilities": {
      "structured_output": "Structured output",
      "tools": "Tools",
      "vision": "Vision",
      "embedding": "Embeddings",
      "thinking": "Thinking",
      "classifier": "Classifier"
    },
    "sourceEnv": "Default from the backend .env file",
    "sourceAdmin": "Set by {name} on {date}",
    "change": "Change model",
    "dialogTitle": "Change the {step} model",
    "requirements": "Required: {list}",
    "search": "Search models",
    "refresh": "Refresh model list",
    "modelList": "Available models",
    "noModels": "No suitable models found. Type a model ID below.",
    "unknownCaps": "Capabilities unknown",
    "free": "Free",
    "price": "${in} / ${out} per 1M tokens",
    "customModel": "Or type a model ID",
    "customHelp": "Any model ID this provider accepts. It must pass the test before it can be saved.",
    "temperature": "Temperature",
    "temperatureHelp": "0 to 2. Leave empty for the step default.",
    "thinking": "Let the model think before answering (slower)",
    "localSlow": "Local models run on this machine. They keep data private but answer more slowly.",
    "test": "Test model",
    "testing": "Testing…",
    "testPassed": "Test passed in {ms} ms.",
    "testFailed": "Test failed: {error}",
    "save": "Save",
    "saving": "Saving…",
    "reindex": "Re-index and switch",
    "confirmTitle": "Switch the embedding model?",
    "confirmDescription": "Every knowledge document will be re-indexed with the new model. Knowledge search pauses until it finishes, and new batches cannot start meanwhile. This cannot start while a batch is running.",
    "confirmAction": "Re-index and switch",
    "switchTitle": "Embedding switch progress",
    "switchRunning": "Re-indexing the knowledge base",
    "switchDone": "Embedding model switched",
    "switchErrors": "Embedding model switched, some documents failed",
    "switchFailed": "Embedding switch stopped",
    "switchProgress": "{done} of {total} documents re-indexed",
    "switchFailedDocs": "Re-index these documents from the knowledge base page: {ids}",
    "runInProgress": "A batch is still running. Try again when it finishes.",
    "switchInProgress": "An embedding switch is already running.",
    "auditTitle": "Change history",
    "auditEmpty": "No model changes yet.",
    "auditBy": "{name} · {date}",
    "usedTitle": "Models used"
  }
```

In `employee-frontend/src/locales/ar.json`, add the same keys in the same places:
- `"nav"`: `"models": "نماذج الذكاء الاصطناعي"`.
- `"layout"`: `"adminSection": "الإدارة"`.
- `"batch"`: `"switchInProgress": "قاعدة المعرفة تبدّل نموذج التضمين الآن. ابدأ الدفعة بعد انتهائها."`.
- Top level:

```json
  "ai": {
    "local": "الذكاء الاصطناعي: محلي",
    "cloud": "الذكاء الاصطناعي: سحابي",
    "mixed": "الذكاء الاصطناعي: مختلط",
    "tooltip": "أين تعمل كل خطوة ذكاء اصطناعي"
  },
  "models": {
    "title": "نماذج الذكاء الاصطناعي",
    "description": "اختر النموذج الذي يشغّل كل خطوة في مسار الدعم. تُطبَّق التغييرات على الدفعات الجديدة ومحادثات الزبائن الجديدة.",
    "lock": "قفل إعدادات المسؤول",
    "unlockTitle": "فتح إعدادات المسؤول",
    "unlockDescription": "أدخل رمز المسؤول من ملف ‎.env‎ في الخادم، واسمك لسجل التغييرات.",
    "nameLabel": "اسمك",
    "tokenLabel": "رمز المسؤول",
    "unlock": "فتح",
    "unlocking": "جارٍ التحقق…",
    "wrongToken": "رمز المسؤول غير صحيح.",
    "disabled": "إعدادات المسؤول متوقفة. اضبط ADMIN_TOKEN في ملف ‎.env‎ للخادم ثم أعد تشغيل الواجهة.",
    "genericError": "حدث خطأ. حاول مرة أخرى.",
    "steps": {
      "intake": "استقبال الزبائن",
      "classify": "التصنيف (Jev)",
      "extract": "استخراج الحقول",
      "draft": "صياغة الرد",
      "embed": "تضمينات البحث في المعرفة"
    },
    "stepHelp": {
      "intake": "يتحدث مع الزبائن في تطبيق الاستقبال ويقرأ لقطات الشاشة. يحتاج إلى الرؤية والمخرجات المنظمة.",
      "classify": "يصنّف كل تذكرة حسب الفئة والأولوية والعلامات. يعمل على TypeSafe.",
      "extract": "يكمل تفاصيل العملية الناقصة من نص التذكرة. يحتاج إلى المخرجات المنظمة.",
      "draft": "يكتب الرد العربي باستخدام الأدوات وقاعدة المعرفة. يحتاج إلى استدعاء الأدوات.",
      "embed": "يحوّل مستندات المعرفة والأسئلة إلى متجهات من 768 رقماً للبحث."
    },
    "locality": { "local": "محلي", "cloud": "سحابي" },
    "status": { "ready": "جاهز", "missing_key": "مفتاح الواجهة مفقود", "unreachable": "تعذّر الوصول" },
    "providers": { "openrouter": "OpenRouter · سحابي", "ollama": "Ollama · محلي", "typesafe": "TypeSafe · سحابي" },
    "capabilities": {
      "structured_output": "مخرجات منظمة",
      "tools": "أدوات",
      "vision": "رؤية",
      "embedding": "تضمينات",
      "thinking": "تفكير",
      "classifier": "مصنّف"
    },
    "sourceEnv": "القيمة الافتراضية من ملف ‎.env‎ للخادم",
    "sourceAdmin": "ضبطه {name} في {date}",
    "change": "تغيير النموذج",
    "dialogTitle": "تغيير نموذج {step}",
    "requirements": "المطلوب: {list}",
    "search": "ابحث في النماذج",
    "refresh": "تحديث قائمة النماذج",
    "modelList": "النماذج المتاحة",
    "noModels": "لا توجد نماذج مناسبة. اكتب معرّف نموذج أدناه.",
    "unknownCaps": "القدرات غير معروفة",
    "free": "مجاني",
    "price": "${in} / ${out} لكل مليون رمز",
    "customModel": "أو اكتب معرّف نموذج",
    "customHelp": "أي معرّف يقبله هذا المزوّد. يجب أن يجتاز الاختبار قبل الحفظ.",
    "temperature": "درجة الحرارة",
    "temperatureHelp": "من 0 إلى 2. اتركها فارغة لاستخدام القيمة الافتراضية للخطوة.",
    "thinking": "دع النموذج يفكّر قبل الإجابة (أبطأ)",
    "localSlow": "النماذج المحلية تعمل على هذا الجهاز. تحافظ على خصوصية البيانات لكنها أبطأ في الرد.",
    "test": "اختبار النموذج",
    "testing": "جارٍ الاختبار…",
    "testPassed": "نجح الاختبار خلال {ms} ملّي ثانية.",
    "testFailed": "فشل الاختبار: {error}",
    "save": "حفظ",
    "saving": "جارٍ الحفظ…",
    "reindex": "إعادة الفهرسة والتبديل",
    "confirmTitle": "تبديل نموذج التضمين؟",
    "confirmDescription": "ستُعاد فهرسة كل مستندات المعرفة بالنموذج الجديد. يتوقف البحث في المعرفة حتى تنتهي، ولا يمكن بدء دفعات جديدة خلال ذلك. لا يمكن البدء أثناء تشغيل دفعة.",
    "confirmAction": "إعادة الفهرسة والتبديل",
    "switchTitle": "تقدّم تبديل التضمين",
    "switchRunning": "جارٍ إعادة فهرسة قاعدة المعرفة",
    "switchDone": "تم تبديل نموذج التضمين",
    "switchErrors": "تم تبديل نموذج التضمين مع فشل بعض المستندات",
    "switchFailed": "توقف تبديل التضمين",
    "switchProgress": "أُعيدت فهرسة {done} من {total} مستند",
    "switchFailedDocs": "أعد فهرسة هذه المستندات من صفحة قاعدة المعرفة: {ids}",
    "runInProgress": "ما زالت دفعة قيد التشغيل. حاول مجدداً بعد انتهائها.",
    "switchInProgress": "تبديل التضمين قيد التشغيل بالفعل.",
    "auditTitle": "سجل التغييرات",
    "auditEmpty": "لا توجد تغييرات على النماذج بعد.",
    "auditBy": "{name} · {date}",
    "usedTitle": "النماذج المستخدمة"
  }
```

Run: `npm run typecheck`
Expected: exit code 0 (a missing Arabic key fails here).

- [ ] **Step 2: Write the failing tests**

`employee-frontend/src/components/layout/AiLocalityChip.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { afterEach, expect, it } from "vitest"
import { TooltipProvider } from "@/components/ui/tooltip"
import { getLocale, setLocale } from "@/lib/locale"
import type { Health } from "@/lib/types"
import { WorkspaceContext } from "@/lib/workspace"
import { AiLocalityChip } from "./AiLocalityChip"

const originalLocale = getLocale()
afterEach(() => setLocale(originalLocale))

const base: Health = {
  database: "connected",
  configured_modes: ["jev"],
  capabilities: { drafting: true, rag_indexing: true, evaluation: false },
}

function chip(health: Health) {
  return renderToStaticMarkup(
    <TooltipProvider>
      <WorkspaceContext.Provider
        value={{ revision: 0, refresh: () => {}, health, connectionError: null, notify: () => {} }}
      >
        <AiLocalityChip />
      </WorkspaceContext.Provider>
    </TooltipProvider>,
  )
}

const mixed: Health = {
  ...base,
  ai: {
    locality: "mixed",
    steps: { draft: { provider: "ollama", model: "qwen3:4b", locality: "local", status: "ready" } },
  },
}

it("shows where AI runs", () => {
  setLocale("en")
  expect(chip(mixed)).toContain("AI: Mixed")
  setLocale("ar")
  expect(chip(mixed)).toContain("الذكاء الاصطناعي: مختلط")
})

it("renders nothing before health reports AI steps", () => {
  expect(chip(base)).toBe("")
})
```

`employee-frontend/src/features/runs/run-start-error.test.ts`:

```ts
import { expect, it } from "vitest"
import { ApiError } from "@/lib/api"
import en from "@/locales/en.json"
import { runStartError } from "./run-start-error"

it("explains a batch blocked by an embedding switch", () => {
  expect(runStartError(new ApiError("knowledge_switch_in_progress", 409), en.batch)).toBe(en.batch.switchInProgress)
  expect(runStartError(new Error("Ticket x already exists"), en.batch)).toBe("Ticket x already exists")
  expect(runStartError("nope", en.batch)).toBe(en.batch.startFailed)
})
```

`employee-frontend/src/features/runs/run-models.test.ts`:

```ts
import { expect, it } from "vitest"
import { runModelRows } from "./run-models"

it("orders provider refs by step and keeps colons in model ids", () => {
  expect(runModelRows({ draft: "ollama:qwen3:4b", classify: "typesafe:jev-1.13.0" })).toEqual([
    { step: "classify", provider: "typesafe", model: "jev-1.13.0" },
    { step: "draft", provider: "ollama", model: "qwen3:4b" },
  ])
})

it("maps legacy run model ids to steps", () => {
  expect(runModelRows({ jev: "jev-1.13.0", drafting: "google/gemini-3.8-flash" })).toEqual([
    { step: "classify", provider: null, model: "jev-1.13.0" },
    { step: "draft", provider: null, model: "google/gemini-3.8-flash" },
  ])
  expect(runModelRows(undefined)).toEqual([])
})
```

- [ ] **Step 3: Run the tests to confirm they fail**

Run: `npm test -- src/components/layout/AiLocalityChip.test.tsx src/features/runs`
Expected: FAIL with unresolved imports for `./AiLocalityChip`, `./run-start-error`, `./run-models`.

- [ ] **Step 4: Implement the helpers and the chip**

`employee-frontend/src/features/runs/run-start-error.ts`:

```ts
import type { Copy } from "@/lib/locale"

export function runStartError(error: unknown, text: Copy["batch"]) {
  if (error instanceof Error && error.message === "knowledge_switch_in_progress") return text.switchInProgress
  return error instanceof Error ? error.message : text.startFailed
}
```

`employee-frontend/src/features/runs/run-models.ts`:

```ts
import { MODEL_STEPS } from "@/lib/model-steps"
import type { ModelStep } from "@/lib/types"

const LEGACY: Record<string, ModelStep> = {
  jev: "classify",
  gemini: "extract",
  drafting: "draft",
  embedding: "embed",
}

export type RunModelRow = { step: ModelStep; provider: string | null; model: string }

export function runModelRows(modelIds: Record<string, string> | undefined): RunModelRow[] {
  if (!modelIds) return []
  const byStep = new Map<ModelStep, RunModelRow>()
  for (const [key, value] of Object.entries(modelIds)) {
    const step = (MODEL_STEPS as string[]).includes(key) ? (key as ModelStep) : LEGACY[key]
    if (!step || typeof value !== "string") continue
    const split = value.indexOf(":")
    const isRef = key === step && split > 0
    byStep.set(step, isRef
      ? { step, provider: value.slice(0, split), model: value.slice(split + 1) }
      : { step, provider: null, model: value })
  }
  return MODEL_STEPS.filter((step) => byStep.has(step)).map((step) => byStep.get(step)!)
}
```

`employee-frontend/src/components/layout/AiLocalityChip.tsx`:

```tsx
import { Cpu } from "lucide-react"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { useCopy } from "@/lib/locale"
import { MODEL_STEPS } from "@/lib/model-steps"
import { useWorkspace } from "@/lib/workspace"

export function AiLocalityChip() {
  const { health } = useWorkspace()
  const copy = useCopy()
  const ai = health?.ai
  if (!ai) return null
  return (
    <Tooltip>
      <TooltipTrigger render={<span className={`ai-chip ai-${ai.locality}`} tabIndex={0} />}>
        <Cpu size={12} />
        {copy.ai[ai.locality]}
      </TooltipTrigger>
      <TooltipContent>
        <strong className="ai-chip-line">{copy.ai.tooltip}</strong>
        {MODEL_STEPS.map((step) => {
          const item = ai.steps[step]
          return item ? (
            <span key={step} className="ai-chip-line">
              {copy.models.steps[step]}: <span dir="ltr">{item.model}</span> ({copy.models.locality[item.locality]})
            </span>
          ) : null
        })}
      </TooltipContent>
    </Tooltip>
  )
}
```

- [ ] **Step 5: Use them in the layout and run pages**

`employee-frontend/src/components/layout/WorkspaceLayout.tsx`: import `AiLocalityChip` from `@/components/layout/AiLocalityChip` and render `<AiLocalityChip />` immediately before `<LanguageToggle />`.

`employee-frontend/src/features/runs/NewBatchPage.tsx`: import `{ runStartError } from "./run-start-error"` and replace `setError(e instanceof Error ? e.message : text.startFailed)` inside `start()` with `setError(runStartError(e, text))`.

`employee-frontend/src/features/runs/RunDetailPage.tsx`:
- Add imports `import { useCopy } from "@/lib/locale"` and `import { runModelRows } from "./run-models"`.
- In `RunDetailPage`, add `const copy = useCopy()` after `workspace = useWorkspace()` and `const models = runModelRows(run.model_ids)` after `const progress = ...`.
- Insert directly after the closing `</div>` of `metrics-grid`:

```tsx
      {models.length > 0 && (
        <Card className="run-models-card">
          <CardHeader>
            <CardTitle>{copy.models.usedTitle}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="simple-breakdown">
              {models.map((row) => (
                <div key={row.step}>
                  <span>{copy.models.steps[row.step]}</span>
                  <strong dir="ltr">{row.provider ? `${row.provider} · ${row.model}` : row.model}</strong>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
```

Append to `employee-frontend/src/styles/workspace.css`:

```css
.ai-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--muted-foreground);
  white-space: nowrap;
}
.ai-chip.ai-local {
  color: var(--green);
  border-color: currentColor;
}
.ai-chip-line {
  display: block;
}
.run-models-card {
  margin-bottom: 20px;
}
```

- [ ] **Step 6: Run tests, lint and build**

Run: `npm test`
Expected: PASS (including the existing `NewBatchPage` tests).

Run: `npm run lint && npm run build`
Expected: both exit 0.

- [ ] **Step 7: Commit**

```bash
git add src
git commit -m "feat(workspace): show where AI runs and which models each run used"
```

---

### Task 3: Model choice logic and the change dialog

**Files:**
- Create: `employee-frontend/src/features/admin/model-choice.ts`, `employee-frontend/src/features/admin/admin-errors.ts`, `employee-frontend/src/features/admin/ChangeModelDialog.tsx`
- Modify: `employee-frontend/src/styles/workspace.css`
- Test: `employee-frontend/src/features/admin/model-choice.test.ts`, `employee-frontend/src/features/admin/admin-errors.test.ts`

**Interfaces:**
- Consumes: Task 1 `adminApi`, `adminRequest`, `ApiError`, types; Task 2 copy keys.
- Produces:
  - `choiceKey(choice)`, `isValidTemperature(value)`, `buildOptions(temperature, think: boolean | null)`, `canSave(choice, tested: TestedChoice | null)`, `filterModels(entries, query)`, `offersThinking(entry | undefined)`, `priceLabel(entry, free, template) -> string | null`, `catalogView(provider: CatalogProvider | undefined) -> { kind: "loading" | "problem" | "list"; message: string | null }`, type `TestedChoice = { key: string; result: ProbeResult }`.
  - `adminErrorMessage(error, text: Copy["models"]) -> string`.
  - `ChangeModelDialog({ step: StepModel; changedBy: string; onClose(): void; onSaved(): void })`.

- [ ] **Step 1: Write the failing tests**

`employee-frontend/src/features/admin/model-choice.test.ts`:

```ts
import { expect, it } from "vitest"
import type { CatalogModel, CatalogProvider, ModelChoiceInput } from "@/lib/types"
import {
  buildOptions,
  canSave,
  catalogView,
  choiceKey,
  filterModels,
  isValidTemperature,
  offersThinking,
  priceLabel,
} from "./model-choice"

const choice: ModelChoiceInput = { provider: "ollama", model: "qwen3:4b", options: { think: false } }
const model = (over: Partial<CatalogModel> = {}): CatalogModel => ({
  id: "qwen3:4b", name: "qwen3:4b", capabilities: ["tools"], price_in_per_m: 0, price_out_per_m: 0,
  context_length: null, eligibility: "eligible", ...over,
})
const provider = (over: Partial<CatalogProvider> = {}): CatalogProvider => ({
  provider: "ollama", locality: "local", status: "ready", status_detail: null, entries: [], error: null, ...over,
})

it("enables saving only after a passing test of the exact selection", () => {
  const tested = { key: choiceKey(choice), result: { ok: true, latency_ms: 900, error: null } }
  expect(canSave(choice, tested)).toBe(true)
  expect(canSave({ ...choice, options: { think: true } }, tested)).toBe(false)
  expect(canSave({ ...choice, options: { think: false, temperature: 0.2 } }, tested)).toBe(false)
  expect(canSave({ ...choice, model: "qwen3:8b" }, tested)).toBe(false)
  expect(canSave(choice, { ...tested, result: { ok: false, latency_ms: 5, error: "x" } })).toBe(false)
  expect(canSave(choice, null)).toBe(false)
  expect(canSave({ ...choice, model: "  " }, { ...tested, key: choiceKey({ ...choice, model: "  " }) })).toBe(false)
})

it("builds options from form values and validates temperature", () => {
  expect(buildOptions("", null)).toEqual({})
  expect(buildOptions("0.3", false)).toEqual({ temperature: 0.3, think: false })
  expect(isValidTemperature("")).toBe(true)
  expect(isValidTemperature("2")).toBe(true)
  expect(isValidTemperature("2.5")).toBe(false)
  expect(isValidTemperature("abc")).toBe(false)
})

it("filters by id or name and offers thinking only when possible", () => {
  const entries = [model(), model({ id: "gemma3:4b", name: "Gemma 3", capabilities: null })]
  expect(filterModels(entries, "gem").map((e) => e.id)).toEqual(["gemma3:4b"])
  expect(filterModels(entries, " ")).toHaveLength(2)
  expect(offersThinking(model())).toBe(false)
  expect(offersThinking(model({ capabilities: ["tools", "thinking"] }))).toBe(true)
  expect(offersThinking(model({ capabilities: null }))).toBe(true)
  expect(offersThinking(undefined)).toBe(true)
})

it("labels prices", () => {
  const template = "${in} / ${out} per 1M tokens"
  expect(priceLabel(model(), "Free", template)).toBe("Free")
  expect(priceLabel(model({ price_in_per_m: 3, price_out_per_m: 15 }), "Free", template)).toBe("$3.00 / $15.00 per 1M tokens")
  expect(priceLabel(model({ price_in_per_m: null, price_out_per_m: null }), "Free", template)).toBeNull()
})

it("catalogView reports provider problems without hiding the custom model field", () => {
  expect(catalogView(undefined).kind).toBe("loading")
  expect(catalogView(provider({ status: "unreachable", status_detail: "Ollama is not reachable at x." }))).toEqual({
    kind: "problem", message: "Ollama is not reachable at x.",
  })
  expect(catalogView(provider({ error: "Could not list models: ConnectError" }))).toEqual({
    kind: "problem", message: "Could not list models: ConnectError",
  })
  expect(catalogView(provider({ entries: [model()] }))).toEqual({ kind: "list", message: null })
})
```

`employee-frontend/src/features/admin/admin-errors.test.ts`:

```ts
import { expect, it } from "vitest"
import { ApiError } from "@/lib/api"
import en from "@/locales/en.json"
import { adminErrorMessage } from "./admin-errors"

it("maps admin API errors to readable messages", () => {
  expect(adminErrorMessage(new ApiError("admin_disabled", 403), en.models)).toBe(en.models.disabled)
  expect(adminErrorMessage(new ApiError("invalid_admin_token", 401), en.models)).toBe(en.models.wrongToken)
  expect(adminErrorMessage(new ApiError("run_in_progress", 409), en.models)).toBe(en.models.runInProgress)
  expect(adminErrorMessage(new ApiError("switch_in_progress", 409), en.models)).toBe(en.models.switchInProgress)
  expect(adminErrorMessage(new ApiError("Model test failed: x", 422), en.models)).toBe("Model test failed: x")
  expect(adminErrorMessage(42, en.models)).toBe(en.models.genericError)
})
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `npm test -- src/features/admin`
Expected: FAIL with unresolved imports.

- [ ] **Step 3: Implement the helpers**

`employee-frontend/src/features/admin/model-choice.ts`:

```ts
import { fill } from "@/lib/locale"
import type { CatalogModel, CatalogProvider, ModelChoiceInput, ModelOptions, ProbeResult } from "@/lib/types"

export type TestedChoice = { key: string; result: ProbeResult }

export function choiceKey(choice: ModelChoiceInput) {
  return JSON.stringify([
    choice.provider,
    choice.model.trim(),
    choice.options.temperature ?? null,
    choice.options.think ?? null,
  ])
}

export function isValidTemperature(value: string) {
  if (value.trim() === "") return true
  const number = Number(value)
  return Number.isFinite(number) && number >= 0 && number <= 2
}

export function buildOptions(temperature: string, think: boolean | null): ModelOptions {
  const options: ModelOptions = {}
  if (temperature.trim() !== "" && isValidTemperature(temperature)) options.temperature = Number(temperature)
  if (think !== null) options.think = think
  return options
}

export function canSave(choice: ModelChoiceInput, tested: TestedChoice | null) {
  return choice.model.trim() !== "" && tested !== null && tested.result.ok && tested.key === choiceKey(choice)
}

export function filterModels(entries: CatalogModel[], query: string) {
  const needle = query.trim().toLowerCase()
  if (!needle) return entries
  return entries.filter(
    (entry) => entry.id.toLowerCase().includes(needle) || entry.name.toLowerCase().includes(needle),
  )
}

export function offersThinking(entry: CatalogModel | undefined) {
  return entry === undefined || entry.capabilities === null || entry.capabilities.includes("thinking")
}

export function priceLabel(entry: CatalogModel, free: string, template: string): string | null {
  const input = entry.price_in_per_m
  const output = entry.price_out_per_m
  if (input === null && output === null) return null
  if ((input ?? 0) === 0 && (output ?? 0) === 0) return free
  return fill(template, { in: (input ?? 0).toFixed(2), out: (output ?? 0).toFixed(2) })
}

export function catalogView(provider: CatalogProvider | undefined): {
  kind: "loading" | "problem" | "list"
  message: string | null
} {
  if (!provider) return { kind: "loading", message: null }
  if (provider.status !== "ready") return { kind: "problem", message: provider.status_detail ?? provider.status }
  if (provider.error) return { kind: "problem", message: provider.error }
  return { kind: "list", message: null }
}
```

`employee-frontend/src/features/admin/admin-errors.ts`:

```ts
import { ApiError } from "@/lib/api"
import type { Copy } from "@/lib/locale"

export function adminErrorMessage(error: unknown, text: Copy["models"]): string {
  if (error instanceof ApiError) {
    if (error.status === 403) return text.disabled
    if (error.status === 401) return text.wrongToken
    if (error.message === "run_in_progress") return text.runInProgress
    if (error.message === "switch_in_progress") return text.switchInProgress
    return error.message
  }
  return error instanceof Error ? error.message : text.genericError
}
```

- [ ] **Step 4: Implement the dialog**

`employee-frontend/src/features/admin/ChangeModelDialog.tsx`:

```tsx
import { useMemo, useState } from "react"
import { CheckCircle2, CircleAlert, LoaderCircle, RefreshCw } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ConfirmDialog } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { adminApi, adminRequest } from "@/lib/api"
import { fill, useCopy } from "@/lib/locale"
import type { CatalogModel, CatalogProvider, ModelChoiceInput, StepModel } from "@/lib/types"
import { adminErrorMessage } from "./admin-errors"
import {
  buildOptions,
  canSave,
  catalogView,
  choiceKey,
  filterModels,
  isValidTemperature,
  offersThinking,
  priceLabel,
  type TestedChoice,
} from "./model-choice"

export function ChangeModelDialog({
  step,
  changedBy,
  onClose,
  onSaved,
}: {
  step: StepModel
  changedBy: string
  onClose: () => void
  onSaved: () => void
}) {
  const copy = useCopy()
  const text = copy.models
  const [provider, setProvider] = useState(
    step.providers.includes(step.provider) ? step.provider : step.providers[0],
  )
  const [refresh, setRefresh] = useState(0)
  const [query, setQuery] = useState("")
  const [selected, setSelected] = useState(step.model)
  const [custom, setCustom] = useState("")
  const [temperature, setTemperature] = useState(step.options.temperature?.toString() ?? "")
  const [think, setThink] = useState(step.options.think ?? false)
  const [tested, setTested] = useState<TestedChoice | null>(null)
  const [busy, setBusy] = useState<"test" | "save" | null>(null)
  const [error, setError] = useState("")
  const [confirm, setConfirm] = useState(false)
  const catalog = useResource<{ providers: CatalogProvider[] }>(
    `/models/catalog?step=${step.step}&refresh=${refresh > 0}`,
    refresh,
    0,
    adminRequest,
  )
  const current = catalog.data?.providers.find((item) => item.provider === provider)
  const view = catalogView(current)
  const model = custom.trim() || selected
  const entry = current?.entries.find((item) => item.id === model)
  const tunable = step.step !== "classify" && step.step !== "embed"
  const thinking = tunable && offersThinking(entry)
  const choice: ModelChoiceInput = {
    provider,
    model,
    options: buildOptions(tunable ? temperature : "", thinking ? think : null),
  }
  const temperatureOk = isValidTemperature(temperature)
  const visible = useMemo(() => filterModels(current?.entries ?? [], query), [current, query])
  const result = tested && tested.key === choiceKey(choice) ? tested.result : null

  async function runTest() {
    if (!model || !temperatureOk || busy) return
    setBusy("test")
    setError("")
    const key = choiceKey(choice)
    try {
      setTested({ key, result: await adminApi.test(step.step, choice) })
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(null)
    }
  }

  async function save() {
    if (!canSave(choice, tested) || busy) return
    setBusy("save")
    setError("")
    try {
      if (step.step === "embed") await adminApi.startEmbeddingSwitch(choice, changedBy)
      else await adminApi.save(step.step, choice, changedBy)
      onSaved()
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(null)
      setConfirm(false)
    }
  }

  return (
    <Dialog open onOpenChange={(open) => { if (!open && !busy) onClose() }}>
      <DialogContent className="model-dialog">
        <DialogHeader>
          <DialogTitle>{fill(text.dialogTitle, { step: text.steps[step.step] })}</DialogTitle>
          <DialogDescription>
            {fill(text.requirements, {
              list: step.requirements.map((item) => text.capabilities[item]).join(" · "),
            })}
          </DialogDescription>
        </DialogHeader>
        <Tabs
          value={provider}
          onValueChange={(value) => {
            setProvider(String(value))
            setSelected("")
            setCustom("")
            setTested(null)
          }}
        >
          <TabsList>
            {step.providers.map((name) => (
              <TabsTrigger key={name} value={name}>
                {name in text.providers ? text.providers[name as keyof typeof text.providers] : name}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
        <div className="catalog-toolbar">
          <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={text.search} aria-label={text.search} />
          <Button variant="outline" size="icon" aria-label={text.refresh} onClick={() => setRefresh((value) => value + 1)}>
            <RefreshCw size={15} />
          </Button>
        </div>
        {catalog.error && <p className="error-text">{catalog.error}</p>}
        {view.kind === "loading" && !catalog.error && <p className="muted small">{copy.common.loading}</p>}
        {view.kind === "problem" && <p className="error-text">{view.message}</p>}
        {view.kind === "list" && (
          <div className="catalog-list" role="radiogroup" aria-label={text.modelList}>
            {visible.length === 0 && <p className="muted small">{text.noModels}</p>}
            {visible.map((item) => (
              <CatalogOption
                key={item.id}
                item={item}
                active={!custom.trim() && selected === item.id}
                onSelect={() => {
                  setSelected(item.id)
                  setCustom("")
                }}
              />
            ))}
          </div>
        )}
        <label className="model-field">
          {text.customModel}
          <Input dir="ltr" value={custom} onChange={(e) => setCustom(e.target.value)} placeholder={step.step === "classify" ? "jev-1.13.0" : "qwen3:4b"} />
          <span className="field-help">{text.customHelp}</span>
        </label>
        {tunable && (
          <div className="model-options">
            <label className="model-field">
              {text.temperature}
              <Input type="number" min={0} max={2} step={0.1} value={temperature} onChange={(e) => setTemperature(e.target.value)} aria-invalid={!temperatureOk} />
              <span className="field-help">{text.temperatureHelp}</span>
            </label>
            {thinking && (
              <label className="model-toggle">
                <input type="checkbox" checked={think} onChange={(e) => setThink(e.target.checked)} />
                {text.thinking}
              </label>
            )}
          </div>
        )}
        {provider === "ollama" && <p className="field-help">{text.localSlow}</p>}
        {result && (
          <p className={result.ok ? "probe-ok" : "error-text"} role="status">
            {result.ok ? <CheckCircle2 size={15} /> : <CircleAlert size={15} />}
            {result.ok
              ? fill(text.testPassed, { ms: result.latency_ms })
              : fill(text.testFailed, { error: result.error ?? "" })}
          </p>
        )}
        {error && <p className="error-text" role="alert">{error}</p>}
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={busy !== null}>
            {copy.common.cancel}
          </Button>
          <Button variant="outline" onClick={() => void runTest()} disabled={!model || !temperatureOk || busy !== null}>
            {busy === "test" && <LoaderCircle className="animate-spin" size={15} />}
            {busy === "test" ? text.testing : text.test}
          </Button>
          <Button
            onClick={() => (step.step === "embed" ? setConfirm(true) : void save())}
            disabled={!canSave(choice, tested) || busy !== null}
          >
            {busy === "save" ? text.saving : step.step === "embed" ? text.reindex : text.save}
          </Button>
        </DialogFooter>
        <ConfirmDialog
          open={confirm}
          onClose={() => setConfirm(false)}
          title={text.confirmTitle}
          description={text.confirmDescription}
          action={text.confirmAction}
          onConfirm={() => void save()}
        />
      </DialogContent>
    </Dialog>
  )
}

function CatalogOption({
  item,
  active,
  onSelect,
}: {
  item: CatalogModel
  active: boolean
  onSelect: () => void
}) {
  const text = useCopy().models
  const price = priceLabel(item, text.free, text.price)
  return (
    <button
      type="button"
      role="radio"
      aria-checked={active}
      className={`catalog-option ${active ? "is-active" : ""}`}
      onClick={onSelect}
    >
      <span dir="ltr">{item.name}</span>
      <span className="chip-row">
        {item.capabilities === null ? (
          <Badge variant="outline">{text.unknownCaps}</Badge>
        ) : (
          item.capabilities.map((capability) => (
            <Badge key={capability} variant="secondary">{text.capabilities[capability]}</Badge>
          ))
        )}
        {price && <span className="muted small" dir="ltr">{price}</span>}
      </span>
    </button>
  )
}
```

Append to `employee-frontend/src/styles/workspace.css`:

```css
.model-dialog {
  max-width: 640px;
  display: grid;
  gap: 12px;
}
.catalog-toolbar {
  display: flex;
  gap: 8px;
}
.catalog-list {
  display: grid;
  gap: 6px;
  max-height: 260px;
  overflow-y: auto;
}
.catalog-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  text-align: start;
  padding: 8px 10px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
}
.catalog-option.is-active {
  border-color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary);
}
.chip-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}
.model-field {
  display: grid;
  gap: 6px;
  font-size: 13px;
}
.model-options {
  display: flex;
  flex-wrap: wrap;
  align-items: end;
  gap: 16px;
}
.model-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
.probe-ok {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--green);
  font-size: 13px;
}
```

- [ ] **Step 5: Run tests, lint and build**

Run: `npm test -- src/features/admin`
Expected: PASS.

Run: `npm run lint && npm run build`
Expected: both exit 0.

- [ ] **Step 6: Commit**

```bash
git add src/features/admin src/styles/workspace.css
git commit -m "feat(admin): add model choice logic and the change model dialog"
```

---

### Task 4: The Models page, navigation and route

**Files:**
- Create: `employee-frontend/src/features/admin/ModelsPage.tsx`, `AdminUnlock.tsx`, `ModelStepCard.tsx`, `AuditList.tsx`, `EmbeddingSwitchStatus.tsx`
- Modify: `employee-frontend/src/App.tsx`, `employee-frontend/src/components/layout/WorkspaceLayout.tsx`, `employee-frontend/src/styles/workspace.css`
- Test: `employee-frontend/src/features/admin/ModelsPage.test.tsx`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: route `/admin/models`; sidebar **Admin → AI models**; `ModelStepCard({ value, disabled, onChange })`; `EmbeddingSwitchStatus({ value })`.

- [ ] **Step 1: Write the failing tests**

`employee-frontend/src/features/admin/ModelsPage.test.tsx`:

```tsx
import { renderToStaticMarkup } from "react-dom/server"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, it } from "vitest"
import { setAdminSession } from "@/lib/admin-session"
import { getLocale, setLocale } from "@/lib/locale"
import type { EmbeddingSwitch, StepModel } from "@/lib/types"
import { WorkspaceContext } from "@/lib/workspace"
import { EmbeddingSwitchStatus } from "./EmbeddingSwitchStatus"
import { ModelStepCard } from "./ModelStepCard"
import { ModelsPage } from "./ModelsPage"

const originalLocale = getLocale()
afterEach(() => {
  setLocale(originalLocale)
  setAdminSession(null)
})

function page() {
  return renderToStaticMarkup(
    <MemoryRouter>
      <WorkspaceContext.Provider
        value={{ revision: 0, refresh: () => {}, health: null, connectionError: null, notify: () => {} }}
      >
        <ModelsPage />
      </WorkspaceContext.Provider>
    </MemoryRouter>,
  )
}

const embed: StepModel = {
  step: "embed", provider: "ollama", model: "nomic-embed-text", options: {}, source: "admin",
  updated_at: "2026-11-12T10:00:00+03:00", updated_by: "Sara", locality: "local", status: "ready",
  status_detail: null, requirements: ["embedding"], providers: ["openrouter", "ollama"],
}

it("asks for the admin token before showing models", () => {
  setLocale("en")
  const html = page()
  expect(html).toContain("Unlock admin settings")
  expect(html).toContain("Admin token")
  expect(html).not.toContain("Lock admin settings")
})

it("shows the lock button and loads models once unlocked", () => {
  setLocale("en")
  setAdminSession({ token: "secret", name: "Sara" })
  const html = page()
  expect(html).toContain("Lock admin settings")
  expect(html).not.toContain("Unlock admin settings")
})

it("disables the embed change button while a switch runs", () => {
  setLocale("en")
  const html = renderToStaticMarkup(<ModelStepCard value={embed} disabled onChange={() => {}} />)
  expect(html).toContain("nomic-embed-text")
  expect(html).toContain("Set by Sara")
  expect(html).toMatch(/<button[^>]*disabled/)
})

it("shows switch progress and failed documents", () => {
  setLocale("ar")
  const value: EmbeddingSwitch = {
    id: 1, status: "completed_with_errors", total: 3, done: 3, failed_document_ids: [7], error: null,
    target: { provider: "ollama", model: "nomic-embed-text", options: {} },
    previous: { provider: "openrouter", model: "openai/text-embedding-3-small", options: {} },
    started_by: "Sara", started_at: "2026-11-12T10:00:00+03:00", finished_at: "2026-11-12T10:01:00+03:00",
  }
  const html = renderToStaticMarkup(<EmbeddingSwitchStatus value={value} />)
  expect(html).toContain("تم تبديل نموذج التضمين مع فشل بعض المستندات")
  expect(html).toContain("أُعيدت فهرسة 3 من 3 مستند")
  expect(html).toContain("7")
})
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `npm test -- src/features/admin/ModelsPage.test.tsx`
Expected: FAIL with unresolved imports.

- [ ] **Step 3: Implement the components**

`employee-frontend/src/features/admin/AdminUnlock.tsx`:

```tsx
import { useState, type FormEvent } from "react"
import { KeyRound } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { setAdminSession } from "@/lib/admin-session"
import { adminApi } from "@/lib/api"
import { useCopy } from "@/lib/locale"
import { adminErrorMessage } from "./admin-errors"

export function AdminUnlock() {
  const text = useCopy().models
  const [name, setName] = useState("")
  const [token, setToken] = useState("")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const ready = name.trim() !== "" && token.trim() !== ""

  async function unlock(event: FormEvent) {
    event.preventDefault()
    if (!ready || busy) return
    setBusy(true)
    setError("")
    try {
      await adminApi.verify(token.trim())
      setAdminSession({ token: token.trim(), name: name.trim() })
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Card className="admin-unlock">
      <CardHeader>
        <CardTitle className="section-title">
          <KeyRound size={18} />
          {text.unlockTitle}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{text.unlockDescription}</p>
        <form className="admin-unlock-form" onSubmit={unlock}>
          <label className="model-field">
            {text.nameLabel}
            <Input value={name} onChange={(e) => setName(e.target.value)} autoComplete="name" maxLength={64} />
          </label>
          <label className="model-field">
            {text.tokenLabel}
            <Input type="password" value={token} onChange={(e) => setToken(e.target.value)} autoComplete="current-password" />
          </label>
          {error && <p className="error-text" role="alert">{error}</p>}
          <Button type="submit" disabled={!ready || busy}>
            {busy ? text.unlocking : text.unlock}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```

`employee-frontend/src/features/admin/ModelStepCard.tsx`:

```tsx
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { dateLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { StepModel } from "@/lib/types"

export function ModelStepCard({
  value,
  disabled,
  onChange,
}: {
  value: StepModel
  disabled: boolean
  onChange: () => void
}) {
  const text = useCopy().models
  return (
    <Card className="model-card">
      <CardHeader>
        <CardTitle className="section-title">
          {text.steps[value.step]}
          <Badge variant={value.locality === "local" ? "secondary" : "outline"}>
            {text.locality[value.locality]}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="field-help">{text.stepHelp[value.step]}</p>
        <div className="model-current">
          <span className="muted small" dir="ltr">{value.provider}</span>
          <strong dir="ltr">{value.model}</strong>
        </div>
        <p className={`model-status status-${value.status}`}>
          {text.status[value.status]}
          {value.status_detail ? ` · ${value.status_detail}` : ""}
        </p>
        <p className="muted small">
          {value.source === "admin" && value.updated_at
            ? fill(text.sourceAdmin, { name: value.updated_by ?? "", date: dateLabel(value.updated_at) })
            : text.sourceEnv}
        </p>
        <Button variant="outline" onClick={onChange} disabled={disabled}>
          {text.change}
        </Button>
      </CardContent>
    </Card>
  )
}
```

`employee-frontend/src/features/admin/AuditList.tsx`:

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { dateLabel } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { AuditEntry } from "@/lib/types"

export function AuditList({ items, error }: { items: AuditEntry[]; error: string | null }) {
  const text = useCopy().models
  return (
    <Card className="audit-card">
      <CardHeader>
        <CardTitle>{text.auditTitle}</CardTitle>
      </CardHeader>
      <CardContent>
        {error && <p className="error-text">{error}</p>}
        {!error && items.length === 0 && <p className="muted small">{text.auditEmpty}</p>}
        {items.length > 0 && (
          <ul className="audit-list">
            {items.map((item) => (
              <li key={item.id}>
                <strong>{text.steps[item.step]}</strong>
                <span dir="ltr">
                  {item.previous ? `${item.previous.provider}:${item.previous.model}` : "—"} →{" "}
                  {item.current.provider}:{item.current.model}
                </span>
                <span className="muted small">
                  {fill(text.auditBy, { name: item.changed_by, date: dateLabel(item.changed_at) })}
                </span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
```

`employee-frontend/src/features/admin/EmbeddingSwitchStatus.tsx`:

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { fill, useCopy } from "@/lib/locale"
import type { EmbeddingSwitch } from "@/lib/types"

export function EmbeddingSwitchStatus({ value }: { value: EmbeddingSwitch }) {
  const text = useCopy().models
  const progress = value.total ? Math.round((value.done / value.total) * 100) : 100
  const title = {
    running: text.switchRunning,
    completed: text.switchDone,
    completed_with_errors: text.switchErrors,
    failed: text.switchFailed,
  }[value.status]
  return (
    <Card className="switch-card" role="status">
      <CardContent>
        <h2>{title}</h2>
        <p dir="ltr">
          {value.previous.model} → {value.target.model}
        </p>
        <p>{fill(text.switchProgress, { done: value.done, total: value.total })}</p>
        <div
          className="run-progress"
          role="progressbar"
          aria-label={text.switchTitle}
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <span style={{ width: `${progress}%` }} />
        </div>
        {value.failed_document_ids.length > 0 && (
          <p className="error-text">
            {fill(text.switchFailedDocs, { ids: value.failed_document_ids.join(", ") })}
          </p>
        )}
        {value.error && <p className="error-text">{value.error}</p>}
      </CardContent>
    </Card>
  )
}
```

`employee-frontend/src/features/admin/ModelsPage.tsx`:

```tsx
import { useState } from "react"
import { Lock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ErrorState, LoadingState, PageHeader } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { setAdminSession, useAdminSession, type AdminSession } from "@/lib/admin-session"
import { adminRequest } from "@/lib/api"
import { useCopy } from "@/lib/locale"
import type { AuditEntry, EmbeddingSwitch, StepModel } from "@/lib/types"
import { useWorkspace } from "@/lib/workspace"
import { AdminUnlock } from "./AdminUnlock"
import { AuditList } from "./AuditList"
import { ChangeModelDialog } from "./ChangeModelDialog"
import { EmbeddingSwitchStatus } from "./EmbeddingSwitchStatus"
import { ModelStepCard } from "./ModelStepCard"

export function ModelsPage() {
  const text = useCopy().models
  const session = useAdminSession()
  return (
    <>
      <PageHeader title={text.title} description={text.description}>
        {session && (
          <Button variant="outline" onClick={() => setAdminSession(null)}>
            <Lock size={15} />
            {text.lock}
          </Button>
        )}
      </PageHeader>
      {session ? <UnlockedModels session={session} /> : <AdminUnlock />}
    </>
  )
}

function UnlockedModels({ session }: { session: AdminSession }) {
  const workspace = useWorkspace()
  const [revision, setRevision] = useState(0)
  const [editing, setEditing] = useState<StepModel | null>(null)
  const models = useResource<{ steps: StepModel[] }>("/models", revision, 0, adminRequest)
  const audit = useResource<{ items: AuditEntry[] }>("/models/audit?limit=50", revision, 0, adminRequest)
  // One-row status read, polled like RunDetailPage polls its run.
  const embedSwitch = useResource<EmbeddingSwitch | null>("/models/embed/switch", revision, 3000, adminRequest)
  const switching = embedSwitch.data?.status === "running"
  if (models.error) return <ErrorState message={models.error} retry={models.reload} />
  if (!models.data) return <LoadingState />
  return (
    <>
      {embedSwitch.data && <EmbeddingSwitchStatus value={embedSwitch.data} />}
      <div className="models-grid">
        {models.data.steps.map((step) => (
          <ModelStepCard
            key={step.step}
            value={step}
            disabled={step.step === "embed" && switching}
            onChange={() => setEditing(step)}
          />
        ))}
      </div>
      <AuditList items={audit.data?.items ?? []} error={audit.error} />
      {editing && (
        <ChangeModelDialog
          step={editing}
          changedBy={session.name}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null)
            setRevision((value) => value + 1)
            workspace.refresh()
          }}
        />
      )}
    </>
  )
}
```

The embed card already shows the new model when a switch starts (the backend saves the setting first), so only the status card needs polling.

Append to `employee-frontend/src/styles/workspace.css`:

```css
.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.model-current {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 10px 0;
}
.model-status {
  font-size: 12px;
}
.model-status.status-ready {
  color: var(--green);
}
.model-status.status-missing_key,
.model-status.status-unreachable {
  color: var(--destructive);
}
.admin-unlock {
  max-width: 460px;
}
.admin-unlock-form {
  display: grid;
  gap: 12px;
  margin-top: 12px;
}
.switch-card,
.audit-card {
  margin-bottom: 20px;
}
.audit-list {
  display: grid;
  gap: 8px;
  list-style: none;
  padding: 0;
  margin: 0;
}
.audit-list li {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 13px;
}
```

- [ ] **Step 4: Add the route and the sidebar entry**

`employee-frontend/src/App.tsx`: add with the other lazy imports

```tsx
const ModelsPage = lazy(() =>
  import("@/features/admin/ModelsPage").then((module) => ({
    default: module.ModelsPage,
  }))
)
```

and the route `<Route path="admin/models" element={<ModelsPage />} />` before the `*` route.

`employee-frontend/src/components/layout/WorkspaceLayout.tsx`:
- Add `SlidersHorizontal` to the lucide import.
- Below `navigation`, add:

```tsx
const adminNavigation = [{ to: "/admin/models", key: "models", icon: SlidersHorizontal }] as const
```

- Change the `current` lookup to search both lists:

```tsx
  const current = [...navigation, ...adminNavigation].find(
    (item) => item.to !== "/" && location.pathname.startsWith(item.to)
  )
```

- After the closing `</nav>` of the main navigation, add:

```tsx
        <div className="nav-section-label">{copy.layout.adminSection}</div>
        <nav aria-label={copy.layout.adminSection}>
          {adminNavigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setMenu(false)}
              className={({ isActive }) => `nav-item ${isActive ? "nav-active" : ""}`}
            >
              <item.icon size={18} strokeWidth={1.7} />
              <span>{copy.nav[item.key]}</span>
            </NavLink>
          ))}
        </nav>
```

- [ ] **Step 5: Run tests, lint and build**

Run: `npm test`
Expected: PASS.

Run: `npm run lint && npm run build`
Expected: both exit 0.

- [ ] **Step 6: Manual check against the running backend**

With the backend plan implemented, `ADMIN_TOKEN` set and the API running on port 8000, run `npm run dev` and open `http://localhost:5173/admin/models`:

1. The page shows the unlock form; a wrong token shows "That admin token is not correct."
2. After unlocking, five cards appear in pipeline order with **Default from the backend .env file**.
3. **Change model** on Reply drafting → Ollama tab lists `qwen3:4b` (with Ollama reachable) → turn thinking off → **Test model** passes → **Save**. The card shows **Local** and **Set by …**, the top bar shows **AI: Mixed**, and the history lists the change.
4. Change a field after a passing test: **Save** becomes disabled until you test again.
5. Switch to Arabic: labels are Arabic, the layout is right-to-left, and `qwen3:4b` still reads left-to-right.

- [ ] **Step 7: Commit**

```bash
git add src
git commit -m "feat(admin): add the AI models admin page"
```
