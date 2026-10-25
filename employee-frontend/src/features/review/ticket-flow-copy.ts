import { humanize } from "../../lib/format"

const ARABIC = /[\u0600-\u06FF\u0750-\u077F]/

export function isArabicMessage(text: string): boolean {
  return ARABIC.test(text)
}

const EN = {
  messageHadText: "The message had text.",
  askedGeminiDirectly: "This run asked Gemini directly.",
  jevWasSure: "Jev was already sure.",
  emptyEnded: "The empty message ended the path.",
  runStopped: "The run stopped.",
  chartFailed: "The chart could not be drawn.",
  notUsed: "not used",
  notRecorded: "not recorded",
  notAsked: "This step was not asked.",
  notRecordedStep: "This step was not recorded.",
  recorded: "Recorded.",
  prepareReceived: "Read the {channel} message ({length} characters).",
  prepareEmpty: "No customer message was recorded for this step.",
  prepareProduced: "Arabic digits were converted to 0–9, and card numbers were hidden.",
  emptyReceived: "The customer message was empty.",
  emptyProduced: "Held for a person because the message was empty.",
  cleaned: "Received the cleaned message.",
  jevSure: "Jev classified this ticket. Gemini was not asked. {category}, {confidence} confidence, priority {priority}.",
  jevUnsure: "Jev was unsure, so Gemini was asked.",
  geminiAfterJev: "Received Jev's uncertain classification.",
  classified: "{category}, {confidence} confidence, priority {priority}.",
  extractReceived: "Received the classification {category}.",
  fieldLine: "{label}: {value}.",
  fieldFrom: "{label}: {value} from “{span}”.",
  fieldMissing: "{label}: This field was not recorded.",
  notStated: "Not stated",
  lookupReceived: "Received the extracted details.",
  lookupMissing: "Lookup was not recorded.",
  decideReceived: "Received the investigation result.",
  assigned: "Assigned to {team}.",
  held: "Held for a person: {reasons}.",
  noEscalation: "No escalation. Ready for review.",
  draftReceived: "Received {category} for {team}.",
  draftSaved: "A reply was saved for a person to review.",
  draftMissing: "No reply was saved.",
  citations: "{count} policy passages were cited.",
  citationOne: "1 policy passage was cited.",
  credentialPassed: "The credential check passed.",
  credentialFailed: "The credential check failed.",
  credentialUnavailable: "The credential check was unavailable.",
  credentialUnrecorded: "No credential check was recorded.",
  safetyFlagged: "Safety checks flagged {findings}.",
  safetyClear: "No safety-check findings were recorded.",
  draftCheckReasons: "Draft {status}: {reasons}.",
  draftCheckPlain: "Draft {status}.",
  draftStatusUnknown: "status unknown",
  noPriority: "no priority",
  noTeam: "no team",
  noCategory: "Unclassified",
  toolFallback: "Ran {name}",
  toolOk: "{action}. Completed.",
  toolCancelled: "{action}. Cancelled.",
  toolIncomplete: "{action}. Did not complete.",
  toolPlain: "{action}.",
  lookupMatched: "One transaction matched.",
  lookupAmount: "A transaction was found, but the amount in the message does not match the record.",
  lookupDate: "A transaction was found, but the date does not match the record.",
  lookupMissingStatus: "No transaction matched the details in the message.",
  lookupAmbiguous: "Several transactions matched, so none was selected.",
  lookupSkipped: "This issue does not need a transaction lookup.",
} as const

const AR: Record<keyof typeof EN, string> = {
  messageHadText: "الرسالة تحتوي على نص.",
  askedGeminiDirectly: "هذا التشغيل طلب جيميناي مباشرة.",
  jevWasSure: "جيف كان متأكدًا.",
  emptyEnded: "الرسالة الفارغة أنهت المسار.",
  runStopped: "توقف التشغيل.",
  chartFailed: "تعذّر رسم المسار.",
  notUsed: "لم تُستخدم",
  notRecorded: "غير مسجّلة",
  notAsked: "لم يُطلب تنفيذ هذه الخطوة.",
  notRecordedStep: "هذه الخطوة غير مسجّلة.",
  recorded: "مُسجّلة.",
  prepareReceived: "قُرئت رسالة {channel} ({length} حرفًا).",
  prepareEmpty: "لم تُسجَّل رسالة للعميل في هذه الخطوة.",
  prepareProduced: "حُوّلت الأرقام العربية إلى 0–9، وأُخفيت أرقام البطاقات.",
  emptyReceived: "كانت رسالة العميل فارغة.",
  emptyProduced: "أُبقيت لموظف لأن الرسالة كانت فارغة.",
  cleaned: "استلم الرسالة بعد تنظيفها.",
  jevSure: "صنّف جيف هذه التذكرة. لم يُسأل جيميناي. {category}، ثقة {confidence}، أولوية {priority}.",
  jevUnsure: "جيف لم يكن متأكدًا، لذلك سُئل جيميناي.",
  geminiAfterJev: "استلم تصنيف جيف غير المؤكد.",
  classified: "{category}، ثقة {confidence}، أولوية {priority}.",
  extractReceived: "استلم التصنيف {category}.",
  fieldLine: "{label}: {value}.",
  fieldFrom: "{label}: {value} من «{span}».",
  fieldMissing: "{label}: هذا الحقل غير مسجّل.",
  notStated: "غير مذكور",
  lookupReceived: "استلم التفاصيل المستخرجة.",
  lookupMissing: "لم يُسجَّل البحث.",
  decideReceived: "استلم نتيجة التحقق.",
  assigned: "أُسندت إلى {team}.",
  held: "أُبقيت لموظف: {reasons}.",
  noEscalation: "لا يوجد تصعيد. جاهزة للمراجعة.",
  draftReceived: "استلم {category} لفريق {team}.",
  draftSaved: "حُفظ رد ليراجعه موظف.",
  draftMissing: "لم يُحفظ رد.",
  citations: "استُشهد بـ {count} مقاطع من السياسة.",
  citationOne: "استُشهد بمقطع واحد من السياسة.",
  credentialPassed: "نجح فحص بيانات الدخول.",
  credentialFailed: "فشل فحص بيانات الدخول.",
  credentialUnavailable: "فحص بيانات الدخول غير متاح.",
  credentialUnrecorded: "لم يُسجَّل فحص بيانات الدخول.",
  safetyFlagged: "فحوصات السلامة أشارت إلى {findings}.",
  safetyClear: "لم تُسجَّل ملاحظات من فحوصات السلامة.",
  draftCheckReasons: "فحص المسودة ({status}): {reasons}.",
  draftCheckPlain: "فحص المسودة ({status}).",
  draftStatusUnknown: "حالة غير معروفة",
  noPriority: "بدون أولوية",
  noTeam: "بدون فريق",
  noCategory: "بدون تصنيف",
  toolFallback: "شغّل الأداة {name}",
  toolOk: "{action}. اكتمل.",
  toolCancelled: "{action}. أُلغي.",
  toolIncomplete: "{action}. لم يكتمل.",
  toolPlain: "{action}.",
  lookupMatched: "تطابق تحويل واحد.",
  lookupAmount: "وُجد تحويل، لكن المبلغ في الرسالة لا يطابق السجل.",
  lookupDate: "وُجد تحويل، لكن التاريخ لا يطابق السجل.",
  lookupMissingStatus: "لا يوجد تحويل يطابق التفاصيل في الرسالة.",
  lookupAmbiguous: "تطابق أكثر من تحويل، لذلك لم يُختَر أي منها.",
  lookupSkipped: "هذه المشكلة لا تحتاج إلى البحث عن تحويل.",
}

export type SentenceId = keyof typeof EN

export function sentence(id: SentenceId, arabic: boolean, vars: Record<string, string | number> = {}): string {
  return (arabic ? AR : EN)[id].replace(/\{(\w+)\}/g, (_, key: string) => String(vars[key] ?? ""))
}

const TEAMS_AR: Record<string, string> = {
  "Payments Ops": "عمليات المدفوعات",
  Disputes: "النزاعات",
  "Account & Security": "الحساب والأمان",
  "Agent Network": "شبكة الوكلاء",
  Cards: "البطاقات",
  "Tech Support": "الدعم التقني",
  "General Care": "الرعاية العامة",
}

const REASONS_AR: Record<string, string> = {
  low_confidence: "ثقة منخفضة",
  classifier_disagreement: "اختلاف في التصنيف",
  fraud_suspected: "احتيال محتمل",
  multi_issue: "أكثر من مشكلة",
  asks_for_human: "طلب التحدث مع موظف",
  missing_required_fields: "تفاصيل مطلوبة ناقصة",
  txn_not_found: "لا توجد عملية مطابقة",
  txn_ambiguous: "عدة عمليات مطابقة",
  amount_mismatch: "المبلغ لا يطابق السجل",
  date_mismatch: "التاريخ لا يطابق السجل",
  empty_ticket: "الرسالة فارغة",
  llm_unavailable: "نموذج الصياغة غير متاح",
  draft_failed_guardrail: "المسودة لم تجتز فحص الأمان",
  no_kb_support: "لا يوجد مستند سياسة يدعم الرد",
}

export function teamName(id: string, arabic: boolean): string {
  if (!arabic) return id
  return TEAMS_AR[id] || id
}

export function reasonName(id: string, arabic: boolean): string {
  const key = id.trim().toLowerCase().replaceAll(" ", "_")
  if (!arabic) return humanize(key)
  return REASONS_AR[key] || REASONS_AR[id] || humanize(id)
}

export function channelName(channel: string, arabic: boolean): string {
  if (channel === "app") return arabic ? "تطبيق زين كاش" : "ZainCash app"
  if (channel === "whatsapp") return arabic ? "واتساب" : "WhatsApp"
  if (channel === "call_note") return arabic ? "ملاحظة مكالمة" : "call note"
  return humanize(channel)
}

const FIELDS: Record<string, [string, string]> = {
  txn_ref: ["Transaction reference", "الرقم المرجعي"],
  amount: ["Amount", "المبلغ"],
  date: ["Date", "التاريخ"],
  phone: ["Phone number", "رقم الهاتف"],
}

export function fieldLabel(key: string, arabic: boolean): string {
  const pair = FIELDS[key]
  if (!pair) return humanize(key)
  return arabic ? pair[1] : pair[0]
}

const LOOKUP: Record<string, SentenceId> = {
  matched: "lookupMatched",
  amount_mismatch: "lookupAmount",
  date_mismatch: "lookupDate",
  not_found: "lookupMissingStatus",
  ambiguous: "lookupAmbiguous",
  not_applicable: "lookupSkipped",
}

export function lookupSentence(status: string | null, arabic: boolean): string {
  if (!status) return sentence("lookupMissing", arabic)
  const id = LOOKUP[status]
  return id ? sentence(id, arabic) : humanize(status)
}

const TOOLS: Record<string, [string, string]> = {
  lookup_transaction: ["Looked up a transaction reference", "بحث عن رقم مرجعي للتحويل"],
  search_transactions: ["Searched transactions", "بحث في التحويلات"],
  get_customer_recent_transactions: ["Listed recent transactions", "عرض آخر التحويلات"],
  get_customer_ticket_history: ["Checked earlier tickets for this customer", "راجع التذاكر السابقة لهذا العميل"],
  check_service_status: ["Checked whether a service was disrupted", "تحقق من حالة الخدمة"],
  search_knowledge_base: ["Searched the knowledge base", "بحث في قاعدة المعرفة"],
  flag_for_human: ["Flagged the ticket for a person", "أحال التذكرة إلى موظف"],
  submit_draft: ["Submitted a draft reply", "أرسل مسودة رد"],
}

const SAFE_ARGS = ["query", "txn_ref", "phone", "service", "reason"] as const

export function toolLine(event: { tool?: string; status?: string; arguments?: unknown }, arabic: boolean): string {
  const name = event.tool || "a lookup"
  const args = event.arguments
  const record = args !== null && typeof args === "object" && !Array.isArray(args) ? (args as Record<string, unknown>) : {}
  const key = SAFE_ARGS.find((item) => typeof record[item] === "string" && String(record[item]).trim())
  const raw = key ? String(record[key]).trim() : ""
  const detail = key === "reason" && raw ? reasonName(raw, arabic) : raw
  const pair = TOOLS[name]
  const base = pair ? (arabic ? pair[1] : pair[0]) : (arabic ? sentence("toolFallback", true, { name }) : humanize(name))
  const action = `${base}${detail ? `: ${detail}` : ""}`
  if (event.status === "ok") return sentence("toolOk", arabic, { action })
  if (event.status === "cancelled") return sentence("toolCancelled", arabic, { action })
  if (event.status) return sentence("toolIncomplete", arabic, { action })
  return sentence("toolPlain", arabic, { action })
}

function texts(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string" && item.trim() !== "") : []
}

export function checkLines(
  events: { kind?: string; status?: string; findings?: unknown; credential_check_degraded?: unknown; reasons?: unknown }[],
  arabic: boolean,
): string[] {
  return events.flatMap((event) => {
    if (event.kind === "guardrail") {
      const findings = texts(event.findings)
      if (event.credential_check_degraded === true) return [sentence("credentialUnavailable", arabic)]
      const credential = event.status === "passed" && findings.length === 0
        ? sentence("credentialPassed", arabic)
        : findings.length
          ? sentence("credentialFailed", arabic)
          : sentence("credentialUnrecorded", arabic)
      const safety = findings.length
        ? sentence("safetyFlagged", arabic, { findings: findings.map(humanize).join(", ") })
        : sentence("safetyClear", arabic)
      return [credential, safety]
    }
    if (event.kind === "draft") {
      const reasons = texts(event.reasons).map((item) => reasonName(item, arabic)).join(arabic ? "، " : ", ")
      const status = event.status
        ? arabic
          ? { submitted: "أُرسلت", passed: "نجح", failed: "فشل" }[event.status] || humanize(event.status)
          : humanize(event.status).toLowerCase()
        : sentence("draftStatusUnknown", arabic)
      return [reasons ? sentence("draftCheckReasons", arabic, { status, reasons }) : sentence("draftCheckPlain", arabic, { status })]
    }
    return []
  })
}
