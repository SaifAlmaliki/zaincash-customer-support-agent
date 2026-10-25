import { useEffect, useRef, useState } from "react"
import { Link, useParams } from "react-router-dom"
import {
  ArrowLeft,
  Check,
  Copy,
  FileText,
  ShieldCheck,
  ShieldAlert,
  SquarePen,
  X,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import {
  ConfirmDialog,
  EmptyState,
  ErrorState,
  FilterSelect,
  LoadingState,
  PageHeader,
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { useWorkspace } from "@/lib/workspace"
import { api } from "@/lib/api"
import { dateLabel, teamLabel, teams, timeLabel, humanize } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { Result, ReviewInput } from "@/lib/types"
import { SourceEvidence } from "./SourceEvidence"
import { TicketFlow } from "./TicketFlow"
import { IntakeEvidence } from "./IntakeEvidence"
import { canReview } from "./review-availability"

function reviewerNote(result: Result) {
  const own = result.internal_note?.trim()
  if (own) return own
  const parts = (result.escalation_note ?? "").split(/(?<=\.)\s+/).map((part) => part.trim()).filter(Boolean)
  const seen = new Set<string>()
  const unique = parts.filter((part) => (seen.has(part) ? false : seen.add(part)))
  const escalated = unique.filter((part) => part.startsWith("Escalated:"))
  const analysis = unique.filter((part) => !part.startsWith("Escalated:"))
  const summary = escalated.sort((a, b) => b.length - a.length)[0]
  return [summary, ...analysis].filter(Boolean).join(" ")
}

function ReviewEditor({
  result,
  onSaved,
}: {
  result: Result
  onSaved: () => void
}) {
  const workspace = useWorkspace()
  const textCopy = useCopy().review
  const [text, setText] = useState(result.final_text || result.draft_text || "")
  const [reviewer, setReviewer] = useState(textCopy.reviewerDefault),
    [team, setTeam] = useState(result.team || "General Care")
  const [saving, setSaving] = useState(false),
    [reject, setReject] = useState(false)
  const approved = ["approved", "edited"].includes(result.status)
  const reviewable = canReview(result.status)
  const findings = result.guardrail_findings ?? []
  const note = reviewerNote(result)
  async function save(action: ReviewInput["action"]) {
    if (saving) return
    setSaving(true)
    const review: ReviewInput = {
      action,
      reviewer,
      final_text: text,
      team,
      expected_updated_at: result.updated_at,
    }
    try {
      await api.review(result.id, review)
      workspace.notify(
        action === "reject"
          ? textCopy.noticeRejected
          : action === "reassign"
            ? textCopy.noticeReassigned
            : textCopy.noticeApproved
      )
      setReject(false)
      onSaved()
    } catch (error) {
      workspace.notify(
        error instanceof Error ? error.message : textCopy.saveFailed,
        true
      )
    } finally {
      setSaving(false)
    }
  }
  async function copy() {
    try {
      await navigator.clipboard.writeText(result.final_text || "")
      workspace.notify(textCopy.copied)
    } catch {
      workspace.notify(textCopy.copyFailed, true)
    }
  }
  return (
    <div className="review-editor-stack">
      {!reviewable && (
        <p className="processing-hold" role="status">
          {result.status === "failed" ? textCopy.failedHold : textCopy.processingHold}
        </p>
      )}
      {reviewable && (
      <Card>
        <CardHeader><CardTitle className="section-title"><ShieldAlert size={17} />{textCopy.checksTitle}</CardTitle></CardHeader>
        <CardContent>
          <p className="muted small">{textCopy.checksApply}</p>
          {findings.length ? <ul className="guardrail-findings">{findings.map((finding) => <li key={finding}><strong>{humanize(finding)}</strong><code>{finding}</code></li>)}</ul> : <p className="field-help">{result.guardrail_findings ? textCopy.noFindings : textCopy.findingsUnavailable}</p>}
          <div className={result.credential_check_degraded ? "knowledge-message" : "field-help checker-summary"}>
            <strong>{result.credential_check_degraded === true ? textCopy.credentialDegraded : result.credential_check_degraded === false ? textCopy.credentialAvailable : textCopy.credentialUnknown}</strong>
            <p>{result.credential_check_degraded === true ? textCopy.credentialDegradedBody : result.credential_check_degraded == null ? textCopy.credentialUnknownBody : textCopy.credentialOkBody}</p>
            {result.requests_credentials != null && <p>{fill(textCopy.credentialScore, { score: result.requests_credentials.toFixed(3) })}</p>}
          </div>
          <div className="internal-note"><strong>{textCopy.internalNote}</strong>{note ? <p className="passage-text" dir="auto">{note}</p> : <p className="field-help">{textCopy.noNote}</p>}</div>
        </CardContent>
      </Card>
      )}
      <Card className="draft-card">
        <CardHeader>
          <CardTitle className="section-title">
            <SquarePen size={18} />
            {textCopy.workspace}<Badge variant="outline">{textCopy.humanReview}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {reviewable && !result.draft_text && (
            <div className="draft-unavailable">
              <FileText size={17} />
              <span>
                <strong>{textCopy.noDraft}</strong>{textCopy.noDraftBody}
              </span>
            </div>
          )}
          {result.draft_text && <div className="saved-reply"><strong>{textCopy.original}</strong><p className="passage-text" dir="auto" lang="ar">{result.draft_text}</p></div>}
          {result.final_text && <div className="saved-reply"><strong>{textCopy.final}</strong><p className="passage-text" dir="auto" lang="ar">{result.final_text}</p></div>}
          <label className="field-label" htmlFor="reply">
            {result.final_text ? textCopy.editReply : textCopy.writeReply}
          </label>
          <Textarea
            id="reply"
            className="reply-editor"
            dir="rtl"
            lang="ar"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="اكتب ردك للزبون هنا…"
            maxLength={8000}
          />
          <div className="editor-meta">
            <span>{textCopy.language}</span>
            <span>
              {fill(textCopy.words, { count: text.trim() ? text.trim().split(/\s+/).length : 0 })}
            </span>
          </div>
          <div className="reviewer-fields">
            <label className="field-label" htmlFor="reviewer">
              {textCopy.reviewer}
              <Input
                id="reviewer"
                value={reviewer}
                onChange={(e) => setReviewer(e.target.value)}
                maxLength={64}
              />
            </label>
            <div>
              <span className="field-label">{textCopy.team}</span>
              <FilterSelect
                label={textCopy.team}
                value={team}
                options={teams.map((value) => ({ value, label: teamLabel(value) }))}
                onChange={setTeam}
              />
            </div>
          </div>
          {team !== result.team && (
            <Button
              variant="outline"
              disabled={saving || !reviewable || !reviewer.trim()}
              onClick={() => void save("reassign")}
            >
              {textCopy.saveTeam}
            </Button>
          )}
          <div className="review-actions">
            <Button
              variant="outline"
              disabled={saving || !reviewable}
              onClick={() => setReject(true)}
            >
              <X size={16} />
              {textCopy.reject}
            </Button>
            <Button
              disabled={
                saving ||
                !reviewable ||
                !text.trim() ||
                !reviewer.trim()
              }
              onClick={() =>
                void save(
                  text === result.draft_text ? "approve" : "edit_approve"
                )
              }
            >
              <Check size={16} />
              {saving
                ? textCopy.saving
                : text !== result.draft_text
                  ? textCopy.saveApprove
                  : textCopy.approve}
            </Button>
          </div>
          {approved && result.final_text && (
            <Button
              variant="secondary"
              className="copy-reply"
              onClick={() => void copy()}
            >
              <Copy size={15} />
              {textCopy.copy}
            </Button>
          )}
          <p className="approval-footnote">
            <ShieldCheck size={14} />
            {textCopy.footnote}
          </p>
          <ConfirmDialog
            open={reject}
            onClose={() => setReject(false)}
            title={textCopy.rejectTitle}
            description={textCopy.rejectBody}
            action={textCopy.rejectAction}
            onConfirm={() => void save("reject")}
          />
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="section-title">
            <FileText size={16} />
            {textCopy.history}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!result.reviews?.length && <p className="muted small">{textCopy.noHistory}</p>}
          <div className="audit-list">
            {result.reviews?.map((review) => (
              <div key={review.id}>
                <span className="audit-dot" />
                <div>
                  <strong>
                    {(textCopy.actions as Record<string, string>)[review.action] || humanize(review.action)}{" "}
                    <span>{fill(textCopy.historyBy, { name: review.reviewer })}</span>
                  </strong>
                  <small>
                    {fill(textCopy.historyWhen, {
                      date: dateLabel(review.created_at),
                      time: timeLabel(review.created_at),
                    })}
                  </small>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
      <TicketFlow result={result} />
    </div>
  )
}

export function TicketReviewPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const textCopy = useCopy().review
  const query = useResource<Result>(`/results/${id}`, workspace.revision)
  const result = query.data
  const reload = useRef(query.reload)
  useEffect(() => {
    reload.current = query.reload
  }, [query.reload])
  useEffect(() => {
    if (result?.status !== "processing") return
    const timer = window.setInterval(() => reload.current(), 2000)
    return () => window.clearInterval(timer)
  }, [result?.status])
  if (query.error)
    return <ErrorState message={query.error} retry={query.reload} />
  if (query.loading) return <LoadingState />
  if (!result)
    return (
      <EmptyState
        title={textCopy.notFound}
        description={textCopy.notFoundDetail}
      >
        <Button nativeButton={false} render={<Link to="/" />}>
          {textCopy.back}
        </Button>
      </EmptyState>
    )
  return (
    <>
      <Link to="/" className="back-link">
        <ArrowLeft size={15} />
        {textCopy.back}
      </Link>
      <PageHeader
        title={result.ticket.external_id}
        description={`${result.ticket.display_name || textCopy.customerTicket} · ${dateLabel(result.ticket.received_at)}, ${timeLabel(result.ticket.received_at)} ${textCopy.baghdad}`}
      >
        <PriorityBadge priority={result.priority} />
        <StatusBadge status={result.status} />
      </PageHeader>
      <div className="review-layout">
        <div>
          <IntakeEvidence intake={result.intake} />
          <SourceEvidence result={result} />
        </div>
        <ReviewEditor
          key={result.id}
          result={result}
          onSaved={() => {
            query.reload()
            workspace.refresh()
          }}
        />
      </div>
    </>
  )
}
