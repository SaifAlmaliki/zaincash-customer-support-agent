# Admin model configuration — backend implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every model in the pipeline (intake, classify, extract, draft, embed) is chosen by an admin at runtime from OpenRouter, Ollama or TypeSafe, through a token-protected API, with live tests before saving and a guarded embedding switch.

**Architecture:** A new `app/models_config/` package holds provider adapters (`providers/`), a database-backed store with an in-memory cache, and `ActiveModels`, an immutable snapshot that is the only thing the pipeline, intake and knowledge base use to build model clients. Admin endpoints live in `app/api/admin.py`. Existing `.env` values remain the defaults for any step the admin has not set.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2 + Postgres/pgvector, LangChain 1.x (`langchain-openrouter`, new `langchain-ollama`), `langchain-typesafe`, httpx, pytest + pytest-asyncio, uv, ruff.

**Spec:** `docs/superpowers/specs/2026-11-12-admin-model-config-design.md`

## Global Constraints

- Steps are exactly `intake`, `classify`, `extract`, `draft`, `embed`.
- Providers: `openrouter` (cloud), `ollama` (local), `typesafe` (cloud). `classify` accepts only `typesafe`; the other steps accept `openrouter` and `ollama`.
- Embedding vectors are exactly 768 dimensions; the KB tables are not changed.
- No silent fallback: a configured provider that is unavailable makes its step fail visibly; nothing switches provider automatically.
- API keys and provider URLs stay in `.env` and never appear in API responses.
- With no admin rows saved, behavior equals today's `.env` behavior.
- New settings: `ADMIN_TOKEN` (default empty = admin disabled), `OLLAMA_BASE_URL` (default `http://localhost:11434`), `LOCAL_AGENT_TIMEOUT_S` (default 180, max 600), `LOCAL_INTAKE_TIMEOUT_S` (default 180, max 600). `AGENT_TIMEOUT_S` keeps its 30 s cap for cloud.
- Thinking (`think`) is only sent to a provider when the stored options contain it.
- Only `app/models_config/providers/` constructs provider clients or imports `langchain_openrouter`, `openrouter`, `langchain_ollama`.
- Admin routes are under `/api/admin`, require `X-Admin-Token`, return `403 "admin_disabled"` when `ADMIN_TOKEN` is empty and `401 "invalid_admin_token"` on a wrong or missing token.
- Run every backend command from `backend/`: tests `uv run pytest -q`, lint `uv run ruff check app tests`. Integration tests need `docker compose up -d db` (Postgres on port 5433, database `support_test`).

## Review Focus

1. **Ollama stops after an admin saved a local model.** Expected: the step reports `unreachable`, drafts escalate with `llm_unavailable`, and no OpenRouter call is made. Test: Task 5 `test_unreachable_local_draft_provider_never_falls_back_to_cloud`.
2. **Admin token header with non-ASCII characters or blank value.** Expected: `401`, never a `500` from `hmac.compare_digest`. Test: Task 9 `test_non_ascii_and_blank_tokens_are_rejected`.
3. **Embedding switch with an empty knowledge base.** Expected: the job completes immediately with `total == 0`. Test: Task 10 `test_switch_with_no_documents_completes_immediately`.
4. **A stored row names a provider the code no longer has.** Expected: the store skips it with a warning and the API keeps working. Test: Task 4 `test_rows_for_unknown_providers_are_ignored`.
5. **Ollama model IDs containing colons (`qwen3:4b`).** Expected: they survive JSON storage, `ref`, `model_ids` and the catalog without being split. Test: Task 4 `test_model_ids_keep_colons_in_model_names`.

---

## File structure

| File | Responsibility |
| --- | --- |
| `app/models_config/__init__.py` | Package docstring |
| `app/models_config/types.py` | `Step`, `Capability`, `ModelChoice`, `CatalogEntry`, `ProviderStatus`, `ProbeResult` |
| `app/models_config/steps.py` | Step requirements, allowed providers, `.env` defaults, timeouts |
| `app/models_config/providers/base.py` | `Provider` protocol, `UnsupportedOperation` |
| `app/models_config/providers/openrouter_chat.py` | `OpenRouterChat` (moved from `stage6_draft/model.py`) |
| `app/models_config/providers/openrouter.py` | OpenRouter adapter |
| `app/models_config/providers/ollama.py` | Ollama adapter |
| `app/models_config/providers/typesafe.py` | TypeSafe adapter |
| `app/models_config/providers/registry.py` | `ProviderRegistry`, `provider_errors()` |
| `app/models_config/db_models.py` | `model_settings`, `model_settings_audit`, `embedding_switch` tables |
| `app/models_config/resolver.py` | `ActiveModels` snapshot |
| `app/models_config/store.py` | `ModelSettingsStore` |
| `app/models_config/embedder.py` | `ConfiguredEmbedder` for the long-lived KB service |
| `app/models_config/probe.py` | Per-step live tests |
| `app/models_config/catalog.py` | Catalog cache and per-step filtering |
| `app/models_config/embedding_switch.py` | `EmbeddingSwitches` |
| `app/pipeline/stage6_draft/model_info.py` | `DraftModelInfo` |
| `app/api/admin.py` | Admin router |
| `tests/models_config/` | New tests; `tests/models_config_fakes.py` holds shared fakes |

---

### Task 1: Settings, model types and step rules

**Files:**
- Modify: `backend/app/config.py`
- Create: `backend/app/models_config/__init__.py`, `backend/app/models_config/types.py`, `backend/app/models_config/steps.py`
- Test: `backend/tests/models_config/__init__.py`, `backend/tests/models_config/test_steps.py`

**Interfaces:**
- Produces: `Step`, `Capability`, `ModelChoice(provider, model, options)` with `.ref`, `.to_json()`, `ModelChoice.from_json()`; `CatalogEntry`, `ProviderStatus`, `ProbeResult` (each with `.to_json()`); `Locality`, `ProviderState`, `CatalogKind` literals; in `steps.py`: `EMBED_DIMENSIONS`, `REQUIREMENTS`, `PROVIDERS_FOR_STEP`, `CATALOG_KIND`, `DEFAULT_TEMPERATURE`, `env_defaults(settings) -> dict[Step, ModelChoice]`, `eligibility(step, capabilities) -> "eligible" | "unknown" | "ineligible"`, `draft_timeout_s(settings, locality)`, `intake_timeout_s(settings, locality)`.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/models_config/__init__.py` (empty) and `backend/tests/models_config/test_steps.py`:

```python
import pytest
from pydantic import ValidationError

from app.config import Settings
from app.models_config.steps import (
    draft_timeout_s,
    eligibility,
    env_defaults,
    intake_timeout_s,
)
from app.models_config.types import Capability, ModelChoice, Step


def _settings(**kw):
    return Settings(_env_file=None, **kw)


def test_env_defaults_match_todays_settings():
    defaults = env_defaults(_settings())
    assert defaults[Step.INTAKE] == ModelChoice("openrouter", "google/gemini-3.8-flash")
    assert defaults[Step.CLASSIFY] == ModelChoice("typesafe", "jev-1.13.0")
    assert defaults[Step.EXTRACT] == ModelChoice("openrouter", "google/gemini-3.8-flash")
    assert defaults[Step.DRAFT] == ModelChoice("openrouter", "google/gemini-3.8-flash")
    assert defaults[Step.EMBED] == ModelChoice("openrouter", "openai/text-embedding-3-small")


def test_env_overrides_for_draft_and_intake():
    defaults = env_defaults(_settings(anthropic_model="anthropic/claude-sonnet-5.5",
                                      intake_model="google/gemini-2.5-flash"))
    assert defaults[Step.DRAFT].model == "anthropic/claude-sonnet-5.5"
    assert defaults[Step.INTAKE].model == "google/gemini-2.5-flash"
    assert defaults[Step.EXTRACT].model == "google/gemini-3.8-flash"


def test_choice_round_trip_keeps_colons_and_rejects_blank_model():
    choice = ModelChoice("ollama", "qwen3:4b", {"think": False})
    assert choice.ref == "ollama:qwen3:4b"
    assert ModelChoice.from_json(choice.to_json()) == choice
    with pytest.raises(ValueError):
        ModelChoice.from_json({"provider": "ollama", "model": "  "})
    with pytest.raises(ValueError):
        ModelChoice.from_json({"provider": "ollama", "model": "m", "options": []})


@pytest.mark.parametrize("step, capabilities, expected", [
    (Step.DRAFT, frozenset({Capability.TOOLS, Capability.STRUCTURED}), "eligible"),
    (Step.DRAFT, frozenset({Capability.STRUCTURED}), "ineligible"),
    (Step.INTAKE, frozenset({Capability.STRUCTURED}), "ineligible"),
    (Step.INTAKE, frozenset({Capability.STRUCTURED, Capability.VISION}), "eligible"),
    (Step.EMBED, None, "unknown"),
])
def test_eligibility(step, capabilities, expected):
    assert eligibility(step, capabilities) == expected


def test_local_timeouts_and_limits():
    settings = _settings(local_agent_timeout_s=200, local_intake_timeout_s=150)
    assert draft_timeout_s(settings, "local") == 200
    assert draft_timeout_s(settings, "cloud") == 30
    assert intake_timeout_s(settings, "local") == 150
    assert intake_timeout_s(settings, "cloud") == 60
    with pytest.raises(ValidationError):
        _settings(local_agent_timeout_s=601)


def test_new_settings_defaults():
    settings = _settings(ollama_base_url="http://host.docker.internal:11434/")
    assert settings.ollama_base_url == "http://host.docker.internal:11434"
    assert _settings().admin_token == ""
    assert _settings().local_agent_timeout_s == 180
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_steps.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.models_config'`.

- [ ] **Step 3: Add the settings**

In `backend/app/config.py`, after the `intake_max_images_per_session` line add:

```python
    # Admin model configuration. An empty token disables every /api/admin route.
    admin_token: str = ""
    ollama_base_url: str = "http://localhost:11434"
    local_agent_timeout_s: float = Field(default=180, gt=0, le=600, allow_inf_nan=False)
    local_intake_timeout_s: float = Field(default=180, gt=0, le=600, allow_inf_nan=False)
```

and, next to the other validators:

```python
    @field_validator("ollama_base_url")
    @classmethod
    def trim_ollama_url(cls, value: str) -> str:
        return value.strip().rstrip("/")
```

- [ ] **Step 4: Create the types**

`backend/app/models_config/__init__.py`:

```python
"""Admin-managed, provider-neutral model configuration for every pipeline step."""
```

`backend/app/models_config/types.py`:

```python
"""Provider-neutral values shared by the store, the resolver, probes and the admin API."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal

Locality = Literal["local", "cloud"]
ProviderState = Literal["ready", "missing_key", "unreachable"]
CatalogKind = Literal["chat", "embedding"]


class Step(StrEnum):
    INTAKE = "intake"
    CLASSIFY = "classify"
    EXTRACT = "extract"
    DRAFT = "draft"
    EMBED = "embed"


class Capability(StrEnum):
    STRUCTURED = "structured_output"
    TOOLS = "tools"
    VISION = "vision"
    EMBEDDING = "embedding"
    THINKING = "thinking"
    CLASSIFIER = "classifier"


@dataclass(frozen=True)
class ModelChoice:
    provider: str
    model: str
    options: dict[str, Any] = field(default_factory=dict)

    @property
    def ref(self) -> str:
        return f"{self.provider}:{self.model}"

    def to_json(self) -> dict[str, Any]:
        return {"provider": self.provider, "model": self.model, "options": dict(self.options)}

    @classmethod
    def from_json(cls, value: Any) -> ModelChoice:
        if not isinstance(value, dict):
            raise ValueError("A model choice must be an object.")
        provider, model = value.get("provider"), value.get("model")
        options = value.get("options") if value.get("options") is not None else {}
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("A model choice needs a provider.")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("A model choice needs a model ID.")
        if not isinstance(options, dict):
            raise ValueError("Model options must be an object.")
        return cls(provider.strip(), model.strip(), dict(options))


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    name: str
    capabilities: frozenset[Capability] | None  # None: the provider did not report them
    price_in_per_m: float | None = None
    price_out_per_m: float | None = None
    context_length: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id, "name": self.name,
            "capabilities": None if self.capabilities is None else sorted(c.value for c in self.capabilities),
            "price_in_per_m": self.price_in_per_m, "price_out_per_m": self.price_out_per_m,
            "context_length": self.context_length,
        }


@dataclass(frozen=True)
class ProviderStatus:
    name: str
    locality: Locality
    state: ProviderState
    detail: str | None = None


@dataclass(frozen=True)
class ProbeResult:
    ok: bool
    latency_ms: int
    error: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {"ok": self.ok, "latency_ms": self.latency_ms, "error": self.error}
```

- [ ] **Step 5: Create the step rules**

`backend/app/models_config/steps.py`:

```python
"""What each pipeline step needs, who may serve it, and today's .env defaults."""
from __future__ import annotations

from typing import Literal

from app.config import Settings
from app.models_config.types import Capability, CatalogKind, Locality, ModelChoice, Step

EMBED_DIMENSIONS = 768

REQUIREMENTS: dict[Step, frozenset[Capability]] = {
    Step.INTAKE: frozenset({Capability.STRUCTURED, Capability.VISION}),
    Step.CLASSIFY: frozenset({Capability.CLASSIFIER}),
    Step.EXTRACT: frozenset({Capability.STRUCTURED}),
    Step.DRAFT: frozenset({Capability.TOOLS}),
    Step.EMBED: frozenset({Capability.EMBEDDING}),
}

PROVIDERS_FOR_STEP: dict[Step, tuple[str, ...]] = {
    Step.INTAKE: ("openrouter", "ollama"),
    Step.CLASSIFY: ("typesafe",),
    Step.EXTRACT: ("openrouter", "ollama"),
    Step.DRAFT: ("openrouter", "ollama"),
    Step.EMBED: ("openrouter", "ollama"),
}

CATALOG_KIND: dict[Step, CatalogKind] = {
    Step.INTAKE: "chat", Step.CLASSIFY: "chat", Step.EXTRACT: "chat",
    Step.DRAFT: "chat", Step.EMBED: "embedding",
}

DEFAULT_TEMPERATURE: dict[Step, float] = {Step.EXTRACT: 0.0, Step.DRAFT: 0.1}


def env_defaults(settings: Settings) -> dict[Step, ModelChoice]:
    return {
        Step.INTAKE: ModelChoice("openrouter", settings.intake_model or settings.gemini_model),
        Step.CLASSIFY: ModelChoice("typesafe", settings.jev_model),
        Step.EXTRACT: ModelChoice("openrouter", settings.gemini_model),
        Step.DRAFT: ModelChoice("openrouter", settings.draft_model),
        Step.EMBED: ModelChoice("openrouter", settings.embedding_model),
    }


def eligibility(step: Step, capabilities: frozenset[Capability] | None
                ) -> Literal["eligible", "unknown", "ineligible"]:
    if capabilities is None:
        return "unknown"
    return "eligible" if REQUIREMENTS[step] <= capabilities else "ineligible"


def draft_timeout_s(settings: Settings, locality: Locality) -> float:
    return settings.local_agent_timeout_s if locality == "local" else settings.agent_timeout_s


def intake_timeout_s(settings: Settings, locality: Locality) -> float:
    return settings.local_intake_timeout_s if locality == "local" else settings.intake_timeout_s
```

- [ ] **Step 6: Run the tests**

Run: `uv run pytest tests/models_config/test_steps.py tests/test_config.py -q`
Expected: PASS.

- [ ] **Step 7: Lint and commit**

```bash
uv run ruff check app tests
git add app/config.py app/models_config tests/models_config
git commit -m "feat(models): add model configuration types and step rules"
```

---

### Task 2: OpenRouter and TypeSafe providers, registry, generic embedder

**Files:**
- Create: `backend/app/models_config/providers/__init__.py`, `base.py`, `openrouter_chat.py`, `openrouter.py`, `typesafe.py`, `registry.py`
- Delete: `backend/app/pipeline/stage6_draft/model.py`
- Modify: `backend/app/kb/embeddings.py`, `backend/app/pipeline/factory.py:52-60`, `backend/app/pipeline/stage6_draft/agent.py:33`
- Test: `backend/tests/models_config/test_openrouter_provider.py`, `backend/tests/test_embeddings.py` (append)

**Interfaces:**
- Consumes: Task 1 types.
- Produces:
  - `Provider` protocol: `name: str`, `locality: Locality`, `status() -> ProviderStatus`, `async catalog(kind: CatalogKind) -> list[CatalogEntry]`, `chat_model(model, *, temperature: float | None, timeout_s: float, options: Mapping[str, Any]) -> BaseChatModel`, `embedder(model, *, dimensions: int) -> Embedder`, `classifier(model) -> Any`.
  - `UnsupportedOperation(ValueError)`.
  - `OpenRouterProvider(settings, *, transport=None)`, `TypeSafeProvider(settings)`.
  - `ProviderRegistry(settings, *, providers: Mapping[str, Provider] | None = None)` with `get(name)`, `names()`, `status(name)`; `UnknownProvider(ValueError)`; `provider_errors() -> tuple[type[BaseException], ...]`.
  - `OpenAICompatibleEmbedder(*, model, dimensions, url, api_key="", price_per_m=0.0, send_dimensions=True, transport=None)`; `OpenRouterEmbedder(settings, *, transport=None)` keeps its signature.
  - `OpenRouterChat` and `DraftProviderResponseError` in `app.models_config.providers.openrouter_chat` (the error keeps its name because traces record `error_type`).

- [ ] **Step 1: Write the failing tests**

`backend/tests/models_config/test_openrouter_provider.py`:

```python
import json

import httpx
import pytest

from app.config import Settings
from app.models_config.providers.openrouter import OpenRouterProvider
from app.models_config.providers.registry import ProviderRegistry, UnknownProvider, provider_errors
from app.models_config.providers.typesafe import TypeSafeProvider
from app.models_config.types import Capability


def _provider(handler=None, **kw):
    settings = Settings(_env_file=None, **({"openrouter_api_key": "test-key"} | kw))
    return OpenRouterProvider(settings, transport=httpx.MockTransport(handler) if handler else None)


def test_status_reports_missing_key():
    assert _provider(openrouter_api_key="").status().state == "missing_key"
    ready = _provider().status()
    assert ready.state == "ready" and ready.locality == "cloud"


async def test_chat_catalog_maps_capabilities_and_prices():
    def handler(request):
        assert str(request.url) == "https://openrouter.ai/api/v1/models"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(200, json={"data": [
            {"id": "anthropic/claude-sonnet-5.5", "name": "Claude Sonnet 5.5", "context_length": 200000,
             "pricing": {"prompt": "0.000003", "completion": "0.000015"},
             "architecture": {"input_modalities": ["text", "image"]},
             "supported_parameters": ["tools", "structured_outputs", "reasoning"]},
            {"id": "x/plain", "name": "Plain", "pricing": {"prompt": "-1"}, "supported_parameters": []},
            {"name": "missing id"},
        ]})

    first, plain = await _provider(handler).catalog("chat")
    assert first.capabilities == {Capability.TOOLS, Capability.STRUCTURED, Capability.THINKING, Capability.VISION}
    assert first.price_in_per_m == pytest.approx(3.0) and first.price_out_per_m == pytest.approx(15.0)
    assert first.context_length == 200000
    assert plain.capabilities == frozenset() and plain.price_in_per_m is None


async def test_embedding_catalog_uses_the_embedding_listing():
    def handler(request):
        assert str(request.url) == "https://openrouter.ai/api/v1/embeddings/models"
        return httpx.Response(200, json={"data": [{"id": "openai/text-embedding-3-small", "name": "Small"}]})

    [entry] = await _provider(handler).catalog("embedding")
    assert entry.capabilities == {Capability.EMBEDDING}


def test_chat_model_disables_sdk_retries_and_maps_thinking():
    chat = _provider().chat_model("google/gemini-3.8-flash", temperature=0.1, timeout_s=30,
                                  options={"think": False})
    assert chat.model_name == "google/gemini-3.8-flash"
    assert chat.temperature == 0.1
    assert chat.request_timeout == 30000 and chat.max_retries == 0
    assert chat.model_kwargs == {"retries": None}
    assert chat.reasoning == {"enabled": False}
    assert _provider().chat_model("m", temperature=None, timeout_s=60, options={}).reasoning is None


async def test_embedder_posts_to_openrouter_with_dimensions():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [1.0] + [0.0] * 767}]})

    batch = await _provider(handler).embedder("openai/text-embedding-3-small", dimensions=768).embed(["x"])
    assert len(batch.vectors[0]) == 768
    assert str(seen[0].url) == "https://openrouter.ai/api/v1/embeddings"
    assert json.loads(seen[0].content)["dimensions"] == 768


def test_typesafe_status_and_unsupported_chat():
    provider = TypeSafeProvider(Settings(_env_file=None, typesafe_api_key=""))
    assert provider.status().state == "missing_key"
    with pytest.raises(ValueError):
        provider.chat_model("jev-1.13.0", temperature=None, timeout_s=1, options={})


def test_registry_rejects_unknown_providers_and_exposes_errors():
    registry = ProviderRegistry(Settings(_env_file=None))
    assert {"openrouter", "typesafe"} <= set(registry.names())
    with pytest.raises(UnknownProvider):
        registry.get("nope")
    from openrouter.errors import OpenRouterError

    assert OpenRouterError in provider_errors() and httpx.HTTPError in provider_errors()
```

Append to `backend/tests/test_embeddings.py`:

```python
async def test_keyless_compatible_embedder_omits_auth_and_dimensions():
    from app.kb.embeddings import OpenAICompatibleEmbedder

    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(200, json=response_payload([item(0)]))

    embedder = OpenAICompatibleEmbedder(
        model="nomic-embed-text", dimensions=768, url="http://ollama:11434/v1/embeddings",
        send_dimensions=False, transport=httpx.MockTransport(respond),
    )
    batch = await embedder.embed(["سياسة"])
    assert len(batch.vectors[0]) == 768 and batch.cost_usd == 0.0
    assert "authorization" not in seen[0].headers
    assert json.loads(seen[0].content) == {
        "input": ["سياسة"], "model": "nomic-embed-text", "encoding_format": "float",
    }
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_openrouter_provider.py tests/test_embeddings.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.models_config.providers'` and `ImportError: cannot import name 'OpenAICompatibleEmbedder'`.

- [ ] **Step 3: Generalize the embedder**

In `backend/app/kb/embeddings.py`, replace the whole `class OpenRouterEmbedder:` block (from `class OpenRouterEmbedder:` to the end of the file) with:

```python
class OpenAICompatibleEmbedder:
    """Implements Embedder for any OpenAI-compatible /embeddings endpoint.

    Owns one context-managed HTTP client per embed call. A transport may be
    injected for offline tests. Requests are sequential, batched at 32 texts,
    have a 20s elapsed request deadline plus HTTP timeouts, and are never
    automatically retried. The request deadline includes the full body read.
    Caller cancellation propagates with this call's measured cost_usd attached to
    the original CancelledError. An outer asyncio.timeout retains it as the raised
    TimeoutError's __cause__. Consumers record that cost once on failure, instead
    of the EmbeddingBatch cost they would record on success.
    """

    def __init__(
        self, *, model: str, dimensions: int, url: str, api_key: str = "",
        price_per_m: float = 0.0, send_dimensions: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.model = model
        self.dimensions = dimensions
        self._url = url
        self._api_key = api_key
        self._price_per_m = price_per_m
        self._send_dimensions = send_dimensions
        self._transport = transport

    async def embed(self, texts: list[str]) -> EmbeddingBatch:
        if not texts:
            return EmbeddingBatch(())
        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise EmbeddingError("Embedding input must contain non-empty text strings.")
        vectors: list[tuple[float, ...]] = []
        cost_usd = 0.0
        headers = {"Authorization": f"Bearer {self._api_key}"} if self._api_key else {}
        try:
            async with httpx.AsyncClient(
                transport=self._transport, timeout=EMBEDDING_TIMEOUT_S, headers=headers,
            ) as client:
                for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
                    batch = texts[start:start + EMBEDDING_BATCH_SIZE]
                    payload = await self._request(client, batch)
                    cost_usd = _nonnegative_number(cost_usd + _response_cost(payload, self._price_per_m))
                    batch_vectors = _ordered_vectors(payload, len(batch), self.dimensions)
                    vectors.extend(batch_vectors)
        except (EmbeddingError, asyncio.CancelledError) as exc:
            # Include cancellation during client cleanup. Re-raise the same exception
            # so asyncio.timeout can still translate its own cancellation normally.
            exc.cost_usd = cost_usd
            raise
        return EmbeddingBatch(tuple(vectors), cost_usd)

    async def _request(self, client: httpx.AsyncClient, texts: list[str]) -> dict:
        body: dict[str, Any] = {"input": texts, "model": self.model, "encoding_format": "float"}
        if self._send_dimensions:
            body["dimensions"] = self.dimensions
        try:
            async with asyncio.timeout(EMBEDDING_TIMEOUT_S):
                response = await client.post(self._url, json=body)
                response.raise_for_status()
        except (TimeoutError, httpx.TimeoutException):
            raise EmbeddingError("Embedding request timed out; please retry.") from None
        except httpx.HTTPStatusError as exc:
            raise EmbeddingError(
                f"Embedding provider request failed (HTTP {exc.response.status_code}); check provider availability and configuration."
            ) from None
        except httpx.RequestError:
            raise EmbeddingError("Embedding provider is unavailable; please retry.") from None
        try:
            payload = response.json()
        except ValueError:
            raise EmbeddingError("Embedding provider returned invalid JSON.") from None
        if not isinstance(payload, dict) or "error" in payload:
            raise EmbeddingError("Embedding provider returned an invalid response.")
        return payload


class OpenRouterEmbedder(OpenAICompatibleEmbedder):
    """The .env-configured OpenRouter embedder (kept for the CLI and existing tests)."""

    def __init__(self, settings: Settings, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        super().__init__(
            model=settings.embedding_model, dimensions=settings.embed_dim, url=EMBEDDING_URL,
            api_key=settings.openrouter_api_key, price_per_m=settings.price_embedding_in,
            transport=transport,
        )
```

Also change the module docstring to `"""Injectable OpenAI-compatible embeddings with validated, input-ordered immutable results."""`.

- [ ] **Step 4: Move the OpenRouter chat class**

Create `backend/app/models_config/providers/__init__.py` with `"""One adapter per model provider."""`.

Create `backend/app/models_config/providers/openrouter_chat.py` with the content of `backend/app/pipeline/stage6_draft/model.py`, renaming `DraftChatOpenRouter` to `OpenRouterChat`:

```python
"""Narrow normalization of known non-streaming OpenRouter response failures."""
from __future__ import annotations

from typing import Any

from langchain_core.outputs import ChatResult
from langchain_openrouter import ChatOpenRouter
from langchain_openrouter.chat_models import _create_usage_metadata

from app.llm import LLMUnavailable


class DraftProviderResponseError(LLMUnavailable):
    """Unusable provider response with usage retained before AIMessage creation.

    The per-ticket callback consumes response_metadata/usage_metadata using the
    same pricing and response-ID deduplication as successful model responses.
    """

    def __init__(self, message: str, response: dict[str, Any], *, model: str):
        super().__init__(message)
        usage = response.get("usage") or {}
        self.usage_metadata = _create_usage_metadata(usage)
        self.response_metadata = {
            "model_name": response.get("model") or model,
            **{key: response[key] for key in ("id", "provider", "system_fingerprint") if key in response},
            **{key: usage[key] for key in ("cost", "cost_details") if key in usage},
        }


class OpenRouterChat(ChatOpenRouter):
    """Keep the SDK/LC request path; normalize only known unusable wire shapes."""

    def _create_chat_result(self, response: Any) -> ChatResult:
        raw = response if isinstance(response, dict) else response.model_dump(by_alias=True)
        # The upstream converter raises bare ValueError for these two provider
        # outcomes before producing a message (and hence before usage callbacks).
        # Do not catch ValueError from general conversion or application code.
        if raw.get("error") or not raw.get("choices"):
            reason = "an error" if raw.get("error") else "no choices"
            raise DraftProviderResponseError(f"OpenRouter returned {reason}", raw, model=self.model_name)
        return super()._create_chat_result(raw)
```

Delete the old file: `git rm app/pipeline/stage6_draft/model.py`.

In `backend/app/pipeline/stage6_draft/agent.py` line 33, change the import to:

```python
from app.models_config.providers.openrouter_chat import DraftProviderResponseError
```

(Task 5 removes this import entirely.)

In `backend/app/pipeline/factory.py`, replace the body of `make_draft_model` with:

```python
def make_draft_model(settings: Settings) -> BaseChatModel:
    from app.models_config.providers.openrouter_chat import OpenRouterChat

    # Same provider conventions as llm.py. The agent retries individual transient
    # requests, inside its overall deadline; the SDK must never retry on its own.
    return OpenRouterChat(model=settings.draft_model, temperature=0.1,
                          api_key=settings.openrouter_api_key,
                          timeout=int(settings.agent_timeout_s * 1000), max_retries=0,
                          model_kwargs={"retries": None})
```

- [ ] **Step 5: Create the protocol, adapters and registry**

`backend/app/models_config/providers/base.py`:

```python
"""The contract every model provider adapter implements."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from langchain_core.language_models.chat_models import BaseChatModel

from app.kb.contracts import Embedder
from app.models_config.types import CatalogEntry, CatalogKind, Locality, ProviderStatus


class UnsupportedOperation(ValueError):
    """The provider does not offer this kind of model."""


class Provider(Protocol):
    name: str
    locality: Locality

    def status(self) -> ProviderStatus: ...

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]: ...

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]) -> BaseChatModel: ...

    def embedder(self, model: str, *, dimensions: int) -> Embedder: ...

    def classifier(self, model: str) -> Any: ...
```

`backend/app/models_config/providers/openrouter.py`:

```python
"""OpenRouter: cloud chat models, embeddings and the public model catalog."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from app.config import Settings
from app.kb.embeddings import OpenAICompatibleEmbedder
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import Capability, CatalogEntry, CatalogKind, ProviderStatus

OPENROUTER_API = "https://openrouter.ai/api/v1"
CATALOG_TIMEOUT_S = 10.0


def _per_million(value: Any) -> float | None:
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    return price * 1_000_000 if price >= 0 else None


def _capabilities(item: dict, kind: CatalogKind) -> frozenset[Capability]:
    if kind == "embedding":
        return frozenset({Capability.EMBEDDING})
    params = set(item.get("supported_parameters") or [])
    modalities = set((item.get("architecture") or {}).get("input_modalities") or [])
    found = set()
    if "tools" in params:
        found.add(Capability.TOOLS)
    if "structured_outputs" in params:
        found.add(Capability.STRUCTURED)
    if "reasoning" in params:
        found.add(Capability.THINKING)
    if "image" in modalities:
        found.add(Capability.VISION)
    return frozenset(found)


class OpenRouterProvider:
    name = "openrouter"
    locality = "cloud"

    def __init__(self, settings: Settings, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._settings = settings
        self._transport = transport

    def status(self) -> ProviderStatus:
        if not self._settings.openrouter_api_key:
            return ProviderStatus(self.name, self.locality, "missing_key", "Set OPENROUTER_API_KEY in .env.")
        return ProviderStatus(self.name, self.locality, "ready")

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        path = "/embeddings/models" if kind == "embedding" else "/models"
        async with httpx.AsyncClient(
            transport=self._transport, timeout=CATALOG_TIMEOUT_S,
            headers={"Authorization": f"Bearer {self._settings.openrouter_api_key}"},
        ) as client:
            response = await client.get(OPENROUTER_API + path)
            response.raise_for_status()
        entries = []
        for item in response.json().get("data") or []:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            pricing = item.get("pricing") or {}
            context = item.get("context_length")
            entries.append(CatalogEntry(
                id=item["id"], name=str(item.get("name") or item["id"]),
                capabilities=_capabilities(item, kind),
                price_in_per_m=_per_million(pricing.get("prompt")),
                price_out_per_m=_per_million(pricing.get("completion")),
                context_length=context if isinstance(context, int) else None,
            ))
        return entries

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        from app.models_config.providers.openrouter_chat import OpenRouterChat

        extra: dict[str, Any] = {}
        if options.get("think") is not None:
            extra["reasoning"] = {"enabled": bool(options["think"])}
        # The caller owns bounded retries; the SDK must never retry on its own.
        return OpenRouterChat(model=model, temperature=temperature,
                              api_key=self._settings.openrouter_api_key,
                              timeout=int(timeout_s * 1000), max_retries=0,
                              model_kwargs={"retries": None}, **extra)

    def embedder(self, model: str, *, dimensions: int) -> OpenAICompatibleEmbedder:
        return OpenAICompatibleEmbedder(
            model=model, dimensions=dimensions, url=f"{OPENROUTER_API}/embeddings",
            api_key=self._settings.openrouter_api_key, price_per_m=self._settings.price_embedding_in,
            transport=self._transport,
        )

    def classifier(self, model: str):
        raise UnsupportedOperation("OpenRouter does not provide the Jev classifier.")
```

`backend/app/models_config/providers/typesafe.py`:

```python
"""TypeSafe: the Jev classifier. It has no model catalog."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.config import Settings
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import CatalogEntry, CatalogKind, ProviderStatus


class TypeSafeProvider:
    name = "typesafe"
    locality = "cloud"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def status(self) -> ProviderStatus:
        if not self._settings.typesafe_api_key:
            return ProviderStatus(self.name, self.locality, "missing_key", "Set TYPESAFE_API_KEY in .env.")
        return ProviderStatus(self.name, self.locality, "ready")

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        return []

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        raise UnsupportedOperation("TypeSafe only provides the Jev classifier.")

    def embedder(self, model: str, *, dimensions: int):
        raise UnsupportedOperation("TypeSafe only provides the Jev classifier.")

    def classifier(self, model: str):
        from langchain_typesafe import TypeSafeClassifier

        return TypeSafeClassifier(model=model, api_key=self._settings.typesafe_api_key)
```

`backend/app/models_config/providers/registry.py`:

```python
"""Look up provider adapters by name; the single place that lists every provider."""
from __future__ import annotations

from collections.abc import Mapping

from app.config import Settings
from app.models_config.providers.base import Provider
from app.models_config.providers.openrouter import OpenRouterProvider
from app.models_config.providers.typesafe import TypeSafeProvider
from app.models_config.types import ProviderStatus


class UnknownProvider(ValueError):
    pass


class ProviderRegistry:
    def __init__(self, settings: Settings, *, providers: Mapping[str, Provider] | None = None) -> None:
        if providers is None:
            providers = {
                "openrouter": OpenRouterProvider(settings),
                "typesafe": TypeSafeProvider(settings),
            }
        self._providers = dict(providers)

    def get(self, name: str) -> Provider:
        try:
            return self._providers[name]
        except KeyError:
            raise UnknownProvider(f"Unknown model provider {name!r}.") from None

    def names(self) -> tuple[str, ...]:
        return tuple(self._providers)

    def status(self, name: str) -> ProviderStatus:
        return self.get(name).status()


def provider_errors() -> tuple[type[BaseException], ...]:
    """Errors any chat provider may raise for an unusable model request."""
    import httpx
    from openrouter.errors import OpenRouterError

    from app.llm import LLMUnavailable

    return (httpx.HTTPError, OpenRouterError, LLMUnavailable)
```

- [ ] **Step 6: Run the tests**

Run: `uv run pytest tests/models_config tests/test_embeddings.py tests/test_draft_model.py tests/test_llm.py tests/test_rag_drafter.py -q`
Expected: PASS.

- [ ] **Step 7: Check that nothing else imported the deleted module, lint, commit**

Run: `grep -rn "stage6_draft.model import\|DraftChatOpenRouter" app tests --include=*.py`
Expected: no output.

```bash
uv run ruff check app tests
git add -A app/models_config app/kb/embeddings.py app/pipeline tests/models_config tests/test_embeddings.py
git commit -m "feat(models): add OpenRouter and TypeSafe provider adapters"
```

---

### Task 3: Ollama provider

**Files:**
- Modify: `backend/pyproject.toml`, `backend/uv.lock` (via `uv add`), `backend/app/models_config/providers/registry.py`
- Create: `backend/app/models_config/providers/ollama.py`
- Test: `backend/tests/models_config/test_ollama_provider.py`

**Interfaces:**
- Consumes: Task 2 `Provider` protocol, `OpenAICompatibleEmbedder`.
- Produces: `OllamaProvider(settings, *, transport=None, clock=time.monotonic)`; registry default now includes `"ollama"`; `provider_errors()` also contains `ollama.ResponseError` and `ConnectionError`.

- [ ] **Step 1: Add the dependency and confirm the constructor fields**

Run: `uv add "langchain-ollama>=1.0,<2"`

Run: `uv run python -c "from langchain_ollama import ChatOllama; print(sorted({'reasoning','client_kwargs','base_url','validate_model_on_init','temperature'} - set(ChatOllama.model_fields)))"`
Expected: `[]`. If any name is printed, stop and adapt `chat_model` in Step 4 to that version's field names before continuing.

- [ ] **Step 2: Write the failing tests**

`backend/tests/models_config/test_ollama_provider.py`:

```python
import json

import httpx

from app.config import Settings
from app.models_config.providers.ollama import OllamaProvider
from app.models_config.providers.registry import ProviderRegistry, provider_errors
from app.models_config.types import Capability

BASE = "http://ollama.test:11434"


def _provider(handler, clock=None):
    settings = Settings(_env_file=None, ollama_base_url=BASE)
    kwargs = {"clock": clock} if clock else {}
    return OllamaProvider(settings, transport=httpx.MockTransport(handler), **kwargs)


async def test_catalog_lists_installed_models_with_reported_capabilities():
    def handler(request):
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [
                {"name": "qwen3:4b", "model": "qwen3:4b"},
                {"name": "nomic-embed-text:latest", "model": "nomic-embed-text:latest"},
                {"name": "old:1b", "model": "old:1b"},
            ]})
        body = json.loads(request.content)
        if body["model"] == "qwen3:4b":
            return httpx.Response(200, json={"capabilities": ["completion", "tools", "thinking"],
                                             "model_info": {"qwen3.context_length": 40960}})
        if body["model"] == "nomic-embed-text:latest":
            return httpx.Response(200, json={"capabilities": ["embedding"]})
        return httpx.Response(200, json={})

    qwen, nomic, old = await _provider(handler).catalog("chat")
    assert qwen.id == "qwen3:4b"
    assert qwen.capabilities == {Capability.STRUCTURED, Capability.TOOLS, Capability.THINKING}
    assert qwen.context_length == 40960 and qwen.price_in_per_m == 0.0
    assert nomic.capabilities == {Capability.EMBEDDING}
    assert old.capabilities is None


def test_status_is_cached_and_reports_unreachable():
    calls = []
    now = [0.0]

    def handler(request):
        calls.append(request.url.path)
        raise httpx.ConnectError("refused", request=request)

    provider = _provider(handler, clock=lambda: now[0])
    first = provider.status()
    assert first.state == "unreachable" and first.locality == "local" and BASE in first.detail
    provider.status()
    assert calls == ["/api/version"]
    now[0] = 16.0
    provider.status()
    assert calls == ["/api/version", "/api/version"]


def test_status_ready_when_version_answers():
    provider = _provider(lambda request: httpx.Response(200, json={"version": "0.35.1"}))
    assert provider.status().state == "ready"


def test_chat_model_targets_the_configured_server():
    chat = _provider(lambda r: httpx.Response(200)).chat_model(
        "qwen3:4b", temperature=0.1, timeout_s=180, options={"think": False})
    assert chat.model == "qwen3:4b" and chat.base_url == BASE
    assert chat.temperature == 0.1 and chat.reasoning is False
    assert chat.client_kwargs == {"timeout": 180}
    unset = _provider(lambda r: httpx.Response(200)).chat_model(
        "qwen3:4b", temperature=None, timeout_s=10, options={})
    assert unset.reasoning is None


async def test_embedder_uses_openai_compatible_endpoint_without_dimensions():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [0.5] + [0.0] * 767}],
                                         "usage": {"prompt_tokens": 3, "total_tokens": 3}})

    batch = await _provider(handler).embedder("nomic-embed-text", dimensions=768).embed(["سؤال"])
    assert batch.cost_usd == 0.0 and len(batch.vectors[0]) == 768
    assert str(seen[0].url) == f"{BASE}/v1/embeddings"
    assert "dimensions" not in json.loads(seen[0].content)


def test_registry_includes_ollama_and_its_errors():
    from ollama import ResponseError

    assert "ollama" in ProviderRegistry(Settings(_env_file=None)).names()
    assert ResponseError in provider_errors() and ConnectionError in provider_errors()
```

- [ ] **Step 3: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_ollama_provider.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.models_config.providers.ollama'`.

- [ ] **Step 4: Implement the adapter**

`backend/app/models_config/providers/ollama.py`:

```python
"""Ollama: local chat models, OpenAI-compatible embeddings and the installed-model list."""
from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Callable, Mapping
from typing import Any

import httpx

from app.config import Settings
from app.kb.embeddings import OpenAICompatibleEmbedder
from app.models_config.providers.base import UnsupportedOperation
from app.models_config.types import Capability, CatalogEntry, CatalogKind, ProviderStatus

CATALOG_TIMEOUT_S = 10.0
STATUS_TIMEOUT_S = 2.0
STATUS_TTL_S = 15.0
_CAPABILITIES = {
    "completion": Capability.STRUCTURED,  # Ollama applies JSON-schema output to any completion model.
    "tools": Capability.TOOLS,
    "vision": Capability.VISION,
    "thinking": Capability.THINKING,
    "embedding": Capability.EMBEDDING,
}


class OllamaProvider:
    name = "ollama"
    locality = "local"

    def __init__(self, settings: Settings, *, transport: httpx.BaseTransport | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._base = settings.ollama_base_url
        self._transport = transport
        self._clock = clock
        self._lock = threading.Lock()
        self._cached: tuple[float, ProviderStatus] | None = None

    def status(self) -> ProviderStatus:
        with self._lock:
            if self._cached is not None and self._clock() - self._cached[0] < STATUS_TTL_S:
                return self._cached[1]
        try:
            with httpx.Client(transport=self._transport, timeout=STATUS_TIMEOUT_S) as client:
                client.get(f"{self._base}/api/version").raise_for_status()
            status = ProviderStatus(self.name, self.locality, "ready")
        except httpx.HTTPError:
            status = ProviderStatus(self.name, self.locality, "unreachable",
                                    f"Ollama is not reachable at {self._base}.")
        with self._lock:
            self._cached = (self._clock(), status)
        return status

    async def catalog(self, kind: CatalogKind) -> list[CatalogEntry]:
        async with httpx.AsyncClient(transport=self._transport, timeout=CATALOG_TIMEOUT_S) as client:
            response = await client.get(f"{self._base}/api/tags")
            response.raise_for_status()
            names = []
            for item in response.json().get("models") or []:
                name = (item.get("model") or item.get("name")) if isinstance(item, dict) else None
                if isinstance(name, str) and name:
                    names.append(name)
            details = await asyncio.gather(*(self._show(client, name) for name in names))
        return [CatalogEntry(id=name, name=name, capabilities=capabilities, price_in_per_m=0.0,
                             price_out_per_m=0.0, context_length=context)
                for name, (capabilities, context) in zip(names, details, strict=True)]

    async def _show(self, client: httpx.AsyncClient, name: str):
        try:
            response = await client.post(f"{self._base}/api/show", json={"model": name})
            response.raise_for_status()
            body = response.json()
        except (httpx.HTTPError, ValueError):
            return None, None
        raw = body.get("capabilities") if isinstance(body, dict) else None
        capabilities = (frozenset(_CAPABILITIES[item] for item in raw if item in _CAPABILITIES)
                        if isinstance(raw, list) else None)
        info = body.get("model_info") if isinstance(body, dict) else None
        context = next((value for key, value in (info or {}).items()
                        if key.endswith(".context_length") and isinstance(value, int)), None)
        return capabilities, context

    def chat_model(self, model: str, *, temperature: float | None, timeout_s: float,
                   options: Mapping[str, Any]):
        from langchain_ollama import ChatOllama

        return ChatOllama(model=model, base_url=self._base, temperature=temperature,
                          reasoning=options.get("think"), client_kwargs={"timeout": timeout_s},
                          validate_model_on_init=False)

    def embedder(self, model: str, *, dimensions: int) -> OpenAICompatibleEmbedder:
        return OpenAICompatibleEmbedder(model=model, dimensions=dimensions,
                                        url=f"{self._base}/v1/embeddings", send_dimensions=False,
                                        transport=self._transport)

    def classifier(self, model: str):
        raise UnsupportedOperation("Ollama does not provide the Jev classifier.")
```

In `backend/app/models_config/providers/registry.py`, import `from app.models_config.providers.ollama import OllamaProvider`, add `"ollama": OllamaProvider(settings),` to the default providers, and make `provider_errors()`:

```python
def provider_errors() -> tuple[type[BaseException], ...]:
    """Errors any chat provider may raise for an unusable model request."""
    import httpx
    from ollama import ResponseError
    from openrouter.errors import OpenRouterError

    from app.llm import LLMUnavailable

    # The Ollama client raises the builtin ConnectionError when the server is down.
    return (httpx.HTTPError, OpenRouterError, ResponseError, ConnectionError, LLMUnavailable)
```

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/models_config -q`
Expected: PASS.

- [ ] **Step 6: Lint and commit**

```bash
uv run ruff check app tests
git add pyproject.toml uv.lock app/models_config/providers tests/models_config/test_ollama_provider.py
git commit -m "feat(models): add Ollama provider adapter"
```

---

### Task 4: Stored settings, the ActiveModels snapshot and intake pinning

**Files:**
- Create: `backend/app/models_config/db_models.py`, `backend/app/models_config/resolver.py`, `backend/app/models_config/store.py`, `backend/app/pipeline/stage6_draft/model_info.py`, `backend/tests/models_config_fakes.py`
- Modify: `backend/app/db/session.py:6-11`, `backend/app/db/workspace_schema.py`, `backend/app/intake/db_models.py:15-28`
- Test: `backend/tests/models_config/test_resolver.py`, `backend/tests/models_config/test_store.py`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces:
  - `DraftModelInfo(model: str, token_prices: tuple[float, float], timeout_s: float, embedding_model: str)` with `DraftModelInfo.from_settings(settings)`.
  - `ActiveModels(settings, choices: Mapping[Step, ModelChoice], registry)`; `ActiveModels.from_env(settings, registry=None)`; methods `choice(step)`, `locality(step)`, `is_local(step)`, `ready(step)`, `overall_locality()`, `temperature(step)`, `chat(step, *, timeout_s) -> BaseChatModel`, `structured_llm(*, max_retries=2) -> StructuredChatLLM`, `embedder()`, `jev_client()`, `token_prices(step)`, `draft_info()`, `model_ids() -> dict[str, str]`, `summary() -> dict`. Attributes `settings`, `registry`.
  - `ModelSettingsStore(session_factory, settings, registry=None)` with `registry`, `settings`, `load()`, `active()`, `choice(step)`, `describe() -> list[dict]`, `save(step, choice, *, changed_by, latency_ms, session=None)`, `audit(limit=50) -> list[dict]`, `intake_pin(session_id) -> tuple[ModelChoice, float]`.
  - Tables `model_settings`, `model_settings_audit`, `embedding_switch` (`EmbeddingSwitchRow`, used in Task 10); column `intake_sessions.model_choice`.
  - Test fakes: `NamedEmbedder`, `FakeProvider`, `fake_registry(settings, **providers)`.

Task 5 adds `StructuredChatLLM` to `app/llm.py`; `ActiveModels.structured_llm` imports it lazily, so this task's tests do not call `structured_llm`.

- [ ] **Step 1: Write the shared fakes**

`backend/tests/models_config_fakes.py`:

```python
"""Provider doubles: real store/resolver logic, scripted provider boundaries."""
from __future__ import annotations

from app.kb.contracts import EmbeddingBatch
from app.kb.embeddings import EmbeddingError
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.types import ProviderStatus
from tests.fakes import FakeJevRunnable


class NamedEmbedder:
    dimensions = 768

    def __init__(self, model, *, fail_for=()):
        self.model, self.fail_for, self.calls = model, tuple(fail_for), []

    async def embed(self, texts):
        self.calls.append(list(texts))
        if any(marker in text for text in texts for marker in self.fail_for):
            raise EmbeddingError("Fake embedding failure.")
        return EmbeddingBatch(tuple(tuple([1.0] + [0.0] * 767) for _ in texts))


class FakeProvider:
    def __init__(self, name, *, locality="cloud", state="ready", chat=None, entries=(),
                 catalog_error=None, classifier=None, embed_fail_for=()):
        self.name, self.locality, self.state = name, locality, state
        self.chat, self.entries, self.catalog_error = chat, list(entries), catalog_error
        self.classifier_obj, self.embed_fail_for = classifier, embed_fail_for
        self.chat_calls, self.catalog_calls, self.embedders = [], 0, []

    def status(self):
        return ProviderStatus(self.name, self.locality, self.state)

    async def catalog(self, kind):
        self.catalog_calls += 1
        if self.catalog_error is not None:
            raise self.catalog_error
        return list(self.entries)

    def chat_model(self, model, *, temperature, timeout_s, options):
        self.chat_calls.append({"model": model, "temperature": temperature,
                                "timeout_s": timeout_s, "options": dict(options)})
        if self.chat is None:
            raise AssertionError(f"{self.name} chat was not expected")
        return self.chat(model) if callable(self.chat) else self.chat

    def embedder(self, model, *, dimensions):
        embedder = NamedEmbedder(model, fail_for=self.embed_fail_for)
        self.embedders.append(embedder)
        return embedder

    def classifier(self, model):
        return self.classifier_obj or FakeJevRunnable(model=model)


def fake_registry(settings, **providers):
    defaults = {
        "openrouter": FakeProvider("openrouter"),
        "ollama": FakeProvider("ollama", locality="local"),
        "typesafe": FakeProvider("typesafe"),
    }
    return ProviderRegistry(settings, providers=defaults | providers)
```

`ScriptedChat` (in `tests/rag_fakes.py`) is a pydantic model and is not callable, so it can be passed directly as `chat=`.

- [ ] **Step 2: Write the failing resolver tests**

`backend/tests/models_config/test_resolver.py`:

```python
from app.config import Settings
from app.models_config.resolver import ActiveModels
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import FakeProvider, fake_registry


def _settings(**kw):
    return Settings(_env_file=None, **({"openrouter_api_key": "k", "typesafe_api_key": "t"} | kw))


def test_env_snapshot_is_cloud_and_records_refs():
    models = ActiveModels.from_env(_settings())
    assert models.overall_locality() == "cloud"
    assert models.model_ids() == {
        "intake": "openrouter:google/gemini-3.8-flash", "classify": "typesafe:jev-1.13.0",
        "extract": "openrouter:google/gemini-3.8-flash", "draft": "openrouter:google/gemini-3.8-flash",
        "embed": "openrouter:openai/text-embedding-3-small",
    }


def test_model_ids_keep_colons_in_model_names():
    settings = _settings()
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(settings))
    assert models.model_ids()["draft"] == "ollama:qwen3:4b"
    assert models.choice(Step.DRAFT).model == "qwen3:4b"


def test_local_draft_uses_local_timeout_zero_prices_and_option_temperature():
    settings = _settings(local_agent_timeout_s=200)
    ollama = FakeProvider("ollama", locality="local", chat=object())
    choice = ModelChoice("ollama", "qwen3:4b", {"think": False, "temperature": 0.3})
    models = ActiveModels(settings, {Step.DRAFT: choice}, fake_registry(settings, ollama=ollama))
    info = models.draft_info()
    assert info.model == "qwen3:4b" and info.timeout_s == 200 and info.token_prices == (0.0, 0.0)
    assert info.embedding_model == "openai/text-embedding-3-small"
    assert models.overall_locality() == "mixed"
    models.chat(Step.DRAFT, timeout_s=info.timeout_s)
    assert ollama.chat_calls == [{"model": "qwen3:4b", "temperature": 0.3, "timeout_s": 200,
                                  "options": {"think": False, "temperature": 0.3}}]


def test_default_temperature_and_cloud_prices():
    settings = _settings(anthropic_model="anthropic/claude-sonnet-5.5")
    models = ActiveModels.from_env(settings)
    assert models.temperature(Step.DRAFT) == 0.1 and models.temperature(Step.INTAKE) is None
    assert models.token_prices(Step.DRAFT) == settings.draft_token_prices
    assert models.token_prices(Step.EXTRACT) == (settings.price_gemini_flash_in, settings.price_gemini_flash_out)
    assert models.token_prices(Step.CLASSIFY) == (settings.price_jev_in, 0.0)


def test_ready_and_summary_follow_provider_status():
    settings = _settings()
    registry = fake_registry(settings, ollama=FakeProvider("ollama", locality="local", state="unreachable"))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, registry)
    assert not models.ready(Step.DRAFT) and models.ready(Step.EXTRACT)
    summary = models.summary()
    assert summary["locality"] == "mixed"
    assert summary["steps"]["draft"] == {"provider": "ollama", "model": "qwen3:4b",
                                         "locality": "local", "status": "unreachable"}
```

- [ ] **Step 3: Write the failing store tests (integration)**

`backend/tests/models_config/test_store.py`:

```python
import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.intake.db_models import IntakeSessionRow
from app.models_config.db_models import ModelSettingRow
from app.models_config.store import ModelSettingsStore
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import fake_registry

pytestmark = pytest.mark.integration


@pytest.fixture
def env():
    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="t",
                        local_intake_timeout_s=150)
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    yield settings, make_sessionmaker(engine)
    engine.dispose()


def _store(settings, sf):
    store = ModelSettingsStore(sf, settings, fake_registry(settings))
    store.load()
    return store


def test_empty_store_uses_env_defaults(env):
    store = _store(*env)
    assert store.choice(Step.DRAFT) == ModelChoice("openrouter", "google/gemini-3.8-flash")
    draft = next(item for item in store.describe() if item["step"] == "draft")
    assert draft["source"] == "env" and draft["updated_by"] is None
    assert draft["requirements"] == ["tools"] and draft["providers"] == ["openrouter", "ollama"]


def test_save_updates_cache_database_and_audit(env):
    settings, sf = env
    store = _store(settings, sf)
    choice = ModelChoice("ollama", "qwen3:4b", {"think": False})
    store.save(Step.DRAFT, choice, changed_by="Sara", latency_ms=1200)
    assert store.choice(Step.DRAFT) == choice
    assert _store(settings, sf).choice(Step.DRAFT) == choice
    [entry] = store.audit()
    assert entry["step"] == "draft" and entry["changed_by"] == "Sara"
    assert entry["previous"]["model"] == "google/gemini-3.8-flash"
    assert entry["current"] == choice.to_json() and entry["test_latency_ms"] == 1200
    draft = next(item for item in store.describe() if item["step"] == "draft")
    assert draft["source"] == "admin" and draft["locality"] == "local" and draft["updated_by"] == "Sara"


def test_rows_for_unknown_providers_are_ignored(env):
    settings, sf = env
    with sf.begin() as session:
        session.add(ModelSettingRow(step="draft", provider="retired", model="x", options={},
                                    updated_at=datetime.now(UTC), updated_by="old"))
        session.add(ModelSettingRow(step="no-such-step", provider="ollama", model="x", options={},
                                    updated_at=datetime.now(UTC), updated_by="old"))
    store = _store(settings, sf)
    assert store.choice(Step.DRAFT).provider == "openrouter"
    assert len(store.describe()) == 5


def test_intake_pin_keeps_the_first_model_for_a_session(env):
    settings, sf = env
    store = _store(settings, sf)
    session_id = uuid.uuid4()
    with sf.begin() as session:
        session.add(IntakeSessionRow(id=session_id, token_hash="h" * 64, state={}))
    store.save(Step.INTAKE, ModelChoice("ollama", "gemma3:4b"), changed_by="Sara", latency_ms=1)
    first, timeout = store.intake_pin(session_id)
    assert first == ModelChoice("ollama", "gemma3:4b") and timeout == 150
    store.save(Step.INTAKE, ModelChoice("openrouter", "google/gemini-2.5-flash"), changed_by="Sara", latency_ms=1)
    assert store.intake_pin(session_id)[0] == first
    assert store.intake_pin(uuid.uuid4())[0] == ModelChoice("openrouter", "google/gemini-2.5-flash")
```

- [ ] **Step 4: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_resolver.py tests/models_config/test_store.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.models_config.resolver'`.

- [ ] **Step 5: Add the tables and the intake column**

`backend/app/models_config/db_models.py`:

```python
"""Admin model settings, their audit trail and embedding switch jobs."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class ModelSettingRow(Base):
    __tablename__ = "model_settings"
    step: Mapped[str] = mapped_column(String(16), primary_key=True)
    provider: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(255))
    options: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_by: Mapped[str] = mapped_column(String(64))


class ModelSettingAuditRow(Base):
    __tablename__ = "model_settings_audit"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    step: Mapped[str] = mapped_column(String(16))
    previous: Mapped[dict | None] = mapped_column(JSONB)
    current: Mapped[dict] = mapped_column(JSONB)
    changed_by: Mapped[str] = mapped_column(String(64))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    test_latency_ms: Mapped[int] = mapped_column(Integer, default=0)


class EmbeddingSwitchRow(Base):
    __tablename__ = "embedding_switch"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    target: Mapped[dict] = mapped_column(JSONB)
    previous: Mapped[dict] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(32))
    total: Mapped[int] = mapped_column(Integer, default=0)
    done: Mapped[int] = mapped_column(Integer, default=0)
    failed_document_ids: Mapped[list] = mapped_column(JSONB, default=list)
    error: Mapped[str | None] = mapped_column(Text)
    started_by: Mapped[str] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
```

In `backend/app/db/session.py` add, next to the other registration imports:

```python
from app.models_config import db_models as model_config_db_models  # noqa: F401 -- register before create_all/drop_all
```

In `backend/app/intake/db_models.py`, add to `IntakeSessionRow` after `error_code`:

```python
    model_choice: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
```

In `backend/app/db/workspace_schema.py`, append inside `upgrade_workspace_schema` (still inside the `with engine.begin() as connection:` block):

```python
        # Intake sessions created before admin model settings have no pinned model.
        connection.execute(text(
            "ALTER TABLE IF EXISTS intake_sessions ADD COLUMN IF NOT EXISTS model_choice JSONB"
        ))
```

and update its docstring to `"""Apply additive schema upgrades that create_all cannot perform on existing tables."""`.

- [ ] **Step 6: Add DraftModelInfo**

`backend/app/pipeline/stage6_draft/model_info.py`:

```python
"""What the drafting agent needs to know about its model, independent of the provider."""
from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings


@dataclass(frozen=True)
class DraftModelInfo:
    model: str
    token_prices: tuple[float, float]
    timeout_s: float
    embedding_model: str

    @classmethod
    def from_settings(cls, settings: Settings) -> DraftModelInfo:
        return cls(settings.draft_model, settings.draft_token_prices, settings.agent_timeout_s,
                   settings.embedding_model)
```

- [ ] **Step 7: Implement the resolver**

`backend/app/models_config/resolver.py`:

```python
"""One immutable snapshot of the configured models; consumers build clients only through it."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from app.config import Settings
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import DEFAULT_TEMPERATURE, EMBED_DIMENSIONS, draft_timeout_s, env_defaults
from app.models_config.types import Locality, ModelChoice, Step
from app.pipeline.stage6_draft.model_info import DraftModelInfo

EXTRACT_TIMEOUT_S = 60.0


class ActiveModels:
    def __init__(self, settings: Settings, choices: Mapping[Step, ModelChoice],
                 registry: ProviderRegistry) -> None:
        self.settings = settings
        self.registry = registry
        self._choices: dict[Step, ModelChoice] = {**env_defaults(settings), **dict(choices)}

    @classmethod
    def from_env(cls, settings: Settings, registry: ProviderRegistry | None = None) -> ActiveModels:
        return cls(settings, {}, registry or ProviderRegistry(settings))

    def choice(self, step: Step) -> ModelChoice:
        return self._choices[step]

    def locality(self, step: Step) -> Locality:
        return self.registry.get(self.choice(step).provider).locality

    def is_local(self, step: Step) -> bool:
        return self.locality(step) == "local"

    def ready(self, step: Step) -> bool:
        return self.registry.status(self.choice(step).provider).state == "ready"

    def overall_locality(self) -> Literal["local", "cloud", "mixed"]:
        values = {self.locality(step) for step in Step}
        return values.pop() if len(values) == 1 else "mixed"

    def temperature(self, step: Step) -> float | None:
        value = self.choice(step).options.get("temperature")
        return value if value is not None else DEFAULT_TEMPERATURE.get(step)

    def chat(self, step: Step, *, timeout_s: float):
        choice = self.choice(step)
        return self.registry.get(choice.provider).chat_model(
            choice.model, temperature=self.temperature(step), timeout_s=timeout_s, options=choice.options)

    def structured_llm(self, *, max_retries: int = 2):
        from app.llm import StructuredChatLLM

        choice = self.choice(Step.EXTRACT)
        provider = self.registry.get(choice.provider)
        timeout = self.settings.local_agent_timeout_s if provider.locality == "local" else EXTRACT_TIMEOUT_S
        override = choice.options.get("temperature")
        price_in, price_out = self.token_prices(Step.EXTRACT)

        def chat_factory(temperature: float):
            return provider.chat_model(choice.model, temperature=temperature if override is None else override,
                                       timeout_s=timeout, options=choice.options)

        return StructuredChatLLM(chat_factory=chat_factory, price_in_per_m=price_in,
                                 price_out_per_m=price_out, max_retries=max_retries)

    def embedder(self):
        choice = self.choice(Step.EMBED)
        return self.registry.get(choice.provider).embedder(choice.model, dimensions=EMBED_DIMENSIONS)

    def jev_client(self) -> Any:
        choice = self.choice(Step.CLASSIFY)
        return self.registry.get(choice.provider).classifier(choice.model)

    def token_prices(self, step: Step) -> tuple[float, float]:
        if self.is_local(step):
            return 0.0, 0.0
        settings = self.settings
        if step is Step.CLASSIFY:
            return settings.price_jev_in, 0.0
        if step is Step.EMBED:
            return settings.price_embedding_in, 0.0
        if step is Step.DRAFT:
            if self.choice(step) == env_defaults(settings)[Step.DRAFT]:
                return settings.draft_token_prices
            if self.choice(step).model.startswith("anthropic/"):
                return settings.price_anthropic_in, settings.price_anthropic_out
        return settings.price_gemini_flash_in, settings.price_gemini_flash_out

    def draft_info(self) -> DraftModelInfo:
        return DraftModelInfo(model=self.choice(Step.DRAFT).model, token_prices=self.token_prices(Step.DRAFT),
                              timeout_s=draft_timeout_s(self.settings, self.locality(Step.DRAFT)),
                              embedding_model=self.choice(Step.EMBED).model)

    def model_ids(self) -> dict[str, str]:
        return {step.value: self.choice(step).ref for step in Step}

    def summary(self) -> dict[str, Any]:
        steps = {}
        for step in Step:
            choice = self.choice(step)
            status = self.registry.status(choice.provider)
            steps[step.value] = {"provider": choice.provider, "model": choice.model,
                                 "locality": status.locality, "status": status.state}
        return {"locality": self.overall_locality(), "steps": steps}
```

- [ ] **Step 8: Implement the store**

`backend/app/models_config/store.py`:

```python
"""Admin model settings: Postgres is durable, an in-process cache serves reads.

This API runs one worker process, so the cache is authoritative after load()
and is updated on every save.
"""
from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.intake.db_models import IntakeSessionRow
from app.models_config.db_models import ModelSettingAuditRow, ModelSettingRow
from app.models_config.providers.registry import ProviderRegistry, UnknownProvider
from app.models_config.resolver import ActiveModels
from app.models_config.steps import PROVIDERS_FOR_STEP, REQUIREMENTS, intake_timeout_s
from app.models_config.types import ModelChoice, Step

logger = logging.getLogger(__name__)


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


class ModelSettingsStore:
    def __init__(self, session_factory: sessionmaker, settings: Settings,
                 registry: ProviderRegistry | None = None) -> None:
        self._sf = session_factory
        self.settings = settings
        self.registry = registry or ProviderRegistry(settings)
        self._lock = threading.Lock()
        self._rows: dict[Step, dict[str, Any]] = {}

    def load(self) -> None:
        with self._sf() as session:
            rows = list(session.scalars(select(ModelSettingRow)))
        loaded: dict[Step, dict[str, Any]] = {}
        for row in rows:
            try:
                step = Step(row.step)
                self.registry.get(row.provider)
            except (ValueError, UnknownProvider):
                logger.warning("Ignoring stored model setting %s=%s:%s", row.step, row.provider, row.model)
                continue
            loaded[step] = {"choice": ModelChoice(row.provider, row.model, dict(row.options or {})),
                            "updated_at": row.updated_at, "updated_by": row.updated_by}
        with self._lock:
            self._rows = loaded

    def active(self) -> ActiveModels:
        with self._lock:
            choices = {step: entry["choice"] for step, entry in self._rows.items()}
        return ActiveModels(self.settings, choices, self.registry)

    def choice(self, step: Step) -> ModelChoice:
        return self.active().choice(step)

    def describe(self) -> list[dict[str, Any]]:
        active = self.active()
        with self._lock:
            rows = dict(self._rows)
        described = []
        for step in Step:
            choice, entry = active.choice(step), rows.get(step)
            status = self.registry.status(choice.provider)
            described.append({
                "step": step.value, "provider": choice.provider, "model": choice.model,
                "options": dict(choice.options), "source": "admin" if entry else "env",
                "updated_at": _iso(entry["updated_at"]) if entry else None,
                "updated_by": entry["updated_by"] if entry else None,
                "locality": status.locality, "status": status.state, "status_detail": status.detail,
                "requirements": sorted(c.value for c in REQUIREMENTS[step]),
                "providers": list(PROVIDERS_FOR_STEP[step]),
            })
        return described

    def save(self, step: Step, choice: ModelChoice, *, changed_by: str, latency_ms: int,
             session: Session | None = None) -> None:
        """Persist and audit. With an external session the caller commits, then calls load()."""
        own = session is None
        session = session or self._sf()
        try:
            previous = self.choice(step)
            now = datetime.now(UTC)
            row = session.get(ModelSettingRow, step.value, with_for_update=True)
            if row is None:
                row = ModelSettingRow(step=step.value)
                session.add(row)
            row.provider, row.model, row.options = choice.provider, choice.model, dict(choice.options)
            row.updated_at, row.updated_by = now, changed_by
            session.add(ModelSettingAuditRow(step=step.value, previous=previous.to_json(),
                                             current=choice.to_json(), changed_by=changed_by,
                                             changed_at=now, test_latency_ms=latency_ms))
            if own:
                session.commit()
        finally:
            if own:
                session.close()
        if own:
            with self._lock:
                self._rows[step] = {"choice": choice, "updated_at": now, "updated_by": changed_by}

    def audit(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._sf() as session:
            rows = session.scalars(select(ModelSettingAuditRow)
                                   .order_by(ModelSettingAuditRow.id.desc()).limit(limit))
            return [{"id": row.id, "step": row.step, "previous": row.previous, "current": row.current,
                     "changed_by": row.changed_by, "changed_at": _iso(row.changed_at),
                     "test_latency_ms": row.test_latency_ms} for row in rows]

    def intake_pin(self, session_id: UUID) -> tuple[ModelChoice, float]:
        """The intake model for one customer conversation: pinned on its first model call."""
        current = self.choice(Step.INTAKE)
        with self._sf.begin() as session:
            session.execute(update(IntakeSessionRow)
                            .where(IntakeSessionRow.id == session_id, IntakeSessionRow.model_choice.is_(None))
                            .values(model_choice=current.to_json()))
            stored = session.scalar(select(IntakeSessionRow.model_choice)
                                    .where(IntakeSessionRow.id == session_id))
        choice = current
        if stored:
            try:
                candidate = ModelChoice.from_json(stored)
                self.registry.get(candidate.provider)
                choice = candidate
            except (ValueError, UnknownProvider):
                logger.warning("Intake session %s has an unusable pinned model", session_id)
        return choice, intake_timeout_s(self.settings, self.registry.get(choice.provider).locality)
```

- [ ] **Step 9: Run the tests**

Run: `uv run pytest tests/models_config tests/test_db_initialization.py tests/intake -q`
Expected: PASS (integration tests need the db container).

- [ ] **Step 10: Lint and commit**

```bash
uv run ruff check app tests
git add app/models_config app/db app/intake/db_models.py app/pipeline/stage6_draft/model_info.py tests/models_config tests/models_config_fakes.py
git commit -m "feat(models): store admin model settings and resolve active models"
```

---

### Task 5: Pipeline and knowledge base use ActiveModels

**Files:**
- Modify: `backend/app/llm.py`, `backend/app/pipeline/factory.py`, `backend/app/pipeline/stage6_draft/agent.py`, `backend/app/kb/service.py:133-138`, `backend/app/services/knowledge_runtime.py:12-14`
- Create: `backend/app/models_config/embedder.py`
- Test: `backend/tests/test_factory.py`, `backend/tests/test_llm.py`, `backend/tests/models_config/test_embedder.py`

**Interfaces:**
- Consumes: Task 4 `ActiveModels`, `DraftModelInfo`, `ModelSettingsStore`, fakes.
- Produces:
  - `StructuredChatLLM(*, chat_factory: Callable[[float], Any], price_in_per_m, price_out_per_m, max_retries=2)` implementing `StructuredLLM`. `GeminiStructuredLLM` is removed.
  - `build_pipeline(settings, mode, txn_repo, *, models: ActiveModels | None = None, jev_client=None, llm=None, drafter=None, model_factory=None, knowledge=None, investigation=None, credential_checker=None)`.
  - `factory.make_gemini_llm(settings)`, `factory.make_draft_model(settings)`, `factory.model_ids(settings)` remain as `.env` conveniences; `factory.make_jev_client` is removed.
  - `RagDrafter(settings, *, model_factory, knowledge, investigation, credential_checker, info: DraftModelInfo | None = None)`.
  - `ConfiguredEmbedder(store)` with `model` (property), `dimensions == 768`, `async embed(texts)`.
  - `make_knowledge_service(session_factory, settings, store=None)`.

- [ ] **Step 1: Write the failing tests**

Create `backend/tests/models_config/test_embedder.py`:

```python
from app.config import Settings
from app.models_config.embedder import ConfiguredEmbedder
from app.models_config.resolver import ActiveModels
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import fake_registry


class _Store:
    def __init__(self, models):
        self.models = models

    def choice(self, step):
        return self.models.choice(step)

    def active(self):
        return self.models


async def test_configured_embedder_follows_the_current_setting():
    settings = Settings(_env_file=None, openrouter_api_key="k")
    registry = fake_registry(settings)
    store = _Store(ActiveModels(settings, {}, registry))
    embedder = ConfiguredEmbedder(store)
    assert embedder.model == "openai/text-embedding-3-small" and embedder.dimensions == 768
    store.models = ActiveModels(settings, {Step.EMBED: ModelChoice("ollama", "nomic-embed-text")}, registry)
    assert embedder.model == "nomic-embed-text"
    batch = await embedder.embed(["سؤال"])
    assert len(batch.vectors[0]) == 768
    assert registry.get("ollama").embedders[0].model == "nomic-embed-text"
```

In `backend/tests/test_factory.py`:

Replace `test_model_ids` with:

```python
def test_model_ids():
    assert model_ids(_settings()) == {
        "intake": "openrouter:google/gemini-3.8-flash", "classify": "typesafe:jev-1.13.0",
        "extract": "openrouter:google/gemini-3.8-flash", "draft": "openrouter:google/gemini-3.8-flash",
        "embed": "openrouter:openai/text-embedding-3-small",
    }
    claude = model_ids(_settings(anthropic_model="anthropic/claude-sonnet-5.5"))
    assert claude["draft"] == "openrouter:anthropic/claude-sonnet-5.5"
    assert claude["extract"] == "openrouter:google/gemini-3.8-flash"
```

Replace `test_jev_mode_builds_real_jev_checker_when_only_key_is_supplied` with:

```python
async def test_jev_mode_builds_real_jev_checker_from_the_classify_provider():
    from app.models_config.resolver import ActiveModels
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import Knowledge, ScriptedChat, draft_state, script

    settings = _settings(openrouter_api_key="test", typesafe_api_key="test")
    typesafe = FakeProvider("typesafe", classifier=FakeJevRunnable(
        category="general_inquiry", flags={"requests_credentials": 0.9}))
    models = ActiveModels(settings, {}, fake_registry(settings, typesafe=typesafe))
    graph = build_pipeline(settings, "jev", REPO, models=models, llm=FakeStructuredLLM([None]),
                           knowledge=Knowledge(), investigation=object(),
                           model_factory=lambda: ScriptedChat(steps=script()))
    [outcome], summary = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.decision.reasons == ("draft_failed_guardrail",)
    assert "requests_credentials" in outcome.decision.note and not summary.degraded
```

In `test_sql_defaults_retrieve_real_indexed_evidence`, delete the line `monkeypatch.setattr(factory, "OpenRouterEmbedder", lambda settings: PaidEmbedder())`, remove the unused `from app.pipeline import factory` import and `monkeypatch` parameter, and change the `build_pipeline(...)` call to pass a model snapshot whose embedder is a `PaidEmbedder`:

```python
        from app.models_config.resolver import ActiveModels
        from tests.models_config_fakes import FakeProvider, fake_registry

        class PaidProvider(FakeProvider):
            def embedder(self, model, *, dimensions):
                return PaidEmbedder()

        models = ActiveModels(settings, {}, fake_registry(settings, openrouter=PaidProvider("openrouter")))
        graph = build_pipeline(settings, "jev", SqlTransactionRepo(sf), models=models,
                               jev_client=FakeJevRunnable(category="general_inquiry"),
                               model_factory=lambda: model)
```

Append two new tests to `backend/tests/test_factory.py`:

```python
async def test_local_draft_model_is_built_by_its_provider_with_local_timeout():
    from app.models_config.resolver import ActiveModels
    from app.models_config.types import ModelChoice, Step
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import REPLY, Knowledge, ScriptedChat, draft_state, script

    settings = _settings(typesafe_api_key="t", local_agent_timeout_s=200)
    ollama = FakeProvider("ollama", locality="local", chat=ScriptedChat(steps=script()))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")},
                          fake_registry(settings, ollama=ollama))
    graph = build_pipeline(settings, "jev", REPO, models=models,
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([None]), knowledge=Knowledge(), investigation=object())
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.draft.text == REPLY
    assert ollama.chat_calls[0]["model"] == "qwen3:4b" and ollama.chat_calls[0]["timeout_s"] == 200
    assert outcome.draft.trace[-1]["model"] == "qwen3:4b"


async def test_unreachable_local_draft_provider_never_falls_back_to_cloud():
    from app.models_config.resolver import ActiveModels
    from app.models_config.types import ModelChoice, Step
    from app.pipeline.graph import run_batch
    from tests.models_config_fakes import FakeProvider, fake_registry
    from tests.rag_fakes import Knowledge, draft_state

    settings = _settings(openrouter_api_key="k", typesafe_api_key="t")
    openrouter = FakeProvider("openrouter")  # chat=None: any chat call fails the test
    registry = fake_registry(settings, openrouter=openrouter,
                             ollama=FakeProvider("ollama", locality="local", state="unreachable"))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, registry)
    graph = build_pipeline(settings, "jev", REPO, models=models,
                           jev_client=FakeJevRunnable(category="general_inquiry"),
                           llm=FakeStructuredLLM([None]), knowledge=Knowledge(), investigation=object())
    [outcome], _ = await run_batch(graph, [draft_state()["ticket"]], concurrency=1)
    assert outcome.decision.reasons == ("llm_unavailable",)
    assert openrouter.chat_calls == []
```

In `backend/tests/test_llm.py`:
- Change the imports to `from app.llm import StructuredChatLLM` and keep `from app.pipeline.factory import make_gemini_llm`.
- Replace `_llm()` with:

```python
def _llm():
    return StructuredChatLLM(chat_factory=lambda temperature: None, price_in_per_m=1.0, price_out_per_m=2.0)
```

- In `test_openrouter_retry_budget_is_bounded`, replace the `GeminiStructuredLLM(...)` construction with:

```python
    from app.models_config.resolver import ActiveModels

    llm = ActiveModels.from_env(Settings(_env_file=None, openrouter_api_key="test-key")).structured_llm(
        max_retries=max_retries)
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/test_factory.py tests/test_llm.py tests/models_config/test_embedder.py -q`
Expected: FAIL with `ImportError: cannot import name 'StructuredChatLLM'` and `TypeError: build_pipeline() got an unexpected keyword argument 'models'`.

- [ ] **Step 3: Make the structured LLM provider-neutral**

In `backend/app/llm.py`, change the docstring to `"""Structured-output sampling over any LangChain chat model, behind a small protocol."""`, add `from collections.abc import Callable` to the imports, and replace the whole `class GeminiStructuredLLM:` block with:

```python
class StructuredChatLLM:
    """`chat.with_structured_output(method="json_schema", include_raw=True)` for any provider."""

    def __init__(
        self,
        *,
        chat_factory: Callable[[float], Any],
        price_in_per_m: float,
        price_out_per_m: float,
        max_retries: int = 2,
    ) -> None:
        self._chat_factory = chat_factory
        self._price_in = price_in_per_m
        self._price_out = price_out_per_m
        self._max_retries = max_retries
        self._cache: dict[tuple[type, float], Any] = {}

    def _runnable(self, schema: type[BaseModel], temperature: float) -> Any:
        key = (schema, temperature)
        if key not in self._cache:
            chat = self._chat_factory(temperature)
            self._cache[key] = chat.with_structured_output(schema, method="json_schema", include_raw=True)
        return self._cache[key]
```

Keep `sample`, `_invoke` and `to_sample` exactly as they are, indented under `StructuredChatLLM`.

- [ ] **Step 4: Rewrite the factory**

Replace `backend/app/pipeline/factory.py` with:

```python
"""Wire settings and the active model snapshot into a compiled pipeline graph."""
from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import Settings
from app.db.repository import SqlTransactionRepo
from app.kb.service import KnowledgeService
from app.llm import StructuredChatLLM, StructuredLLM
from app.models_config.resolver import ActiveModels
from app.models_config.types import Step
from app.pipeline.graph import MODES, PipelineDeps, build_graph
from app.pipeline.stage2_classify.jev import JevClassifier
from app.pipeline.stage3_extract.gemini import GeminiExtractor
from app.pipeline.stage4_lookup.lookup import TransactionRepo
from app.pipeline.stage6_draft.agent import RagDrafter
from app.pipeline.stage6_draft.credentials import (
    CredentialChecker,
    DegradedCredentialChecker,
    JevCredentialChecker,
)
from app.pipeline.stage6_draft.drafting import Drafter, NullDrafter, UnavailableDrafter
from app.pipeline.stage6_draft.investigation import SqlInvestigationRepo
from app.taxonomy import load_taxonomy


class ConfigError(RuntimeError):
    """Missing or invalid configuration (for example, an API key)."""


def make_gemini_llm(settings: Settings) -> StructuredChatLLM:
    """The .env-configured extraction model (CLI and tests)."""
    return ActiveModels.from_env(settings).structured_llm()


def model_ids(settings: Settings) -> dict[str, str]:
    return ActiveModels.from_env(settings).model_ids()


def make_draft_model(settings: Settings) -> BaseChatModel:
    # The agent retries individual transient requests, inside its overall
    # deadline; providers must never retry on their own.
    models = ActiveModels.from_env(settings)
    return models.chat(Step.DRAFT, timeout_s=models.draft_info().timeout_s)


def build_pipeline(settings: Settings, mode: str, txn_repo: TransactionRepo, *,
                   models: ActiveModels | None = None,
                   jev_client: Any = None, llm: StructuredLLM | None = None,
                   drafter: Drafter | None = None,
                   model_factory: Callable[[], BaseChatModel] | None = None,
                   knowledge: KnowledgeService | None = None,
                   investigation: SqlInvestigationRepo | None = None,
                   credential_checker: CredentialChecker | None = None):
    """Build the Jev classifier and, for SQL repositories, an isolated bounded drafter.

    `models` is the snapshot for this run; omitted, the .env defaults apply.
    A supplied drafter wins. SQL defaults use the repository's public session
    factory; alternative repositories may opt into RAG by supplying BOTH adapters.
    A no-DB repository without both adapters stays classification-only.
    """
    if mode not in MODES:
        raise ConfigError(f"unknown mode {mode!r}; choose one of {MODES}")
    models = models or ActiveModels.from_env(settings)
    taxonomy = load_taxonomy(settings.taxonomy_path)
    if llm is None and models.ready(Step.EXTRACT):
        llm = models.structured_llm()
    if jev_client is None:
        if not models.ready(Step.CLASSIFY):
            raise ConfigError("TYPESAFE_API_KEY is required for Jev classification")
        jev_client = models.jev_client()
    jev_price = models.token_prices(Step.CLASSIFY)[0]
    jev = JevClassifier(
        jev_client, taxonomy, model_id=models.choice(Step.CLASSIFY).model, t_jev=settings.t_jev,
        min_top_prob=settings.jev_min_top_prob, price_in_per_m=jev_price,
        max_state_chars=settings.max_state_chars,
    )
    if drafter is None:
        database_backed = isinstance(txn_repo, SqlTransactionRepo)
        if not settings.rag_enabled:
            drafter = NullDrafter("rag_disabled")
        elif not database_backed and (knowledge is None or investigation is None):
            drafter = NullDrafter("no_database")
        elif not models.ready(Step.DRAFT):
            drafter = UnavailableDrafter()
        else:
            if knowledge is None:
                knowledge = KnowledgeService(txn_repo.session_factory, settings, models.embedder())
            if investigation is None:
                investigation = SqlInvestigationRepo(txn_repo.session_factory)
            if credential_checker is None:
                if models.ready(Step.CLASSIFY):
                    credential_checker = JevCredentialChecker(jev_client, price_in_per_m=jev_price)
                else:
                    credential_checker = DegradedCredentialChecker()
            info = models.draft_info()
            drafter = RagDrafter(settings,
                                 model_factory=model_factory or partial(models.chat, Step.DRAFT,
                                                                        timeout_s=info.timeout_s),
                                 knowledge=knowledge, investigation=investigation,
                                 credential_checker=credential_checker, info=info)
    deps = PipelineDeps(
        taxonomy=taxonomy, txn_repo=txn_repo, jev=jev,
        gap_filler=GeminiExtractor(llm, max_state_chars=settings.max_state_chars) if llm else None,
        drafter=drafter,
    )
    return build_graph(deps)
```

- [ ] **Step 5: Make the draft agent provider-neutral**

In `backend/app/pipeline/stage6_draft/agent.py`:

1. Delete `from openrouter.errors import OpenRouterError` and `from app.models_config.providers.openrouter_chat import DraftProviderResponseError`.
2. Add `from app.models_config.providers.registry import provider_errors` and `from app.pipeline.stage6_draft.model_info import DraftModelInfo`.
3. Replace `_PROVIDER_ERRORS = (httpx.HTTPError, OpenRouterError, LLMUnavailable)` with `_PROVIDER_ERRORS = provider_errors()`.
4. Add this helper below `_error_cost`:

```python
def _has_response_usage(error: BaseException) -> bool:
    """Provider failures that still carry a paid response's usage (for example OpenRouter's)."""
    return isinstance(error, LLMUnavailable) and hasattr(error, "usage_metadata") and hasattr(error, "response_metadata")
```

5. In `_ModelUsage`, change `__init__` to:

```python
    def __init__(self, context: DraftContext, info: DraftModelInfo):
        self.context, self.info = context, info
        self.seen: set[str] = set()
        self.cost_usd = 0.0
```

   replace `price_in, price_out = self.settings.draft_token_prices` with `price_in, price_out = self.info.token_prices`, replace both `self.settings.draft_model` occurrences with `self.info.model`, and replace `if isinstance(error, DraftProviderResponseError):` with `if _has_response_usage(error):`.
6. Change `RagDrafter.__init__` to:

```python
    def __init__(self, settings: Settings, *, model_factory: Callable[[], BaseChatModel],
                 knowledge: KnowledgeService, investigation: SqlInvestigationRepo,
                 credential_checker: CredentialChecker, info: DraftModelInfo | None = None):
        self.settings, self.model_factory = settings, model_factory
        self.knowledge, self.investigation = knowledge, investigation
        self.credential_checker = credential_checker
        self.info = info or DraftModelInfo.from_settings(settings)
```

7. In `draft()`: `usage = _ModelUsage(context, self.info)`; the budget line becomes `budget = ticket_run.draft_budget(self.info.timeout_s) if ticket_run else self.info.timeout_s`; in the final trace entry use `"model": self.info.model` and `"embedding_model": self.info.embedding_model`.

- [ ] **Step 6: Let the knowledge base follow the configured embedder**

Create `backend/app/models_config/embedder.py`:

```python
"""An Embedder for the long-lived KnowledgeService that follows the current embed setting."""
from __future__ import annotations

from typing import Protocol

from app.kb.contracts import EmbeddingBatch
from app.models_config.resolver import ActiveModels
from app.models_config.steps import EMBED_DIMENSIONS
from app.models_config.types import ModelChoice, Step


class _Store(Protocol):
    def choice(self, step: Step) -> ModelChoice: ...

    def active(self) -> ActiveModels: ...


class ConfiguredEmbedder:
    dimensions = EMBED_DIMENSIONS

    def __init__(self, store: _Store) -> None:
        self._store = store

    @property
    def model(self) -> str:
        return self._store.choice(Step.EMBED).model

    async def embed(self, texts: list[str]) -> EmbeddingBatch:
        # KnowledgeService re-reads `model` after embedding and rejects a switch mid-call.
        return await self._store.active().embedder().embed(texts)
```

In `backend/app/kb/service.py`, replace `_metadata` with:

```python
    def _metadata(self) -> tuple[str, int]:
        if self._embedder.dimensions != self._settings.embed_dim or self._embedder.dimensions != 768:
            raise ValueError("Embedding configuration does not match the provider/index schema.")
        return self._embedder.model, self._embedder.dimensions
```

In `backend/app/services/knowledge_runtime.py`, replace the `OpenRouterEmbedder` import with:

```python
from app.models_config.embedder import ConfiguredEmbedder
from app.models_config.store import ModelSettingsStore
```

and `make_knowledge_service` with:

```python
def make_knowledge_service(session_factory, settings, store=None):
    # The configured embedder owns a short-lived HTTP client per invocation, not per app.
    if store is None:
        store = ModelSettingsStore(session_factory, settings)
        store.load()
    return KnowledgeService(session_factory, settings, ConfiguredEmbedder(store))
```

- [ ] **Step 7: Run the full backend suite**

Run: `uv run pytest -q`
Expected: PASS. If a test still refers to `GeminiStructuredLLM`, `make_jev_client` or `settings.draft_model` in a trace assertion, update it to the new names shown above; behavior assertions must not change.

- [ ] **Step 8: Lint and commit**

```bash
uv run ruff check app tests
git add app tests
git commit -m "refactor(pipeline): build every model through the active model snapshot"
```

---

### Task 6: Intake uses the configured, per-session model

**Files:**
- Modify: `backend/app/intake/model.py`, `backend/app/intake/graph.py`, `backend/app/services/intake_runtime.py`, `backend/app/intake/submission.py:39-41,97-99`
- Modify (rename only): `backend/tests/intake/test_model.py`, `backend/tests/intake/test_graph.py`, `backend/tests/intake/live_probe.py`
- Test: `backend/tests/intake/test_model.py` (append), `backend/tests/intake/test_model_pin.py`

**Interfaces:**
- Consumes: Task 4 `ModelSettingsStore.intake_pin`, `ProviderRegistry`, `env_defaults`, `intake_timeout_s`.
- Produces:
  - `ModelBudget(timeout_s, max_requests, choice: ModelChoice | None = None)` with attribute `choice`.
  - `IntakeModel(settings, *, registry=None, runnable_factory=None)` (renamed from `OpenRouterIntakeModel`).
  - `IntakeGraph(model, taxonomy, store, settings, *, choice_for: Callable[[UUID], tuple[ModelChoice, float]] | None = None)`; `async _budget(context) -> ModelBudget`.
  - `make_intake_service(session_factory, settings, taxonomy, *, model_store=None)`.
  - `SubmissionService(session_factory, settings, *, model_store=None)`.

- [ ] **Step 1: Rename the class in tests**

Run: `sed -i 's/OpenRouterIntakeModel/IntakeModel/g' tests/intake/test_model.py tests/intake/test_graph.py tests/intake/live_probe.py`

- [ ] **Step 2: Write the failing tests**

Append to `backend/tests/intake/test_model.py`:

```python
def test_budget_choice_selects_provider_model_and_local_timeout():
    from app.models_config.types import ModelChoice
    from tests.models_config_fakes import FakeProvider, fake_registry

    runnable = CapturingRunnable()

    class StructuredChat:
        def with_structured_output(self, schema, **kwargs):
            assert kwargs == {"method": "json_schema", "include_raw": True}
            return runnable

    settings = Settings(_env_file=None, local_intake_timeout_s=150)
    ollama = FakeProvider("ollama", locality="local", chat=StructuredChat())
    model = IntakeModel(settings, registry=fake_registry(settings, ollama=ollama))
    budget = ModelBudget(60, 3, choice=ModelChoice("ollama", "gemma3:4b", {"temperature": 0.2}))

    import asyncio
    result = asyncio.run(model.analyze(context([message("hello", language="en")]), [], budget))
    assert ollama.chat_calls == [{"model": "gemma3:4b", "temperature": 0.2, "timeout_s": 150,
                                  "options": {"temperature": 0.2}}]
    assert result.trace[-1]["model"] == "gemma3:4b"
```

Create `backend/tests/intake/test_model_pin.py`:

```python
import pytest

from app.config import Settings
from app.intake.errors import ModelUnavailable
from app.intake.graph import IntakeGraph
from app.models_config.types import ModelChoice
from tests.intake.helpers import context, message


async def test_graph_budget_uses_the_pinned_choice_and_timeout(tax):
    seen = []
    choice = ModelChoice("ollama", "gemma3:4b")

    def choice_for(session_id):
        seen.append(session_id)
        return choice, 150.0

    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None), choice_for=choice_for)
    turn = context([message("hello", language="en")])
    budget = await graph._budget(turn)
    assert budget.choice == choice and 149 < budget.remaining_s() <= 150
    assert seen == [turn.session_id]


async def test_pin_failure_is_reported_as_model_unavailable(tax):
    def broken(session_id):
        raise RuntimeError("database down")

    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None), choice_for=broken)
    with pytest.raises(ModelUnavailable):
        await graph._budget(context([message("hello", language="en")]))


async def test_without_pinning_the_budget_uses_settings(tax):
    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None, intake_timeout_s=42))
    budget = await graph._budget(context([message("hi", language="en")]))
    assert budget.choice is None and budget.remaining_s() <= 42
```

- [ ] **Step 3: Run the tests to confirm they fail**

Run: `uv run pytest tests/intake/test_model.py tests/intake/test_model_pin.py -q`
Expected: FAIL with `ImportError: cannot import name 'IntakeModel'`.

- [ ] **Step 4: Implement the intake model changes**

In `backend/app/intake/model.py`:

1. Add imports:

```python
import json

from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import env_defaults, intake_timeout_s
from app.models_config.types import ModelChoice, Step
```

2. `ModelBudget.__init__` becomes:

```python
    def __init__(self, timeout_s: float, max_requests: int, choice: ModelChoice | None = None) -> None:
        self.max_requests = max_requests
        self.deadline = time.monotonic() + timeout_s
        self.used = 0
        self.trace: list[dict] = []
        self.choice = choice
```

3. Replace `class OpenRouterIntakeModel:` through its `_runnable` method with:

```python
class IntakeModel:
    def __init__(self, settings: Settings, *, registry: ProviderRegistry | None = None,
                 runnable_factory=None) -> None:
        self.settings = settings
        self._registry = registry or ProviderRegistry(settings)
        self._runnable_factory = runnable_factory
        self._cache: dict[tuple, object] = {}

    async def analyze(self, context: TurnContext, images: list[ImageInput], budget: ModelBudget) -> ModelCall:
        system, blocks = _analysis_prompt(context, images)
        return await self._invoke(Analysis, system, blocks, budget,
            validate=lambda value: merge_analysis(context, value, visible_image_ids={item.id for item in images}))

    async def summarize(self, state: IntakeState, language: str, budget: ModelBudget) -> ModelCall:
        system, blocks = _review_prompt(state, language)
        def validate(value):
            validate_review_numbers(state, value)
            if not set(material_keys(state.category)).issubset(value.fact_keys):
                raise InvalidEvidence("Include all required_fact_keys, even when their values are unknown.")
        return await self._invoke(ReviewText, system, blocks, budget, validate=validate)

    def _choice(self, budget: ModelBudget) -> ModelChoice:
        return budget.choice or env_defaults(self.settings)[Step.INTAKE]

    def _runnable(self, schema: type, budget: ModelBudget):
        if self._runnable_factory is not None:
            return self._runnable_factory(schema)
        choice = self._choice(budget)
        key = (schema, choice.provider, choice.model, json.dumps(choice.options, sort_keys=True))
        if key not in self._cache:
            provider = self._registry.get(choice.provider)
            chat = provider.chat_model(choice.model, temperature=choice.options.get("temperature"),
                                       timeout_s=intake_timeout_s(self.settings, provider.locality),
                                       options=choice.options)
            self._cache[key] = chat.with_structured_output(schema, method="json_schema", include_raw=True)
        return self._cache[key]
```

4. In `_invoke`, change `self._runnable(schema)` to `self._runnable(schema, budget)` and both `self._model_name()` calls to `self._model_name(budget)`.
5. Replace `_model_name` with:

```python
    def _model_name(self, budget: ModelBudget) -> str:
        return self._choice(budget).model
```

6. Change the module docstring to `"""Bounded multimodal intake adapter over the configured provider. No transaction or knowledge tools."""`.

- [ ] **Step 5: Pin the model per session in the graph**

In `backend/app/intake/graph.py`:

1. Add imports: `import asyncio`, `from collections.abc import Callable`, `from uuid import UUID`, `from app.intake.errors import ModelUnavailable` (extend the existing errors import), `from app.models_config.types import ModelChoice`.
2. Change `__init__` to accept `choice_for`:

```python
    def __init__(self, model, taxonomy, store, settings, *,
                 choice_for: Callable[[UUID], tuple[ModelChoice, float]] | None = None) -> None:
        self.model = model
        self.taxonomy = taxonomy
        self.store = store
        self.settings = settings
        self.choice_for = choice_for
```

   (keep the graph construction lines that follow unchanged).
3. In `advance` and `review`, replace `budget = self._budget()` with `budget = await self._budget(context)`.
4. Replace `_budget` with:

```python
    async def _budget(self, context: TurnContext) -> ModelBudget:
        timeout, choice = self.settings.intake_timeout_s, None
        if self.choice_for is not None:
            try:
                choice, timeout = await asyncio.to_thread(self.choice_for, context.session_id)
            except Exception as exc:
                # Never fall back to a different provider for a customer conversation.
                raise ModelUnavailable("The assistant is temporarily unavailable.", trace=[]) from exc
        return ModelBudget(timeout, self.settings.intake_max_model_requests, choice=choice)
```

- [ ] **Step 6: Wire the runtime and submission**

`backend/app/services/intake_runtime.py`: replace the model import with `from app.intake.model import IntakeModel` and `make_intake_service` with:

```python
def make_intake_service(session_factory, settings, taxonomy, *, model_store=None) -> IntakeService:
    store = AttachmentStore(settings, session_factory)
    model = IntakeModel(settings, registry=model_store.registry if model_store else None)
    graph = IntakeGraph(model, taxonomy, store, settings,
                        choice_for=model_store.intake_pin if model_store else None)
    repo = IntakeRepository(session_factory)
    turns = TurnStore(session_factory, max_images_per_message=settings.intake_max_images_per_message)
    return IntakeService(repo, turns, graph, store)
```

`backend/app/intake/submission.py`:
- Change the import `from app.pipeline.factory import model_ids` to `from app.models_config.resolver import ActiveModels`.
- `SubmissionService.__init__(self, session_factory: sessionmaker, settings: Settings, *, model_store=None) -> None:` and store `self.model_store = model_store` alongside the existing assignments.
- In `_create`, replace `model_ids=model_ids(self.settings)` with:

```python
            model_ids=(self.model_store.active() if self.model_store
                       else ActiveModels.from_env(self.settings)).model_ids()
```

- [ ] **Step 7: Run the intake and full suites**

Run: `uv run pytest tests/intake -q`
Expected: PASS.

Run: `uv run pytest -q`
Expected: PASS.

- [ ] **Step 8: Lint and commit**

```bash
uv run ruff check app tests
git add app/intake app/services/intake_runtime.py tests/intake
git commit -m "feat(intake): use the admin-configured model, pinned per customer session"
```

---

### Task 7: Application wiring, health and run records

**Files:**
- Modify: `backend/app/main.py`, `backend/app/services/batch_jobs.py`, `backend/app/api/runs.py`, `backend/app/api/workspace.py`, `backend/app/api/knowledge.py`, `backend/app/services/knowledge_runtime.py:17-18`, `backend/app/cli.py`
- Test: `backend/tests/test_workspace_api.py` (append), `backend/tests/models_config/test_batch_timeout.py`

**Interfaces:**
- Consumes: Tasks 4–6.
- Produces:
  - `create_app(settings=None, *, session_factory=None, pipeline_builder=None, knowledge_builder=None, intake_builder=None, intake_dispatcher=None, model_registry=None)`.
  - `app.state.model_store: ModelSettingsStore`, `app.state.pipeline_accepts_models: bool`.
  - `process_batch(app, run_id, tickets, mode, models=None)`, `run_job(app, run_id, tickets, mode, models=None)`, `ticket_timeout_s(models) -> float` in `batch_jobs`.
  - `knowledge_configured(settings, models) -> bool`.
  - `GET /api/health` gains `ai: {locality, steps}`; `knowledge.embedding_model` is the configured embed model.
  - CORS allows `PUT` and the `X-Admin-Token` header.

- [ ] **Step 1: Write the failing tests**

`backend/tests/models_config/test_batch_timeout.py`:

```python
from app.config import Settings
from app.models_config.resolver import ActiveModels
from app.models_config.types import ModelChoice, Step
from app.services import batch_jobs
from tests.models_config_fakes import fake_registry


def test_cloud_runs_keep_the_ticket_timeout():
    assert batch_jobs.ticket_timeout_s(ActiveModels.from_env(Settings(_env_file=None))) == batch_jobs.TICKET_TIMEOUT_S


def test_local_drafts_get_room_for_their_longer_deadline():
    settings = Settings(_env_file=None, local_agent_timeout_s=300)
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(settings))
    assert batch_jobs.ticket_timeout_s(models) == 360
```

Append to `backend/tests/test_workspace_api.py`:

```python
def test_health_reports_ai_locality_and_runs_record_provider_refs():
    from app.models_config.types import ModelChoice, Step
    from tests.models_config_fakes import fake_registry

    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="t")
    engine = make_engine(settings.test_database_url)
    reset_db(engine)

    def pipeline(_settings, _mode, _repo):
        return build_graph(PipelineDeps(
            taxonomy=load_taxonomy(settings.taxonomy_path), txn_repo=InMemoryTransactionRepo([]),
            jev=FakeClassifier(make_output("general_inquiry", priority="P4")),
        ))

    app = create_app(settings, session_factory=make_sessionmaker(engine), pipeline_builder=pipeline,
                     model_registry=fake_registry(settings))
    with TestClient(app) as client:
        assert client.get("/api/health").json()["ai"]["locality"] == "cloud"
        app.state.model_store.save(Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), changed_by="t", latency_ms=1)
        health = client.get("/api/health").json()
        assert health["ai"]["locality"] == "mixed"
        assert health["ai"]["steps"]["draft"] == {"provider": "ollama", "model": "qwen3:4b",
                                                  "locality": "local", "status": "ready"}
        run_id = start_run(client)
        assert client.get(f"/api/runs/{run_id}").json()["model_ids"]["draft"] == "ollama:qwen3:4b"
    engine.dispose()
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_batch_timeout.py tests/test_workspace_api.py -q`
Expected: FAIL with `AttributeError: module 'app.services.batch_jobs' has no attribute 'ticket_timeout_s'` and `TypeError: create_app() got an unexpected keyword argument 'model_registry'`.

- [ ] **Step 3: Batch jobs take a model snapshot**

In `backend/app/services/batch_jobs.py`:

1. Add imports `from app.models_config.resolver import ActiveModels` and `from app.models_config.types import Step`.
2. Add below `TICKET_TIMEOUT_S = 180`:

```python
LOCAL_TICKET_MARGIN_S = 60


def ticket_timeout_s(models: ActiveModels) -> float:
    """Cloud tickets keep the fixed budget; local drafts need room for their longer deadline."""
    if not models.is_local(Step.DRAFT):
        return TICKET_TIMEOUT_S
    return max(TICKET_TIMEOUT_S, models.draft_info().timeout_s + LOCAL_TICKET_MARGIN_S)


def _current_models(app) -> ActiveModels:
    store = getattr(app.state, "model_store", None)
    return store.active() if store is not None else ActiveModels.from_env(app.state.settings)
```

3. Change `process_batch` to:

```python
async def process_batch(app, run_id, tickets, mode, models=None):
    sf = app.state.session_factory
    models = models or _current_models(app)
    extra = {"models": models} if getattr(app.state, "pipeline_accepts_models", False) else {}
    graph = app.state.pipeline_builder(app.state.settings, mode, SqlTransactionRepo(sf), **extra)
    timeout_s = ticket_timeout_s(models)
```

   and inside `process`, change `TicketExecution(asyncio.timeout(TICKET_TIMEOUT_S))` to `TicketExecution(asyncio.timeout(timeout_s))`. Leave the rest unchanged.
4. Change `run_job` to `def run_job(app, run_id, tickets, mode, models=None):` and its call to `asyncio.run(process_batch(app, run_id, tickets, mode, models))`.

- [ ] **Step 4: Wire main.py**

In `backend/app/main.py`:

1. Add imports `from app.models_config.store import ModelSettingsStore`.
2. Add a helper above `create_app`:

```python
def _accepts(builder, name: str) -> bool:
    parameters = signature(builder).parameters
    return name in parameters or any(p.kind == Parameter.VAR_KEYWORD for p in parameters.values())
```

3. Add `model_registry=None` to `create_app`'s keyword parameters.
4. In `lifespan`, right after the `if session_factory is None:` block, insert:

```python
        model_store = ModelSettingsStore(app.state.session_factory, settings, model_registry)
        await run_in_threadpool(model_store.load)
        app.state.model_store = model_store
```

   then change the intake builder line to:

```python
        intake_service = (intake_builder or partial(make_intake_service, model_store=model_store))(
            app.state.session_factory, settings, app.state.taxonomy)
```

   the submission line to `app.state.submission = SubmissionService(app.state.session_factory, settings, model_store=model_store)`, the knowledge line to:

```python
            service = (knowledge_builder or partial(make_knowledge_service, store=model_store))(
                app.state.session_factory, settings)
```

   and replace the `parameters = ...` / `accepts_knowledge = ...` lines with:

```python
            builder = pipeline_builder or build_pipeline
            app.state.pipeline_builder = partial(builder, knowledge=service) if _accepts(builder, "knowledge") else builder
            app.state.pipeline_accepts_models = _accepts(builder, "models")
```

5. In `create_app` (outside lifespan), add `app.state.pipeline_accepts_models = False` next to `app.state.testing_pipeline`.
6. Change CORS to `allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Authorization", "Content-Type", "X-Admin-Token"]`.

- [ ] **Step 5: Runs, health, knowledge and CLI**

`backend/app/services/knowledge_runtime.py`: replace `knowledge_configured` with:

```python
def knowledge_configured(settings, models):
    return settings.rag_enabled and models.ready(Step.EMBED)
```

and add `from app.models_config.types import Step`.

`backend/app/api/runs.py`:
- Replace `from app.pipeline.factory import model_ids` with `from app.models_config.types import Step`.
- In `start_run`, after `settings = request.app.state.settings`, add `models = request.app.state.model_store.active()`; change the key check to `if not models.ready(Step.CLASSIFY): missing.append("TYPESAFE_API_KEY")`; change `model_ids=model_ids(settings)` to `model_ids=models.model_ids()`; change the background call to `background.add_task(run_job, request.app, run_id, stored, batch.mode, models)`.

`backend/app/api/workspace.py` `health`:

```python
@router.get("/health")
def health(request: Request, session: SessionDep):
    session.execute(text("SELECT 1"))
    settings = request.app.state.settings
    models = request.app.state.model_store.active()
    embedding_model = models.choice(Step.EMBED).model
    modes = ["jev"] if models.ready(Step.CLASSIFY) else []
    configured = knowledge_configured(settings, models)
    compatible_chunks = select(KnowledgeChunk.id).where(
        KnowledgeChunk.document_id == KnowledgeDocumentIndex.document_id,
        KnowledgeChunk.attempt_id == KnowledgeDocumentIndex.attempt_id,
        KnowledgeChunk.embedding_model == embedding_model,
    ).exists()
    indexed_count = session.scalar(select(func.count()).select_from(KnowledgeDocumentIndex).where(
        KnowledgeDocumentIndex.status == "indexed",
        KnowledgeDocumentIndex.embedding_model == embedding_model,
        KnowledgeDocumentIndex.embedding_dimensions == settings.embed_dim,
        KnowledgeDocumentIndex.chunking_version == CHUNKING_VERSION,
        KnowledgeDocumentIndex.chunk_count > 0, compatible_chunks,
    ))
    ready = configured and indexed_count > 0
    states = set(session.scalars(select(KnowledgeDocumentIndex.status).distinct()))
    status = ("disabled" if not settings.rag_enabled else "unconfigured" if not configured
              else "ready" if ready else "indexing" if "indexing" in states
              else "failed" if "failed" in states else "empty")
    return {"database": "connected", "configured_modes": modes,
            "capabilities": {"drafting": ready, "rag_indexing": configured, "evaluation": False},
            "knowledge": {"enabled": settings.rag_enabled, "configured": configured, "ready": ready,
                          "status": status, "indexed_document_count": indexed_count,
                          "embedding_model": embedding_model, "embedding_dimensions": settings.embed_dim},
            "drafting": {"enabled": settings.rag_enabled, "configured": configured, "ready": ready,
                         "credential_check_configured": models.ready(Step.CLASSIFY)},
            "ai": models.summary()}
```

with `from app.models_config.types import Step` added.

`backend/app/api/knowledge.py`: add

```python
def _configured(request) -> bool:
    return knowledge_configured(request.app.state.settings, request.app.state.model_store.active())
```

and replace both `knowledge_configured(request.app.state.settings)` calls with `_configured(request)`.

`backend/app/cli.py`:
- Add `from app.models_config.store import ModelSettingsStore`.
- In `_run_with_db`, after `sf = _sessionmaker(settings)` insert:

```python
    store = ModelSettingsStore(sf, settings)
    store.load()
    models = store.active()
```

  pass `models=models` to `factory.build_pipeline(...)`, and change `model_ids=factory.model_ids(settings)` to `model_ids=models.model_ids()`.
- In `ingest_kb_cmd`, delete the `if not knowledge_configured(settings): ...` block before the `try`, and inside the `try`, after `sf = _sessionmaker(settings)`, insert:

```python
        store = ModelSettingsStore(sf, settings)
        store.load()
        if not knowledge_configured(settings, store.active()):
            typer.echo("Knowledge provider is disabled or unconfigured.", err=True)
            raise typer.Exit(2)
```

  and change `make_knowledge_service(sf, settings)` to `make_knowledge_service(sf, settings, store)`. Add `except typer.Exit: raise` as the first `except` clause of that `try` so the exit is not swallowed by the generic handler.

- [ ] **Step 6: Run the full suite**

Run: `uv run pytest -q`
Expected: PASS.

- [ ] **Step 7: Lint and commit**

```bash
uv run ruff check app tests
git add app tests
git commit -m "feat(api): use admin model settings for runs, health and the CLI"
```

---

### Task 8: Live model tests and the model catalog

**Files:**
- Create: `backend/app/models_config/probe.py`, `backend/app/models_config/catalog.py`
- Test: `backend/tests/models_config/test_probe.py`, `backend/tests/models_config/test_catalog.py`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces:
  - `PROBE_TIMEOUT_S = 60.0`; `async probe(step: Step, choice: ModelChoice, registry: ProviderRegistry) -> ProbeResult`.
  - `CatalogCache(registry, *, ttl_s=300.0, clock=time.monotonic)` with `async entries(provider_name, kind, *, refresh=False) -> list[CatalogEntry]`.
  - `async step_catalog(step, registry, cache, *, refresh=False) -> list[dict]`; each dict has `provider`, `locality`, `status`, `status_detail`, `entries` (list of `CatalogEntry.to_json()` plus `eligibility`), `error`.

- [ ] **Step 1: Write the failing tests**

`backend/tests/models_config/test_probe.py`:

```python
import asyncio

import pytest

from app.config import Settings
from app.models_config import probe as probe_module
from app.models_config.probe import probe
from app.models_config.types import ModelChoice, Step
from tests.models_config_fakes import FakeProvider, fake_registry
from tests.rag_fakes import ScriptedChat, answer, call


class StructuredChat:
    def __init__(self, parsed=True):
        self.parsed, self.messages = parsed, None

    def with_structured_output(self, schema, **kwargs):
        self.schema = schema
        return self

    async def ainvoke(self, messages):
        self.messages = messages
        return {"raw": None, "parsed": self.schema(word="ok") if self.parsed else None,
                "parsing_error": None if self.parsed else "bad json"}


def _registry(**providers):
    return fake_registry(Settings(_env_file=None), **providers)


async def test_draft_probe_requires_a_correct_tool_call():
    good = FakeProvider("ollama", locality="local",
                        chat=ScriptedChat(steps=[answer(call("record_number", number=7))]))
    result = await probe(Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), _registry(ollama=good))
    assert result.ok and result.error is None
    bad = FakeProvider("ollama", locality="local", chat=ScriptedChat(steps=[answer(content="seven")]))
    result = await probe(Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), _registry(ollama=bad))
    assert not result.ok and "tool" in result.error


async def test_intake_probe_sends_an_image_and_needs_parsed_output():
    chat = StructuredChat()
    result = await probe(Step.INTAKE, ModelChoice("openrouter", "m"), _registry(openrouter=FakeProvider("openrouter", chat=chat)))
    assert result.ok
    assert any(block.get("type") == "image_url" for block in chat.messages[0].content)
    failing = StructuredChat(parsed=False)
    result = await probe(Step.EXTRACT, ModelChoice("openrouter", "m"), _registry(openrouter=FakeProvider("openrouter", chat=failing)))
    assert not result.ok and "bad json" in result.error


async def test_embed_and_classify_probes():
    assert (await probe(Step.EMBED, ModelChoice("ollama", "nomic-embed-text"), _registry())).ok
    assert (await probe(Step.CLASSIFY, ModelChoice("typesafe", "jev-1.13.0"), _registry())).ok


async def test_provider_not_allowed_for_step_and_unknown_provider_fail_cleanly():
    result = await probe(Step.CLASSIFY, ModelChoice("ollama", "qwen3:4b"), _registry())
    assert not result.ok and "cannot run" in result.error
    assert not (await probe(Step.DRAFT, ModelChoice("nope", "m"), _registry())).ok


async def test_probe_times_out(monkeypatch):
    monkeypatch.setattr(probe_module, "PROBE_TIMEOUT_S", 0.05)

    class Slow(StructuredChat):
        async def ainvoke(self, messages):
            await asyncio.sleep(1)

    result = await probe(Step.EXTRACT, ModelChoice("openrouter", "m"),
                         _registry(openrouter=FakeProvider("openrouter", chat=Slow())))
    assert not result.ok and "did not answer" in result.error


@pytest.mark.parametrize("step", list(Step))
async def test_every_step_has_a_probe(step):
    assert step in probe_module._CHECKS
```

`backend/tests/models_config/test_catalog.py`:

```python
import httpx

from app.config import Settings
from app.models_config.catalog import CatalogCache, step_catalog
from app.models_config.types import Capability, CatalogEntry, Step
from tests.models_config_fakes import FakeProvider, fake_registry

TOOLS = CatalogEntry("qwen3:4b", "qwen3:4b", frozenset({Capability.TOOLS, Capability.STRUCTURED}))
PLAIN = CatalogEntry("plain", "plain", frozenset({Capability.STRUCTURED}))
UNKNOWN = CatalogEntry("mystery", "mystery", None)


async def test_step_catalog_filters_and_marks_unknown():
    registry = fake_registry(Settings(_env_file=None),
                             ollama=FakeProvider("ollama", locality="local", entries=[TOOLS, PLAIN, UNKNOWN]),
                             openrouter=FakeProvider("openrouter", state="missing_key"))
    openrouter, ollama = await step_catalog(Step.DRAFT, registry, CatalogCache(registry))
    assert openrouter["status"] == "missing_key" and openrouter["entries"] == []
    assert [(e["id"], e["eligibility"]) for e in ollama["entries"]] == [("mystery", "unknown"), ("qwen3:4b", "eligible")]


async def test_catalog_errors_stay_per_provider_and_cache_respects_ttl():
    now = [0.0]
    ollama = FakeProvider("ollama", locality="local", entries=[TOOLS])
    registry = fake_registry(Settings(_env_file=None), ollama=ollama,
                             openrouter=FakeProvider("openrouter", catalog_error=httpx.ConnectError("down")))
    cache = CatalogCache(registry, ttl_s=300, clock=lambda: now[0])
    openrouter, local = await step_catalog(Step.DRAFT, registry, cache)
    assert openrouter["error"] == "Could not list models: ConnectError" and local["entries"]
    await step_catalog(Step.DRAFT, registry, cache)
    assert ollama.catalog_calls == 1
    await step_catalog(Step.DRAFT, registry, cache, refresh=True)
    now[0] = 301
    await step_catalog(Step.DRAFT, registry, cache)
    assert ollama.catalog_calls == 3


async def test_classify_catalog_only_offers_typesafe():
    registry = fake_registry(Settings(_env_file=None))
    [only] = await step_catalog(Step.CLASSIFY, registry, CatalogCache(registry))
    assert only["provider"] == "typesafe"
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_probe.py tests/models_config/test_catalog.py -q`
Expected: FAIL with `ImportError: cannot import name 'probe'`.

- [ ] **Step 3: Implement the probes**

`backend/app/models_config/probe.py`:

```python
"""Tiny live tests: a model is saved only if it can do its step's real job once."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable, Mapping

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel

from app.models_config.providers.base import Provider
from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import EMBED_DIMENSIONS, PROVIDERS_FOR_STEP
from app.models_config.types import ModelChoice, ProbeResult, Step

PROBE_TIMEOUT_S = 60.0
_PIXEL = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
          "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")


class _ProbeAnswer(BaseModel):
    word: str


@tool
def record_number(number: int) -> str:
    """Record the number the user asks you to record."""
    return "recorded"


def _chat(provider: Provider, choice: ModelChoice):
    return provider.chat_model(choice.model, temperature=choice.options.get("temperature"),
                               timeout_s=PROBE_TIMEOUT_S, options=choice.options)


async def _structured(provider: Provider, choice: ModelChoice, *, image: bool) -> str | None:
    runnable = _chat(provider, choice).with_structured_output(_ProbeAnswer, method="json_schema", include_raw=True)
    content: list[dict] = [{"type": "text", "text": 'Return JSON with the field "word" set to "ok".'}]
    if image:
        content.append({"type": "image_url", "image_url": {"url": _PIXEL}})
    result = await runnable.ainvoke([HumanMessage(content=content)])
    if isinstance(result, dict) and result.get("parsed") is not None:
        return None
    reason = result.get("parsing_error") if isinstance(result, dict) else None
    return f"The model did not return the required JSON ({reason or 'no output'})."


async def _intake(provider: Provider, choice: ModelChoice) -> str | None:
    return await _structured(provider, choice, image=True)


async def _extract(provider: Provider, choice: ModelChoice) -> str | None:
    return await _structured(provider, choice, image=False)


async def _draft(provider: Provider, choice: ModelChoice) -> str | None:
    chat = _chat(provider, choice).bind_tools([record_number])
    message = await chat.ainvoke([HumanMessage(
        content="Call the record_number tool with number 7. Do not answer in text.")])
    for item in getattr(message, "tool_calls", None) or []:
        if item.get("name") == "record_number" and str((item.get("args") or {}).get("number")) == "7":
            return None
    return "The model did not call the test tool correctly."


async def _embed(provider: Provider, choice: ModelChoice) -> str | None:
    batch = await provider.embedder(choice.model, dimensions=EMBED_DIMENSIONS).embed(["probe"])
    if len(batch.vectors) == 1 and len(batch.vectors[0]) == EMBED_DIMENSIONS:
        return None
    return f"Expected one {EMBED_DIMENSIONS}-dimension vector."


async def _classify(provider: Provider, choice: ModelChoice) -> str | None:
    from langchain_typesafe import Noul, NoulCriteria

    response = await provider.classifier(choice.model).ainvoke({
        "state": {"text": "probe"},
        "questions": {"probe": Noul(instructions="Is `text` empty?",
                                    criteria=NoulCriteria(true="It is empty.", false="It has text."))},
    })
    nouls = getattr(response, "nouls", None)
    return None if isinstance(nouls, Mapping) and "probe" in nouls else "Jev did not answer the test question."


_CHECKS: dict[Step, Callable[[Provider, ModelChoice], Awaitable[str | None]]] = {
    Step.INTAKE: _intake, Step.CLASSIFY: _classify, Step.EXTRACT: _extract,
    Step.DRAFT: _draft, Step.EMBED: _embed,
}


def _describe(error: BaseException) -> str:
    if isinstance(error, TimeoutError):
        return f"The model did not answer within {PROBE_TIMEOUT_S:g} seconds."
    return f"{type(error).__name__}: {error}"[:300]


async def probe(step: Step, choice: ModelChoice, registry: ProviderRegistry) -> ProbeResult:
    started = time.monotonic()
    try:
        if choice.provider not in PROVIDERS_FOR_STEP[step]:
            raise ValueError(f"{choice.provider} cannot run the {step.value} step.")
        provider = registry.get(choice.provider)
        async with asyncio.timeout(PROBE_TIMEOUT_S):
            error = await _CHECKS[step](provider, choice)
    except Exception as exc:  # every failure is reported to the admin, never raised
        error = _describe(exc)
    return ProbeResult(error is None, round((time.monotonic() - started) * 1000), error)
```

- [ ] **Step 4: Implement the catalog**

`backend/app/models_config/catalog.py`:

```python
"""Per-provider model listings, cached briefly and filtered by what a step needs."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from typing import Any

from app.models_config.providers.registry import ProviderRegistry
from app.models_config.steps import CATALOG_KIND, PROVIDERS_FOR_STEP, eligibility
from app.models_config.types import CatalogEntry, CatalogKind, Step


class CatalogCache:
    def __init__(self, registry: ProviderRegistry, *, ttl_s: float = 300.0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._registry, self._ttl, self._clock = registry, ttl_s, clock
        self._entries: dict[tuple[str, CatalogKind], tuple[float, list[CatalogEntry]]] = {}

    async def entries(self, provider_name: str, kind: CatalogKind, *, refresh: bool = False) -> list[CatalogEntry]:
        key = (provider_name, kind)
        cached = self._entries.get(key)
        if not refresh and cached is not None and self._clock() - cached[0] < self._ttl:
            return cached[1]
        entries = await self._registry.get(provider_name).catalog(kind)
        self._entries[key] = (self._clock(), entries)
        return entries


async def step_catalog(step: Step, registry: ProviderRegistry, cache: CatalogCache, *,
                       refresh: bool = False) -> list[dict[str, Any]]:
    providers = []
    for name in PROVIDERS_FOR_STEP[step]:
        status = await asyncio.to_thread(registry.status, name)
        item: dict[str, Any] = {"provider": name, "locality": status.locality, "status": status.state,
                                "status_detail": status.detail, "entries": [], "error": None}
        if status.state == "ready":
            try:
                entries = await cache.entries(name, CATALOG_KIND[step], refresh=refresh)
            except Exception as exc:
                item["error"] = f"Could not list models: {type(exc).__name__}"
            else:
                listed = []
                for entry in sorted(entries, key=lambda value: value.name.lower()):
                    verdict = eligibility(step, entry.capabilities)
                    if verdict != "ineligible":
                        listed.append(entry.to_json() | {"eligibility": verdict})
                item["entries"] = listed
        providers.append(item)
    return providers
```

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/models_config -q`
Expected: PASS.

- [ ] **Step 6: Lint and commit**

```bash
uv run ruff check app tests
git add app/models_config/probe.py app/models_config/catalog.py tests/models_config
git commit -m "feat(models): add per-step live tests and a filtered model catalog"
```

---

### Task 9: Admin API

**Files:**
- Create: `backend/app/api/admin.py`
- Modify: `backend/app/main.py` (router + catalog cache)
- Test: `backend/tests/models_config/test_admin_api.py`

**Interfaces:**
- Consumes: Tasks 4, 7, 8.
- Produces: `app.state.catalog: CatalogCache`; routes:
  - `POST /api/admin/session` → `204`
  - `GET /api/admin/models` → `{"steps": [describe items]}`
  - `GET /api/admin/models/catalog?step=&refresh=` → `{"step": str, "providers": [...]}`
  - `POST /api/admin/models/test` body `{step, provider, model, options}` → `ProbeResult.to_json()`
  - `PUT /api/admin/models/{step}` body `{provider, model, options, changed_by}` → the step's describe item; `400 "use_embedding_switch"` for `embed`; `422 "<provider> cannot run the <step> step."` for a disallowed provider; `422 "Model test failed: <error>"` when the probe fails
  - `GET /api/admin/models/audit?limit=50` → `{"items": [...]}`
  - Request models `ModelOptions(temperature: float | None in [0, 2], think: bool | None)` (extra fields forbidden), `ChoiceInput`, `ProbeInput`, `SaveInput`, and `require_admin` dependency, all in `app/api/admin.py`.

- [ ] **Step 1: Write the failing tests**

`backend/tests/models_config/test_admin_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.models_config.types import Capability, CatalogEntry
from tests.models_config_fakes import FakeProvider, fake_registry
from tests.rag_fakes import ScriptedChat, answer, call

pytestmark = pytest.mark.integration
HEADERS = {"X-Admin-Token": "secret"}


def _tool_chat(model):
    return ScriptedChat(steps=[answer(call("record_number", number=7))])


@pytest.fixture
def make_client():
    engines = []

    def build(**settings_kw):
        settings = Settings(_env_file=None, **({"openrouter_api_key": "k", "typesafe_api_key": "t",
                                                "admin_token": "secret"} | settings_kw))
        assert make_url(settings.test_database_url).database == "support_test"
        engine = make_engine(settings.test_database_url)
        engines.append(engine)
        reset_db(engine)
        ollama = FakeProvider("ollama", locality="local", chat=_tool_chat, entries=[
            CatalogEntry("qwen3:4b", "qwen3:4b", frozenset({Capability.TOOLS, Capability.STRUCTURED})),
            CatalogEntry("nomic-embed-text", "nomic-embed-text", frozenset({Capability.EMBEDDING})),
        ])
        app = create_app(settings, session_factory=make_sessionmaker(engine),
                         model_registry=fake_registry(settings, ollama=ollama))
        return TestClient(app)

    yield build
    for engine in engines:
        engine.dispose()


def test_admin_is_disabled_without_a_token(make_client):
    with make_client(admin_token="") as client:
        response = client.get("/api/admin/models", headers=HEADERS)
        assert response.status_code == 403 and response.json()["detail"] == "admin_disabled"


def test_non_ascii_and_blank_tokens_are_rejected(make_client):
    with make_client() as client:
        assert client.post("/api/admin/session").status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": ""}).status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": "sécret".encode("latin-1")}).status_code == 401
        assert client.post("/api/admin/session", headers={"X-Admin-Token": "wrong"}).json()["detail"] == "invalid_admin_token"
        assert client.post("/api/admin/session", headers=HEADERS).status_code == 204


def test_models_and_catalog(make_client):
    with make_client() as client:
        steps = client.get("/api/admin/models", headers=HEADERS).json()["steps"]
        assert [item["step"] for item in steps] == ["intake", "classify", "extract", "draft", "embed"]
        assert all(item["source"] == "env" for item in steps)
        catalog = client.get("/api/admin/models/catalog?step=draft", headers=HEADERS).json()
        assert catalog["step"] == "draft"
        ollama = next(p for p in catalog["providers"] if p["provider"] == "ollama")
        assert [entry["id"] for entry in ollama["entries"]] == ["qwen3:4b"]
        assert client.get("/api/admin/models/catalog?step=bogus", headers=HEADERS).status_code == 422


def test_test_save_and_audit(make_client):
    with make_client() as client:
        body = {"provider": "ollama", "model": "qwen3:4b", "options": {"think": False}}
        result = client.post("/api/admin/models/test", headers=HEADERS, json={"step": "draft", **body}).json()
        assert result["ok"] is True and result["error"] is None
        saved = client.put("/api/admin/models/draft", headers=HEADERS, json={**body, "changed_by": "Sara"})
        assert saved.status_code == 200, saved.text
        assert saved.json()["source"] == "admin" and saved.json()["model"] == "qwen3:4b"
        assert client.get("/api/health").json()["ai"]["steps"]["draft"]["provider"] == "ollama"
        [entry] = client.get("/api/admin/models/audit", headers=HEADERS).json()["items"]
        assert entry["changed_by"] == "Sara" and entry["current"]["model"] == "qwen3:4b"


def test_save_rejections_change_nothing(make_client):
    with make_client() as client:
        failing = client.put("/api/admin/models/extract", headers=HEADERS,
                             json={"provider": "openrouter", "model": "m", "changed_by": "Sara"})
        assert failing.status_code == 422 and failing.json()["detail"].startswith("Model test failed:")
        wrong = client.put("/api/admin/models/classify", headers=HEADERS,
                           json={"provider": "ollama", "model": "qwen3:4b", "changed_by": "Sara"})
        assert wrong.status_code == 422
        embed = client.put("/api/admin/models/embed", headers=HEADERS,
                           json={"provider": "ollama", "model": "nomic-embed-text", "changed_by": "Sara"})
        assert embed.status_code == 400 and embed.json()["detail"] == "use_embedding_switch"
        extra = client.put("/api/admin/models/draft", headers=HEADERS,
                           json={"provider": "ollama", "model": "qwen3:4b", "changed_by": "Sara",
                                 "options": {"api_key": "x"}})
        assert extra.status_code == 422
        assert client.get("/api/admin/models/audit", headers=HEADERS).json()["items"] == []
```

The `extract` failure works because the default fake OpenRouter provider has `chat=None`, so the probe records `AssertionError: openrouter chat was not expected`.

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_admin_api.py -q`
Expected: FAIL with `404` responses for `/api/admin/...`.

- [ ] **Step 3: Implement the router**

`backend/app/api/admin.py`:

```python
"""Admin-only model configuration. Every route requires X-Admin-Token == ADMIN_TOKEN."""
from __future__ import annotations

import hmac
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from app.models_config.catalog import step_catalog
from app.models_config.probe import probe
from app.models_config.steps import PROVIDERS_FOR_STEP
from app.models_config.types import ModelChoice, Step


def require_admin(request: Request, x_admin_token: Annotated[str | None, Header()] = None) -> None:
    expected = request.app.state.settings.admin_token
    if not expected:
        raise HTTPException(403, "admin_disabled")
    supplied = (x_admin_token or "").encode("utf-8", "surrogateescape")
    if not supplied or not hmac.compare_digest(supplied, expected.encode("utf-8")):
        raise HTTPException(401, "invalid_admin_token")


router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


class ModelOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    temperature: float | None = Field(default=None, ge=0, le=2)
    think: bool | None = None


class ChoiceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str = Field(min_length=1, max_length=32)
    model: str = Field(min_length=1, max_length=255)
    options: ModelOptions = Field(default_factory=ModelOptions)

    def choice(self) -> ModelChoice:
        return ModelChoice(self.provider.strip(), self.model.strip(), self.options.model_dump(exclude_none=True))


class ProbeInput(ChoiceInput):
    step: Step


class SaveInput(ChoiceInput):
    changed_by: str = Field(min_length=1, max_length=64)


def _store(request: Request):
    return request.app.state.model_store


def _check_provider(step: Step, choice: ModelChoice) -> None:
    if choice.provider not in PROVIDERS_FOR_STEP[step]:
        raise HTTPException(422, f"{choice.provider} cannot run the {step.value} step.")


async def _tested(request: Request, step: Step, body: ChoiceInput):
    choice = body.choice()
    _check_provider(step, choice)
    result = await probe(step, choice, _store(request).registry)
    if not result.ok:
        raise HTTPException(422, f"Model test failed: {result.error}")
    return choice, result


@router.post("/session", status_code=204)
def session() -> Response:
    return Response(status_code=204)


@router.get("/models")
async def models(request: Request):
    return {"steps": await run_in_threadpool(_store(request).describe)}


@router.get("/models/catalog")
async def catalog(request: Request, step: Step, refresh: bool = False):
    store = _store(request)
    return {"step": step.value,
            "providers": await step_catalog(step, store.registry, request.app.state.catalog, refresh=refresh)}


@router.post("/models/test")
async def test_model(request: Request, body: ProbeInput):
    choice = body.choice()
    _check_provider(body.step, choice)
    return (await probe(body.step, choice, _store(request).registry)).to_json()


@router.put("/models/{step}")
async def save_model(request: Request, step: Step, body: SaveInput):
    if step is Step.EMBED:
        raise HTTPException(400, "use_embedding_switch")
    choice, result = await _tested(request, step, body)
    store = _store(request)
    await run_in_threadpool(lambda: store.save(step, choice, changed_by=body.changed_by.strip(),
                                               latency_ms=result.latency_ms))
    described = await run_in_threadpool(store.describe)
    return next(item for item in described if item["step"] == step.value)


@router.get("/models/audit")
async def audit(request: Request, limit: Annotated[int, Query(ge=1, le=200)] = 50):
    return {"items": await run_in_threadpool(_store(request).audit, limit)}
```

In `backend/app/main.py`:
- Import `admin` alongside the other routers: `from app.api import admin, intake, knowledge, results, runs, workspace` and `from app.models_config.catalog import CatalogCache`.
- In `lifespan`, after `app.state.model_store = model_store`, add `app.state.catalog = CatalogCache(model_store.registry)`.
- Add `admin.router` to the router tuple.

Note: Starlette decodes header bytes as latin-1, so `"sécret".encode("latin-1")` arrives as the string `"sécret"`; `surrogateescape` encoding never raises, and comparing bytes avoids `compare_digest`'s `TypeError` on non-ASCII `str`.

- [ ] **Step 4: Run the tests**

Run: `uv run pytest tests/models_config -q`
Expected: PASS.

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff check app tests
git add app/api/admin.py app/main.py tests/models_config/test_admin_api.py
git commit -m "feat(api): add token-protected admin model endpoints"
```

---

### Task 10: Guarded embedding switch

**Files:**
- Create: `backend/app/models_config/embedding_switch.py`
- Modify: `backend/app/api/admin.py`, `backend/app/api/runs.py`, `backend/app/main.py`
- Test: `backend/tests/models_config/test_embedding_switch.py`

**Interfaces:**
- Consumes: Task 4 `EmbeddingSwitchRow`, `ModelSettingsStore.save(..., session=...)`, Task 5 `KnowledgeService`, Task 9 router helpers `_tested`, `SaveInput`.
- Produces:
  - `SwitchConflict(RuntimeError)` with `.code` in `{"run_in_progress", "switch_in_progress"}`.
  - `EmbeddingSwitches(session_factory, store, knowledge)` with `running() -> bool`, `current() -> dict | None`, `start(choice, *, changed_by, latency_ms) -> dict`, `async run(switch_id) -> None`, `recover_interrupted() -> int`.
  - `app.state.embedding_switches`.
  - Routes `POST /api/admin/models/embed/switch` (`202` + switch view, `409` with the conflict code, `422` on a failed test) and `GET /api/admin/models/embed/switch` (view or `null`).
  - `POST /api/runs` returns `409 "knowledge_switch_in_progress"` while a switch runs.
  - Switch view keys: `id, status, total, done, failed_document_ids, error, target, previous, started_by, started_at, finished_at`.

- [ ] **Step 1: Write the failing tests**

`backend/tests/models_config/test_embedding_switch.py`:

```python
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.models import RunRow
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.kb.documents import store_document
from app.kb.models import KnowledgeChunk
from app.main import create_app
from app.models_config.db_models import EmbeddingSwitchRow
from tests.models_config_fakes import FakeProvider, fake_registry

pytestmark = pytest.mark.integration
HEADERS = {"X-Admin-Token": "secret"}
SWITCH = {"provider": "ollama", "model": "nomic-embed-text", "changed_by": "Sara"}


@pytest.fixture
def env():
    settings = Settings(_env_file=None, openrouter_api_key="k", typesafe_api_key="t", admin_token="secret")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    sf = make_sessionmaker(engine)
    yield settings, sf
    engine.dispose()


def _client(settings, sf, **providers):
    return TestClient(create_app(settings, session_factory=sf, model_registry=fake_registry(settings, **providers)))


def _documents(sf, *texts):
    with sf.begin() as session:
        return [store_document(session, f"doc-{i}.md", text.encode()).id for i, text in enumerate(texts)]


def test_switch_reindexes_every_document_with_the_new_model(env):
    settings, sf = env
    ids = _documents(sf, "# Policy A\nسياسة أولى", "# Policy B\nسياسة ثانية")
    with _client(settings, sf) as client:
        response = client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        assert response.status_code == 202, response.text
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
        assert view["status"] == "completed" and view["total"] == 2 and view["done"] == 2
        assert view["previous"]["model"] == "openai/text-embedding-3-small"
        assert client.get("/api/health").json()["knowledge"]["embedding_model"] == "nomic-embed-text"
    with sf() as session:
        models = set(session.scalars(select(KnowledgeChunk.embedding_model).where(KnowledgeChunk.document_id.in_(ids))))
    assert models == {"nomic-embed-text"}


def test_failed_documents_are_listed(env):
    settings, sf = env
    good, bad = _documents(sf, "# Good\nسياسة", "# Bad\nFAILME")
    ollama = FakeProvider("ollama", locality="local", embed_fail_for=("FAILME",))
    with _client(settings, sf, ollama=ollama) as client:
        client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
    assert view["status"] == "completed_with_errors" and view["failed_document_ids"] == [bad]


def test_switch_with_no_documents_completes_immediately(env):
    with _client(*env) as client:
        client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
    assert view["status"] == "completed" and view["total"] == 0


def test_switch_is_refused_while_a_run_is_running(env):
    settings, sf = env
    with _client(settings, sf) as client:
        with sf.begin() as session:
            session.add(RunRow(mode="jev", prompt_version="v", model_ids={}, status="running", counts={}))
        response = client.post("/api/admin/models/embed/switch", headers=HEADERS, json=SWITCH)
        assert response.status_code == 409 and response.json()["detail"] == "run_in_progress"
        assert client.get("/api/admin/models/embed/switch", headers=HEADERS).json() is None


def test_runs_are_blocked_while_a_switch_runs_and_restart_recovers(env):
    settings, sf = env
    with sf.begin() as session:
        session.add(EmbeddingSwitchRow(target={"provider": "ollama", "model": "n", "options": {}},
                                       previous={"provider": "openrouter", "model": "o", "options": {}},
                                       status="running", total=1, done=0, failed_document_ids=[],
                                       started_by="Sara", started_at=datetime.now(UTC)))
    app = create_app(settings, session_factory=sf, model_registry=fake_registry(settings))
    app.state.recover_embedding_switches = False  # keep the row running for the first assertion
    with TestClient(app) as client:
        blocked = client.post("/api/runs", json={"tickets": [{"external_id": "x", "text": "شكد العمولة"}]})
        assert blocked.status_code == 409 and blocked.json()["detail"] == "knowledge_switch_in_progress"
    with TestClient(create_app(settings, session_factory=sf, model_registry=fake_registry(settings))) as client:
        view = client.get("/api/admin/models/embed/switch", headers=HEADERS).json()
        assert view["status"] == "failed" and "restarted" in view["error"]
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run pytest tests/models_config/test_embedding_switch.py -q`
Expected: FAIL with `404` on `/api/admin/models/embed/switch`.

- [ ] **Step 3: Implement the switch service**

`backend/app/models_config/embedding_switch.py`:

```python
"""Switch the embedding model: flip the setting, then re-index every document once.

The KB keeps one index per document, so search pauses while documents are
re-indexed. Workspace batch starts are blocked meanwhile; intake runs are not.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.orm import sessionmaker

from app.db.document_models import UploadedDocument
from app.db.models import RunRow
from app.kb.service import DocumentNotFoundError, KnowledgeService
from app.models_config.db_models import EmbeddingSwitchRow
from app.models_config.store import ModelSettingsStore
from app.models_config.types import ModelChoice, Step

logger = logging.getLogger(__name__)
RESTART_ERROR = "API restarted during switch; run the switch again."


class SwitchConflict(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _view(row: EmbeddingSwitchRow) -> dict[str, Any]:
    return {"id": row.id, "status": row.status, "total": row.total, "done": row.done,
            "failed_document_ids": list(row.failed_document_ids or []), "error": row.error,
            "target": row.target, "previous": row.previous, "started_by": row.started_by,
            "started_at": row.started_at.isoformat() if row.started_at else None,
            "finished_at": row.finished_at.isoformat() if row.finished_at else None}


class EmbeddingSwitches:
    def __init__(self, session_factory: sessionmaker, store: ModelSettingsStore,
                 knowledge: KnowledgeService) -> None:
        self._sf, self._store, self._knowledge = session_factory, store, knowledge

    def running(self) -> bool:
        with self._sf() as session:
            return session.scalar(select(EmbeddingSwitchRow.id)
                                  .where(EmbeddingSwitchRow.status == "running").limit(1)) is not None

    def current(self) -> dict[str, Any] | None:
        with self._sf() as session:
            row = session.scalar(select(EmbeddingSwitchRow).order_by(EmbeddingSwitchRow.id.desc()).limit(1))
            return _view(row) if row else None

    def start(self, choice: ModelChoice, *, changed_by: str, latency_ms: int) -> dict[str, Any]:
        with self._sf() as session:
            # Serialize concurrent starts; the check-then-insert below is then race-free.
            session.execute(text("LOCK TABLE embedding_switch IN EXCLUSIVE MODE"))
            if session.scalar(select(RunRow.id).where(RunRow.status == "running").limit(1)) is not None:
                raise SwitchConflict("run_in_progress")
            if session.scalar(select(EmbeddingSwitchRow.id)
                              .where(EmbeddingSwitchRow.status == "running").limit(1)) is not None:
                raise SwitchConflict("switch_in_progress")
            total = session.scalar(select(func.count()).select_from(UploadedDocument)) or 0
            row = EmbeddingSwitchRow(target=choice.to_json(), previous=self._store.choice(Step.EMBED).to_json(),
                                     status="running", total=total, done=0, failed_document_ids=[],
                                     started_by=changed_by, started_at=datetime.now(UTC))
            session.add(row)
            self._store.save(Step.EMBED, choice, changed_by=changed_by, latency_ms=latency_ms, session=session)
            session.commit()
            view = _view(row)
        self._store.load()
        return view

    async def run(self, switch_id: int) -> None:
        failed: list[int] = []
        try:
            ids = await asyncio.to_thread(self._document_ids)
            for document_id in ids:
                try:
                    view = await self._knowledge.index_document(document_id)
                    if view.get("status") != "indexed":
                        failed.append(document_id)
                except DocumentNotFoundError:
                    pass  # deleted during the switch: nothing left to index
                except Exception as exc:
                    logger.warning("Switch %s could not index document %s: %s",
                                   switch_id, document_id, type(exc).__name__)
                    failed.append(document_id)
                await asyncio.to_thread(self._progress, switch_id, failed)
            await asyncio.to_thread(self._finish, switch_id, failed, None)
        except Exception as exc:
            logger.warning("Switch %s failed: %s", switch_id, type(exc).__name__)
            await asyncio.to_thread(self._finish, switch_id, failed, f"{type(exc).__name__}: switch stopped.")

    def recover_interrupted(self) -> int:
        with self._sf.begin() as session:
            rows = list(session.scalars(select(EmbeddingSwitchRow).where(EmbeddingSwitchRow.status == "running")))
            for row in rows:
                row.status, row.error, row.finished_at = "failed", RESTART_ERROR, datetime.now(UTC)
            return len(rows)

    def _document_ids(self) -> list[int]:
        with self._sf() as session:
            return list(session.scalars(select(UploadedDocument.id).order_by(UploadedDocument.id)))

    def _progress(self, switch_id: int, failed: list[int]) -> None:
        with self._sf.begin() as session:
            row = session.get(EmbeddingSwitchRow, switch_id, with_for_update=True)
            row.done = min(row.total, row.done + 1)
            row.failed_document_ids = list(failed)

    def _finish(self, switch_id: int, failed: list[int], error: str | None) -> None:
        with self._sf.begin() as session:
            row = session.get(EmbeddingSwitchRow, switch_id, with_for_update=True)
            row.failed_document_ids = list(failed)
            row.error = error
            row.status = "failed" if error else "completed_with_errors" if failed else "completed"
            row.finished_at = datetime.now(UTC)
```

- [ ] **Step 4: Wire the endpoints, the runs guard and startup recovery**

In `backend/app/api/admin.py` add `from fastapi import BackgroundTasks` (extend the existing import) and `from app.models_config.embedding_switch import SwitchConflict`, then:

```python
@router.post("/models/embed/switch", status_code=202)
async def start_embedding_switch(request: Request, body: SaveInput, background: BackgroundTasks):
    switches = request.app.state.embedding_switches
    if await run_in_threadpool(switches.running):
        raise HTTPException(409, "switch_in_progress")
    choice, result = await _tested(request, Step.EMBED, body)
    try:
        view = await run_in_threadpool(lambda: switches.start(
            choice, changed_by=body.changed_by.strip(), latency_ms=result.latency_ms))
    except SwitchConflict as exc:
        raise HTTPException(409, exc.code) from None
    background.add_task(switches.run, view["id"])
    return view


@router.get("/models/embed/switch")
async def embedding_switch(request: Request):
    return await run_in_threadpool(request.app.state.embedding_switches.current)
```

In `backend/app/api/runs.py`, at the start of `start_run` (before any database writes):

```python
    switches = getattr(request.app.state, "embedding_switches", None)
    if switches is not None and switches.running():
        raise HTTPException(409, "knowledge_switch_in_progress")
```

In `backend/app/main.py`:
- Import `from app.models_config.embedding_switch import EmbeddingSwitches`.
- In `lifespan`, after `app.state.index_jobs = IndexJobs(service)`, add `app.state.embedding_switches = EmbeddingSwitches(app.state.session_factory, model_store, service)`.
- In `recover()`, as its first line, add:

```python
                if getattr(app.state, "recover_embedding_switches", True):
                    app.state.embedding_switches.recover_interrupted()
```

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/models_config -q`
Expected: PASS.

Run: `uv run pytest -q`
Expected: PASS.

- [ ] **Step 6: Lint and commit**

```bash
uv run ruff check app tests
git add app tests/models_config/test_embedding_switch.py
git commit -m "feat(models): add guarded embedding model switch"
```

---

### Task 11: Configuration, Docker and documentation

**Files:**
- Modify: `.env.example`, `docker-compose.yml`, `README.md`

**Interfaces:**
- Consumes: Tasks 1–10.
- Produces: documented settings and a working Docker route to a host Ollama.

- [ ] **Step 1: Document the settings**

Append to `.env.example`:

```dotenv
# --- Admin model configuration ---
# Enables /api/admin and the workspace Admin → Models page. Empty disables admin access.
ADMIN_TOKEN=
# Ollama for local models. API in Docker: http://host.docker.internal:11434
# API in WSL (default NAT networking) with Ollama on Windows: http://<windows-host-ip>:11434
OLLAMA_BASE_URL=http://localhost:11434
# Deadlines used when a step runs on a local model (seconds, max 600).
LOCAL_AGENT_TIMEOUT_S=180
LOCAL_INTAKE_TIMEOUT_S=180
```

- [ ] **Step 2: Let the API container reach the host**

In `docker-compose.yml`, under the `api:` service, add:

```yaml
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

- [ ] **Step 3: Document local models**

In `README.md`, directly after the per-step model table, add:

```markdown
The table shows the `.env` defaults. An admin can change any step's provider and model at runtime in the workspace under **Admin → Models** (requires `ADMIN_TOKEN`). Saved choices are stored in Postgres and apply to new runs and new intake sessions without a restart.

### Using local models (Ollama)

1. Install and start Ollama, then pull models:
   - `ollama pull qwen3:4b` for extraction and drafting (tools, structured output),
   - `ollama pull nomic-embed-text` for embeddings (768 dimensions),
   - a vision model such as `ollama pull gemma3:4b` for customer intake (`qwen3:4b` has no vision).
2. Make Ollama reachable from the API and set `OLLAMA_BASE_URL`:
   - API in Docker: `http://host.docker.internal:11434`.
   - API in WSL with Ollama on Windows: either enable mirrored networking (`networkingMode=mirrored` in `%UserProfile%\.wslconfig`, then `wsl --shutdown`) and keep `http://localhost:11434`, or set the Windows environment variable `OLLAMA_HOST=0.0.0.0`, restart Ollama and use `http://<windows-host-ip>:11434` (`ip route show default` in WSL prints that IP).
3. Set `ADMIN_TOKEN`, restart the API, open **Admin → Models**, and change a step. Every model must pass a live test before it is saved.

Local models are slower; local steps use `LOCAL_AGENT_TIMEOUT_S` / `LOCAL_INTAKE_TIMEOUT_S`. Jev classification always runs on TypeSafe, so the workspace shows **AI: Mixed** rather than **AI: Local**. Changing the embedding model re-indexes the knowledge base; new workspace batches are blocked until that finishes.
```

Also change README line "Restart the API after changing model settings." to "Restart the API after changing model settings in `.env`; admin changes apply without a restart."

- [ ] **Step 4: Full verification**

Run (from `backend/`): `uv run ruff check app tests`
Expected: `All checks passed!`

Run (from `backend/`): `uv run pytest -q`
Expected: all tests pass.

Run (from repo root): `docker compose config --quiet`
Expected: exit code 0.

- [ ] **Step 5: Commit**

```bash
git add .env.example docker-compose.yml README.md
git commit -m "docs: document admin model settings and local Ollama models"
```
