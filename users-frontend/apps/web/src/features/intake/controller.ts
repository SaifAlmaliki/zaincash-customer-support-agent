import { IntakeRequestError, type IntakeApi } from "./api"
import type { SessionStorage } from "./session"
import type {
  Credentials,
  Language,
  MessageCommand,
  PendingOperation,
  ReviewCommand,
  SessionView,
  SubmitCommand,
} from "./types"

const POLL_MS = 2000
const POLL_LIMIT_MS = 70_000
const RESUME_UNAVAILABLE = "This browser cannot save the conversation for later. It stays open on this screen."

export type ControllerState = {
  session: SessionView | null
  busy: boolean
  error: string | null
  uploads: Record<string, number>
  resumeUnavailable: boolean
  pollingExhausted: boolean
}

function emptyState(): ControllerState {
  return {
    session: null,
    busy: false,
    error: null,
    uploads: {},
    resumeUnavailable: false,
    pollingExhausted: false,
  }
}

function safeMessage(error: unknown) {
  const message = error instanceof Error ? error.message : ""
  if (!message || /bearer|token/i.test(message)) return "The conversation could not be updated. Try again."
  return message
}

function isOffline(error: unknown) {
  return error instanceof TypeError
}

function isConflict(error: unknown) {
  return error instanceof IntakeRequestError && error.status === 409
}

export class IntakeController {
  private readonly listeners = new Set<() => void>()
  private snapshot: ControllerState = emptyState()
  private credentials: Credentials | null = null
  private pending: PendingOperation | null = null
  private generation = 0
  private initPromise: Promise<void> | null = null
  private tail: Promise<void> = Promise.resolve()
  private submitFlight: Promise<void> | null = null
  private sendFlight: Promise<void> | null = null
  private abort: AbortController | null = null
  private pollTimer: ReturnType<typeof setTimeout> | null = null
  private pollStarted = 0
  private pollGeneration = 0
  private pollAbort: AbortController | null = null
  private language: Language = "ar"
  private pendingUpload: File | null = null
  private pendingRemoval: { attachmentId: string; request_id: string; expected_revision: number } | null = null
  private readonly uploadIds = new Map<string, string>()

  private readonly api: IntakeApi
  private readonly storage: SessionStorage

  constructor(api: IntakeApi, storage: SessionStorage) {
    this.api = api
    this.storage = storage
  }

  subscribe = (listener: () => void) => {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  getSnapshot = () => this.snapshot

  access() {
    return this.credentials
  }

  transport() {
    return this.api
  }

  async initialize(language: Language) {
    this.language = language
    if (this.credentials && this.snapshot.session) return
    if (!this.initPromise) {
      const generation = this.generation
      this.initPromise = this.boot(language, generation).finally(() => {
        if (generation === this.generation) this.initPromise = null
      })
    }
    return this.initPromise
  }

  async send(text: string, language: Language, attachmentIds: string[]) {
    if (this.sendFlight) return this.sendFlight
    this.sendFlight = this.enqueue(async () => {
      if (this.unreconciled()) return
      await this.sendNow(text, language, attachmentIds)
    }).finally(() => { this.sendFlight = null })
    return this.sendFlight
  }

  async requestReview(allowPartial: boolean, language: Language) {
    return this.enqueue(async () => {
      if (this.unreconciled()) return
      await this.reviewNow(allowPartial, language)
    })
  }

  async submit() {
    if (this.submitFlight) return this.submitFlight
    this.submitFlight = this.enqueue(() => this.submitNow()).finally(() => {
      this.submitFlight = null
    })
    return this.submitFlight
  }

  async retry() {
    return this.enqueue(async () => {
      try { await this.retryNow() } catch (error) {
        this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
      }
    })
  }

  async upload(file: File) {
    return this.enqueue(() => this.uploadNow(file))
  }

  async remove(attachmentId: string) {
    return this.enqueue(() => this.removeNow(attachmentId))
  }

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
      try {
        this.storage.clear()
      } catch {
        this.replace({ ...emptyState(), resumeUnavailable: true, error: RESUME_UNAVAILABLE })
      }
      this.replace(emptyState())
      this.initPromise = null
      await this.boot(language, generation)
    })
  }

  async refresh() {
    return this.enqueue(async () => {
      const generation = this.generation
      try { await this.reload(generation) } catch (error) {
        if (generation === this.generation) this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
      }
    })
  }

  dispose() {
    this.generation += 1
    this.stopPoll()
    this.abortCurrent()
    this.listeners.clear()
  }

  private async boot(language: Language, generation: number) {
    try {
      await this.bootNow(language, generation)
    } catch (error) {
      if (generation !== this.generation) return
      if (error instanceof DOMException && error.name === "AbortError") return
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
    }
  }

  private async bootNow(language: Language, generation: number) {
    let saved: ReturnType<SessionStorage["load"]>
    try {
      saved = this.storage.load()
    } catch {
      saved = null
    }
    if (saved?.credentials) {
      this.credentials = saved.credentials
      this.pending = saved.pending
      await this.reload(generation)
      return
    }
    const signal = this.nextSignal()
    const created = await this.api.create(language, signal)
    if (generation !== this.generation) return
    this.credentials = created.credentials
    this.pending = null
    this.replace({ ...this.snapshot, session: created.session, busy: false, error: null, pollingExhausted: false })
    this.persist()
    this.watch(created.session)
  }

  private async sendNow(text: string, language: Language, attachmentIds: string[]) {
    const session = this.requireSession()
    if (!session || session.turn_status === "processing") return
    const generation = this.generation
    const command: MessageCommand = this.pending?.kind === "message"
      ? (this.pending.payload as MessageCommand)
      : {
          request_id: crypto.randomUUID(),
          expected_revision: session.revision,
          text,
          language,
          attachment_ids: attachmentIds,
        }
    if (this.pending?.kind !== "message") {
      this.pending = { kind: "message", request_id: command.request_id, payload: command }
      this.persist()
    }
    await this.dispatch(generation, () => this.api.message(this.credentials!, command, this.nextSignal()))
  }

  private async reviewNow(allowPartial: boolean, language: Language) {
    const session = this.requireSession()
    if (!session || session.turn_status === "processing") return
    const generation = this.generation
    const command: ReviewCommand = this.pending?.kind === "review"
      ? (this.pending.payload as ReviewCommand)
      : {
          request_id: crypto.randomUUID(),
          expected_revision: session.revision,
          allow_partial: allowPartial,
          language,
        }
    if (this.pending?.kind !== "review") {
      this.pending = { kind: "review", request_id: command.request_id, payload: command }
      this.persist()
    }
    await this.dispatch(generation, () => this.api.review(this.credentials!, command, this.nextSignal()))
  }

  private async submitNow() {
    if (this.snapshot.session?.phase === "submitted") return
    if ((this.pending && this.pending.kind !== "submit") || this.pendingUpload || this.pendingRemoval) {
      this.unreconciled()
      return
    }
    const session = this.requireSession()
    if (!session?.review) {
      this.replace({ ...this.snapshot, error: "Review the report before submitting." })
      return
    }
    const generation = this.generation
    const command: SubmitCommand = this.pending?.kind === "submit"
      ? (this.pending.payload as SubmitCommand)
      : {
          request_id: crypto.randomUUID(),
          expected_revision: session.revision,
          review_id: session.review.id,
          confirmed: true,
        }
    if (this.pending?.kind !== "submit") {
      this.pending = { kind: "submit", request_id: command.request_id, payload: command }
      this.persist()
    }
    this.replace({ ...this.snapshot, busy: true, error: null })
    try {
      const receipt = await this.api.submit(this.credentials!, command, this.nextSignal())
      if (generation !== this.generation) return
      this.pending = null
      this.persist()
      const current = this.snapshot.session
      this.replace({
        ...this.snapshot,
        busy: false,
        error: null,
        session: current
          ? { ...current, phase: "submitted", receipt, revision: current.revision }
          : current,
      })
    } catch (error) {
      if (generation !== this.generation) return
      if (isConflict(error)) {
        await this.reconcileConflict(generation)
        this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
        return
      }
      if (isOffline(error)) {
        try {
          await this.reload(generation)
        } catch {
          /* Keep the in-memory report and the original request. */
        }
      }
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
    }
  }

  private async retryNow() {
    if (!this.credentials) return this.initialize(this.language)
    const generation = this.generation
    await this.reload(generation)
    if (generation !== this.generation) return
    const session = this.snapshot.session
    if (session?.phase === "submitted") {
      this.pending = null
      this.persist()
      this.replace({ ...this.snapshot, error: null })
      return
    }
    if (session?.turn_status === "processing") return
    if (session?.turn_status === "retryable_failure" && session.active_request_id &&
        (!this.pending || this.pending.request_id === session.active_request_id)) {
      await this.dispatch(generation, () =>
        this.api.retry(this.credentials!, session.active_request_id!, session.revision, this.nextSignal()),
      )
      return
    }
    if (this.pendingUpload) return this.uploadNow(this.pendingUpload)
    if (this.pendingRemoval) return this.removeNow(this.pendingRemoval.attachmentId)
    if (this.pending?.kind === "submit") return this.submitNow()
    if (this.pending?.kind === "message") {
      const command = this.pending.payload as MessageCommand
      return this.sendNow(command.text, command.language, command.attachment_ids)
    }
    if (this.pending?.kind === "review") {
      const command = this.pending.payload as ReviewCommand
      return this.reviewNow(command.allow_partial, command.language)
    }
    if (session?.turn_status === "retryable_failure" && session.active_request_id && this.credentials) {
      const generation = this.generation
      await this.dispatch(generation, () =>
        this.api.retry(this.credentials!, session.active_request_id!, session.revision, this.nextSignal()),
      )
    }
  }

  private async uploadNow(file: File) {
    const session = this.requireSession()
    if (!session) return
    if (this.pending || this.pendingRemoval) { this.unreconciled(); return }
    const generation = this.generation
    const identity = await fileIdentity(file)
    if (generation !== this.generation) return
    if (this.pendingUpload && this.pendingUpload !== file) {
      const prior = await fileIdentity(this.pendingUpload)
      if (prior !== identity) { this.unreconciled(); return }
    }
    const requestId = this.uploadIds.get(identity) ?? crypto.randomUUID()
    this.uploadIds.set(identity, requestId)
    this.pendingUpload = file
    this.replace({
      ...this.snapshot,
      busy: true,
      error: null,
      uploads: { ...this.snapshot.uploads, [file.name]: 0 },
    })
    try {
      const result = await this.api.upload(
        this.credentials!,
        file,
        requestId,
        this.snapshot.session?.revision ?? session.revision,
        (fraction) => {
          if (generation !== this.generation) return
          this.replace({ ...this.snapshot, uploads: { ...this.snapshot.uploads, [file.name]: fraction } })
        },
        this.nextSignal(),
      )
      if (generation !== this.generation) return
      this.uploadIds.delete(identity)
      this.pendingUpload = null
      const uploads = { ...this.snapshot.uploads }
      delete uploads[file.name]
      this.replace({ ...this.snapshot, session: result.session, busy: false, error: null, uploads })
    } catch (error) {
      if (generation !== this.generation) throw error
      if (error instanceof IntakeRequestError && error.status < 500 && error.code !== "invalid_response") {
        this.pendingUpload = null
        this.uploadIds.delete(identity)
      }
      try { await this.reload(generation) } catch { /* Retain the uncertain upload for retry. */ }
      if (generation !== this.generation) return
      const uploads = { ...this.snapshot.uploads }
      delete uploads[file.name]
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error), uploads })
      throw error
    }
  }

  private async removeNow(attachmentId: string) {
    const session = this.requireSession()
    if (!session) return
    if (this.pending || this.pendingUpload) { this.unreconciled(); return }
    const generation = this.generation
    const command = this.pendingRemoval?.attachmentId === attachmentId ? this.pendingRemoval : {
      request_id: crypto.randomUUID(),
      expected_revision: session.revision,
    }
    this.pendingRemoval = { ...command, attachmentId }
    this.replace({ ...this.snapshot, busy: true, error: null })
    try {
      const view = await this.api.remove(this.credentials!, attachmentId,
        { request_id: command.request_id, expected_revision: command.expected_revision }, this.nextSignal())
      if (generation !== this.generation) return
      this.pendingRemoval = null
      this.replace({ ...this.snapshot, session: view, busy: false, error: null })
    } catch (error) {
      if (generation !== this.generation) return
      try { await this.reload(generation) } catch { /* Preserve removal identity. */ }
      if (generation !== this.generation) return
      if (isConflict(error) || this.snapshot.session?.attachments.find((item) => item.id === attachmentId)?.removed) this.pendingRemoval = null
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
      throw error
    }
  }

  private async dispatch(generation: number, run: () => Promise<SessionView>) {
    this.stopPoll()
    this.replace({ ...this.snapshot, busy: true, error: null, pollingExhausted: false })
    try {
      const view = await run()
      if (generation !== this.generation) return
      this.pending = null
      this.persist()
      this.replace({ ...this.snapshot, session: view, busy: false, error: null })
      this.watch(view)
    } catch (error) {
      if (generation !== this.generation) return
      if (isConflict(error)) {
        await this.reconcileConflict(generation)
        this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
        return
      }
      if (isOffline(error)) {
        try {
          await this.reload(generation)
        } catch {
          /* The pending payload remains available for an explicit retry. */
        }
      }
      this.replace({ ...this.snapshot, busy: false, error: safeMessage(error) })
    }
  }

  private async reload(generation: number) {
    if (!this.credentials) return
    this.stopPoll()
    const view = await this.api.get(this.credentials, this.nextSignal())
    if (generation !== this.generation) return
    this.replace({ ...this.snapshot, session: view, busy: false, error: null, pollingExhausted: false })
    this.watch(view)
  }

  private watch(session: SessionView) {
    if (session.turn_status === "processing") this.startPoll()
    else this.stopPoll()
  }

  private startPoll() {
    this.stopPoll()
    this.pollStarted = Date.now()
    const generation = this.generation
    const pollGeneration = this.pollGeneration
    this.pollAbort = new AbortController()
    const signal = this.pollAbort.signal
    const tick = async () => {
      if (generation !== this.generation || pollGeneration !== this.pollGeneration) return
      if (Date.now() - this.pollStarted >= POLL_LIMIT_MS) {
        this.replace({
          ...this.snapshot,
          pollingExhausted: true,
          error: "The reply is still processing. Refresh to check again.",
        })
        return
      }
      try {
        if (this.credentials) {
          const view = await this.api.get(this.credentials, signal)
          if (generation !== this.generation || pollGeneration !== this.pollGeneration) return
          this.replace({ ...this.snapshot, session: view })
          if (view.turn_status !== "processing") return
        }
      } catch {
        /* Keep polling until the deadline. The saved messages stay put. */
      }
      if (generation !== this.generation || pollGeneration !== this.pollGeneration) return
      this.pollTimer = setTimeout(() => void tick(), POLL_MS)
    }
    this.pollTimer = setTimeout(() => void tick(), POLL_MS)
  }

  private stopPoll() {
    this.pollGeneration += 1
    this.pollAbort?.abort()
    this.pollAbort = null
    if (this.pollTimer !== null) clearTimeout(this.pollTimer)
    this.pollTimer = null
  }

  private requireSession() {
    if (!this.credentials || !this.snapshot.session || this.snapshot.session.phase === "submitted") return null
    return this.snapshot.session
  }

  private persist() {
    if (!this.credentials) return
    try {
      this.storage.save({ credentials: this.credentials, pending: this.pending })
    } catch {
      this.replace({ ...this.snapshot, resumeUnavailable: true, error: RESUME_UNAVAILABLE })
    }
  }

  private enqueue(work: () => Promise<void>): Promise<void> {
    const generation = this.generation
    const guarded = async () => { if (generation === this.generation) await work() }
    const run = this.tail.then(guarded, guarded)
    this.tail = run.then(
      () => undefined,
      () => undefined,
    )
    return run
  }

  private nextSignal() {
    this.abortCurrent()
    this.abort = new AbortController()
    return this.abort.signal
  }

  private abortCurrent() {
    this.abort?.abort()
    this.abort = null
  }

  private replace(next: ControllerState) {
    this.snapshot = next
    for (const listener of this.listeners) listener()
  }

  private unreconciled() {
    if (!this.pending && !this.pendingUpload && !this.pendingRemoval) return false
    this.replace({ ...this.snapshot, error: "Retry the previous operation before sending new information." })
    return true
  }

  private async reconcileConflict(generation: number) {
    try {
      await this.reload(generation)
      if (generation !== this.generation) return
      this.pending = null
      this.persist()
    } catch { /* Keep the original payload until the server can be reconciled. */ }
  }
}

async function fileIdentity(file: File) {
  const bytes = await file.arrayBuffer()
  const digest = await crypto.subtle.digest("SHA-256", bytes)
  const hex = [...new Uint8Array(digest)].map((part) => part.toString(16).padStart(2, "0")).join("")
  return `${file.name}:${hex}`
}
