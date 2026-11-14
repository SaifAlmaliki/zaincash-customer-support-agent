from app.config import Settings
from app.models_config.pricing import prices_for, with_catalog_prices
from app.models_config.types import CatalogEntry, ModelChoice, Step

S = Settings(_env_file=None, anthropic_model="anthropic/claude-sonnet-5.5")


def test_local_is_free():
    assert prices_for(S, Step.DRAFT, ModelChoice("ollama", "qwen3:4b"), "local") == (0.0, 0.0)


def test_saved_prices_win():
    choice = ModelChoice("openrouter", "openai/gpt-5.5", {"price_in_per_m": 1.25, "price_out_per_m": 10.0})
    assert prices_for(S, Step.EXTRACT, choice, "cloud") == (1.25, 10.0)


def test_env_defaults_keep_their_prices():
    assert prices_for(S, Step.CLASSIFY, ModelChoice("typesafe", S.jev_model), "cloud") == (S.price_jev_in, 0.0)
    assert prices_for(S, Step.EMBED, ModelChoice("openrouter", S.embedding_model), "cloud") == (S.price_embedding_in, 0.0)
    assert prices_for(S, Step.EXTRACT, ModelChoice("openrouter", S.gemini_model), "cloud") == (
        S.price_gemini_flash_in, S.price_gemini_flash_out)
    assert prices_for(S, Step.DRAFT, ModelChoice("openrouter", S.draft_model), "cloud") == S.draft_token_prices
    assert prices_for(S, Step.INTAKE, ModelChoice("openrouter", "anthropic/claude-sonnet-5.5"), "cloud") == (
        S.price_anthropic_in, S.price_anthropic_out)


def test_unknown_price_is_never_estimated():
    assert prices_for(S, Step.EXTRACT, ModelChoice("openrouter", "mistralai/unknown-model"), "cloud") is None
    assert prices_for(S, Step.EMBED, ModelChoice("openrouter", "other/embedder"), "cloud") is None


def test_with_catalog_prices():
    entries = [CatalogEntry("x/y", "x/y", None, 1.5, 6.0), CatalogEntry("a/b", "a/b", None)]
    priced = with_catalog_prices(ModelChoice("openrouter", "x/y", {"think": False}), entries)
    assert priced.options == {"think": False, "price_in_per_m": 1.5, "price_out_per_m": 6.0}
    unchanged = ModelChoice("openrouter", "a/b")
    assert with_catalog_prices(unchanged, entries) == unchanged
