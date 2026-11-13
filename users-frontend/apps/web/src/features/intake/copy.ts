import ar from "./locales/ar.json"
import en from "./locales/en.json"
import type { Language } from "./types"

export type IntakeCopy = {
  title: string
  conversation: string
  message: string
  placeholder: string
  send: string
  attach: string
  remove: string
  review: string
  reviewNow: string
  partial: string
  submit: string
  unknown: string
  conflicting: string
  notApplicable: string
  processing: string
  updateError: string
  errorTitle: string
  fieldLabels: Record<string, string>
  continueChat: string
  startNew: string
  confirmNew: string
  confirmNewBody: string
  cancel: string
  retry: string
  refresh: string
  language: string
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
  phoneTitle: string
  phoneHelp: string
  phoneLabel: string
  phoneContinue: string
  phoneInvalid: string
  profileLabel: string
  changeNumber: string
  confirmChange: string
  confirmChangeBody: string
  receiptFor: string
  whyPrefix: string
  quickReplies: string
  choiceYes: string
  choiceNo: string
  choiceUnknown: string
  choiceNoReference: string
  choiceAttach: string
  hintPhone: string
  hintAmount: string
  hintReference: string
  hintDate: string
  typing: string
  sending: string
  uploading: string
  removing: string
  submitting: string
  notSent: string
  resend: string
  empty: string
}

export const copy: Record<Language, IntakeCopy> = { ar, en }
