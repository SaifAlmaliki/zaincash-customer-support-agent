import { useMemo, useState } from "react"
import { CheckCircle2, CircleAlert, LoaderCircle, RefreshCw } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ConfirmDialog } from "@/components/shared/workspace-ui"
import { useResource } from "@/hooks/use-resource"
import { adminApi, adminRequest } from "@/lib/api"
import { fill, useCopy } from "@/lib/locale"
import type { CatalogModel, CatalogProvider, ModelChoiceInput, StepModel } from "@/lib/types"
import { adminErrorMessage } from "./admin-errors"
import {
  buildOptions,
  canSave,
  catalogView,
  choiceKey,
  filterModels,
  isValidTemperature,
  offersThinking,
  priceLabel,
  type TestedChoice,
} from "./model-choice"

export function ChangeModelDialog({
  step,
  changedBy,
  onClose,
  onSaved,
}: {
  step: StepModel
  changedBy: string
  onClose: () => void
  onSaved: () => void
}) {
  const copy = useCopy()
  const text = copy.models
  const [provider, setProvider] = useState(
    step.providers.includes(step.provider) ? step.provider : step.providers[0],
  )
  const [refresh, setRefresh] = useState(0)
  const [query, setQuery] = useState("")
  const [selected, setSelected] = useState(step.model)
  const [custom, setCustom] = useState("")
  const [temperature, setTemperature] = useState(step.options.temperature?.toString() ?? "")
  const [think, setThink] = useState(step.options.think ?? false)
  const [tested, setTested] = useState<TestedChoice | null>(null)
  const [busy, setBusy] = useState<"test" | "save" | null>(null)
  const [error, setError] = useState("")
  const [confirm, setConfirm] = useState(false)
  const catalog = useResource<{ providers: CatalogProvider[] }>(
    `/models/catalog?step=${step.step}&refresh=${refresh > 0}`,
    refresh,
    0,
    adminRequest,
  )
  const current = catalog.data?.providers.find((item) => item.provider === provider)
  const view = catalogView(current)
  const model = custom.trim() || selected
  const entry = current?.entries.find((item) => item.id === model)
  const tunable = step.step !== "classify" && step.step !== "embed"
  const thinking = tunable && offersThinking(entry)
  const choice: ModelChoiceInput = {
    provider,
    model,
    options: buildOptions(tunable ? temperature : "", thinking ? think : null),
  }
  const temperatureOk = isValidTemperature(temperature)
  const savable = canSave(choice, tested, tunable ? temperature : "")
  const visible = useMemo(() => filterModels(current?.entries ?? [], query), [current, query])
  const result = tested && tested.key === choiceKey(choice) ? tested.result : null

  async function runTest() {
    if (!model || !temperatureOk || busy) return
    setBusy("test")
    setError("")
    const key = choiceKey(choice)
    try {
      setTested({ key, result: await adminApi.test(step.step, choice) })
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(null)
    }
  }

  async function save() {
    if (!savable || busy) return
    setBusy("save")
    setError("")
    try {
      if (step.step === "embed") await adminApi.startEmbeddingSwitch(choice, changedBy)
      else await adminApi.save(step.step, choice, changedBy)
      onSaved()
    } catch (e) {
      setError(adminErrorMessage(e, text))
    } finally {
      setBusy(null)
      setConfirm(false)
    }
  }

  return (
    <Dialog open onOpenChange={(open) => { if (!open && !busy) onClose() }}>
      <DialogContent className="model-dialog">
        <DialogHeader>
          <DialogTitle>{fill(text.dialogTitle, { step: text.steps[step.step] })}</DialogTitle>
          <DialogDescription>
            {fill(text.requirements, {
              list: step.requirements.map((item) => text.capabilities[item]).join(" · "),
            })}
          </DialogDescription>
        </DialogHeader>
        <Tabs
          value={provider}
          onValueChange={(value) => {
            setProvider(String(value))
            setSelected("")
            setCustom("")
            setTested(null)
          }}
        >
          <TabsList>
            {step.providers.map((name) => (
              <TabsTrigger key={name} value={name}>
                {name in text.providers ? text.providers[name as keyof typeof text.providers] : name}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
        <div className="catalog-toolbar">
          <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={text.search} aria-label={text.search} />
          <Button variant="outline" size="icon" aria-label={text.refresh} onClick={() => setRefresh((value) => value + 1)}>
            <RefreshCw size={15} />
          </Button>
        </div>
        {catalog.error && <p className="error-text">{catalog.error}</p>}
        {view.kind === "loading" && !catalog.error && <p className="muted small">{copy.common.loading}</p>}
        {view.kind === "problem" && <p className="error-text">{view.message}</p>}
        {view.kind === "list" && (
          <div className="catalog-list" role="radiogroup" aria-label={text.modelList}>
            {visible.length === 0 && <p className="muted small">{text.noModels}</p>}
            {visible.map((item) => (
              <CatalogOption
                key={item.id}
                item={item}
                active={!custom.trim() && selected === item.id}
                onSelect={() => {
                  setSelected(item.id)
                  setCustom("")
                }}
              />
            ))}
          </div>
        )}
        <label className="model-field">
          {text.customModel}
          <Input dir="ltr" value={custom} onChange={(e) => setCustom(e.target.value)} placeholder={step.step === "classify" ? "jev-1.13.0" : "qwen3:4b"} />
          <span className="field-help">{text.customHelp}</span>
        </label>
        {tunable && (
          <div className="model-options">
            <label className="model-field">
              {text.temperature}
              <Input type="number" min={0} max={2} step={0.1} value={temperature} onChange={(e) => setTemperature(e.target.value)} aria-invalid={!temperatureOk} />
              <span className="field-help">{text.temperatureHelp}</span>
            </label>
            {thinking && (
              <label className="model-toggle">
                <input type="checkbox" checked={think} onChange={(e) => setThink(e.target.checked)} />
                {text.thinking}
              </label>
            )}
          </div>
        )}
        {provider === "ollama" && <p className="field-help">{text.localSlow}</p>}
        {result && (
          <p className={result.ok ? "probe-ok" : "error-text"} role="status">
            {result.ok ? <CheckCircle2 size={15} /> : <CircleAlert size={15} />}
            {result.ok
              ? fill(text.testPassed, { ms: result.latency_ms })
              : fill(text.testFailed, { error: result.error ?? "" })}
          </p>
        )}
        {error && <p className="error-text" role="alert">{error}</p>}
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={busy !== null}>
            {copy.common.cancel}
          </Button>
          <Button variant="outline" onClick={() => void runTest()} disabled={!model || !temperatureOk || busy !== null}>
            {busy === "test" && <LoaderCircle className="animate-spin" size={15} />}
            {busy === "test" ? text.testing : text.test}
          </Button>
          <Button
            onClick={() => (step.step === "embed" ? setConfirm(true) : void save())}
            disabled={!savable || busy !== null}
          >
            {busy === "save" ? text.saving : step.step === "embed" ? text.reindex : text.save}
          </Button>
        </DialogFooter>
        <ConfirmDialog
          open={confirm}
          onClose={() => setConfirm(false)}
          title={text.confirmTitle}
          description={text.confirmDescription}
          action={text.confirmAction}
          onConfirm={() => void save()}
        />
      </DialogContent>
    </Dialog>
  )
}

function CatalogOption({
  item,
  active,
  onSelect,
}: {
  item: CatalogModel
  active: boolean
  onSelect: () => void
}) {
  const text = useCopy().models
  const price = priceLabel(item, text.free, text.price)
  return (
    <button
      type="button"
      role="radio"
      aria-checked={active}
      className={`catalog-option ${active ? "is-active" : ""}`}
      onClick={onSelect}
    >
      <span dir="ltr">{item.name}</span>
      <span className="chip-row">
        {item.capabilities === null ? (
          <Badge variant="outline">{text.unknownCaps}</Badge>
        ) : (
          item.capabilities.map((capability) => (
            <Badge key={capability} variant="secondary">{text.capabilities[capability]}</Badge>
          ))
        )}
        {price && <span className="muted small" dir="ltr">{price}</span>}
      </span>
    </button>
  )
}
