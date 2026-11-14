import { useState } from "react"

export function retainLast<T>(last: T | null, next: T | null): T | null {
  return next ?? last
}

/** Keeps showing the last loaded value while a new request for it is in flight. */
export function useLastData<T>(data: T | null): T | null {
  const [last, setLast] = useState<T | null>(data)
  if (data !== null && data !== last) setLast(data)
  return retainLast(last, data)
}
