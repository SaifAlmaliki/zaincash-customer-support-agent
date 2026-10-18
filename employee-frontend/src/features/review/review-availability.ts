const REVIEWABLE = new Set(["pending_review", "escalated", "approved", "edited", "rejected"])

export function canReview(status: string) {
  return REVIEWABLE.has(status)
}
