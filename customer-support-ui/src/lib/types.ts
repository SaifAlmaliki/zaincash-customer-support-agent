export type Mode = "jev" | "gemini" | "cascade"
export type WorkspaceMode = "live" | "preview"
export type TicketInput = { external_id?: string; text: string; received_at?: string; channel: "app" | "whatsapp" | "call_note"; customer_phone?: string | null }
export type Ticket = TicketInput & { id: number; external_id: string; received_at: string; display_name?: string }
export type ExtractedField = { value: string | number | null; span: string | null; start: number | null; end: number | null; method: string; confidence: number; currency?: string | null }
export type TraceEvent = { kind?: string; node?: string; status?: string; elapsed_ms?: number; tool?: string; [key: string]: unknown }
export type Review = { id: number; reviewer: string; action: string; final_text: string | null; created_at: string }
export type Result = {
  id: number; ticket_id: number; run_id: number; ticket: Ticket;
  category: string | null; category_confidence: number | null; category_probs: Record<string, number>;
  priority: string | null; priority_confidence: number | null; flags: Record<string, number>;
  classifier_path: string | null; extracted: Record<string, ExtractedField>; lookup_status: string | null;
  matched_txn_ref: string | null; team: string | null; escalated: boolean; escalation_reasons: string[];
  escalation_note: string | null; draft_text: string | null; final_text: string | null; citations: string[];
  agent_trace: TraceEvent[]; status: string; error: string | null; latency_ms: number; cost_usd: number;
  updated_at: string; jev_model_version?: string | null; reviews?: Review[]; transaction?: Record<string, string | number | null> | null;
}
export type ReviewInput = { action: "approve" | "edit_approve" | "reject" | "reassign"; reviewer: string; final_text?: string; team?: string; expected_updated_at: string }
export type Run = { id: number; started_at: string; finished_at: string | null; mode: Mode; status: string;
  total: number; processed: number; degraded: boolean; total_cost_usd: number;
  counts: { by_status?: Record<string, number>; by_category?: Record<string, number>; escalation_reasons?: Record<string, number>; latency_p50_ms?: number; latency_p95_ms?: number; fallback_rate?: number; error?: string } }
export type Health = { database: string; configured_modes: Mode[]; capabilities: { drafting: boolean; rag_indexing: boolean; evaluation: boolean } }
export type KnowledgeDocument = { id: number; filename: string; size: number; status: string; content_type: string; sha256: string; created_at: string }
export type Insights = { total: number; categories: Record<string, number>; reasons: Record<string, number>; weeks: { start: string; end: string; total: number; categories: Record<string, number> }[]; evaluation: null }
export type EvaluationReport = { model: string; split: "test"; sample_size: number; generated_at: string; classification_accuracy: number; extraction_accuracy: number; confusion_cases: string[] }
