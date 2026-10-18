import type { IntakeMessage } from "./types"
import type { IntakeCopy } from "./copy"

export function ChatTranscript({
  messages,
  copy,
  announcedId,
}: {
  messages: IntakeMessage[]
  copy: IntakeCopy
  announcedId: string | null
}) {
  const announced = messages.find((message) => message.id === announcedId)
  return (
    <section className="intake-thread" aria-label={copy.conversation} role="log" aria-relevant="additions">
      {announced && announced.role === "assistant" ? (
        <p className="intake-announce" aria-live="polite">
          {announced.text}
        </p>
      ) : null}
      {messages.map((message) => (
        <article key={message.id} dir="auto" lang={message.language} className={`intake-bubble intake-${message.role}`}>
          <span className="intake-speaker">{message.role === "user" ? copy.you : copy.assistant}</span>
          <p>{message.text}</p>
        </article>
      ))}
    </section>
  )
}
