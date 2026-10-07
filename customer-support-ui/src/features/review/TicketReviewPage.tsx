import { useState } from "react"
import { Link, useParams } from "react-router-dom"
import {
  ArrowLeft,
  Check,
  Copy,
  FileText,
  ShieldCheck,
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
import { dateLabel, teams, timeLabel, humanize } from "@/lib/format"
import type { Result, ReviewInput } from "@/lib/types"
import { SourceEvidence } from "./SourceEvidence"
import { PipelineTrace } from "./PipelineTrace"

function ReviewEditor({
  result,
  onSaved,
}: {
  result: Result
  onSaved: () => void
}) {
  const workspace = useWorkspace()
  const [text, setText] = useState(result.final_text || result.draft_text || "")
  const [reviewer, setReviewer] = useState("Support agent"),
    [team, setTeam] = useState(result.team || "General Care")
  const [saving, setSaving] = useState(false),
    [reject, setReject] = useState(false)
  const approved = ["approved", "edited"].includes(result.status)
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
      if (workspace.mode === "preview")
        workspace.reviewPreview(result.id, review)
      else await api.review(result.id, review)
      workspace.notify(
        `${action === "reject" ? "Response rejected" : action === "reassign" ? "Team reassigned" : "Response approved"}${workspace.mode === "preview" ? " in preview only" : " and recorded"}.`
      )
      setReject(false)
      onSaved()
    } catch (error) {
      workspace.notify(
        error instanceof Error ? error.message : "Could not save review.",
        true
      )
    } finally {
      setSaving(false)
    }
  }
  async function copy() {
    try {
      await navigator.clipboard.writeText(result.final_text || "")
      workspace.notify("Approved reply copied.")
    } catch {
      workspace.notify(
        "Clipboard is unavailable. Select and copy the approved text manually.",
        true
      )
    }
  }
  return (
    <div className="review-editor-stack">
      <Card className="draft-card">
        <CardHeader>
          <CardTitle className="section-title">
            <SquarePen size={18} />
            Response workspace<Badge variant="outline">Human review</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!result.draft_text && (
            <div className="draft-unavailable">
              <FileText size={17} />
              <span>
                <strong>No generated draft</strong>The drafting agent is not
                connected yet. You can write a response below.
              </span>
            </div>
          )}
          {workspace.mode === "preview" && (
            <p className="field-help">
              This response is an illustrative preview, not a model output.
            </p>
          )}
          <label className="field-label" htmlFor="reply">
            Reply in Iraqi Arabic
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
            <span>Iraqi Arabic</span>
            <span>
              {text.trim() ? text.trim().split(/\s+/).length : 0} words
            </span>
          </div>
          <div className="reviewer-fields">
            <label className="field-label" htmlFor="reviewer">
              Reviewed by
              <Input
                id="reviewer"
                value={reviewer}
                onChange={(e) => setReviewer(e.target.value)}
                maxLength={64}
              />
            </label>
            <div>
              <span className="field-label">Assigned team</span>
              <FilterSelect
                label="Assigned team"
                value={team}
                options={teams.map((value) => ({ value, label: value }))}
                onChange={setTeam}
              />
            </div>
          </div>
          {team !== result.team && (
            <Button
              variant="outline"
              disabled={saving || !reviewer.trim()}
              onClick={() => void save("reassign")}
            >
              Save team assignment
            </Button>
          )}
          <div className="review-actions">
            <Button
              variant="outline"
              disabled={saving || result.status === "failed"}
              onClick={() => setReject(true)}
            >
              <X size={16} />
              Reject
            </Button>
            <Button
              disabled={
                saving ||
                !text.trim() ||
                !reviewer.trim() ||
                result.status === "failed"
              }
              onClick={() =>
                void save(
                  text === result.draft_text ? "approve" : "edit_approve"
                )
              }
            >
              <Check size={16} />
              {saving
                ? "Saving…"
                : text !== result.draft_text
                  ? "Save & approve"
                  : "Approve reply"}
            </Button>
          </div>
          {approved && result.final_text && (
            <Button
              variant="secondary"
              className="copy-reply"
              onClick={() => void copy()}
            >
              <Copy size={15} />
              Copy approved reply
            </Button>
          )}
          <p className="approval-footnote">
            <ShieldCheck size={14} />
            Approval saves your decision. Nothing is sent automatically.
          </p>
          <ConfirmDialog
            open={reject}
            onClose={() => setReject(false)}
            title="Reject this response?"
            description="The result and original draft remain available for audit. No reply will be approved."
            action="Reject response"
            onConfirm={() => void save("reject")}
          />
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="section-title">
            <FileText size={16} />
            Sources & review history
          </CardTitle>
        </CardHeader>
        <CardContent>
          {result.citations.length ? (
            result.citations.map((citation) => (
              <code key={citation} className="citation-id">
                {citation}
              </code>
            ))
          ) : (
            <p className="muted small">
              No retrieved policy citations are recorded for this ticket.
            </p>
          )}
          <div className="audit-list">
            {result.reviews?.map((review) => (
              <div key={review.id}>
                <span className="audit-dot" />
                <div>
                  <strong>
                    {humanize(review.action)} <span>by {review.reviewer}</span>
                  </strong>
                  <small>
                    {dateLabel(review.created_at)} at{" "}
                    {timeLabel(review.created_at)} Baghdad
                  </small>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
      <PipelineTrace result={result} />
    </div>
  )
}

export function TicketReviewPage() {
  const { id } = useParams(),
    workspace = useWorkspace()
  const query = useResource<Result>(
    workspace.mode === "preview" ? null : `/results/${id}`,
    workspace.revision
  )
  const result =
    workspace.mode === "preview"
      ? workspace.preview.find((row) => row.id === Number(id))
      : query.data
  if (workspace.mode === "live" && query.error)
    return <ErrorState message={query.error} retry={query.reload} />
  if (workspace.mode === "live" && query.loading) return <LoadingState />
  if (!result)
    return (
      <EmptyState
        title="Ticket not found"
        description="Return to the queue and select a ticket in this workspace."
      >
        <Button nativeButton={false} render={<Link to="/" />}>
          Back to queue
        </Button>
      </EmptyState>
    )
  return (
    <>
      <Link to="/" className="back-link">
        <ArrowLeft size={15} />
        Back to queue
      </Link>
      <PageHeader
        title={result.ticket.external_id}
        description={`${result.ticket.display_name || "Customer support ticket"} · ${dateLabel(result.ticket.received_at)}, ${timeLabel(result.ticket.received_at)} Baghdad`}
      >
        <PriorityBadge priority={result.priority} />
        <StatusBadge status={result.status} />
      </PageHeader>
      <div className="review-layout">
        <SourceEvidence result={result} />
        <ReviewEditor
          key={`${workspace.mode}-${result.id}`}
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
