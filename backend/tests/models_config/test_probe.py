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


async def test_probes_use_the_production_default_temperature_unless_overridden():
    draft = FakeProvider("ollama", locality="local",
                         chat=ScriptedChat(steps=[answer(call("record_number", number=7))] * 2))
    await probe(Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), _registry(ollama=draft))
    await probe(Step.DRAFT, ModelChoice("ollama", "qwen3:4b", {"temperature": 0.5}), _registry(ollama=draft))
    assert [call_["temperature"] for call_ in draft.chat_calls] == [0.1, 0.5]
    extract = FakeProvider("openrouter", chat=StructuredChat())
    await probe(Step.EXTRACT, ModelChoice("openrouter", "m"), _registry(openrouter=extract))
    intake = FakeProvider("openrouter", chat=StructuredChat())
    await probe(Step.INTAKE, ModelChoice("openrouter", "m"), _registry(openrouter=intake))
    assert extract.chat_calls[0]["temperature"] == 0.0 and intake.chat_calls[0]["temperature"] is None


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


async def test_probe_errors_keep_urls_and_keys_out():
    class Exploding(StructuredChat):
        async def ainvoke(self, messages):
            raise RuntimeError("failed for url 'http://10.0.0.5:11434/api/chat' with key sk-or-v1-abcdef123456")

    result = await probe(Step.EXTRACT, ModelChoice("openrouter", "m"),
                         _registry(openrouter=FakeProvider("openrouter", chat=Exploding())))
    assert not result.ok
    assert "http://" not in result.error and "sk-or-v1" not in result.error
    assert "RuntimeError" in result.error and "<url>" in result.error


async def test_probe_scrubs_parsing_errors_and_keeps_the_useful_message():
    class Leaky(StructuredChat):
        async def ainvoke(self, messages):
            return {"raw": None, "parsed": None,
                    "parsing_error": "model 'x' not found at https://api.example.com/v1 Bearer abc.def"}

    result = await probe(Step.EXTRACT, ModelChoice("openrouter", "m"),
                         _registry(openrouter=FakeProvider("openrouter", chat=Leaky())))
    assert not result.ok and "model 'x' not found" in result.error
    assert "example.com" not in result.error and "abc.def" not in result.error
