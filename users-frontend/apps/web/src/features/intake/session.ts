import type { SavedSession } from "./types"

export interface SessionStorage {
  load(): SavedSession | null
  save(value: SavedSession): void
  clear(): void
}

const STORAGE_KEY = "zaincash.intake.session"

export function browserSessionStorage(storage?: Storage): SessionStorage {
  const currentStorage = () => storage ?? window.localStorage
  return {
    load() {
      const raw = currentStorage().getItem(STORAGE_KEY)
      if (!raw) return null
      try {
        const parsed = JSON.parse(raw) as SavedSession
        if (!parsed?.credentials?.session_id || !parsed.credentials.token) return null
        return parsed
      } catch {
        return null
      }
    },
    save(value) {
      currentStorage().setItem(STORAGE_KEY, JSON.stringify(value))
    },
    clear() {
      currentStorage().removeItem(STORAGE_KEY)
    },
  }
}

export function memoryStorage(initial: SavedSession | null = null): SessionStorage {
  let current = initial
  return {
    load: () => current,
    save(value) {
      current = value
    },
    clear() {
      current = null
    },
  }
}
