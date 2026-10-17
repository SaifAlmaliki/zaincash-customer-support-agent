import asyncio
import json

import httpx
import pytest
from pydantic import ValidationError

from app.config import Settings
from app.kb.contracts import EmbeddingBatch
from app.kb.embeddings import EmbeddingError, OpenRouterEmbedder


def settings(**overrides):
    return Settings(_env_file=None, openrouter_api_key="test-openrouter-key", **overrides)


def response_payload(data, **extra):
    return {"object": "list", "model": "openai/text-embedding-3-small", "data": data, **extra}


def item(index=0, vector=None):
    return {"object": "embedding", "index": index,
            "embedding": [1.0] + [0.0] * 767 if vector is None else vector}


def embedder_for(payload, **overrides):
    # Explicit JSON serialization permits deliberately malformed NaN/Infinity responses.
    return OpenRouterEmbedder(settings(**overrides), transport=httpx.MockTransport(
        lambda request: httpx.Response(200, content=json.dumps(payload),
                                       headers={"content-type": "application/json"})
    ))


async def test_reordered_response_restores_input_order_and_sends_configured_request():
    requests = []

    def respond(request):
        requests.append(request)
        assert request.method == "POST"
        assert str(request.url) == "https://openrouter.ai/api/v1/embeddings"
        assert request.headers["authorization"] == "Bearer test-openrouter-key"
        assert request.extensions["timeout"] == {
            "connect": 20.0, "read": 20.0, "write": 20.0, "pool": 20.0,
        }
        assert json.loads(request.content) == {
            "input": ["سياسة أولى", "سياسة ثانية"], "model": "openai/text-embedding-3-small",
            "dimensions": 768, "encoding_format": "float",
        }
        return httpx.Response(200, json=response_payload([
            item(1, [0.0] * 767 + [1.0]), item(0, [1.0] + [0.0] * 767),
        ], usage={"prompt_tokens": 10, "total_tokens": 10, "cost": 0.0123}))

    embedder = OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond))
    batch = await embedder.embed(["سياسة أولى", "سياسة ثانية"])
    assert isinstance(batch, EmbeddingBatch)
    assert len(requests) == 1
    assert len(batch.vectors) == 2
    assert batch.vectors[0][0] == 1.0 and sum(batch.vectors[0]) == 1.0
    assert batch.vectors[1][-1] == 1.0 and batch.vectors[1][0] == 0.0
    assert sum(batch.vectors[1]) == 1.0
    assert isinstance(batch.vectors, tuple) and isinstance(batch.vectors[0], tuple)
    assert batch.cost_usd == 0.0123  # One request cost, not one per vector.
    assert embedder.model == "openai/text-embedding-3-small" and embedder.dimensions == 768


async def test_33_inputs_are_batched_and_each_batch_maps_its_own_indexes():
    inputs = [f"policy {i}" for i in range(33)]
    bodies = []

    def respond(request):
        body = json.loads(request.content)
        bodies.append(body)
        rows = [item(i, [float(int(text.split()[1]) + 1)] + [0.0] * 767)
                for i, text in enumerate(body["input"])]
        cost = 0.01 if len(bodies) == 1 else 0.002
        return httpx.Response(200, json=response_payload(
            list(reversed(rows)), usage={"prompt_tokens": 100, "total_tokens": 100, "cost": cost},
        ))

    batch = await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond)).embed(inputs)
    assert [len(body["input"]) for body in bodies] == [32, 1]
    assert bodies[0]["input"] == inputs[:32] and bodies[1]["input"] == inputs[32:]
    assert [vector[0] for vector in batch.vectors] == list(range(1, 34))
    assert all(len(vector) == 768 for vector in batch.vectors)
    assert batch.cost_usd == pytest.approx(0.012)


async def test_empty_input_returns_empty_batch_without_a_request():
    def unexpected_request(request):
        pytest.fail("empty inputs must not reach the provider")

    batch = await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(
        unexpected_request,
    )).embed([])
    assert batch == EmbeddingBatch(())


@pytest.mark.parametrize("bad_input", ["", " \n\t", None, 7])
async def test_invalid_text_is_rejected_before_any_batch_is_sent(bad_input):
    def unexpected_request(request):
        pytest.fail("validate the whole input before sending a paid request")

    with pytest.raises(EmbeddingError, match="(?i)non-empty.*text"):
        await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(
            unexpected_request,
        )).embed(["valid"] * 32 + [bad_input])


@pytest.mark.parametrize("vector", [
    [1.0] * 767, [1.0] * 769, [0.0] * 768, [], "base64-vector", None,
    [float("nan")] + [0.0] * 767, [float("inf")] + [0.0] * 767,
    [-float("inf")] + [0.0] * 767, ["1.0"] + [0.0] * 767,
    [True] + [0.0] * 767, [None] + [0.0] * 767, [10**400] + [0.0] * 767,
], ids=["short", "long", "zero", "empty", "encoded", "null", "nan", "infinity",
        "negative-infinity", "numeric-string", "boolean", "null-element", "overflow"])
async def test_invalid_vectors_fail_visibly(vector):
    row = {"object": "embedding", "index": 0, "embedding": vector}
    with pytest.raises(EmbeddingError, match="(?i)vector|embedding") as error:
        await embedder_for(response_payload([row])).embed(["policy"])
    assert len(str(error.value)) <= 250


@pytest.mark.parametrize("data", [
    [item(0), item(0)], [item(0)], [], [item(0), item(2)], [item(-1), item(1)],
    [item(False), item(1)], [item("0"), item(1)], [item(0.0), item(1)],
    [{"embedding": [1.0] * 768}, item(1)], [None, item(1)],
    [item(0), item(1), item(2)], None, {},
], ids=["duplicate", "missing-item", "empty", "out-of-range", "negative", "boolean",
        "string", "float", "missing-index", "null-item", "extra", "null-data", "object-data"])
async def test_invalid_response_indexes_or_counts_are_rejected(data):
    with pytest.raises(EmbeddingError):
        await embedder_for(response_payload(data)).embed(["policy one", "policy two"])


@pytest.mark.parametrize("payload", [None, [], {}, {"error": {"message": "private provider detail"}}])
async def test_invalid_response_envelopes_are_bounded(payload):
    with pytest.raises(EmbeddingError) as error:
        await embedder_for(payload).embed(["policy"])
    assert len(str(error.value)) <= 250
    assert "private provider detail" not in str(error.value)


async def test_non_json_response_is_a_public_embedding_error():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, text="private raw body"))
    with pytest.raises(EmbeddingError) as error:
        await OpenRouterEmbedder(settings(), transport=transport).embed(["policy"])
    assert "private raw body" not in str(error.value)
    assert len(str(error.value)) <= 250


@pytest.mark.parametrize("usage, extra, expected", [
    ({"prompt_tokens": 1_000_000, "total_tokens": 1_000_000, "cost": 0.0}, {}, 0.0),
    ({"prompt_tokens": 1_000_000, "total_tokens": 1_000_000, "cost": 0.125}, {}, 0.125),
    ({"prompt_tokens": 500_000, "total_tokens": 500_000}, {}, 0.2),
    ({"total_tokens": 500_000}, {}, 0.2),
    ({"prompt_tokens": 500_000}, {"cost": 0.07}, 0.07),
    ({"prompt_tokens": 500_000, "cost": 0.03}, {"cost": 0.07}, 0.03),
    (None, {}, 0.0),
])
async def test_cost_uses_one_reported_value_or_configured_token_estimate(usage, extra, expected):
    batch = await embedder_for(
        response_payload([item()], usage=usage, **extra), price_embedding_in=0.4,
    ).embed(["policy"])
    assert batch.cost_usd == pytest.approx(expected)


@pytest.mark.parametrize("usage", [
    {"cost": -1}, {"cost": float("nan")}, {"cost": float("inf")}, {"cost": "private"},
    {"cost": True}, {"prompt_tokens": -1}, {"prompt_tokens": "many"},
    {"prompt_tokens": 1.5}, {"prompt_tokens": True}, {"prompt_tokens": 10**400}, [],
])
async def test_invalid_usage_cannot_poison_recorded_cost(usage):
    with pytest.raises(EmbeddingError):
        await embedder_for(response_payload([item()], usage=usage)).embed(["policy"])


@pytest.mark.parametrize("failure, message", [(401, "401"), (500, "500"),
                                              ("timeout", "timed out"), ("network", "unavailable")])
async def test_provider_failures_are_bounded_redacted_and_not_retried(failure, message):
    attempts = 0
    private = "test-openrouter-key private body " * 100

    def respond(request):
        nonlocal attempts
        attempts += 1
        if failure == "timeout":
            raise httpx.ReadTimeout(private, request=request)
        if failure == "network":
            raise httpx.ConnectError(private, request=request)
        return httpx.Response(failure, json={"error": {"message": private}})

    with pytest.raises(EmbeddingError, match=message) as error:
        await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond)).embed(["policy"])
    assert attempts == 1
    assert len(str(error.value)) <= 250
    assert "test-openrouter-key" not in str(error.value) and "private body" not in str(error.value)
    assert error.value.cost_usd == 0.0


async def test_request_deadline_bounds_trickled_response_body(monkeypatch):
    monkeypatch.setattr("app.kb.embeddings.EMBEDDING_TIMEOUT_S", 0.05)

    class TrickleBody(httpx.AsyncByteStream):
        closed = False
        chunks_sent = 0

        async def __aiter__(self):
            for _ in range(25):
                await asyncio.sleep(0.01)  # Each chunk arrives within the read timeout.
                self.chunks_sent += 1
                yield b" "
            yield json.dumps(response_payload([item()], usage={"cost": 0.003})).encode()

        async def aclose(self):
            self.closed = True

    body = TrickleBody()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, stream=body))
    started = asyncio.get_running_loop().time()
    with pytest.raises(EmbeddingError, match="timed out") as error:
        await OpenRouterEmbedder(settings(), transport=transport).embed(["policy"])
    assert asyncio.get_running_loop().time() - started < 0.2
    assert body.chunks_sent < 25
    assert body.closed
    assert error.value.cost_usd == 0.0  # The unfinished response supplied no measurable cost.


async def test_request_deadline_restarts_for_each_batch(monkeypatch):
    monkeypatch.setattr("app.kb.embeddings.EMBEDDING_TIMEOUT_S", 0.1)
    requests = []

    async def respond(request):
        inputs = json.loads(request.content)["input"]
        requests.append(inputs)
        await asyncio.sleep(0.06)  # Two requests exceed 0.1s together, not individually.
        return httpx.Response(200, json=response_payload(
            [item(i) for i in range(len(inputs))], usage={"cost": 0.003},
        ))

    batch = await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond)).embed(
        ["policy"] * 33,
    )
    assert [len(inputs) for inputs in requests] == [32, 1]
    assert len(batch.vectors) == 33 and batch.cost_usd == pytest.approx(0.006)


async def test_later_batch_failure_retains_prior_successful_request_cost():
    attempts = 0

    def respond(request):
        nonlocal attempts
        attempts += 1
        if attempts == 2:
            return httpx.Response(503, text="unavailable")
        return httpx.Response(200, json=response_payload(
            [item(i) for i in range(32)], usage={"cost": 0.012},
        ))

    with pytest.raises(EmbeddingError) as error:
        await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond)).embed(["x"] * 33)
    assert attempts == 2
    assert error.value.cost_usd == 0.012


async def test_billed_response_cost_is_retained_when_its_vectors_are_invalid():
    with pytest.raises(EmbeddingError) as error:
        await embedder_for(response_payload(
            [item(vector=[0.0] * 768)], usage={"cost": 0.003},
        )).embed(["policy"])
    assert error.value.cost_usd == 0.003


async def test_cancellation_propagates_to_the_callers_deadline():
    async def respond(request):
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError) as error:
        await OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond)).embed(["policy"])
    assert getattr(error.value, "cost_usd", None) == 0.0


@pytest.mark.parametrize("mode", ["cancel", "outer_timeout"])
async def test_billed_batch_cost_survives_cancellation_without_cross_call_leakage(mode):
    second_batch_started = asyncio.Event()
    deadline = None
    billed_requests = 0

    async def respond(request):
        nonlocal billed_requests
        inputs = json.loads(request.content)["input"]
        if inputs == ["other call"]:
            return httpx.Response(200, json=response_payload([item()], usage={"cost": 0.05}))
        billed_requests += 1
        if billed_requests == 2:
            second_batch_started.set()
            await asyncio.Event().wait()
        return httpx.Response(200, json=response_payload(
            [item(i) for i in range(len(inputs))], usage={"cost": 0.012},
        ))

    embedder = OpenRouterEmbedder(settings(), transport=httpx.MockTransport(respond))

    async def run():
        nonlocal deadline
        async with asyncio.timeout(None) as deadline:
            return await embedder.embed(["policy"] * 33)

    task = asyncio.create_task(run())
    try:
        await asyncio.wait_for(second_batch_started.wait(), timeout=1)
        # A simultaneous call on the same adapter must not overwrite the cancelled call's cost.
        other = await embedder.embed(["other call"])
        assert other.cost_usd == 0.05
        if mode == "cancel":
            task.cancel("caller cancelled")
        else:
            deadline.reschedule(asyncio.get_running_loop().time())
        with pytest.raises(asyncio.CancelledError if mode == "cancel" else TimeoutError) as error:
            await task
        cancellation = error.value if mode == "cancel" else error.value.__cause__
        assert type(cancellation) is asyncio.CancelledError
        assert getattr(cancellation, "cost_usd", None) == 0.012
        assert billed_requests == 2
        assert task.cancelled() is (mode == "cancel")
        if mode == "cancel":
            assert cancellation.args == ("caller cancelled",)
    finally:
        if not task.done():
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task


async def test_billed_cost_survives_cancellation_during_client_close():
    close_started = asyncio.Event()

    class SlowCloseTransport(httpx.MockTransport):
        async def aclose(self):
            close_started.set()
            await asyncio.Event().wait()

    transport = SlowCloseTransport(lambda request: httpx.Response(
        200, json=response_payload([item()], usage={"cost": 0.003}),
    ))
    task = asyncio.create_task(OpenRouterEmbedder(settings(), transport=transport).embed(["policy"]))
    try:
        await asyncio.wait_for(close_started.wait(), timeout=1)
        task.cancel()
        with pytest.raises(asyncio.CancelledError) as error:
            await task
        assert getattr(error.value, "cost_usd", None) == 0.003
    finally:
        if not task.done():
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task


async def test_settings_model_override_is_sent_and_exposed():
    def respond(request):
        assert json.loads(request.content)["model"] == "provider/custom-embedding"
        return httpx.Response(200, json={"data": [item()], "model": "provider/custom-embedding"})

    embedder = OpenRouterEmbedder(settings(embedding_model="provider/custom-embedding"),
                                  transport=httpx.MockTransport(respond))
    assert embedder.model == "provider/custom-embedding"
    assert (await embedder.embed(["policy"])).vectors[0][0] == 1.0


@pytest.mark.parametrize("overrides", [
    {"embed_dim": 1536}, {"embed_dim": 0}, {"kb_top_k": 0}, {"kb_top_k": 11},
    {"kb_min_similarity": -1.01}, {"kb_min_similarity": 1.01},
    {"kb_min_similarity": float("nan")}, {"embedding_model": " \t"},
    {"price_embedding_in": -0.1}, {"price_embedding_in": float("inf")},
    {"price_embedding_in": float("nan")},
])
def test_invalid_rag_settings_are_rejected(overrides):
    with pytest.raises(ValidationError):
        settings(**overrides)


def test_rag_defaults_and_environment_overrides(monkeypatch):
    defaults = settings()
    assert defaults.rag_enabled is True
    assert defaults.kb_top_k == 5 and defaults.kb_min_similarity == 0.3
    assert defaults.price_embedding_in == 0.02
    monkeypatch.setenv("RAG_ENABLED", "false")
    monkeypatch.setenv("EMBEDDING_MODEL", "provider/other")
    monkeypatch.setenv("EMBED_DIM", "768")
    monkeypatch.setenv("KB_TOP_K", "10")
    monkeypatch.setenv("KB_MIN_SIMILARITY", "-1")
    monkeypatch.setenv("PRICE_EMBEDDING_IN", "0.5")
    configured = settings()
    assert configured.rag_enabled is False
    assert configured.embedding_model == "provider/other" and configured.embed_dim == 768
    assert configured.kb_top_k == 10 and configured.kb_min_similarity == -1
    assert configured.price_embedding_in == 0.5
