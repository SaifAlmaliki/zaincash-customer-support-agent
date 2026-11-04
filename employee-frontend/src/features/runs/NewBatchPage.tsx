import { useRef, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import {
  ArrowLeft,
  ArrowRight,
  Check,
  FileUp,
  FlaskConical,
  LoaderCircle,
  Play,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FilterSelect, PageHeader } from "@/components/shared/workspace-ui"
import { useWorkspace } from "@/lib/workspace"
import { fill, useCopy } from "@/lib/locale"
import { parseTicketFile } from "@/lib/imports"
import { api } from "@/lib/api"
import type { TicketInput } from "@/lib/types"

const exampleTickets: TicketInput[] = [
  {
    text: "حولت ٥٠ الف لاخوي امس وانخصمت من رصيدي بس ما وصلتله. رقم العملية ZC2410000123",
    channel: "app",
    received_at: "2026-10-07T09:30:00+03:00",
    customer_phone: "07809876543",
  },
  { text: "ما دا يوصلني رمز التحقق حتى افتح حسابي", channel: "whatsapp" },
  { text: "شكد عمولة التحويل لحساب بنكي؟", channel: "app" },
]

export function NewBatchPage() {
  const copy = useCopy()
  const text = copy.batch
  const workspace = useWorkspace(),
    navigate = useNavigate(),
    input = useRef<HTMLInputElement>(null)
  const [tab, setTab] = useState("upload"),
    [fileName, setFileName] = useState("")
  const [tickets, setTickets] = useState<TicketInput[]>([]),
    [message, setMessage] = useState("")
  const [channel, setChannel] = useState<TicketInput["channel"]>("app"),
    [phone, setPhone] = useState("")
  const [error, setError] = useState("")
  const [busy, setBusy] = useState(false),
    [reading, setReading] = useState(false)
  const configured = workspace.health?.configured_modes.includes("jev")
  const selected =
    tab === "upload"
      ? tickets
      : message.trim()
        ? [{ text: message, channel, customer_phone: phone || null }]
        : []
  const ready =
    selected.length === 0
      ? text.readyNone
      : selected.length === 1
        ? text.readyOne
        : fill(text.readyMany, { count: selected.length })
  async function readFile(file?: File) {
    if (!file) return
    setReading(true)
    setError("")
    setTickets([])
    try {
      if (file.size > 10 * 1024 * 1024) throw new Error(text.fileTooLarge)
      const parsed = parseTicketFile(await file.text(), file.name.toLowerCase())
      setTickets(parsed)
      setFileName(file.name)
    } catch (e) {
      setError(e instanceof Error ? e.message : text.readFailed)
    } finally {
      setReading(false)
      if (input.current) input.current.value = ""
    }
  }
  async function start() {
    if (busy || !selected.length) return
    setBusy(true)
    setError("")
    try {
      const run = await api.startRun(selected)
      workspace.refresh()
      workspace.notify(fill(text.submitted, { id: run.id }))
      navigate(`/runs/${run.id}`)
    } catch (e) {
      setError(e instanceof Error ? e.message : text.startFailed)
    } finally {
      setBusy(false)
    }
  }
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        {text.back}
      </Link>
      <PageHeader
        title={copy.pages.newBatchTitle}
        description={copy.pages.newBatchDescription}
      />
      <div className="new-batch-layout">
        <Card className="batch-input-card">
          <CardHeader>
            <CardTitle className="section-title">
              <FileUp size={18} />
              {text.addTickets}
              <Badge variant="secondary">{text.limit}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs
              value={tab}
              onValueChange={(value) => {
                setTab(value)
                setError("")
              }}
            >
              <TabsList className="input-tabs">
                <TabsTrigger value="upload">{text.uploadTab}</TabsTrigger>
                <TabsTrigger value="paste">{text.pasteTab}</TabsTrigger>
              </TabsList>
              <TabsContent value="upload">
                <div
                  className="upload-zone"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault()
                    void readFile(e.dataTransfer.files[0])
                  }}
                >
                  <div className="upload-symbol">
                    <FileUp size={30} strokeWidth={1.4} />
                  </div>
                  <h3>{text.dropTitle}</h3>
                  <p>{text.dropHint}</p>
                  <Button
                    variant="outline"
                    onClick={() => input.current?.click()}
                    disabled={reading}
                  >
                    {reading ? text.reading : text.chooseFile}
                  </Button>
                  <input
                    ref={input}
                    type="file"
                    accept=".csv,.json,.jsonl"
                    aria-label={text.uploadLabel}
                    className="sr-only"
                    onChange={(e) => void readFile(e.target.files?.[0])}
                  />
                </div>
                <button
                  className="example-button"
                  onClick={() => {
                    setTickets(exampleTickets)
                    setFileName(text.sampleName)
                    setError("")
                  }}
                >
                  <FlaskConical size={16} />
                  <span>
                    {text.trySample} <strong>{text.loadSample}</strong>
                  </span>
                  <ArrowRight size={15} />
                </button>
                {tickets.length > 0 && (
                  <div className="batch-preview">
                    <div>
                      <Check size={16} />
                      <strong>{fileName}</strong>
                      <Badge variant="outline">
                        {fill(text.ticketCount, { count: tickets.length })}
                      </Badge>
                    </div>
                    {tickets.slice(0, 3).map((ticket, index) => (
                      <p key={index} dir="auto" lang="ar">
                        {ticket.text}
                      </p>
                    ))}
                    {tickets.length > 3 && (
                      <small>
                        {fill(text.moreMessages, { count: tickets.length - 3 })}
                      </small>
                    )}
                  </div>
                )}
              </TabsContent>
              <TabsContent value="paste">
                <label className="field-label" htmlFor="ticket-message">
                  {text.messageLabel}
                </label>
                <Textarea
                  id="ticket-message"
                  className="paste-ticket"
                  dir="auto"
                  lang="ar"
                  maxLength={6000}
                  placeholder={text.messagePlaceholder}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
                <div className="two-column">
                  <div>
                    <span className="field-label">{text.channel}</span>
                    <FilterSelect
                      label={text.channelLabel}
                      value={channel}
                      options={[
                        { value: "app", label: text.channelApp },
                        { value: "whatsapp", label: text.channelWhatsapp },
                        { value: "call_note", label: text.channelCall },
                      ]}
                      onChange={(value) =>
                        setChannel(value as TicketInput["channel"])
                      }
                    />
                  </div>
                  <label className="field-label" htmlFor="customer-phone">
                    {text.phone}
                    <Input
                      id="customer-phone"
                      className="phone-field"
                      dir="ltr"
                      inputMode="tel"
                      placeholder={text.phonePlaceholder}
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                    />
                  </label>
                </div>
              </TabsContent>
            </Tabs>
            {error && (
              <p className="error-text" role="alert">
                {error}
              </p>
            )}
            <div className="batch-submit">
              <span>{ready}</span>
              <Button
                size="lg"
                disabled={
                  busy ||
                  !selected.length ||
                  !configured ||
                  Boolean(workspace.connectionError)
                }
                onClick={() => void start()}
              >
                {busy ? (
                  <LoaderCircle size={16} className="animate-spin" />
                ) : (
                  <Play size={16} />
                )}
                {text.start}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  )
}
