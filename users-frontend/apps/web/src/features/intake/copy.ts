export type IntakeCopy = {
  title: string
  subtitle: string
  conversation: string
  message: string
  send: string
  attach: string
  remove: string
  review: string
  reviewNow: string
  partial: string
  submit: string
  unknown: string
  continueChat: string
  startNew: string
  confirmNew: string
  confirmNewBody: string
  cancel: string
  retry: string
  refresh: string
  english: string
  arabic: string
  you: string
  assistant: string
  screenshots: string
  facts: string
  issues: string
  receiptTitle: string
  receiptProcessing: string
  receiptReady: string
  receiptAttention: string
  uploadProgress: string
  imageUnavailable: string
  resumeUnavailable: string
  empty: string
}

export const copy: Record<"ar" | "en", IntakeCopy> = {
  ar: {
    title: "زين كاش",
    subtitle: "احچي ويا الدعم قبل ما تنرسل التذكرة",
    conversation: "المحادثة",
    message: "رسالتك",
    send: "إرسال",
    attach: "أرفق لقطات",
    remove: "إزالة",
    review: "راجع تفاصيل المشكلة",
    reviewNow: "راجع المعلومات الحالية",
    partial: "بعض التفاصيل بعدها مو معروفة",
    submit: "إرسال التذكرة",
    unknown: "غير معروف",
    continueChat: "كمّل المحادثة",
    startNew: "تقرير جديد",
    confirmNew: "ابدأ تقرير جديد",
    confirmNewBody: "التقرير الحالي يبقى محفوظ. هالشاشة راح تبدي تقرير منفصل.",
    cancel: "إلغاء",
    retry: "إعادة المحاولة",
    refresh: "تحديث",
    english: "English",
    arabic: "العربية",
    you: "أنت",
    assistant: "الدعم",
    screenshots: "لقطات الشاشة",
    facts: "التفاصيل",
    issues: "مشاكل إضافية",
    receiptTitle: "وصلت التذكرة",
    receiptProcessing: "استلمنا تقريرك. موظف الدعم بعده يراجعه.",
    receiptReady: "انرسل التقرير. موظف الدعم يگدر يراجعه.",
    receiptAttention: "انرسل التقرير، والمعالجة تحتاج متابعة.",
    uploadProgress: "جاري رفع الصورة",
    imageUnavailable: "الصورة غير متاحة",
    resumeUnavailable: "المتصفح ما يگدر يحفظ المحادثة للرجوع إلها.",
    empty: "اكتب شنو صار، أو أرفق لقطة للخطأ.",
  },
  en: {
    title: "ZainCash",
    subtitle: "Tell support what happened before a ticket is sent",
    conversation: "Conversation",
    message: "Your message",
    send: "Send",
    attach: "Attach screenshots",
    remove: "Remove",
    review: "Review your report",
    reviewNow: "Review what I have",
    partial: "Some details are still unknown",
    submit: "Submit ticket",
    unknown: "Unknown",
    continueChat: "Continue conversation",
    startNew: "Start a new report",
    confirmNew: "Start new report",
    confirmNewBody: "The current report stays saved. This screen will start a separate one.",
    cancel: "Cancel",
    retry: "Retry",
    refresh: "Refresh",
    english: "English",
    arabic: "العربية",
    you: "You",
    assistant: "Support",
    screenshots: "Screenshots",
    facts: "Details",
    issues: "Additional issues",
    receiptTitle: "Ticket received",
    receiptProcessing: "We received your report. An employee still needs to review it.",
    receiptReady: "Your report was submitted. An employee can review it.",
    receiptAttention: "Your report was submitted, and processing needs attention.",
    uploadProgress: "Uploading screenshot",
    imageUnavailable: "Image unavailable",
    resumeUnavailable: "This browser cannot save the conversation for later.",
    empty: "Describe what happened, or attach a screenshot of the error.",
  },
}
