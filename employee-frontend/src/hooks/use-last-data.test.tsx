import { renderToStaticMarkup } from "react-dom/server"
import { expect, it } from "vitest"
import { retainLast, useLastData } from "./use-last-data"

it("keeps the last value while the next one loads", () => {
  expect(retainLast({ n: 1 }, null)).toEqual({ n: 1 })
  expect(retainLast({ n: 1 }, { n: 2 })).toEqual({ n: 2 })
  expect(retainLast(null, null)).toBeNull()
})

it("returns the current data and null before anything loaded", () => {
  function Probe({ data }: { data: string | null }) {
    return <span>{useLastData(data) ?? "none"}</span>
  }
  expect(renderToStaticMarkup(<Probe data="fresh" />)).toContain("fresh")
  expect(renderToStaticMarkup(<Probe data={null} />)).toContain("none")
})
