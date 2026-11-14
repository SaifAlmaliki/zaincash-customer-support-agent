from datetime import UTC, datetime

from app.telemetry.calls import AiCall, record
from tests.fakes import FakeClassifier


def fake_call(process="classify", **kw):
    return AiCall(**({"process": process, "provider": "typesafe", "model": "jev-1.13.0",
                      "locality": "cloud", "started_at": datetime.now(UTC), "latency_ms": 12,
                      "input_tokens": 100, "cost_usd": 0.0000042, "cost_source": "estimate"} | kw))


class RecordingClassifier(FakeClassifier):
    async def classify(self, nt, cands):
        record(fake_call())
        return await super().classify(nt, cands)
