"use client"

import {
  memo,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react"
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { Button, buttonVariants } from "@workspace/ui/components/button"

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export type ChatStatus = "ready" | "streaming" | "submitted" | "idle"

export type MessagePart =
  | { type: "text"; text: string }
  | { type: "error"; title?: string; message: string }

export type AgentMessage = {
  id: string
  role: "user" | "assistant"
  parts: MessagePart[]
}

export type AttachedImage = {
  id: string
  filename: string
  url: string
  size?: number
}

export type AttachedFile = {
  id: string
  filename: string
  size?: number
}

export type AgentChatProps = {
  messages: AgentMessage[]
  onSend?: (message: { role: "user"; content: string }) => void
  onStop?: () => void
  status?: ChatStatus
  error?: { message: string; title?: string }
  emptyStatePosition?: "default" | "center"
  attachments?: {
    onAttach?: () => void
    attachInputId?: string
    attachLabel?: string
    removeLabel?: string
    disabled?: boolean
    images?: AttachedImage[]
    files?: AttachedFile[]
    onRemoveImage?: (id: string) => void
    onRemoveFile?: (id: string) => void
  }
  placeholder?: string
  inputLabel?: string
  inputId?: string
  sendLabel?: string
  stopLabel?: string
  sendDisabled?: boolean
  allowEmptySend?: boolean
  hideComposer?: boolean
  conversationLabel?: string
  speakers?: { user: string; assistant: string }
  threadFooter?: ReactNode
  toolbar?: ReactNode
  renderAfter?: (message: AgentMessage) => ReactNode
  value?: string
  onValueChange?: (value: string) => void
  className?: string
}

const SendIcon = () => (
  <svg
    width="14"
    height="14"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <line x1="12" y1="19" x2="12" y2="5" />
    <polyline points="5 12 12 5 19 12" />
  </svg>
)

const StopIcon = () => (
  <svg
    width="12"
    height="12"
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <rect x="6" y="6" width="12" height="12" rx="1" />
  </svg>
)

const PaperclipIcon = () => (
  <svg
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
  </svg>
)

const XIcon = ({ size = 12 }: { size?: number }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
)

const FileIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
    <polyline points="14 2 14 8 20 8" />
  </svg>
)

function UserBubble({ text, speaker }: { text: string; speaker?: string }) {
  return (
    <div className="flex justify-end">
      <div className="max-w-[80%] rounded-2xl bg-[color-mix(in_oklch,#da3345_10%,var(--card))] px-3.5 py-2 text-sm break-words whitespace-pre-wrap text-foreground">
        {speaker ? <span className="sr-only">{speaker}</span> : null}
        {text}
      </div>
    </div>
  )
}

function AssistantText({ text, speaker }: { text: string; speaker?: string }) {
  return (
    <div className="flex justify-start">
      <div
        dir="auto"
        className="max-w-[90%] text-sm leading-relaxed break-words whitespace-pre-wrap text-foreground"
      >
        {speaker ? <span className="sr-only">{speaker}</span> : null}
        {text}
      </div>
    </div>
  )
}

function ErrorBubble({ title, message }: { title?: string; message: string }) {
  return (
    <div className="flex justify-start">
      <div
        role="alert"
        className="rounded-[8px] border border-destructive/30 bg-destructive/10 px-4 py-2.5 text-sm"
      >
        {title ? (
          <div className="font-medium text-foreground">{title}</div>
        ) : null}
        <div className={cn("text-muted-foreground", title && "mt-0.5")}>
          {message}
        </div>
      </div>
    </div>
  )
}

function MessageList({
  messages,
  conversationLabel,
  speakers,
  threadFooter,
  renderAfter,
}: {
  messages: AgentMessage[]
  conversationLabel?: string
  speakers?: AgentChatProps["speakers"]
  threadFooter?: ReactNode
  renderAfter?: AgentChatProps["renderAfter"]
}) {
  const scroller = useRef<HTMLDivElement>(null)
  const stick = useRef(true)

  useEffect(() => {
    const el = scroller.current
    if (!el || !stick.current) return
    el.scrollTop = el.scrollHeight
  }, [messages, threadFooter])

  return (
    <div
      ref={scroller}
      role="log"
      aria-label={conversationLabel}
      aria-relevant="additions"
      className="min-h-0 flex-1 overflow-y-auto px-4 py-6"
      onScroll={(event) => {
        const el = event.currentTarget
        stick.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80
      }}
    >
      <div className="mx-auto flex max-w-[640px] flex-col gap-4">
        {messages.map((message) => (
          <div key={message.id} className="flex flex-col gap-2">
            {message.parts.map((part, index) => {
              if (part.type === "error") {
                return (
                  <ErrorBubble
                    key={index}
                    title={part.title}
                    message={part.message}
                  />
                )
              }
              if (message.role === "user") {
                return (
                  <UserBubble
                    key={index}
                    text={part.text}
                    speaker={speakers?.user}
                  />
                )
              }
              return (
                <AssistantText
                  key={index}
                  text={part.text}
                  speaker={speakers?.assistant}
                />
              )
            })}
            {renderAfter?.(message)}
          </div>
        ))}
        {threadFooter}
      </div>
    </div>
  )
}

function ImageChip({
  url,
  alt,
  onRemove,
  removeLabel,
}: {
  url: string
  alt: string
  onRemove?: () => void
  removeLabel: string
}) {
  return (
    <div className="group relative h-12 w-12 overflow-hidden rounded-md bg-muted">
      <img src={url} alt={alt} className="h-full w-full object-cover" />
      {onRemove ? (
        <Button
          type="button"
          size="icon-xs"
          variant="default"
          onClick={onRemove}
          aria-label={removeLabel}
          className="absolute top-0.5 right-0.5 size-5 min-h-5 min-w-5 rounded-full bg-[#252830] p-0 text-white hover:bg-[#252830]"
        >
          <XIcon size={10} />
        </Button>
      ) : null}
    </div>
  )
}

function FileChip({
  filename,
  size,
  onRemove,
  removeLabel,
  disabled,
}: {
  filename: string
  size?: number
  onRemove?: () => void
  removeLabel: string
  disabled?: boolean
}) {
  const sizeText =
    size === undefined
      ? null
      : size < 1024
        ? `${size} B`
        : size < 1024 * 1024
          ? `${(size / 1024).toFixed(1)} KB`
          : `${(size / (1024 * 1024)).toFixed(1)} MB`
  return (
    <div className="inline-flex items-center gap-2 rounded-md bg-muted px-2 py-1.5">
      <span className="text-muted-foreground">
        <FileIcon />
      </span>
      <div className="flex min-w-0 flex-col">
        <span className="max-w-[140px] truncate text-xs font-medium text-foreground">
          {filename}
        </span>
        {sizeText ? (
          <span className="text-[10px] text-muted-foreground">{sizeText}</span>
        ) : null}
      </div>
      {onRemove ? (
        <Button
          type="button"
          size="icon-xs"
          variant="outline"
          onClick={onRemove}
          aria-label={removeLabel}
          disabled={disabled}
          className="border-border bg-card text-foreground hover:bg-background"
        >
          <XIcon />
        </Button>
      ) : null}
    </div>
  )
}

function InputBar({
  onSend,
  onStop,
  status = "ready",
  placeholder = "Send a message...",
  attachments,
  className,
  value: controlledValue,
  onChange,
  disabled,
  sendDisabled,
  allowEmptySend,
  inputLabel,
  inputId = "intake-message",
  sendLabel = "Send",
  stopLabel = "Stop",
}: {
  onSend?: (message: { role: "user"; content: string }) => void
  onStop?: () => void
  status?: ChatStatus
  placeholder?: string
  attachments?: AgentChatProps["attachments"]
  className?: string
  value?: string
  onChange?: (value: string) => void
  disabled?: boolean
  sendDisabled?: boolean
  allowEmptySend?: boolean
  inputLabel?: string
  inputId?: string
  sendLabel?: string
  stopLabel?: string
}) {
  const [internal, setInternal] = useState("")
  const isControlled = controlledValue !== undefined
  const input = isControlled ? controlledValue : internal
  const setInput = useCallback(
    (next: string) => {
      if (isControlled) onChange?.(next)
      else setInternal(next)
    },
    [isControlled, onChange]
  )
  const ref = useRef<HTMLTextAreaElement>(null)
  const isStreaming = status === "streaming" || status === "submitted"
  const hasInput = input.trim().length > 0
  const images = attachments?.images ?? []
  const files = attachments?.files ?? []
  const hasContext = images.length > 0 || files.length > 0
  const blocked = Boolean(sendDisabled || disabled || isStreaming)
  const armed = !blocked && (hasInput || Boolean(allowEmptySend))
  const removeLabel = attachments?.removeLabel ?? "Remove"

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = "0"
    const next = Math.min(el.scrollHeight, 120)
    el.style.height = `${next}px`
    el.style.overflowY = el.scrollHeight > 120 ? "auto" : "hidden"
  }, [input])

  const submit = useCallback(() => {
    const trimmed = input.trim()
    if (blocked) return
    if (!trimmed && !allowEmptySend) return
    onSend?.({ role: "user", content: trimmed })
    if (!isControlled) setInternal("")
  }, [allowEmptySend, blocked, input, isControlled, onSend])

  const attachLabel = attachments?.attachLabel
  const attachInputId = attachments?.attachInputId

  return (
    <div className={cn("w-full shrink-0 px-3 pb-3", className)}>
      <div className="mx-auto max-w-[640px]">
        <div
          className="relative cursor-text rounded-[16px] bg-card shadow-sm ring-1 ring-border"
          onClick={(event) => {
            if (
              event.target === event.currentTarget ||
              !(event.target as HTMLElement).closest("button, textarea, label")
            ) {
              ref.current?.focus()
            }
          }}
        >
          <div
            className={cn(
              "grid transition-[grid-template-rows] duration-200 ease-out motion-reduce:transition-none",
              hasContext ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
            )}
          >
            <div className="overflow-hidden">
              {hasContext ? (
                <div className="flex flex-wrap items-center gap-1.5 px-2.5 pt-2.5 pb-0.5">
                  {images.map((image) => (
                    <ImageChip
                      key={image.id}
                      url={image.url}
                      alt={image.filename}
                      removeLabel={removeLabel}
                      onRemove={
                        attachments?.onRemoveImage && !attachments.disabled
                          ? () => attachments.onRemoveImage!(image.id)
                          : undefined
                      }
                    />
                  ))}
                  {files.map((file) => (
                    <FileChip
                      key={file.id}
                      filename={file.filename}
                      size={file.size}
                      removeLabel={removeLabel}
                      disabled={attachments?.disabled}
                      onRemove={
                        attachments?.onRemoveFile
                          ? () => attachments.onRemoveFile!(file.id)
                          : undefined
                      }
                    />
                  ))}
                </div>
              ) : null}
            </div>
          </div>
          <div className="min-h-[44px] pt-3 pr-3 pb-0 pl-3.5">
            <textarea
              ref={ref}
              id={inputId}
              value={input}
              dir="auto"
              aria-label={inputLabel}
              onChange={(event) => setInput(event.target.value)}
              onCompositionStart={(event) => {
                event.currentTarget.dataset.composing = "true"
              }}
              onCompositionEnd={(event) => {
                delete event.currentTarget.dataset.composing
              }}
              onKeyDown={(event) => {
                if (
                  event.key !== "Enter" ||
                  event.shiftKey ||
                  event.currentTarget.dataset.composing === "true"
                )
                  return
                event.preventDefault()
                submit()
              }}
              placeholder={placeholder}
              disabled={disabled}
              rows={1}
              className={cn(
                "w-full resize-none overflow-hidden border-0 bg-transparent text-[14px] leading-[1.6] text-foreground outline-none placeholder:text-muted-foreground",
                disabled && "cursor-not-allowed opacity-50"
              )}
            />
          </div>
          <div className="flex items-center justify-between gap-3 px-2 pt-1 pb-2">
            <div className="flex min-w-0 items-center gap-1">
              {attachInputId && attachLabel ? (
                <label
                  htmlFor={attachInputId}
                  className={cn(
                    buttonVariants({ variant: "outline", size: "icon-sm" }),
                    "cursor-pointer rounded-full border-border bg-card text-foreground hover:bg-muted",
                    attachments?.disabled && "pointer-events-none opacity-50"
                  )}
                >
                  <PaperclipIcon />
                  <span className="sr-only">{attachLabel}</span>
                </label>
              ) : attachments?.onAttach ? (
                <Button
                  type="button"
                  size="icon-sm"
                  variant="outline"
                  onClick={attachments.onAttach}
                  aria-label={attachLabel ?? "Attach"}
                  disabled={attachments.disabled}
                  className="rounded-full border-border bg-card text-foreground hover:bg-muted"
                >
                  <PaperclipIcon />
                </Button>
              ) : null}
            </div>
            <Button
              type="button"
              size="icon-sm"
              variant={armed || isStreaming ? "default" : "outline"}
              aria-label={isStreaming ? stopLabel : sendLabel}
              disabled={!isStreaming && blocked}
              onClick={() => {
                if (isStreaming) onStop?.()
                else submit()
              }}
              className={cn(
                "rounded-full disabled:opacity-100",
                armed || isStreaming
                  ? "bg-[#da3345] text-white hover:bg-[#c42d3d]"
                  : "border-border bg-card text-muted-foreground"
              )}
            >
              {isStreaming ? <StopIcon /> : <SendIcon />}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export const AgentChat = memo(function AgentChat({
  messages,
  onSend,
  onStop,
  status = "ready",
  error,
  emptyStatePosition = "default",
  attachments,
  placeholder,
  inputLabel,
  inputId,
  sendLabel,
  stopLabel,
  sendDisabled,
  allowEmptySend,
  hideComposer,
  conversationLabel,
  speakers,
  threadFooter,
  toolbar,
  renderAfter,
  value,
  onValueChange,
  className,
}: AgentChatProps) {
  const messagesWithError: AgentMessage[] = useMemo(() => {
    if (!error) return messages
    return [
      ...messages,
      {
        id: "agent-chat-error",
        role: "assistant" as const,
        parts: [
          {
            type: "error" as const,
            title: error.title,
            message: error.message,
          },
        ],
      },
    ]
  }, [messages, error])

  const isEmpty = !error && messages.length === 0
  const isCenteredEmpty =
    isEmpty && emptyStatePosition === "center" && !threadFooter

  const inputBarNode: ReactNode = (
    <InputBar
      onSend={onSend}
      onStop={onStop}
      status={status}
      placeholder={placeholder}
      attachments={attachments}
      value={value}
      onChange={onValueChange}
      sendDisabled={sendDisabled}
      allowEmptySend={allowEmptySend}
      inputLabel={inputLabel}
      inputId={inputId}
      sendLabel={sendLabel}
      stopLabel={stopLabel}
      className={isCenteredEmpty ? "px-0 pb-0" : undefined}
    />
  )

  return (
    <div className={cn("flex h-full min-h-0 flex-1 flex-col", className)}>
      {isCenteredEmpty ? (
        <div className="flex min-h-0 flex-1 items-center justify-center px-4 py-4">
          <div className="w-full max-w-[640px]">{inputBarNode}</div>
        </div>
      ) : (
        <MessageList
          messages={messagesWithError}
          conversationLabel={conversationLabel}
          speakers={speakers}
          threadFooter={threadFooter}
          renderAfter={renderAfter}
        />
      )}
      {!isCenteredEmpty && toolbar ? (
        <div className="w-full shrink-0 border-t border-border px-3 pt-2">
          <div className="mx-auto flex max-w-[640px] flex-col gap-2 pb-2">
            {toolbar}
          </div>
        </div>
      ) : null}
      {!isCenteredEmpty && !hideComposer ? inputBarNode : null}
    </div>
  )
})

export default AgentChat
