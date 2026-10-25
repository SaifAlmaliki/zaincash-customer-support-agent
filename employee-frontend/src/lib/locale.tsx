import { useSyncExternalStore } from "react"
import ar from "@/locales/ar.json"
import en from "@/locales/en.json"

export type Locale = "ar" | "en"
export type Copy = typeof en

const copies: Record<Locale, Copy> = { ar, en }
const storageKey = "zaincash-employee-locale"
const listeners = new Set<() => void>()

function storedLocale(): Locale {
  try {
    const saved = localStorage.getItem(storageKey)
    if (saved === "ar" || saved === "en") return saved
  } catch {
    /* Private browsing can deny storage. Arabic stays the default. */
  }
  return "ar"
}

let locale: Locale = storedLocale()

export function getLocale() {
  return locale
}

export function getCopy() {
  return copies[locale]
}

export function fill(template: string, values: Record<string, string | number>) {
  return template.replace(/\{(\w+)\}/g, (_, key: string) => String(values[key] ?? ""))
}

export function applyDocumentLocale(next = locale) {
  if (typeof document === "undefined") return
  document.documentElement.lang = next
  document.documentElement.dir = next === "ar" ? "rtl" : "ltr"
  document.title = copies[next].meta.title
  const description = document.querySelector('meta[name="description"]')
  description?.setAttribute("content", copies[next].meta.description)
}

export function setLocale(next: Locale) {
  locale = next
  try {
    localStorage.setItem(storageKey, next)
  } catch {
    /* The choice still applies for this visit. */
  }
  applyDocumentLocale(next)
  listeners.forEach((listener) => listener())
}

function subscribe(listener: () => void) {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export function useCopy() {
  return useSyncExternalStore(subscribe, getCopy, getCopy)
}

export function useLocale() {
  const copy = useCopy()
  return { locale: getLocale(), setLocale, copy }
}

applyDocumentLocale()
