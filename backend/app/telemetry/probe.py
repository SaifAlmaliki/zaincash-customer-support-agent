from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.models_config.types import ModelChoice, ProbeResult, Step
from app.telemetry.calls import AiCall


def probe_call(step: Step, choice: ModelChoice, result: ProbeResult, locality: str) -> AiCall:
    local = locality == "local"
    return AiCall("probe", choice.provider, choice.model, locality,
                  datetime.now(UTC) - timedelta(milliseconds=result.latency_ms), result.latency_ms,
                  cost_source="local" if local else "unknown", status="ok" if result.ok else "error",
                  error=None if result.ok else (result.error or "failed")[:300],
                  detail={"step": step.value})
