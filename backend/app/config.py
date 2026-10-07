from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """All runtime configuration. Environment variable names are the upper-cased field names."""

    model_config = SettingsConfigDict(env_file=str(REPO_ROOT / ".env"), extra="ignore")

    google_api_key: str = ""
    typesafe_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_strong_model: str = "gemini-2.5-pro"
    gemini_embed_model: str = "gemini-embedding-001"
    embed_dim: int = 768
    jev_model: str = "jev-1.13.0"

    t_jev: float = 0.6
    t_gem: float = 0.66
    jev_min_top_prob: float = 0.60
    pipeline_concurrency: int = 20
    max_state_chars: int = 6000
    agent_max_tool_calls: int = 6
    agent_timeout_s: int = 30

    database_url: str = "postgresql+psycopg://support:support@localhost:5432/support"
    test_database_url: str = "postgresql+psycopg://support:support@localhost:5432/support_test"
    taxonomy_path: str = str(REPO_ROOT / "data" / "taxonomy.yaml")

    # USD per 1M tokens. Check current pricing before reporting costs.
    price_gemini_flash_in: float = 0.30
    price_gemini_flash_out: float = 2.50
    price_gemini_pro_in: float = 1.25
    price_gemini_pro_out: float = 10.0
    price_jev_in: float = 0.042


@lru_cache
def get_settings() -> Settings:
    return Settings()
