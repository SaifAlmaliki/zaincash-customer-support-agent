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


def test_a_saved_model_removed_from_the_provider_is_missing_and_not_ready():
    settings = _settings()
    ollama = FakeProvider("ollama", locality="local", installed={"qwen3:4b"})
    registry = fake_registry(settings, ollama=ollama)
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b"),
                                     Step.EXTRACT: ModelChoice("ollama", "gone:1b")}, registry)
    assert models.ready(Step.DRAFT) and not models.ready(Step.EXTRACT)
    missing = models.step_status(Step.EXTRACT)
    assert (missing.state, missing.detail) == ("model_missing", "The model is not installed in Ollama.")
    assert missing.locality == "local" and missing.name == "ollama"
    assert models.step_status(Step.DRAFT).state == "ready"
    steps = models.summary()["steps"]
    assert steps["extract"]["status"] == "model_missing" and steps["draft"]["status"] == "ready"


def test_embedder_receives_the_known_price_or_none():
    settings = _settings()
    default = fake_registry(settings)
    ActiveModels(settings, {}, default).embedder()
    assert default.get("openrouter").embedders[-1].price_per_m == settings.price_embedding_in

    unknown = fake_registry(settings)
    ActiveModels(settings, {Step.EMBED: ModelChoice("openrouter", "other/embedder")}, unknown).embedder()
    assert unknown.get("openrouter").embedders[-1].price_per_m is None

    saved = fake_registry(settings)
    choice = ModelChoice("openrouter", "other/embedder", {"price_in_per_m": 0.13, "price_out_per_m": 0.0})
    ActiveModels(settings, {Step.EMBED: choice}, saved).embedder()
    assert saved.get("openrouter").embedders[-1].price_per_m == 0.13


def test_unknown_model_availability_does_not_block_a_ready_provider():
    settings = _settings()
    registry = fake_registry(settings, ollama=FakeProvider("ollama", locality="local"))
    registry.get("ollama").has_model = lambda model: None
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, registry)
    assert models.ready(Step.DRAFT)


def test_unreachable_provider_keeps_its_own_status_over_model_checks():
    settings = _settings()
    ollama = FakeProvider("ollama", locality="local", state="unreachable", installed=set())
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")},
                          fake_registry(settings, ollama=ollama))
    assert models.step_status(Step.DRAFT).state == "unreachable"


def test_ready_and_summary_follow_provider_status():
    settings = _settings()
    registry = fake_registry(settings, ollama=FakeProvider("ollama", locality="local", state="unreachable"))
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, registry)
    assert not models.ready(Step.DRAFT) and models.ready(Step.EXTRACT)
    summary = models.summary()
    assert summary["locality"] == "mixed"
    assert summary["steps"]["draft"] == {"provider": "ollama", "model": "qwen3:4b",
                                         "locality": "local", "status": "unreachable"}


def test_unknown_admin_model_has_no_price():
    settings = Settings(_env_file=None)
    models = ActiveModels(settings, {Step.EXTRACT: ModelChoice("openrouter", "mistralai/unknown")},
                          fake_registry(settings))
    assert models.prices(Step.EXTRACT) is None
    assert models.token_prices(Step.EXTRACT) == (0.0, 0.0)
    assert models.draft_info().provider == "openrouter" and models.draft_info().prices_known is True
