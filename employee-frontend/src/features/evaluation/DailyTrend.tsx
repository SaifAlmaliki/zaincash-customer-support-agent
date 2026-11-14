import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { msLabel, usd } from "@/lib/format"
import { useCopy } from "@/lib/locale"
import type { UsageDay } from "@/lib/types"
import { trendGeometry } from "./usage-view"

export function DailyTrend({ days }: { days: UsageDay[] }) {
  const copy = useCopy().evaluation.trend
  const g = trendGeometry(days, 80)
  return (
    <Card className="data-card usage-trend">
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {!days.length ? (
          <p className="muted small">{copy.empty}</p>
        ) : (
          <>
            <div dir="ltr">
              <svg viewBox={`0 0 ${g.width} ${g.height + 20}`} role="img" aria-label={copy.title}>
                {g.bars.map((bar) => (
                  <g key={bar.day.date}>
                    <rect className="usage-bar" x={bar.x} y={bar.y} width={24} height={g.height - bar.y}>
                      <title>{`${bar.day.date} · ${usd(bar.day.cost_usd)}`}</title>
                    </rect>
                    <text x={bar.x + 12} y={g.height + 14} textAnchor="middle">{bar.day.date.slice(5)}</text>
                  </g>
                ))}
                <path className="usage-line" d={g.line} fill="none" />
                {g.points.map((p, i) => (
                  <circle key={days[i].date} className="usage-dot" cx={p.x} cy={Math.max(3, p.y)} r={3}>
                    <title>{`${days[i].date} · p95 ${msLabel(days[i].latency_p95_ms)}`}</title>
                  </circle>
                ))}
              </svg>
            </div>
            <table className="sr-only">
              <thead>
                <tr><th>{copy.date}</th><th>{copy.cost}</th><th>{copy.p95}</th></tr>
              </thead>
              <tbody>
                {days.map((d) => (
                  <tr key={d.date}><td>{d.date}</td><td>{usd(d.cost_usd)}</td><td>{msLabel(d.latency_p95_ms)}</td></tr>
                ))}
              </tbody>
            </table>
            <p className="usage-legend">
              <span className="usage-legend-bar" /> {copy.cost} <span className="usage-legend-line" /> {copy.p95}
            </p>
          </>
        )}
      </CardContent>
    </Card>
  )
}
