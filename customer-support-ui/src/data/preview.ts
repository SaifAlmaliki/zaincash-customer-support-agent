import type { Result, Run } from "@/lib/types"

// Illustrative UI fixtures, not measured model outputs or the held-out evaluation dataset.
const examples = [
  [
    "Ali H.",
    "حولت ٥٠ الف لاخوي امس وانخصمت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123",
    "failed_transfer",
    "Payments Ops",
    "P2",
    0.94,
    "pending_review",
  ],
  [
    "Zainab A.",
    "واحد اتصل بيه يكول من زين كاش وطلب الرمز، وهسه اشوف تحويل ما سويته بحسابي!",
    "fraud_report",
    "Account & Security",
    "P1",
    0.97,
    "escalated",
  ],
  [
    "Hassan M.",
    "ما دا يوصلني رمز التحقق حتى افتح حسابي، صارلي من الصبح احاول",
    "login_access",
    "Account & Security",
    "P3",
    0.92,
    "pending_review",
  ],
  [
    "Noor K.",
    "رحت للوكيل وانطيته ٢٠٠ الف يشحن حسابي ولحد هسه الرصيد ما نزل",
    "agent_dispute",
    "Agent Network",
    "P2",
    0.88,
    "pending_review",
  ],
  [
    "Omar S.",
    "دفعت فاتورة الكهرباء وطلعت ناجحة بس بعدها تكول ما مدفوعة، شنو اسوي؟",
    "bill_payment",
    "Payments Ops",
    "P2",
    0.91,
    "pending_review",
  ],
  [
    "Maryam R.",
    "دزيت الفلوس على رقم غلط، اكدر ارجعهن لو شلون؟",
    "wrong_recipient",
    "Disputes",
    "P2",
    0.86,
    "pending_review",
  ],
  [
    "Ahmed J.",
    "الماستر كارد ما تشتغل وحسابي يطلع خطأ من افتحه، مو فاهم المشكلة",
    "card_issue",
    "Cards",
    "P3",
    0.52,
    "escalated",
  ],
  [
    "Sara B.",
    "شكد عمولة التحويل لحساب بنكي؟",
    "general_inquiry",
    "General Care",
    "P4",
    0.98,
    "approved",
  ],
  [
    "Mustafa D.",
    "التطبيق يطفي اول ما افتحه بعد التحديث الجديد",
    "app_bug",
    "Tech Support",
    "P3",
    0.95,
    "pending_review",
  ],
  [
    "Fatima L.",
    "رفضوا هويتي بالتوثيق، الصورة واضحة بس ما اعرف السبب",
    "account_kyc",
    "Account & Security",
    "P3",
    0.9,
    "edited",
  ],
  [
    "Yousif T.",
    "hawalit 25 alf w ma wislat, w el app ykool error",
    "failed_transfer",
    "Payments Ops",
    "P2",
    0.58,
    "escalated",
  ],
  [
    "Lina W.",
    "اشتريت من متجر بالزين كاش والغيت الطلب، يمته ترجع فلوسي؟",
    "refund_request",
    "Disputes",
    "P3",
    0.89,
    "pending_review",
  ],
] as const

const reply =
  "هلا بيك، شكراً لتواصلك ويانا. استلمنا تفاصيل مشكلتك ونحتاج نراجعها ويا الفريق المختص. رجاءً لا تشارك الرمز السري أو رمز التحقق ويا أي شخص."
export const previewResults: Result[] = examples.map(
  (
    [name, text, category, team, priority, confidence, status],
    index
  ): Result => {
    const date = `2026-10-07T${String(9 + Math.floor(index / 4)).padStart(2, "0")}:${String((index % 4) * 12).padStart(2, "0")}:00+03:00`
    const escalated = status === "escalated"
    const field = (span: string, value: string | number) => ({
      value,
      span,
      start: text.indexOf(span),
      end: text.indexOf(span) + span.length,
      confidence: 0.94,
      method: "illustrative",
      currency: "IQD",
    })
    return {
      id: index + 1,
      ticket_id: index + 1,
      run_id: 1,
      ticket: {
        id: index + 1,
        external_id: `ZC-${2084 + index}`,
        text,
        received_at: date,
        display_name: name,
        channel: index % 3 === 0 ? "whatsapp" : "app",
      },
      category,
      team,
      priority,
      category_confidence: confidence,
      category_probs: { [category]: confidence, other: 1 - confidence },
      priority_confidence: 0.9,
      flags: { fraud_suspected: category === "fraud_report" ? 0.97 : 0.02 },
      classifier_path: confidence < 0.7 ? "gemini_fallback" : "jev",
      extracted:
        index === 0
          ? {
              amount: field("٥٠ الف", 50000),
              txn_ref: field("ZC2410000123", "ZC2410000123"),
              date: field("امس", "2026-10-06"),
            }
          : {},
      lookup_status: index === 0 ? "matched" : "not_applicable",
      matched_txn_ref: index === 0 ? "ZC2410000123" : null,
      transaction:
        index === 0
          ? {
              txn_ref: "ZC2410000123",
              amount_iqd: 50000,
              status: "pending",
              type: "p2p",
              created_at: "2026-10-06T18:10:00+03:00",
            }
          : null,
      escalated,
      escalation_reasons: escalated
        ? [category === "fraud_report" ? "fraud_suspected" : "low_confidence"]
        : [],
      escalation_note: escalated
        ? category === "fraud_report"
          ? "Possible unauthorized access. Account & Security should investigate before any reply is approved."
          : "The category is uncertain. Review the original message and confirm the appropriate team."
        : null,
      draft_text: reply,
      final_text: ["approved", "edited"].includes(status) ? reply : null,
      citations: [],
      agent_trace: [],
      status,
      error: null,
      latency_ms: 0,
      cost_usd: 0,
      updated_at: date,
      reviews: [],
    }
  }
)

export const previewRuns: Run[] = [
  {
    id: 1,
    started_at: "2026-10-07T09:00:00+03:00",
    finished_at: "2026-10-07T09:01:00+03:00",
    mode: "cascade",
    status: "completed",
    total: 12,
    processed: 12,
    degraded: false,
    total_cost_usd: 0,
    counts: {
      by_status: { pending_review: 7, escalated: 3, approved: 1, edited: 1 },
    },
  },
]
