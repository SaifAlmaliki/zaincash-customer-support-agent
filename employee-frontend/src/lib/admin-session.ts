import { useSyncExternalStore } from "react"

export type AdminSession = { token: string; name: string }

const storageKey = "zaincash-admin-token"
const listeners = new Set<() => void>()

function read(): AdminSession | null {
  try {
    const raw = sessionStorage.getItem(storageKey)
    if (!raw) return null
    const value = JSON.parse(raw) as Partial<AdminSession>
    return typeof value.token === "string" && value.token && typeof value.name === "string" && value.name
      ? { token: value.token, name: value.name }
      : null
  } catch {
    /* No storage (tests, private browsing): start locked. */
    return null
  }
}

let session: AdminSession | null = read()

export function getAdminSession() {
  return session
}

export function setAdminSession(next: AdminSession | null) {
  session = next
  try {
    if (next) sessionStorage.setItem(storageKey, JSON.stringify(next))
    else sessionStorage.removeItem(storageKey)
  } catch {
    /* The session still applies until the page reloads. */
  }
  listeners.forEach((listener) => listener())
}

function subscribe(listener: () => void) {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export function useAdminSession() {
  return useSyncExternalStore(subscribe, getAdminSession, getAdminSession)
}
