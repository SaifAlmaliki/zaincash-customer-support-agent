# Customer Frontend Maintainability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove reference-verified customer-frontend dead code, make verification meaningful, harden runtime/persisted contracts, and fix the approved upload/controller/chat defects without changing product behavior or appearance.

**Architecture:** Begin with reference-verified cleanup, then make mechanical test/configuration moves, and finally apply TDD defect fixes. A dependency-free intake contract module will own API and persisted-data guards; a focused `useIntakeUploads` hook will own client-keyed preview/upload sequencing while `IntakeController` retains request identity, revisions, and server communication. Existing `AgentChat` internals and current UI structure remain intact except for the approved Stop-button guard.

**Tech Stack:** TypeScript 6, React 19, Vite 8, Vitest 5, Testing Library, npm workspaces, Turbo 2, ESLint 10.

**Spec:** `docs/superpowers/specs/2026-11-02-maintainability-refactor-design.md`

## Global Constraints

- Perform a targeted maintainability pass across the repository. Remove reference-verified dead code, correct confirmed defects, and extract modules only where a clear responsibility boundary already exists. Preserve the current product, visual design, public compatibility contracts, and historical records.
- The user selected a **targeted full pass** and a **cleanup-first sweep**. Safe generated-artifact cleanup is included; old Archify provenance working sets and historical records are excluded from deletion.
- Use a cleanup-first sweep with the recorded baseline as the comparison point:
  1. Remove confirmed dead code and safe stale artifacts.
  2. Perform mechanical, behavior-preserving modularization.
  3. Fix baseline failures and selected confirmed defects with regression tests.
  4. Repair current documentation and regenerate current Graphify outputs.
  5. Run focused checks for each slice, full subsystem checks after each subsystem, and the complete verification matrix at the end.
- Until baseline repair, intermediate verification may show only the three documented backend failures and two documented employee TypeScript errors. Any additional failure is a regression and must be resolved before continuing.
- No git commits or other git mutations are part of this design.
- This pass does not:
  - Rewrite the pipeline, intake architecture, API, or frontend applications.
  - Change visual styling or user flows.
  - Reformat unrelated files or make stylistic changes without a maintainability purpose.
  - Split cohesive functions merely because of line count; `RagDrafter.draft`, `build_tools`, and `AgentChat` internals remain intact unless required by an approved change.
  - Remove public compatibility fields such as `fallback_rate`, `classifier_paths`, or `ClassifierOutput.degraded`.
  - Broaden JSONL parsing, weaken TypeScript contracts, or add type-suppression comments.
  - Add a runtime schema-validation library to the customer frontend.
  - Perform broad localization consolidation or extract `ReviewEditor` in this pass.
  - Optimize every database N+1 pattern; only the result-list work specified below is included.
  - Delete historical material merely because it mentions retired cascade behavior.
  - Delete generated UI primitive exports solely because they currently lack local consumers.
- Existing HTTP status codes, public messages, optimistic-concurrency protections, idempotency keys, revision rules, and safe secret-free responses remain unchanged unless a defect fix explicitly requires otherwise.
- Model and tool execution limits remain in place. The Jev retry change prevents duplicate paid sibling calls rather than adding another retry layer.
- Database changes are limited to query/initialization behavior; no new schema or migration framework is introduced.
- Frontend runtime validation rejects malformed server or persisted data through the existing error paths rather than allowing invalid typed state to propagate.
- Upload failure behavior remains sequential and stop-on-first-failure; only stale preview handling and identity are corrected.
- Dependency removal must be followed by lockfile regeneration and complete builds to catch transitive or tooling assumptions.
- Run focused regression tests before and after each defect fix, then run the relevant full subsystem checks.
- The root and workspace test commands must execute the same web suite. Typechecking must include application, tests, and Vite/Vitest configuration.
- Finish with a complete diff and status review. Only intended source, test, configuration, documentation, lockfile, and current generated-output changes are acceptable. No secret values or unrelated user changes may be included.

## Review Focus

- **Non-finite nested numbers:** attachment `size`, `width`, or `height` containing `NaN`/infinity must be rejected as `invalid_response`, not admitted into typed state; owned by `contracts.test.ts` in Task 5.
- **Ambiguous legacy request identity:** a persisted operation whose legacy outer `request_id` disagrees with `payload.request_id` must be rejected rather than replayed; owned by `session.test.ts` in Task 5.
- **Indistinguishable repeated selections:** two different `File` objects with the same name and bytes must still receive distinct client IDs and independent progress; owned by `useIntakeUploads.test.tsx` in Task 6.
- **Unmount during sequential upload:** unmounting with later files still queued must revoke every outstanding object URL and must not start the later upload when the active request resolves; owned by `useIntakeUploads.test.tsx` in Task 6.
- **Compounded reset/storage failure:** if `storage.clear()` and new-session creation both fail, the final state must still report `RESUME_UNAVAILABLE` without exposing credentials; owned by `controller.test.ts` in Task 7.

---

### Task 1: Cleanup-first removal of reference-verified dead code and dependencies

**Files:**
- Create: No new files.
- Modify: `users-frontend/apps/web/src/features/intake/controller.ts`, `users-frontend/apps/web/src/components/theme-provider.tsx`, `users-frontend/apps/web/src/components/ui/agent-chat.tsx`, `users-frontend/apps/web/package.json`, `users-frontend/packages/ui/package.json`, `users-frontend/package-lock.json`
- Test: `users-frontend/apps/web/src/features/intake/controller.test.ts`, `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`

**Interfaces:**
- Consumes: Existing `IntakeController.retry()`, `ThemeProvider`, named `AgentChat` import, and npm workspace dependency graph.
- Produces: The same public runtime interfaces minus the unreachable private retry path, unused `useTheme` export, redundant default `AgentChat` export, and unused direct dependencies.

- [ ] **Step 1: Repeat reference searches before deleting anything**

Run from the repository root:

```bash
rg -n "useTheme|import AgentChat|@hugeicons|from [\"']zod[\"']|@turbo/gen|@tailwindcss/vite" users-frontend/apps users-frontend/packages --glob '!**/node_modules/**'
rg -n "retryable_failure" users-frontend/apps/web/src/features/intake/controller.ts
```

Expected: `useTheme` occurs only at its definition; no default `AgentChat` import exists; Hugeicons and direct UI `zod` have no source imports; UI has no `@tailwindcss/vite` or `@turbo/gen` consumer. Web retains its own `@tailwindcss/vite` import in `apps/web/vite.config.ts`. The two adjacent retryable-failure branches are visible at `controller.ts:327-350`.

- [ ] **Step 2: Remove only the confirmed dead TypeScript exports and branch**

Delete `controller.ts:345-350`, leaving this as the end of `retryNow()`:

```ts
    if (this.pending?.kind === "review") {
      const command = this.pending.payload as ReviewCommand
      return this.reviewNow(command.allow_partial, command.language)
    }
  }
```

Delete the complete `useTheme` block from `theme-provider.tsx`, leaving `ThemeProvider` as the only export and ending the file after its closing brace:

```tsx
  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}
```

Keep the named `export const AgentChat = memo(...)` declaration and delete only this final line:

```diff
-export default AgentChat
```

- [ ] **Step 3: Remove the approved direct dependencies without disturbing retained packages**

The resulting web dependency block must be:

```json
  "dependencies": {
    "@workspace/ui": "*",
    "clsx": "^2.1.1",
    "react": "^19.3.0",
    "react-dom": "^19.3.0",
    "tailwind-merge": "^3.7.0"
  },
```

The resulting UI dependency blocks must be:

```json
  "dependencies": {
    "@base-ui/react": "^1.9.0",
    "@fontsource-variable/plus-jakarta-sans": "^5.3.0",
    "@fontsource/tajawal": "^5.3.0",
    "class-variance-authority": "^0.7.1",
    "cn": "^0.5.0",
    "react": "^19.3.0",
    "react-dom": "^19.3.0",
    "shadcn": "^4.22.0",
    "tw-animate-css": "^1.4.0"
  },
  "devDependencies": {
    "@eslint/js": "^10",
    "@types/node": "^24",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "eslint": "^10",
    "eslint-plugin-react-hooks": "^7.1.1",
    "eslint-plugin-react-refresh": "^0.5.7",
    "globals": "^17",
    "tailwindcss": "^4",
    "typescript": "~6.0.2",
    "typescript-eslint": "^8"
  }
```

Do not remove the web `@tailwindcss/vite` entry, CSS-imported fonts, `shadcn`, or `tw-animate-css`.

- [ ] **Step 4: Regenerate the lockfile through npm**

Run:

```bash
cd users-frontend
npm install --package-lock-only --ignore-scripts
```

Expected: npm exits 0; root lockfile workspace entries no longer list web/UI Hugeicons, direct UI `zod`, UI `@tailwindcss/vite`, or UI `@turbo/gen`. Transitive packages required by retained dependencies may remain.

- [ ] **Step 5: Run focused regression checks and review the cleanup diff**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/controller.test.ts src/features/intake/IntakePage.test.tsx
npm run build
git diff --check -- apps/web/src/features/intake/controller.ts apps/web/src/components/theme-provider.tsx apps/web/src/components/ui/agent-chat.tsx apps/web/package.json packages/ui/package.json package-lock.json
git diff -- apps/web/src/features/intake/controller.ts apps/web/src/components/theme-provider.tsx apps/web/src/components/ui/agent-chat.tsx apps/web/package.json packages/ui/package.json package-lock.json
```

Expected: all focused tests and the production build pass; diff check is silent; the diff contains only the approved cleanup and lockfile regeneration.

### Task 2: Make standalone typechecking and root test execution real

**Files:**
- Create: No new files.
- Modify: `users-frontend/apps/web/package.json`, `users-frontend/apps/web/tsconfig.node.json`, `users-frontend/package.json`, `users-frontend/turbo.json`
- Test: Existing web suite through root and workspace commands.

**Interfaces:**
- Consumes: Existing `web.test = "vitest run"`, referenced app/node TypeScript projects, and Turbo workspace graph.
- Produces: `npm test -> turbo test -> web/vitest run`, `npm --workspace web run typecheck -> tsc -b`, and node-project inclusion of both Vite and Vitest configs.

- [ ] **Step 1: Apply the mechanical script and project-include changes**

Set the web script exactly as follows while retaining every other script:

```json
    "typecheck": "tsc -b",
```

Set the node project include exactly as follows:

```json
  "include": ["vite.config.ts", "vitest.config.ts"]
```

Add the root script in `users-frontend/package.json`:

```json
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "format": "turbo format",
    "typecheck": "turbo typecheck",
    "test": "turbo test"
  },
```

Add the Turbo task alongside the existing tasks:

```json
    "test": {
      "dependsOn": ["^test"]
    },
```

- [ ] **Step 2: Prove the standalone typechecker includes source, tests, and both configs**

Run:

```bash
cd users-frontend
npm run typecheck
npm --workspace web exec tsc -- -b --listFiles
```

Expected: both commands exit 0. The second command's file list includes `apps/web/src/main.tsx`, all three existing intake test files, `apps/web/vite.config.ts`, and `apps/web/vitest.config.ts`; it is not empty.

- [ ] **Step 3: Prove root and workspace commands execute the same suite and review the diff**

Run:

```bash
cd users-frontend
npm test
npm --workspace web test
git diff --check -- package.json turbo.json apps/web/package.json apps/web/tsconfig.node.json
git diff -- package.json turbo.json apps/web/package.json apps/web/tsconfig.node.json
```

Expected: both test commands run the same web test files and pass with identical test totals; diff check is silent; only the four approved configuration edits appear.

### Task 3: Centralize test cleanup and shared intake fixtures mechanically

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/test/fixtures.ts`
- Modify: `users-frontend/apps/web/src/test/setup.ts`, `users-frontend/apps/web/src/features/intake/controller.test.ts`, `users-frontend/apps/web/src/features/intake/IntakePage.test.tsx`, `users-frontend/apps/web/src/features/intake/api.test.ts`
- Test: All three existing intake test files.

**Interfaces:**
- Consumes: Existing `IntakeApi`, `SessionView`, `CustomerReview`, `Attachment`, and Vitest global-stub/fake-timer APIs.
- Produces: `emptySession(overrides?: Partial<SessionView>): SessionView`, `review: CustomerReview`, `attachment: Attachment`, and `fakeApi(overrides?: Partial<SessionView>): IntakeApi` for all intake tests.

- [ ] **Step 1: Capture the pre-move focused baseline**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/api.test.ts src/features/intake/controller.test.ts src/features/intake/IntakePage.test.tsx
```

Expected: every existing intake test passes before fixture movement.

- [ ] **Step 2: Create the shared fixture module with the union of current fake behavior**

Create `test/fixtures.ts` with:

```ts
import { vi } from "vitest"
import type { IntakeApi } from "../api"
import type { Attachment, CustomerReview, SessionView } from "../types"

export function emptySession(overrides: Partial<SessionView> = {}): SessionView {
  return {
    id: "session-1",
    revision: 1,
    phase: "collecting",
    language: "en",
    turn_status: "idle",
    active_request_id: null,
    messages: [],
    attachments: [],
    readiness: {
      quality: "collecting",
      missing: [],
      conflicts: [],
      reason: "Waiting",
      next_key: null,
    },
    review: null,
    receipt: null,
    error_code: null,
    ...overrides,
  }
}

export const review: CustomerReview = {
  id: "review-1",
  revision: 2,
  language: "en",
  quality: "partial_context",
  text: "The transfer failed.",
  facts: {
    amount: {
      key: "amount",
      status: "unknown",
      value: null,
      normalized: null,
      evidence: [],
    },
  },
  additional_issues: [],
  unknown_keys: ["amount"],
  attachment_ids: [],
}

export const attachment: Attachment = {
  id: "att-1",
  filename: "error.png",
  mime_type: "image/png",
  size: 2,
  width: 1,
  height: 1,
  message_id: null,
  removed: false,
}

export function fakeApi(overrides: Partial<SessionView> = {}): IntakeApi {
  const session = emptySession(overrides)
  return {
    create: vi.fn(async () => ({
      credentials: { session_id: "session-1", token: "secret-token" },
      session,
    })),
    get: vi.fn(async () => session),
    message: vi.fn(async () => session),
    review: vi.fn(async (_credentials, command): Promise<SessionView> =>
      emptySession({
        ...session,
        language: command.language,
        review: { ...review, language: command.language },
      }),
    ),
    retry: vi.fn(async () => session),
    submit: vi.fn(async () => ({
      ticket_reference: "INTAKE-demo",
      submitted_at: "2026-10-18T09:00:00Z",
      processing_status: "processing" as const,
    })),
    upload: vi.fn(async () => ({
      attachment,
      session: emptySession({
        ...session,
        revision: session.revision + 1,
        attachments: [attachment],
      }),
    })),
    remove: vi.fn(async () =>
      emptySession({
        ...session,
        attachments: [{ ...attachment, removed: true }],
      }),
    ),
    image: vi.fn(async () => new Blob(["png"])),
  }
}
```

- [ ] **Step 3: Replace duplicated local fixtures with the shared imports**

In `controller.test.ts`, replace its local `emptySession`, `fakeApi`, and `review` definitions with:

```ts
import { emptySession, fakeApi, review } from "./test/fixtures"
```

Retain the existing type-only `SessionView` import because deferred promises still use it.

In `IntakePage.test.tsx`, replace its local `emptySession`, `review`, `attachment`, and `fakeApi` definitions with:

```ts
import {
  attachment,
  emptySession,
  fakeApi,
  review,
} from "./test/fixtures"
```

Remove the now-unused `Attachment` and `CustomerReview` names from its type import, leaving:

```ts
import type { SessionView } from "./types"
```

In `api.test.ts`, replace the hand-written `SessionView` constant and its now-unused type import with:

```ts
import { emptySession } from "./test/fixtures"

const session = emptySession()
```

- [ ] **Step 4: Centralize global stub, mock, and fake-timer restoration**

Make `src/test/setup.ts` exactly:

```ts
import { afterEach, vi } from "vitest"
import { cleanup } from "@testing-library/react"
import "@testing-library/jest-dom/vitest"

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
  vi.useRealTimers()
})
```

Remove the manual end-of-test cleanup statements now owned by the hook:

```diff
-    vi.unstubAllGlobals()
```

```diff
-    vi.useRealTimers()
```

Keep `beforeEach(() => { vi.restoreAllMocks() })` in `IntakePage.test.tsx`; it is orthogonal to the centralized after-each safety net.

- [ ] **Step 5: Run focused tests, typecheck, and review the mechanical diff**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/api.test.ts src/features/intake/controller.test.ts src/features/intake/IntakePage.test.tsx
npm run typecheck
git diff --check -- apps/web/src/test/setup.ts apps/web/src/features/intake
git diff -- apps/web/src/test/setup.ts apps/web/src/features/intake/test/fixtures.ts apps/web/src/features/intake/api.test.ts apps/web/src/features/intake/controller.test.ts apps/web/src/features/intake/IntakePage.test.tsx
```

Expected: the same tests pass, typecheck passes, diff check is silent, and production behavior files are absent from this task's diff.

### Task 4: Make pending operations discriminated and use one request identity

**Files:**
- Create: No new files.
- Modify: `users-frontend/apps/web/src/features/intake/types.ts`, `users-frontend/apps/web/src/features/intake/controller.ts`, `users-frontend/apps/web/src/features/intake/controller.test.ts`
- Test: `users-frontend/apps/web/src/features/intake/controller.test.ts`

**Interfaces:**
- Consumes: Existing `MessageCommand`, `ReviewCommand`, `SubmitCommand`, `SavedSession`, and shared fixtures.
- Produces: A discriminated `PendingOperation` whose only request identity is `pending.payload.request_id`; controller retry/send/review/submit paths require no kind/payload casts.

- [ ] **Step 1: Add a failing regression test using the new saved-operation shape**

Add this test to `controller.test.ts`:

```ts
it("uses the payload request ID when retrying an accepted failed message", async () => {
  const payload = {
    request_id: "message-retry-1",
    expected_revision: 1,
    text: "Transfer failed",
    language: "en" as const,
    attachment_ids: [] as string[],
  }
  const storage = memoryStorage({
    credentials: { session_id: "session-1", token: "token" },
    pending: { kind: "message", payload },
  })
  const api = fakeApi()
  vi.mocked(api.get).mockResolvedValue(
    emptySession({
      revision: 2,
      turn_status: "retryable_failure",
      active_request_id: payload.request_id,
    }),
  )
  const controller = new IntakeController(api, storage)
  await controller.initialize("en")

  await controller.retry()

  expect(api.retry).toHaveBeenCalledWith(
    { session_id: "session-1", token: "token" },
    "message-retry-1",
    2,
    expect.any(AbortSignal),
  )
  expect(api.message).not.toHaveBeenCalled()
})
```

Also remove the legacy outer IDs from the two existing saved-operation fixtures so they use the new shape:

```ts
pending: {
  kind: "submit",
  payload: {
    request_id: "saved-request",
    expected_revision: 2,
    review_id: "review-1",
    confirmed: true,
  },
},
```

```ts
pending: { kind: "message", payload },
```

- [ ] **Step 2: Run the new test and confirm the old identity lookup fails**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/controller.test.ts -t "uses the payload request ID"
```

Expected: FAIL because the old controller reads `pending.request_id`, skips `api.retry`, and calls `api.message` instead.

- [ ] **Step 3: Make `PendingOperation` a discriminated union**

Replace the type in `types.ts` with:

```ts
export type PendingOperation =
  | { kind: "message"; payload: MessageCommand }
  | { kind: "review"; payload: ReviewCommand }
  | { kind: "submit"; payload: SubmitCommand }
```

Keep `SavedSession` as:

```ts
export type SavedSession = {
  credentials: Credentials
  pending: PendingOperation | null
}
```

- [ ] **Step 4: Narrow payloads and remove the duplicate request-ID source in the controller**

Use direct narrowing for command reuse in `sendNow`, `reviewNow`, and `submitNow`:

```ts
const command: MessageCommand = this.pending?.kind === "message"
  ? this.pending.payload
  : {
      request_id: crypto.randomUUID(),
      expected_revision: session.revision,
      text,
      language,
      attachment_ids: attachmentIds,
    }
```

```ts
const command: ReviewCommand = this.pending?.kind === "review"
  ? this.pending.payload
  : {
      request_id: crypto.randomUUID(),
      expected_revision: session.revision,
      allow_partial: allowPartial,
      language,
    }
```

```ts
const command: SubmitCommand = this.pending?.kind === "submit"
  ? this.pending.payload
  : {
      request_id: crypto.randomUUID(),
      expected_revision: session.revision,
      review_id: session.review.id,
      confirmed: true,
    }
```

Use the payload ID in retryable-failure detection:

```ts
if (
  session?.turn_status === "retryable_failure" &&
  session.active_request_id &&
  (!this.pending || this.pending.payload.request_id === session.active_request_id)
) {
  await this.dispatch(generation, () =>
    this.api.retry(
      this.credentials!,
      session.active_request_id!,
      session.revision,
      this.nextSignal(),
    ),
  )
  return
}
```

Use narrowed replay payloads without casts:

```ts
if (this.pending?.kind === "message") {
  const command = this.pending.payload
  return this.sendNow(command.text, command.language, command.attachment_ids)
}
if (this.pending?.kind === "review") {
  const command = this.pending.payload
  return this.reviewNow(command.allow_partial, command.language)
}
```

The submit replay remains `return this.submitNow()`, which now obtains its narrowed payload from the union.

- [ ] **Step 5: Run controller tests and typecheck, then review identity-related diff lines**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/controller.test.ts
npm run typecheck
rg -n "pending\\.request_id|payload as (MessageCommand|ReviewCommand|SubmitCommand)" apps/web/src/features/intake || true
git diff --check -- apps/web/src/features/intake/types.ts apps/web/src/features/intake/controller.ts apps/web/src/features/intake/controller.test.ts
git diff -- apps/web/src/features/intake/types.ts apps/web/src/features/intake/controller.ts apps/web/src/features/intake/controller.test.ts
```

Expected: all controller tests and typecheck pass; the reference search prints nothing; diff check is silent; no outer pending request ID or kind/payload cast remains.

### Task 5: Add complete dependency-free API and persisted-session guards

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/contracts.ts`, `users-frontend/apps/web/src/features/intake/contracts.test.ts`, `users-frontend/apps/web/src/features/intake/session.test.ts`
- Modify: `users-frontend/apps/web/src/features/intake/types.ts`, `users-frontend/apps/web/src/features/intake/api.ts`, `users-frontend/apps/web/src/features/intake/session.ts`, `users-frontend/apps/web/src/features/intake/api.test.ts`
- Test: `contracts.test.ts`, `session.test.ts`, `api.test.ts`, and `controller.test.ts`.

**Interfaces:**
- Consumes: `PendingOperation` from Task 4 and existing `IntakeRequestError` behavior with message `"The conversation could not be updated. Try again."` and code `invalid_response`.
- Produces: `IntakeRequestError`, `INTAKE_FALLBACK_MESSAGE`, `parseCredentials(unknown): Credentials`, `parseAttachment(unknown): Attachment`, `parseSession(unknown): SessionView`, `parseReceipt(unknown): Receipt`, and `parseSavedSession(unknown): SavedSession | null`; API re-exports preserve existing test imports.

- [ ] **Step 1: Add table-driven malformed nested-response and credential tests**

Create `contracts.test.ts` with:

```ts
import { describe, expect, it } from "vitest"
import {
  IntakeRequestError,
  parseCredentials,
  parseSession,
} from "./contracts"
import { attachment, emptySession, review } from "./test/fixtures"

const populated = emptySession({
  phase: "review_ready",
  active_request_id: null,
  messages: [
    {
      id: "m1",
      role: "user",
      text: "Transfer failed",
      language: "en",
      created_at: "2026-10-18T09:00:00Z",
      attachment_ids: ["att-1"],
    },
  ],
  attachments: [attachment],
  review: {
    ...review,
    facts: {
      amount: {
        key: "amount",
        status: "known",
        value: "50000",
        normalized: "50000",
        evidence: [{ kind: "message", source_id: "m1", quote: "50000" }],
        supersedes: [],
      },
    },
  },
})

const malformed: Array<[string, unknown]> = [
  ["active request ID", { ...populated, active_request_id: 4 }],
  ["error code", { ...populated, error_code: 4 }],
  ["message language", { ...populated, messages: [{ ...populated.messages[0]!, language: "fr" }] }],
  ["message timestamp", { ...populated, messages: [{ ...populated.messages[0]!, created_at: 4 }] }],
  ["message attachments", { ...populated, messages: [{ ...populated.messages[0]!, attachment_ids: [4] }] }],
  ["readiness quality", { ...populated, readiness: { ...populated.readiness, quality: "ready" } }],
  ["readiness reason", { ...populated, readiness: { ...populated.readiness, reason: 4 } }],
  ["readiness next key", { ...populated, readiness: { ...populated.readiness, next_key: 4 } }],
  ["review revision", { ...populated, review: { ...populated.review!, revision: "2" } }],
  ["review language", { ...populated, review: { ...populated.review!, language: "fr" } }],
  ["review quality", { ...populated, review: { ...populated.review!, quality: "collecting" } }],
  ["required fact value", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, value: undefined } } } }],
  ["required fact evidence", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, evidence: undefined } } } }],
  ["fact evidence entry", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, evidence: [{}] } } } }],
  ["fact supersedes entry", { ...populated, review: { ...populated.review!, facts: { amount: { ...populated.review!.facts.amount!, supersedes: [{}] } } } }],
  ["additional issue", { ...populated, review: { ...populated.review!, additional_issues: [{}] } }],
]

describe("intake runtime contracts", () => {
  it.each(malformed)("rejects malformed %s", (_name, value) => {
    expect(() => parseSession(value)).toThrow(IntakeRequestError)
    expect(() => parseSession(value)).toThrow(/could not be updated/i)
  })

  it.each([Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY])(
    "rejects non-finite nested attachment number %s",
    (number) => {
      for (const key of ["size", "width", "height"] as const) {
        const parse = () =>
          parseSession({
            ...populated,
            attachments: [{ ...attachment, [key]: number }],
          })
        expect(parse).toThrow(IntakeRequestError)
        expect(parse).toThrow(expect.objectContaining({ code: "invalid_response" }))
      }
    },
  )

  it.each([
    { session_id: 1, token: "token" },
    { session_id: "session-1", token: {} },
    { session_id: "", token: "token" },
    { session_id: "session-1", token: "" },
  ])("rejects invalid credentials %#", (value) => {
    expect(() => parseCredentials(value)).toThrow(IntakeRequestError)
  })

  it("accepts the fully populated valid session", () => {
    expect(parseSession(populated)).toEqual(populated)
  })
})
```

Add this API integration test to `api.test.ts`:

```ts
it("rejects non-string create credentials before returning typed state", async () => {
  const fetchMock = vi.fn(async () =>
    jsonResponse({
      credentials: { session_id: 7, token: "secret-token" },
      session,
    }),
  )
  vi.stubGlobal("fetch", fetchMock)
  const api = createIntakeApi("http://intake.test/api/intake")

  await expect(api.create("en")).rejects.toBeInstanceOf(IntakeRequestError)
})
```

- [ ] **Step 2: Add corrupted-storage, mismatched-payload, request-ID, and valid-replay tests**

Create `session.test.ts` with:

```ts
import { describe, expect, it } from "vitest"
import { browserSessionStorage } from "./session"
import type { SavedSession } from "./types"

function storageWith(raw: string | null): Storage {
  return {
    length: 0,
    clear: () => undefined,
    getItem: () => raw,
    key: () => null,
    removeItem: () => undefined,
    setItem: () => undefined,
  }
}

const credentials = { session_id: "session-1", token: "token" }
const messagePayload = {
  request_id: "message-1",
  expected_revision: 1,
  text: "Transfer failed",
  language: "en" as const,
  attachment_ids: [] as string[],
}

const invalidValues: Array<[string, unknown]> = [
  ["null", null],
  ["array", []],
  ["missing token", { credentials: { session_id: "session-1" }, pending: null }],
  ["mismatched kind and payload", { credentials, pending: { kind: "message", payload: { request_id: "submit-1", expected_revision: 1, review_id: "review-1", confirmed: true } } }],
  ["conflicting legacy request ID", { credentials, pending: { kind: "message", request_id: "other-id", payload: messagePayload } }],
  ["invalid revision", { credentials, pending: { kind: "message", payload: { ...messagePayload, expected_revision: -1 } } }],
]

describe("browser session storage", () => {
  it.each(invalidValues)("rejects %s", (_name, value) => {
    const storage = browserSessionStorage(storageWith(JSON.stringify(value)))
    expect(storage.load()).toBeNull()
  })

  it("returns null for malformed JSON", () => {
    expect(browserSessionStorage(storageWith("{")).load()).toBeNull()
  })

  it("accepts and replays a valid pending operation", () => {
    const saved: SavedSession = {
      credentials,
      pending: { kind: "message", payload: messagePayload },
    }
    const storage = browserSessionStorage(storageWith(JSON.stringify(saved)))
    expect(storage.load()).toEqual(saved)
  })

  it("accepts a legacy outer ID only when it equals the payload ID", () => {
    const storage = browserSessionStorage(storageWith(JSON.stringify({
      credentials,
      pending: { kind: "message", request_id: "message-1", payload: messagePayload },
    })))
    expect(storage.load()).toEqual({
      credentials,
      pending: { kind: "message", payload: messagePayload },
    })
  })
})
```

- [ ] **Step 3: Run the new tests to confirm missing contracts fail**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/contracts.test.ts src/features/intake/session.test.ts src/features/intake/api.test.ts -t "rejects|accepts|returns null|non-string"
```

Expected: FAIL because `contracts.ts` does not exist and browser storage still casts arbitrary JSON.

- [ ] **Step 4: Make the `Fact` runtime-required fields match the type**

Change only these two fields in `types.ts`:

```ts
export type Fact = {
  key: string
  status: "known" | "missing" | "unknown" | "conflicting" | "not_applicable"
  value: string | null
  normalized?: string | null
  evidence: EvidenceRef[]
  supersedes?: EvidenceRef[]
}
```

The shared `review.facts.amount` fixture from Task 3 already contains `value: null` and `evidence: []`; no fixture change is needed for this type correction.

- [ ] **Step 5: Implement the complete contract module without a new dependency**

Create `contracts.ts` with:

```ts
import type {
  Attachment,
  Credentials,
  EvidenceRef,
  Fact,
  Language,
  MessageCommand,
  PendingOperation,
  Receipt,
  ReviewCommand,
  SavedSession,
  SessionView,
  SubmitCommand,
} from "./types"

export const INTAKE_FALLBACK_MESSAGE =
  "The conversation could not be updated. Try again."

export class IntakeRequestError extends Error {
  readonly status: number
  readonly code: string

  constructor(message: string, status: number, code: string) {
    super(message)
    this.name = "IntakeRequestError"
    this.status = status
    this.code = code
  }
}

function invalid(): never {
  throw new IntakeRequestError(INTAKE_FALLBACK_MESSAGE, 200, "invalid_response")
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value)
}

function stringList(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string")
}

function nullableString(value: unknown): boolean {
  return value === null || typeof value === "string"
}

function finiteNonnegative(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value) && value >= 0
}

function revision(value: unknown): value is number {
  return typeof value === "number" && Number.isInteger(value) && value >= 0
}

function language(value: unknown): value is Language {
  return value === "ar" || value === "en"
}

function validEvidence(value: unknown): value is EvidenceRef {
  return isRecord(value) &&
    (value.kind === "message" || value.kind === "image") &&
    typeof value.source_id === "string" &&
    typeof value.quote === "string"
}

function validEvidenceList(value: unknown): value is EvidenceRef[] {
  return Array.isArray(value) && value.every(validEvidence)
}

function validFact(value: unknown): value is Fact {
  return isRecord(value) &&
    typeof value.key === "string" &&
    ["known", "missing", "unknown", "conflicting", "not_applicable"].includes(String(value.status)) &&
    nullableString(value.value) &&
    (value.normalized === undefined || nullableString(value.normalized)) &&
    validEvidenceList(value.evidence) &&
    (value.supersedes === undefined || validEvidenceList(value.supersedes))
}

function validAttachment(value: unknown): value is Attachment {
  return isRecord(value) &&
    typeof value.id === "string" &&
    typeof value.filename === "string" &&
    ["image/png", "image/jpeg", "image/webp"].includes(String(value.mime_type)) &&
    finiteNonnegative(value.size) &&
    finiteNonnegative(value.width) &&
    finiteNonnegative(value.height) &&
    typeof value.removed === "boolean" &&
    nullableString(value.message_id)
}

function validMessage(value: unknown): boolean {
  return isRecord(value) &&
    typeof value.id === "string" &&
    typeof value.text === "string" &&
    (value.role === "user" || value.role === "assistant") &&
    language(value.language) &&
    typeof value.created_at === "string" &&
    stringList(value.attachment_ids)
}

function validReadiness(value: unknown): boolean {
  return isRecord(value) &&
    ["collecting", "sufficient_context", "partial_context"].includes(String(value.quality)) &&
    stringList(value.missing) &&
    stringList(value.conflicts) &&
    typeof value.reason === "string" &&
    nullableString(value.next_key)
}

function validReview(value: unknown): boolean {
  return isRecord(value) &&
    typeof value.id === "string" &&
    revision(value.revision) &&
    language(value.language) &&
    (value.quality === "sufficient_context" || value.quality === "partial_context") &&
    typeof value.text === "string" &&
    isRecord(value.facts) &&
    Object.values(value.facts).every(validFact) &&
    Array.isArray(value.additional_issues) &&
    value.additional_issues.every(validFact) &&
    stringList(value.unknown_keys) &&
    stringList(value.attachment_ids)
}

export function parseCredentials(value: unknown): Credentials {
  if (!isRecord(value) || typeof value.session_id !== "string" || !value.session_id ||
      typeof value.token !== "string" || !value.token) invalid()
  return { session_id: value.session_id, token: value.token }
}

export function parseAttachment(value: unknown): Attachment {
  if (!validAttachment(value)) invalid()
  return value
}

export function parseReceipt(value: unknown): Receipt {
  if (!isRecord(value) || typeof value.ticket_reference !== "string" || !value.ticket_reference ||
      typeof value.submitted_at !== "string" || !Number.isFinite(Date.parse(value.submitted_at)) ||
      !["processing", "ready_for_employee", "needs_attention"].includes(String(value.processing_status))) {
    invalid()
  }
  return value as unknown as Receipt
}

export function parseSession(value: unknown): SessionView {
  if (!isRecord(value) || typeof value.id !== "string" || !revision(value.revision) ||
      !["collecting", "review_ready", "submitted"].includes(String(value.phase)) ||
      !language(value.language) ||
      !["idle", "processing", "retryable_failure"].includes(String(value.turn_status)) ||
      !nullableString(value.active_request_id) ||
      !Array.isArray(value.messages) || !value.messages.every(validMessage) ||
      !Array.isArray(value.attachments) || !value.attachments.every(validAttachment) ||
      !validReadiness(value.readiness) ||
      (value.review !== null && !validReview(value.review)) ||
      !nullableString(value.error_code)) {
    invalid()
  }
  if (value.receipt !== null) parseReceipt(value.receipt)
  return value as unknown as SessionView
}

function requestIdentity(value: unknown): value is Record<string, unknown> & {
  request_id: string
  expected_revision: number
} {
  return isRecord(value) && typeof value.request_id === "string" && !!value.request_id &&
    revision(value.expected_revision)
}

function validMessageCommand(value: unknown): value is MessageCommand {
  return requestIdentity(value) && typeof value.text === "string" &&
    language(value.language) && stringList(value.attachment_ids)
}

function validReviewCommand(value: unknown): value is ReviewCommand {
  return requestIdentity(value) && typeof value.allow_partial === "boolean" &&
    language(value.language)
}

function validSubmitCommand(value: unknown): value is SubmitCommand {
  return requestIdentity(value) && typeof value.review_id === "string" &&
    value.confirmed === true
}

function parsePendingOperation(value: unknown): PendingOperation | null {
  if (!isRecord(value)) return null
  if (value.kind === "message" && validMessageCommand(value.payload)) {
    return { kind: "message", payload: value.payload }
  }
  if (value.kind === "review" && validReviewCommand(value.payload)) {
    return { kind: "review", payload: value.payload }
  }
  if (value.kind === "submit" && validSubmitCommand(value.payload)) {
    return { kind: "submit", payload: value.payload }
  }
  return null
}

export function parseSavedSession(value: unknown): SavedSession | null {
  try {
    if (!isRecord(value)) return null
    const credentials = parseCredentials(value.credentials)
    if (value.pending === null) return { credentials, pending: null }
    if (!isRecord(value.pending) || !isRecord(value.pending.payload)) return null
    if ("request_id" in value.pending &&
        value.pending.request_id !== value.pending.payload.request_id) return null
    const pending = parsePendingOperation(value.pending)
    return pending ? { credentials, pending } : null
  } catch {
    return null
  }
}
```

- [ ] **Step 6: Route API and browser storage through the new guards**

At the top of `api.ts`, replace the local error/parser definitions with this import/re-export boundary and keep `UploadResult`, `IntakeApi`, transport helpers, and methods:

```ts
import {
  INTAKE_FALLBACK_MESSAGE as FALLBACK,
  IntakeRequestError,
  parseAttachment,
  parseCredentials,
  parseReceipt,
  parseSession,
} from "./contracts"

export { IntakeRequestError, parseReceipt, parseSession } from "./contracts"
```

Use credential parsing in `create`:

```ts
const body = await parseJson(response)
if (!isRecord(body)) {
  throw new IntakeRequestError(FALLBACK, response.status, "invalid_response")
}
return {
  credentials: parseCredentials(body.credentials),
  session: parseSession(body.session),
}
```

Use attachment parsing in the XHR success handler:

```ts
if (!isRecord(body)) {
  throw new IntakeRequestError(FALLBACK, xhr.status, "invalid_response")
}
resolve({
  attachment: parseAttachment(body.attachment),
  session: parseSession(body.session),
})
```

Retain the existing `isRecord` transport helper in `api.ts`, but remove `stringList`, `validFact`, `validAttachment`, and the old parser/error implementations now owned by `contracts.ts`.

Make `session.ts` use the persisted guard; the complete resulting file is:

```ts
import { parseSavedSession } from "./contracts"
import type { SavedSession } from "./types"

export interface SessionStorage {
  load(): SavedSession | null
  save(value: SavedSession): void
  clear(): void
}

const STORAGE_KEY = "zaincash.intake.session"

export function browserSessionStorage(storage?: Storage): SessionStorage {
  const currentStorage = () => storage ?? window.localStorage
  return {
    load() {
      const raw = currentStorage().getItem(STORAGE_KEY)
      if (!raw) return null
      try {
        return parseSavedSession(JSON.parse(raw) as unknown)
      } catch {
        return null
      }
    },
    save(value) {
      currentStorage().setItem(STORAGE_KEY, JSON.stringify(value))
    },
    clear() {
      currentStorage().removeItem(STORAGE_KEY)
    },
  }
}

export function memoryStorage(initial: SavedSession | null = null): SessionStorage {
  let current = initial
  return {
    load: () => current,
    save(value) {
      current = value
    },
    clear() {
      current = null
    },
  }
}
```

- [ ] **Step 7: Run all contract/storage/controller tests and typecheck**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/contracts.test.ts src/features/intake/session.test.ts src/features/intake/api.test.ts src/features/intake/controller.test.ts
npm run typecheck
```

Expected: all listed tests pass; malformed nested data and storage are rejected; valid current and matching-legacy saved operations replay; typecheck passes without suppression comments.

- [ ] **Step 8: Review contract coverage and the diff**

Run:

```bash
cd users-frontend
rg -n "as SavedSession|as unknown as Credentials|pending\\.request_id|payload as (MessageCommand|ReviewCommand|SubmitCommand)" apps/web/src/features/intake || true
git diff --check -- apps/web/src/features/intake
git diff -- apps/web/src/features/intake/types.ts apps/web/src/features/intake/contracts.ts apps/web/src/features/intake/api.ts apps/web/src/features/intake/session.ts apps/web/src/features/intake/contracts.test.ts apps/web/src/features/intake/session.test.ts apps/web/src/features/intake/api.test.ts
```

Expected: the unsafe-cast/reference search prints nothing; diff check is silent; only contract, required-Fact, storage-validation, and associated test changes appear.

### Task 6: Extract stable-ID sequential upload lifecycle with TDD

**Files:**
- Create: `users-frontend/apps/web/src/features/intake/useIntakeUploads.ts`, `users-frontend/apps/web/src/features/intake/useIntakeUploads.test.tsx`
- Modify: `users-frontend/apps/web/src/features/intake/controller.ts`, `users-frontend/apps/web/src/features/intake/controller.test.ts`, `users-frontend/apps/web/src/features/intake/IntakePage.tsx`
- Test: `useIntakeUploads.test.tsx`, `controller.test.ts`, and `IntakePage.test.tsx`.

**Interfaces:**
- Consumes: `IntakeController.upload(file, clientId)` and existing `ControllerState.uploads: Record<string, number>`.
- Produces: `useIntakeUploads(controller, createId?) -> { previews, selectFiles, clearPreviews }`, where `UploadPreview = { id: string; name: string; url: string }`, `selectFiles(files: File[]): Promise<void>`, and `clearPreviews(): void` revokes all outstanding preview URLs; progress is keyed only by stable client ID.

- [ ] **Step 1: Add failing hook tests for duplicate identity, progress, failure cleanup, and unmount**

Create `useIntakeUploads.test.tsx` with:

```tsx
import { act, renderHook, waitFor } from "@testing-library/react"
import { afterEach, describe, expect, it, vi } from "vitest"
import type { IntakeApi, UploadResult } from "./api"
import { IntakeController } from "./controller"
import { memoryStorage } from "./session"
import { attachment, emptySession, fakeApi } from "./test/fixtures"
import { useIntakeUploads } from "./useIntakeUploads"

function uploadResult(): UploadResult {
  return { attachment, session: emptySession({ attachments: [attachment] }) }
}

type Pending = {
  onProgress?: (fraction: number) => void
  resolve: (value: UploadResult) => void
}

function deferredUploads(api: IntakeApi): Pending[] {
  const pending: Pending[] = []
  vi.mocked(api.upload).mockImplementation(
    (_credentials, _file, _requestId, _revision, onProgress) =>
      new Promise<UploadResult>((resolve) => {
        pending.push({ onProgress, resolve })
      }),
  )
  return pending
}

function mockUrls() {
  const create = vi.spyOn(URL, "createObjectURL")
    .mockReturnValueOnce("blob:one")
    .mockReturnValueOnce("blob:two")
  const revoke = vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => undefined)
  return { create, revoke }
}

afterEach(() => {
  vi.restoreAllMocks()
})

describe("useIntakeUploads", () => {
  it("keeps identical filenames and bytes on independent client IDs and progress keys", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    const pending = deferredUploads(api)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )
    const files = [
      new File(["same"], "error.png", { type: "image/png" }),
      new File(["same"], "error.png", { type: "image/png" }),
    ]

    let selection!: Promise<void>
    act(() => {
      selection = result.current.selectFiles(files)
    })
    await waitFor(() => expect(pending).toHaveLength(1))
    expect(result.current.previews.map((item) => item.id)).toEqual([
      "client-one",
      "client-two",
    ])

    act(() => pending[0]!.onProgress?.(0.25))
    expect(controller.getSnapshot().uploads).toEqual({ "client-one": 0.25 })

    await act(async () => {
      pending[0]!.resolve(uploadResult())
      await Promise.resolve()
    })
    await waitFor(() => expect(pending).toHaveLength(2))
    act(() => pending[1]!.onProgress?.(0.5))
    expect(controller.getSnapshot().uploads).toEqual({ "client-two": 0.5 })
    expect(result.current.previews.map((item) => item.id)).toEqual(["client-two"])

    await act(async () => {
      pending[1]!.resolve(uploadResult())
      await selection
    })
    expect(result.current.previews).toEqual([])
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")
  })

  it("stops on the first failure and removes current plus unattempted previews", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    vi.mocked(api.upload).mockRejectedValueOnce(new TypeError("offline"))
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )
    const files = [
      new File(["one"], "one.png", { type: "image/png" }),
      new File(["two"], "two.png", { type: "image/png" }),
    ]

    await act(async () => {
      await result.current.selectFiles(files)
    })

    expect(api.upload).toHaveBeenCalledTimes(1)
    expect(result.current.previews).toEqual([])
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")
  })

  it("revokes outstanding URLs on unmount and does not start a later upload", async () => {
    const { revoke } = mockUrls()
    const api = fakeApi()
    const pending = deferredUploads(api)
    const controller = new IntakeController(api, memoryStorage())
    await controller.initialize("en")
    const ids = ["client-one", "client-two"]
    const { result, unmount } = renderHook(() =>
      useIntakeUploads(controller, () => ids.shift()!),
    )

    let selection!: Promise<void>
    act(() => {
      selection = result.current.selectFiles([
        new File(["one"], "one.png", { type: "image/png" }),
        new File(["two"], "two.png", { type: "image/png" }),
      ])
    })
    await waitFor(() => expect(pending).toHaveLength(1))
    unmount()
    expect(revoke).toHaveBeenCalledWith("blob:one")
    expect(revoke).toHaveBeenCalledWith("blob:two")

    await act(async () => {
      pending[0]!.resolve(uploadResult())
      await selection
    })
    expect(api.upload).toHaveBeenCalledTimes(1)
  })
})
```

- [ ] **Step 2: Run the hook tests to verify the new module is absent**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/useIntakeUploads.test.tsx
```

Expected: FAIL to resolve `./useIntakeUploads`; no test is skipped.

- [ ] **Step 3: Implement the hook with stable IDs, sequential stop-on-failure, and cleanup**

Create `useIntakeUploads.ts` with:

```ts
import { useCallback, useEffect, useRef, useState } from "react"
import type { IntakeController } from "./controller"

export type UploadPreview = {
  id: string
  name: string
  url: string
}

export function useIntakeUploads(
  controller: IntakeController,
  createId: () => string = () => crypto.randomUUID(),
) {
  const [previews, setPreviews] = useState<UploadPreview[]>([])
  const previewUrls = useRef(new Map<string, string>())
  const mounted = useRef(true)

  const clearPreviews = useCallback((ids?: ReadonlySet<string>) => {
    if (mounted.current) {
      setPreviews((current) =>
        ids ? current.filter((item) => !ids.has(item.id)) : [],
      )
    }
    for (const [id, url] of previewUrls.current) {
      if (ids && !ids.has(id)) continue
      URL.revokeObjectURL(url)
      previewUrls.current.delete(id)
    }
  }, [])

  useEffect(() => {
    mounted.current = true
    return () => {
      mounted.current = false
      clearPreviews()
    }
  }, [clearPreviews])

  const selectFiles = useCallback(async (files: File[]) => {
    const local = files.map((file) => ({
      file,
      preview: {
        id: createId(),
        name: file.name,
        url: URL.createObjectURL(file),
      },
    }))
    for (const item of local) {
      previewUrls.current.set(item.preview.id, item.preview.url)
    }
    if (mounted.current) {
      setPreviews((current) => [
        ...current,
        ...local.map((item) => item.preview),
      ])
    }

    for (let index = 0; index < local.length; index += 1) {
      const item = local[index]!
      try {
        await controller.upload(item.file, item.preview.id)
      } catch {
        clearPreviews(new Set(local.slice(index).map((entry) => entry.preview.id)))
        return
      }
      if (!mounted.current) return
      clearPreviews(new Set([item.preview.id]))
    }
  }, [clearPreviews, controller, createId])

  return { previews, selectFiles, clearPreviews }
}
```

- [ ] **Step 4: Key controller pending uploads and progress by client ID**

Change the pending-upload field and public method to:

```ts
private pendingUpload: { clientId: string; file: File } | null = null

async upload(file: File, clientId: string) {
  return this.enqueue(() => this.uploadNow(file, clientId))
}
```

Change retry to retain both values:

```ts
if (this.pendingUpload) {
  return this.uploadNow(this.pendingUpload.file, this.pendingUpload.clientId)
}
```

Replace `uploadNow` with this complete client-keyed implementation:

```ts
private async uploadNow(file: File, clientId: string) {
  const session = this.requireSession()
  if (!session) return
  if (this.pending || this.pendingRemoval) {
    this.unreconciled()
    return
  }
  const generation = this.generation
  const identity = await fileIdentity(file)
  if (generation !== this.generation) return
  if (this.pendingUpload && this.pendingUpload.file !== file) {
    const prior = await fileIdentity(this.pendingUpload.file)
    if (prior !== identity) {
      this.unreconciled()
      return
    }
  }
  const requestId = this.uploadIds.get(identity) ?? crypto.randomUUID()
  this.uploadIds.set(identity, requestId)
  this.pendingUpload = { clientId, file }
  this.replace({
    ...this.snapshot,
    busy: true,
    error: null,
    uploads: { ...this.snapshot.uploads, [clientId]: 0 },
  })
  try {
    const result = await this.api.upload(
      this.credentials!,
      file,
      requestId,
      this.snapshot.session?.revision ?? session.revision,
      (fraction) => {
        if (generation !== this.generation) return
        this.replace({
          ...this.snapshot,
          uploads: { ...this.snapshot.uploads, [clientId]: fraction },
        })
      },
      this.nextSignal(),
    )
    if (generation !== this.generation) return
    this.uploadIds.delete(identity)
    this.pendingUpload = null
    const uploads = { ...this.snapshot.uploads }
    delete uploads[clientId]
    this.replace({
      ...this.snapshot,
      session: result.session,
      busy: false,
      error: null,
      uploads,
    })
  } catch (error) {
    if (generation !== this.generation) throw error
    if (
      error instanceof IntakeRequestError &&
      error.status < 500 &&
      error.code !== "invalid_response"
    ) {
      this.pendingUpload = null
      this.uploadIds.delete(identity)
    }
    try {
      await this.reload(generation)
    } catch {
      // Retain the uncertain upload for retry.
    }
    if (generation !== this.generation) return
    const uploads = { ...this.snapshot.uploads }
    delete uploads[clientId]
    this.replace({
      ...this.snapshot,
      busy: false,
      error: safeMessage(error),
      uploads,
    })
    throw error
  }
}
```

Update existing direct controller test calls to supply stable IDs:

```ts
await controller.upload(file, "upload-reattach-1")
await controller.upload(file, "upload-reattach-2")
await expect(controller.upload(file, "upload-retry")).rejects.toThrow()
await controller.upload(new File(["x"], "x.png"), "upload-submitted")
const uploaded = controller.upload(file, "upload-revision")
```

- [ ] **Step 5: Connect `IntakePage` without changing its rendered controls or classes**

Replace local preview state/URL refs/effects and `selectFiles` with:

```tsx
const { previews, selectFiles, clearPreviews } = useIntakeUploads(controller)
```

Add the import:

```tsx
import { useIntakeUploads } from "./useIntakeUploads"
```

In `send`, replace the old `setPreviews` cleanup block with the hook-owned cleanup so a successful send still revokes and removes every preview:

```tsx
if (!controller.getSnapshot().error) {
  setDraft((current) => (current.trim() === content ? "" : current))
  clearPreviews()
  document.getElementById("intake-message")?.focus()
}
```

Keep the existing file input `onChange` call `void selectFiles(Array.from(picked))`. Change only preview identity/progress mappings:

```tsx
images: previews.map((preview) => ({
  id: preview.id,
  filename: preview.name,
  url: preview.url,
})),
```

```tsx
{previews.map((preview) => (
  <progress
    key={preview.id}
    className="intake-progress"
    value={snapshot.uploads[preview.id] ?? 0}
    max={1}
    aria-label={`${text.uploadProgress} ${preview.name}`}
  />
))}
```

Delete the now-unowned `previewUrls` ref, preview cleanup effect, `setPreviews` calls, and old name-based upload loop; do not alter toolbar conditions, button labels, or CSS classes.

- [ ] **Step 6: Run upload/controller/page tests and typecheck**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/useIntakeUploads.test.tsx src/features/intake/controller.test.ts src/features/intake/IntakePage.test.tsx
npm run typecheck
```

Expected: all tests pass, including duplicate-name/byte selections, independent progress, first-failure cleanup, unmount cleanup, sequential upload ordering, and existing accessible UI tests.

- [ ] **Step 7: Search for stale filename identity and review the upload diff**

Run:

```bash
cd users-frontend
rg -n "uploads\\[preview\\.name\\]|\\[file\\.name\\]|delete uploads\\[file\\.name\\]|key=\\{preview\\.url\\}" apps/web/src/features/intake || true
git diff --check -- apps/web/src/features/intake
git diff -- apps/web/src/features/intake/useIntakeUploads.ts apps/web/src/features/intake/useIntakeUploads.test.tsx apps/web/src/features/intake/controller.ts apps/web/src/features/intake/IntakePage.tsx apps/web/src/features/intake/controller.test.ts
```

Expected: the stale-identity search prints nothing; diff check is silent; the diff contains no styling or user-flow changes.

### Task 7: Preserve resume-unavailable state across `startNew`

**Files:**
- Create: No new files.
- Modify: `users-frontend/apps/web/src/features/intake/controller.ts`, `users-frontend/apps/web/src/features/intake/controller.test.ts`
- Test: `users-frontend/apps/web/src/features/intake/controller.test.ts`

**Interfaces:**
- Consumes: Existing `RESUME_UNAVAILABLE`, `emptyState()`, `boot(language, generation)`, and `SessionStorage.clear()`.
- Produces: `startNew(language): Promise<void>` that retains `resumeUnavailable` and the existing public error string after both successful and failed reboots.

- [ ] **Step 1: Add failing reset-failure regression tests**

Add both tests to `controller.test.ts`:

```ts
it("preserves resume-unavailable state when startNew cannot clear storage", async () => {
  const storage: SessionStorage = {
    load: () => null,
    save: () => undefined,
    clear: () => {
      throw new Error("denied")
    },
  }
  const api = fakeApi()
  const controller = new IntakeController(api, storage)
  await controller.initialize("en")

  await controller.startNew("en")

  expect(controller.getSnapshot().resumeUnavailable).toBe(true)
  expect(controller.getSnapshot().error).toBe(
    "This browser cannot save the conversation for later. It stays open on this screen.",
  )
})

it("preserves the resume error when reboot also fails after a clear failure", async () => {
  const storage: SessionStorage = {
    load: () => null,
    save: () => undefined,
    clear: () => {
      throw new Error("denied token must not leak")
    },
  }
  const api = fakeApi()
  const controller = new IntakeController(api, storage)
  await controller.initialize("en")
  vi.mocked(api.create).mockRejectedValueOnce(new TypeError("offline"))

  await controller.startNew("en")

  expect(controller.getSnapshot().resumeUnavailable).toBe(true)
  expect(controller.getSnapshot().error).toBe(
    "This browser cannot save the conversation for later. It stays open on this screen.",
  )
  expect(controller.getSnapshot().error).not.toMatch(/token|denied/i)
})
```

- [ ] **Step 2: Verify both tests fail against the current reset**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/controller.test.ts -t "resume-unavailable state|resume error"
```

Expected: both tests FAIL because the final snapshot has `resumeUnavailable === false` and either `error === null` or the reboot error.

- [ ] **Step 3: Carry the clear failure through reset and boot**

Replace `startNew` with:

```ts
async startNew(language: Language) {
  this.generation += 1
  const generation = this.generation
  this.stopPoll()
  this.abortCurrent()
  return this.enqueue(async () => {
    if (generation !== this.generation) return
    this.credentials = null
    this.pending = null
    this.uploadIds.clear()
    this.pendingUpload = null
    this.pendingRemoval = null
    let resumeFailure: string | null = null
    try {
      this.storage.clear()
    } catch {
      resumeFailure = RESUME_UNAVAILABLE
    }
    this.replace({
      ...emptyState(),
      resumeUnavailable: resumeFailure !== null,
      error: resumeFailure,
    })
    this.initPromise = null
    await this.boot(language, generation)
    if (generation === this.generation && resumeFailure) {
      this.replace({
        ...this.snapshot,
        resumeUnavailable: true,
        error: resumeFailure,
      })
    }
  })
}
```

Do not include the caught storage exception text in state; the existing safe public message remains the only exposed error.

- [ ] **Step 4: Run focused and full controller tests, then review the diff**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/features/intake/controller.test.ts
npm run typecheck
git diff --check -- apps/web/src/features/intake/controller.ts apps/web/src/features/intake/controller.test.ts
git diff -- apps/web/src/features/intake/controller.ts apps/web/src/features/intake/controller.test.ts
```

Expected: both new tests and every existing controller test pass; typecheck and diff check pass; only reset-state handling and its tests change.

### Task 8: Disable streaming Stop when no handler exists

**Files:**
- Create: `users-frontend/apps/web/src/components/ui/agent-chat.test.tsx`
- Modify: `users-frontend/apps/web/src/components/ui/agent-chat.tsx`
- Test: `agent-chat.test.tsx` and `IntakePage.test.tsx`.

**Interfaces:**
- Consumes: Existing `AgentChatProps.status`, optional `onStop`, default `stopLabel = "Stop"`, and ready-state intake composer.
- Produces: Stop disabled exactly when `status` is `streaming`/`submitted` and `onStop` is absent; supplied handlers remain enabled and callable.

- [ ] **Step 1: Add failing focused chat tests**

Create `agent-chat.test.tsx` with:

```tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { AgentChat } from "./agent-chat"

describe("AgentChat stop control", () => {
  it.each(["streaming", "submitted"] as const)(
    "disables Stop without a handler in %s state",
    (status) => {
      render(<AgentChat messages={[]} status={status} />)
      expect(screen.getByRole("button", { name: "Stop" })).toBeDisabled()
    },
  )

  it("keeps Stop enabled and calls a supplied handler", async () => {
    const user = userEvent.setup()
    const onStop = vi.fn()
    render(<AgentChat messages={[]} status="streaming" onStop={onStop} />)

    const button = screen.getByRole("button", { name: "Stop" })
    expect(button).toBeEnabled()
    await user.click(button)
    expect(onStop).toHaveBeenCalledTimes(1)
  })
})
```

- [ ] **Step 2: Run the no-handler cases and verify the defect**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/components/ui/agent-chat.test.tsx
```

Expected: the two no-handler cases FAIL because Stop is enabled; the supplied-handler case passes.

- [ ] **Step 3: Apply the one-condition button fix**

Change only the button's disabled expression:

```tsx
disabled={isStreaming ? !onStop : blocked}
```

Keep `variant`, `aria-label`, `onClick`, icon selection, and all classes unchanged.

- [ ] **Step 4: Run focused chat/page tests and review the diff**

Run:

```bash
cd users-frontend
npm --workspace web test -- src/components/ui/agent-chat.test.tsx src/features/intake/IntakePage.test.tsx
npm run typecheck
git diff --check -- apps/web/src/components/ui/agent-chat.tsx apps/web/src/components/ui/agent-chat.test.tsx
git diff -- apps/web/src/components/ui/agent-chat.tsx apps/web/src/components/ui/agent-chat.test.tsx
```

Expected: all chat and page tests pass; current ready-state send behavior is unchanged; the production diff is one disabled-condition line.

### Task 9: Run the complete customer acceptance matrix and final diff review

**Files:**
- Create: No new files.
- Modify: No additional product files; this task only verifies and reviews the accumulated changes.
- Test: Entire customer web suite, TypeScript projects, lint, and production build.

**Interfaces:**
- Consumes: All interfaces and configuration produced by Tasks 1-8.
- Produces: Verified customer-frontend acceptance results and a reviewed, minimal diff with no unrelated changes.

- [ ] **Step 1: Run the exact customer verification commands from the specification**

Run:

```bash
cd users-frontend
npm test
npm run typecheck
npm run lint
npm run build
npm --workspace web test
```

Expected: every command exits 0. Root and workspace test commands report the same files and test totals. Typechecking covers application code, all tests, `vite.config.ts`, and `vitest.config.ts`. The production build completes without missing-dependency errors.

- [ ] **Step 2: Verify removed symbols/dependencies and retained reusable capabilities**

Run from the repository root:

```bash
rg -n "useTheme|export default AgentChat|pending\\.request_id|payload as (MessageCommand|ReviewCommand|SubmitCommand)" users-frontend/apps users-frontend/packages --glob '!**/node_modules/**' || true
rg -n '"(@hugeicons/core-free-icons|@hugeicons/react|zod|@tailwindcss/vite|@turbo/gen)"' users-frontend/apps/web/package.json users-frontend/packages/ui/package.json || true
rg -n "emptyStatePosition|onAttach|onRemoveImage|@workspace/ui/lib/utils" users-frontend/apps users-frontend/packages --glob '!**/node_modules/**'
```

Expected: the first search prints nothing. The second search prints only web's retained `@tailwindcss/vite` entry in `apps/web/package.json`; Hugeicons, direct UI `zod`, UI `@tailwindcss/vite`, and UI `@turbo/gen` are absent. The final search still finds reusable `AgentChat` capabilities and shadcn aliases, confirming they were not removed.

- [ ] **Step 3: Review whitespace, status, and the complete customer diff**

Run from the repository root:

```bash
git diff --check
git status --short
git diff -- users-frontend
```

Expected: diff check is silent. Status/diff contain only the intended customer source, test, configuration, manifest, and lockfile changes from Tasks 1-8 plus this plan document; no product snapshots, secrets, unrelated user edits, generated caches, or historical-record deletions appear. Any unexpected change is investigated and excluded rather than overwritten.
