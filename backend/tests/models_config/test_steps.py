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
