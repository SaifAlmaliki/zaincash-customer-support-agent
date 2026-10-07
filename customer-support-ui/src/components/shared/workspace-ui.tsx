import type { ReactNode } from "react"
import { CircleAlert, Inbox, LoaderCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { humanize, percentage } from "@/lib/format"

const statusLabels: Record<string, string> = { pending_review: "Needs review", escalated: "Escalated", approved: "Approved", edited: "Edited & approved", rejected: "Rejected", running: "Processing", completed: "Completed", completed_with_errors: "Partial failure", failed: "Failed", awaiting_indexing: "Awaiting indexing" }
export function StatusBadge({ status }: { status: string }) {
  return <Badge variant="outline" className={`status-badge status-${status}`}><span className="status-dot" />{statusLabels[status] || humanize(status)}</Badge>
}
export function PriorityBadge({ priority }: { priority: string | null }) {
  return <span className={`priority priority-${priority}`}><span className="priority-bars"><i /><i /><i /></span>{priority || "—"}</span>
}
export function Confidence({ value }: { value: number | null }) {
  return <div className={`confidence ${value !== null && value < .7 ? "confidence-low" : ""}`}>
    <span className="confidence-track"><span style={{ width: `${(value || 0) * 100}%` }} /></span><span>{percentage(value)}</span>
  </div>
}
export function PageHeader({ title, description, children }: { title: string; description: string; children?: ReactNode }) {
  return <div className="page-heading"><div><h1>{title}</h1><p>{description}</p></div><div className="heading-actions">{children}</div></div>
}
export function EmptyState({ title, description, children }: { title: string; description: string; children?: ReactNode }) {
  return <div className="empty-state"><div className="empty-icon"><Inbox size={25} strokeWidth={1.4} /></div><h3>{title}</h3><p>{description}</p>{children}</div>
}
export function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return <div className="error-state" role="alert"><CircleAlert size={18} /><div><strong>Couldn’t load the workspace</strong><p>{message}</p></div>{retry && <Button variant="outline" onClick={retry}>Retry</Button>}</div>
}
export function LoadingState() {
  return <div className="loading-state" role="status"><LoaderCircle className="animate-spin" size={20} />Loading workspace…</div>
}
export function Metric({ label, value, detail, icon, tone = "" }: { label: string; value: ReactNode; detail: string; icon: ReactNode; tone?: string }) {
  return <Card className={`metric-card ${tone}`}><CardContent><div className="metric-top"><span>{label}</span>{icon}</div><div className="metric-value">{value}</div><p>{detail}</p></CardContent></Card>
}
export function FilterSelect({ label, value, options, onChange }: { label: string; value: string; options: { value: string; label: string }[]; onChange: (value: string) => void }) {
  return <Select value={value} onValueChange={(v) => { if (v !== null) onChange(v) }} items={options}>
    <SelectTrigger aria-label={label} className="filter-select"><SelectValue /></SelectTrigger>
    <SelectContent alignItemWithTrigger={false}>{options.map((option) => <SelectItem value={option.value} key={option.value}>{option.label}</SelectItem>)}</SelectContent>
  </Select>
}
export function ConfirmDialog({ open, onClose, title, description, action, onConfirm }: { open: boolean; onClose: () => void; title: string; description: string; action: string; onConfirm: () => void }) {
  return <Dialog open={open} onOpenChange={(value) => { if (!value) onClose() }}><DialogContent>
    <DialogHeader><DialogTitle>{title}</DialogTitle><DialogDescription>{description}</DialogDescription></DialogHeader>
    <DialogFooter><Button variant="outline" onClick={onClose}>Cancel</Button><Button variant="destructive" onClick={onConfirm}>{action}</Button></DialogFooter>
  </DialogContent></Dialog>
}
