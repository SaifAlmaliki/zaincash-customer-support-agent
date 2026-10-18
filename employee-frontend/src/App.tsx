import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { TooltipProvider } from "@/components/ui/tooltip"
import { WorkspaceLayout } from "@/components/layout/WorkspaceLayout"
import { WorkspaceProvider } from "@/components/layout/WorkspaceProvider"
const QueuePage = lazy(() =>
  import("@/features/queue/QueuePage").then((module) => ({ default: module.QueuePage }))
)
const TicketReviewPage = lazy(() =>
  import("@/features/review/TicketReviewPage").then((module) => ({
    default: module.TicketReviewPage,
  }))
)
const RunsPage = lazy(() =>
  import("@/features/runs/RunsPage").then((module) => ({
    default: module.RunsPage,
  }))
)
const RunDetailPage = lazy(() =>
  import("@/features/runs/RunsPage").then((module) => ({
    default: module.RunDetailPage,
  }))
)
const NewBatchPage = lazy(() =>
  import("@/features/runs/NewBatchPage").then((module) => ({
    default: module.NewBatchPage,
  }))
)
const KnowledgePage = lazy(() =>
  import("@/features/knowledge/KnowledgePage").then((module) => ({
    default: module.KnowledgePage,
  }))
)
const InsightsPage = lazy(() =>
  import("@/features/insights/InsightsPage").then((module) => ({
    default: module.InsightsPage,
  }))
)
const EvaluationPage = lazy(() =>
  import("@/features/insights/EvaluationPage").then((module) => ({
    default: module.EvaluationPage,
  }))
)

export default function App() {
  return (
    <BrowserRouter>
      <TooltipProvider>
        <WorkspaceProvider>
          <Routes>
            <Route element={<WorkspaceLayout />}>
              <Route index element={<QueuePage />} />
              <Route path="tickets/:id" element={<TicketReviewPage />} />
              <Route path="runs" element={<RunsPage />} />
              <Route path="runs/new" element={<NewBatchPage />} />
              <Route path="runs/:id" element={<RunDetailPage />} />
              <Route path="knowledge" element={<KnowledgePage />} />
              <Route path="insights" element={<InsightsPage />} />
              <Route path="evaluation" element={<EvaluationPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </WorkspaceProvider>
      </TooltipProvider>
    </BrowserRouter>
  )
}
import { lazy } from "react"
