import { useRef, useState } from "react"
import {
  CheckCheck,
  FileCheck2,
  FileUp,
  FlaskConical,
  Target,
  UsersRound,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Metric, PageHeader } from "@/components/shared/workspace-ui"
import { validateEvaluation } from "@/lib/imports"
import { percentage } from "@/lib/format"
import { useWorkspace } from "@/lib/workspace"
import { useCopy } from "@/lib/locale"
import type { EvaluationReport } from "@/lib/types"

export function EvaluationPage() {
  const copy = useCopy()
  const input = useRef<HTMLInputElement>(null),
    workspace = useWorkspace()
  const [report, setReport] = useState<EvaluationReport | null>(null),
    [filename, setFilename] = useState("")
  async function readReport(file?: File) {
    if (!file) return
    try {
      if (file.size > 2 * 1024 * 1024)
        throw new Error("Report must be smaller than 2 MB.")
      const parsed = validateEvaluation(JSON.parse(await file.text()))
      setReport(parsed)
      setFilename(file.name)
      workspace.notify(
        "Imported report loaded. Its measurements were supplied by the file, not verified by this UI."
      )
    } catch (error) {
      workspace.notify(
        error instanceof Error ? error.message : "Invalid report.",
        true
      )
    } finally {
      if (input.current) input.current.value = ""
    }
  }
  return (
    <>
      <PageHeader
        title={copy.pages.evaluationTitle}
        description={copy.pages.evaluationDescription}
      >
        <Button variant="outline" onClick={() => input.current?.click()}>
          <FileUp size={16} />
          Import results
        </Button>
        <input
          ref={input}
          type="file"
          className="sr-only"
          aria-label="Import evaluation report"
          accept=".json"
          onChange={(e) => void readReport(e.target.files?.[0])}
        />
      </PageHeader>
      {report ? (
        <div className="report-provenance">
          <FileCheck2 size={18} />
          <div>
            <strong>{filename}</strong>
            <span>
              User-imported report · {report.model} · {report.generated_at} ·
              provenance not independently verified
            </span>
          </div>
          <Badge variant="outline">Held-out test split</Badge>
        </div>
      ) : (
        <div className="evaluation-intro">
          <span className="evaluation-icon">
            <FlaskConical size={28} />
          </span>
          <div>
            <h2>
              A demo shows what’s possible.
              <br />
              An evaluation shows what works.
            </h2>
            <p>
              No held-out evaluation has been run in this workspace. Import a
              measured report when it’s ready; the numbers below stay empty
              until then.
            </p>
          </div>
        </div>
      )}
      <div className="metrics-grid">
        <Metric
          label="Classification accuracy"
          value={percentage(report?.classification_accuracy)}
          detail="Correct issue category"
          icon={<Target size={19} />}
        />
        <Metric
          label="Extraction accuracy"
          value={percentage(report?.extraction_accuracy)}
          detail="Correct structured details"
          icon={<FileCheck2 size={19} />}
        />
        <Metric
          label="Held-out tickets"
          value={report?.sample_size || "—"}
          detail="Not used for prompt tuning"
          icon={<UsersRound size={19} />}
        />
        <Metric
          label="Evaluation source"
          value={report ? "Imported" : "Not run"}
          detail={
            report ? "User-provided measurements" : "No fabricated metrics"
          }
          icon={<CheckCheck size={19} />}
        />
      </div>
      <div className="two-column">
        <Card>
          <CardHeader>
            <CardTitle>Compare the classification strategies</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="model-comparison">
              {["Jev", "Gemini", "Jev → Gemini cascade"].map((name, index) => (
                <div key={name}>
                  <span className={`model-logo model-${index}`}>
                    {index === 0 ? "J" : index === 1 ? "G" : "J+G"}
                  </span>
                  <div>
                    <strong>{name}</strong>
                    <small>
                      {
                        [
                          "Fast typed classification",
                          "LLM self-consistency",
                          "Fast path with a second opinion",
                        ][index]
                      }
                    </small>
                  </div>
                  <Badge variant="outline">Awaiting comparison</Badge>
                </div>
              ))}
            </div>
            <p className="field-help">
              Compare accuracy, escalation rate, latency and cost on the same
              held-out set.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Confusion cases & limitations</CardTitle>
          </CardHeader>
          <CardContent>
            {report?.confusion_cases.length ? (
              <ul className="confusion-list">
                {report.confusion_cases.map((text, index) => (
                  <li key={index}>{text}</li>
                ))}
              </ul>
            ) : (
              <div className="evaluation-checklist">
                <p>The Topic 06 brief asks for:</p>
                <span>
                  <CheckCheck size={16} />
                  At least 200 synthetic Iraqi-dialect tickets
                </span>
                <span>
                  <CheckCheck size={16} />A labelled, held-out test split
                </span>
                <span>
                  <CheckCheck size={16} />
                  Classification and extraction accuracy
                </span>
                <span>
                  <CheckCheck size={16} />A discussion of confusing and failed
                  cases
                </span>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      <details className="report-schema">
        <summary>Expected report format</summary>
        <pre>
          {
            '{\n  "model": "your-model-version",\n  "split": "test",\n  "sample_size": 100,\n  "generated_at": "2026-10-07",\n  "classification_accuracy": 0.0,\n  "extraction_accuracy": 0.0,\n  "confusion_cases": []\n}'
          }
        </pre>
        <p>
          Format example only. Replace each value with your measured result;
          accuracy values are fractions from 0 to 1. Imported files are not
          persisted by this screen.
        </p>
      </details>
    </>
  )
}
