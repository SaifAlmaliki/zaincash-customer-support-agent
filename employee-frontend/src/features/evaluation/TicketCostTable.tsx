import { ChevronLeft, ChevronRight, ListTree } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { FilterSelect, StatusBadge } from "@/components/shared/workspace-ui"
import { categoryLabel, dateLabel, msLabel, timeLabel, usd } from "@/lib/format"
import { fill, useCopy } from "@/lib/locale"
import type { UsageTicketPage } from "@/lib/types"
import { costSegments, processLabel } from "./usage-view"

type Sort = "recent" | "cost" | "time"

export function TicketCostTable({ page, sort, onSort, offset, limit, onPage, onOpen }: {
  page: UsageTicketPage
  sort: Sort
  onSort: (sort: Sort) => void
  offset: number
  limit: number
  onPage: (offset: number) => void
  onOpen: (resultId: number) => void
}) {
  const copy = useCopy().evaluation
  const t = copy.tickets
  return (
    <Card className="data-card usage-tickets">
      <CardHeader className="usage-tickets-header">
        <CardTitle>{t.title}</CardTitle>
        <FilterSelect label={t.sort} value={sort}
          options={[{ value: "recent", label: t.sortRecent }, { value: "cost", label: t.sortCost },
                    { value: "time", label: t.sortTime }]}
          onChange={(value) => onSort(value as Sort)} />
      </CardHeader>
      <CardContent>
        {!page.items.length ? (
          <p className="muted small">{t.empty}</p>
        ) : (
          <>
            <div className="usage-scroll">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t.ticket}</TableHead>
                    <TableHead>{t.received}</TableHead>
                    <TableHead>{t.status}</TableHead>
                    <TableHead className="usage-col-wide">{t.category}</TableHead>
                    <TableHead>{t.cost}</TableHead>
                    <TableHead className="usage-col-mid">{t.breakdown}</TableHead>
                    <TableHead>{t.aiTime}</TableHead>
                    <TableHead className="usage-col-wide">{t.draftTime}</TableHead>
                    <TableHead>{t.errors}</TableHead>
                    <TableHead />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {page.items.map((item) => (
                    <TableRow key={item.result_id}>
                      <TableCell>
                        <bdi dir="ltr" className="ticket-id usage-ticket-id" title={item.external_id}>
                          {item.external_id}
                        </bdi>
                      </TableCell>
                      <TableCell>
                        {dateLabel(item.received_at)}
                        <small className="block-muted">{timeLabel(item.received_at)}</small>
                      </TableCell>
                      <TableCell><StatusBadge status={item.status} /></TableCell>
                      <TableCell className="usage-col-wide">{categoryLabel(item.category)}</TableCell>
                      <TableCell>
                        {usd(item.total_cost_usd)}
                        {item.intake_cost_usd > 0 && (
                          <small className="block-muted">{fill(t.intake, { value: usd(item.intake_cost_usd) })}</small>
                        )}
                      </TableCell>
                      <TableCell className="usage-col-mid">
                        {item.detail_recorded ? (
                          <span className="usage-stack">
                            {costSegments(item.cost_by_process).map((s) => (
                              <span key={s.process} className={`usage-seg usage-seg-${s.process}`}
                                    style={{ width: `${s.share * 100}%` }}
                                    title={`${processLabel(s.process, copy)} · ${usd(item.cost_by_process[s.process])}`} />
                            ))}
                          </span>
                        ) : (
                          <small className="muted">{t.notRecorded}</small>
                        )}
                      </TableCell>
                      <TableCell>{msLabel(item.ai_time_ms)}</TableCell>
                      <TableCell className="usage-col-wide">{msLabel(item.draft_time_ms)}</TableCell>
                      <TableCell className={item.errors ? "error-text" : undefined}>{item.errors}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="icon-sm" onClick={() => onOpen(item.result_id)}
                                aria-label={fill(t.open, { id: item.external_id })}>
                          <ListTree size={15} />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <div className="usage-pager">
              <span>{fill(t.range, { from: offset + 1, to: offset + page.items.length, total: page.total })}</span>
              <Button variant="outline" size="icon-sm" aria-label={t.previous} disabled={offset === 0}
                      onClick={() => onPage(Math.max(0, offset - limit))}>
                <ChevronRight className="usage-pager-icon" size={15} />
              </Button>
              <Button variant="outline" size="icon-sm" aria-label={t.next}
                      disabled={offset + page.items.length >= page.total} onClick={() => onPage(offset + limit)}>
                <ChevronLeft className="usage-pager-icon" size={15} />
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
