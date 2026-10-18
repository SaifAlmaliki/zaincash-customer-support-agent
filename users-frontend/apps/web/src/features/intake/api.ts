import type {
  Attachment,
  Credentials,
  Language,
  MessageCommand,
  Receipt,
  RemoveCommand,
  ReviewCommand,
  SessionView,
  SubmitCommand,
} from "./types"

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

export type UploadResult = {
  attachment: Attachment
  session: SessionView
}

export interface IntakeApi {
  create(language: Language, signal?: AbortSignal): Promise<{ credentials: Credentials; session: SessionView }>
  get(credentials: Credentials, signal?: AbortSignal): Promise<SessionView>
  message(credentials: Credentials, command: MessageCommand, signal?: AbortSignal): Promise<SessionView>
  review(credentials: Credentials, command: ReviewCommand, signal?: AbortSignal): Promise<SessionView>
  retry(credentials: Credentials, requestId: string, expectedRevision: number, signal?: AbortSignal): Promise<SessionView>
  submit(credentials: Credentials, command: SubmitCommand, signal?: AbortSignal): Promise<Receipt>
  upload(
    credentials: Credentials,
    file: File,
    requestId: string,
    expectedRevision: number,
    onProgress?: (fraction: number) => void,
    signal?: AbortSignal,
  ): Promise<UploadResult>
  remove(credentials: Credentials, attachmentId: string, command: RemoveCommand, signal?: AbortSignal): Promise<SessionView>
  image(credentials: Credentials, attachmentId: string, signal?: AbortSignal): Promise<Blob>
}

const FALLBACK = "The conversation could not be updated. Try again."

function sessionUrl(baseUrl: string, credentials: Credentials, suffix = "") {
  return `${baseUrl}/sessions/${credentials.session_id}${suffix}`
}

function authHeaders(credentials: Credentials, json = false): Headers {
  const headers = new Headers()
  headers.set("Authorization", `Bearer ${credentials.token}`)
  if (json) headers.set("Content-Type", "application/json")
  return headers
}

async function readError(response: Response): Promise<IntakeRequestError> {
  let message = FALLBACK
  let code = "intake_error"
  try {
    const body = (await response.json()) as { detail?: { message?: string; code?: string } | string }
    if (body && typeof body === "object" && body.detail && typeof body.detail === "object") {
      if (typeof body.detail.message === "string" && body.detail.message.trim()) message = body.detail.message
      if (typeof body.detail.code === "string") code = body.detail.code
    }
  } catch {
    message = FALLBACK
  }
  return new IntakeRequestError(message, response.status, code)
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object"
}

export function parseSession(value: unknown): SessionView {
  if (!isRecord(value) || typeof value.id !== "string" || typeof value.revision !== "number" || typeof value.phase !== "string") {
    throw new IntakeRequestError(FALLBACK, 200, "invalid_response")
  }
  return value as unknown as SessionView
}

export function parseReceipt(value: unknown): Receipt {
  if (!isRecord(value) || typeof value.ticket_reference !== "string" || typeof value.processing_status !== "string") {
    throw new IntakeRequestError(FALLBACK, 200, "invalid_response")
  }
  return value as unknown as Receipt
}

async function parseJson(response: Response): Promise<unknown> {
  if (!response.ok) throw await readError(response)
  try {
    return await response.json()
  } catch {
    throw new IntakeRequestError(FALLBACK, response.status, "invalid_response")
  }
}

export function createIntakeApi(baseUrl = "/api/intake"): IntakeApi {
  return {
    async create(language, signal) {
      const response = await fetch(`${baseUrl}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language }),
        signal,
      })
      const body = await parseJson(response)
      if (!isRecord(body) || !isRecord(body.credentials)) throw new IntakeRequestError(FALLBACK, response.status, "invalid_response")
      const credentials = body.credentials as unknown as Credentials
      if (!credentials.session_id || !credentials.token) throw new IntakeRequestError(FALLBACK, response.status, "invalid_response")
      return { credentials, session: parseSession(body.session) }
    },
    async get(credentials, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials), { headers: authHeaders(credentials), signal })
      return parseSession(await parseJson(response))
    },
    async message(credentials, command, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, "/messages"), {
        method: "POST",
        headers: authHeaders(credentials, true),
        body: JSON.stringify(command),
        signal,
      })
      return parseSession(await parseJson(response))
    },
    async review(credentials, command, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, "/review"), {
        method: "POST",
        headers: authHeaders(credentials, true),
        body: JSON.stringify(command),
        signal,
      })
      return parseSession(await parseJson(response))
    },
    async retry(credentials, requestId, expectedRevision, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, `/operations/${requestId}/retry`), {
        method: "POST",
        headers: authHeaders(credentials, true),
        body: JSON.stringify({ expected_revision: expectedRevision }),
        signal,
      })
      return parseSession(await parseJson(response))
    },
    async submit(credentials, command, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, "/submit"), {
        method: "POST",
        headers: authHeaders(credentials, true),
        body: JSON.stringify(command),
        signal,
      })
      return parseReceipt(await parseJson(response))
    },
    upload(credentials, file, requestId, expectedRevision, onProgress, signal) {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        const fail = () => reject(new TypeError("connection lost"))
        xhr.open("POST", sessionUrl(baseUrl, credentials, "/attachments"))
        xhr.setRequestHeader("Authorization", `Bearer ${credentials.token}`)
        xhr.upload.onprogress = (event) => {
          if (onProgress && event.lengthComputable && event.total > 0) onProgress(event.loaded / event.total)
        }
        xhr.onerror = fail
        xhr.onabort = () => reject(new DOMException("The upload was cancelled.", "AbortError"))
        xhr.onload = () => {
          const response = new Response(xhr.responseText, { status: xhr.status })
          void parseJson(response)
            .then((body) => {
              if (!isRecord(body)) throw new IntakeRequestError(FALLBACK, xhr.status, "invalid_response")
              resolve({ attachment: body.attachment as Attachment, session: parseSession(body.session) })
            })
            .catch(reject)
        }
        if (signal) {
          if (signal.aborted) {
            xhr.abort()
            return
          }
          signal.addEventListener("abort", () => xhr.abort(), { once: true })
        }
        const body = new FormData()
        body.append("file", file, file.name)
        body.append("request_id", requestId)
        body.append("expected_revision", String(expectedRevision))
        xhr.send(body)
      })
    },
    async remove(credentials, attachmentId, command, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, `/attachments/${attachmentId}`), {
        method: "DELETE",
        headers: authHeaders(credentials, true),
        body: JSON.stringify(command),
        signal,
      })
      return parseSession(await parseJson(response))
    },
    async image(credentials, attachmentId, signal) {
      const response = await fetch(sessionUrl(baseUrl, credentials, `/attachments/${attachmentId}`), {
        headers: authHeaders(credentials),
        signal,
      })
      if (!response.ok) throw await readError(response)
      return response.blob()
    },
  }
}
