import { useRef, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import {
  ArrowLeft,
  ArrowRight,
  Check,
  FileJson,
  FileUp,
  FlaskConical,
  LoaderCircle,
  LockKeyhole,
  Play,
  ShieldCheck,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FilterSelect, PageHeader } from "@/components/shared/workspace-ui"
import { useWorkspace } from "@/lib/workspace"
import { parseTicketFile } from "@/lib/imports"
import { api } from "@/lib/api"
import type { Mode, TicketInput } from "@/lib/types"

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
  const workspace = useWorkspace(),
    navigate = useNavigate(),
    input = useRef<HTMLInputElement>(null)
  const [tab, setTab] = useState("upload"),
    [fileName, setFileName] = useState("")
  const [tickets, setTickets] = useState<TicketInput[]>([]),
    [text, setText] = useState("")
  const [channel, setChannel] = useState<TicketInput["channel"]>("app"),
    [phone, setPhone] = useState("")
  const [mode, setMode] = useState<Mode>("cascade"),
    [error, setError] = useState("")
  const [busy, setBusy] = useState(false),
    [reading, setReading] = useState(false)
  const configured = workspace.health?.configured_modes.includes(mode)
  const selected =
    tab === "upload"
      ? tickets
      : text.trim()
        ? [{ text, channel, customer_phone: phone || null }]
        : []
  async function readFile(file?: File) {
    if (!file) return
    setReading(true)
    setError("")
    setTickets([])
    try {
      if (file.size > 10 * 1024 * 1024)
        throw new Error("Choose a file smaller than 10 MB.")
      const parsed = parseTicketFile(await file.text(), file.name.toLowerCase())
      setTickets(parsed)
      setFileName(file.name)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not read this file.")
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
      const run = await api.startRun(mode, selected)
      workspace.refresh()
      workspace.notify(`Batch #${run.id} submitted for processing.`)
      navigate(`/runs/${run.id}`)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not start the batch.")
    } finally {
      setBusy(false)
    }
  }
  return (
    <>
      <Link to="/runs" className="back-link">
        <ArrowLeft size={15} />
        Pipeline runs
      </Link>
      <PageHeader
        title="Prepare a new batch"
        description="Bring the messages. Let the pipeline do the sorting."
      />
      <div className="new-batch-layout">
        <Card className="batch-input-card">
          <CardHeader>
            <CardTitle className="section-title">
              <FileUp size={18} />
              Add your tickets
              <Badge variant="secondary">Up to 500 per batch</Badge>
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
                <TabsTrigger value="upload">Upload a file</TabsTrigger>
                <TabsTrigger value="paste">Paste a ticket</TabsTrigger>
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
                  <h3>Drop your ticket file here</h3>
                  <p>CSV, JSON or JSONL · up to 10 MB</p>
                  <Button
                    variant="outline"
                    onClick={() => input.current?.click()}
                    disabled={reading}
                  >
                    {reading ? "Reading file…" : "Choose file"}
                  </Button>
                  <input
                    ref={input}
                    type="file"
                    accept=".csv,.json,.jsonl"
                    aria-label="Upload ticket batch"
                    className="sr-only"
                    onChange={(e) => void readFile(e.target.files?.[0])}
                  />
                </div>
                <button
                  className="example-button"
                  onClick={() => {
                    setTickets(exampleTickets)
                    setFileName("Illustrative sample tickets")
                    setError("")
                  }}
                >
                  <FlaskConical size={16} />
                  <span>
                    Just trying it out?{" "}
                    <strong>Load 3 synthetic examples</strong>
                  </span>
                  <ArrowRight size={15} />
                </button>
                {tickets.length > 0 && (
                  <div className="batch-preview">
                    <div>
                      <Check size={16} />
                      <strong>{fileName}</strong>
                      <Badge variant="outline">{tickets.length} tickets</Badge>
                    </div>
                    {tickets.slice(0, 3).map((ticket, index) => (
                      <p key={index} dir="auto" lang="ar">
                        {ticket.text}
                      </p>
                    ))}
                    {tickets.length > 3 && (
                      <small>And {tickets.length - 3} more messages</small>
                    )}
                  </div>
                )}
              </TabsContent>
              <TabsContent value="paste">
                <label className="field-label" htmlFor="ticket-message">
                  Customer’s message
                </label>
                <Textarea
                  id="ticket-message"
                  className="paste-ticket"
                  dir="auto"
                  lang="ar"
                  maxLength={6000}
                  placeholder="الصق رسالة الزبون هنا…"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
                <div className="two-column">
                  <div>
                    <span className="field-label">Channel</span>
                    <FilterSelect
                      label="Ticket channel"
                      value={channel}
                      options={[
                        { value: "app", label: "ZainCash app" },
                        { value: "whatsapp", label: "WhatsApp" },
                        { value: "call_note", label: "Call note" },
                      ]}
                      onChange={(value) =>
                        setChannel(value as TicketInput["channel"])
                      }
                    />
                  </div>
                  <label className="field-label" htmlFor="customer-phone">
                    Customer phone (optional)
                    <Input
                      id="customer-phone"
                      placeholder="07…"
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
              <span>
                {selected.length} {selected.length === 1 ? "ticket" : "tickets"}{" "}
                ready
              </span>
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
                Start processing
              </Button>
            </div>
          </CardContent>
        </Card>
        <aside className="evidence-stack">
          <Card>
            <CardHeader>
              <CardTitle>Processing setup</CardTitle>
            </CardHeader>
            <CardContent>
              <label className="field-label">Classification strategy</label>
              <FilterSelect
                label="Classification strategy"
                value={mode}
                options={[
                  { value: "cascade", label: "Jev → Gemini fallback" },
                  { value: "jev", label: "Jev only" },
                  { value: "gemini", label: "Gemini only" },
                ]}
                onChange={(value) => setMode(value as Mode)}
              />
              <p className="muted small setup-description">
                Jev handles fast triage. Gemini can give a second opinion on
                uncertain cases. Low-confidence results are flagged for human
                review.
              </p>
              {!configured && (
                <div className="setup-callout">
                  <LockKeyhole size={18} />
                  <strong>Model setup needed</strong>
                  <p>
                    Set{" "}
                    {mode === "jev"
                      ? "TYPESAFE_API_KEY"
                      : mode === "gemini"
                        ? "OPENROUTER_API_KEY"
                        : "OPENROUTER_API_KEY and TYPESAFE_API_KEY"}{" "}
                    in the backend <code>.env</code>, then restart the API.
                  </p>
                  <Button variant="outline" onClick={workspace.refresh}>
                    Check connection
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="section-title">
                <FileJson size={17} />
                Expected file format
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="muted small">
                Each row needs a <code>text</code> or <code>message</code>{" "}
                field. ID, channel, phone and received date are optional.
              </p>
              <pre className="format-example">
                {'[{\n  "text": "حولت وما وصلت",\n  "channel": "app"\n}]'}
              </pre>
            </CardContent>
          </Card>
          <div className="human-note">
            <ShieldCheck size={22} />
            <p>
              Use synthetic customer tickets only. The pipeline prepares work
              for your support team; responses always need human approval.
            </p>
          </div>
        </aside>
      </div>
    </>
  )
}
