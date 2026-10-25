from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """All runtime configuration. Environment variable names are the upper-cased field names."""

    model_config = SettingsConfigDict(env_file=str(REPO_ROOT / ".env"), extra="ignore")

    openrouter_api_key: str = ""
    typesafe_api_key: str = ""
    gemini_model: str = "google/gemini-3.8-flash"
    gemini_strong_model: str = "google/gemini-2.5-pro"
    gemini_embed_model: str = "gemini-embedding-001"
    # When set, drafting uses this model. Classification stays on gemini_model.
    anthropic_model: str = ""
    rag_enabled: bool = True
    embedding_model: str = "openai/text-embedding-3-small"
    embed_dim: int = 768
    kb_top_k: int = Field(default=5, ge=1, le=10)
    kb_min_similarity: float = Field(default=0.3, ge=-1, le=1, allow_inf_nan=False)
    jev_model: str = "jev-1.13.0"

    t_jev: float = 0.6
    t_gem: float = 0.66
    jev_min_top_prob: float = 0.60
    pipeline_concurrency: int = 20
    max_state_chars: int = 6000
    agent_max_tool_calls: int = Field(default=6, ge=1, le=6, strict=True)
    agent_timeout_s: float = Field(default=30, gt=0, le=30, allow_inf_nan=False)

    database_url: str = "postgresql+psycopg://support:support@localhost:5433/support"
    test_database_url: str = "postgresql+psycopg://support:support@localhost:5433/support_test"
    taxonomy_path: str = str(REPO_ROOT / "data" / "taxonomy.yaml")

    # Empty means the intake adapter uses gemini_model. A configured ID must be non-blank.
    intake_model: str = ""
    intake_timeout_s: float = Field(default=60, gt=0, allow_inf_nan=False)
    intake_max_model_requests: int = Field(default=3, ge=1, le=20, strict=True)
    intake_upload_dir: str = str(REPO_ROOT / "data" / "intake-uploads")
    intake_max_image_bytes: int = Field(default=5 * 1024 * 1024, gt=0)
    intake_max_image_pixels: int = Field(default=20_000_000, gt=0)
    intake_max_images_per_message: int = Field(default=3, gt=0)
    intake_max_images_per_session: int = Field(default=10, gt=0)

    # USD per 1M tokens. Check current pricing before reporting costs.
    price_gemini_flash_in: float = 0.75
    price_gemini_flash_out: float = 3.75
    price_gemini_pro_in: float = 1.25
    price_gemini_pro_out: float = 10.0
    price_jev_in: float = 0.042
    # Fallback estimate only: OpenAI text-embedding-3-small, $0.02/1M input tokens.
    # https://developers.openai.com/api/docs/models/text-embedding-3-small (2026-10-17)
    # OpenRouter-reported cost takes precedence; update this when changing models.
    price_embedding_in: float = Field(default=0.02, ge=0, allow_inf_nan=False)

    @field_validator("intake_max_model_requests", mode="before")
    @classmethod
    def parse_intake_request_limit(cls, value):
        if isinstance(value, str) and value.strip().isdecimal():
            return int(value.strip())
        return value

    @field_validator("intake_model")
    @classmethod
    def validate_intake_model(cls, value: str) -> str:
        stripped = value.strip()
        if value and not stripped:
            raise ValueError("INTAKE_MODEL must be a non-empty model ID")
        return stripped

    @field_validator("intake_upload_dir")
    @classmethod
    def resolve_intake_upload_dir(cls, value: str) -> str:
        path = Path(value).expanduser()
        return str(path if path.is_absolute() else REPO_ROOT / path)

    @field_validator("agent_max_tool_calls", mode="before")
    @classmethod
    def parse_tool_limit_env(cls, value):
        # Environment settings arrive as strings; keep strict rejection of bools
        # and fractional numbers while accepting ordinary integer env values.
        if isinstance(value, str) and value.strip().isdecimal():
            return int(value.strip())
        return value

    @field_validator("embed_dim")
    @classmethod
    def validate_embed_dim(cls, value: int) -> int:
        if value != 768:
            raise ValueError("EMBED_DIM must be 768 to match the knowledge index schema")
        return value

    @field_validator("embedding_model")
    @classmethod
    def validate_embedding_model(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("EMBEDDING_MODEL must be a non-empty model ID")
        return value.strip()

    @field_validator("gemini_model", "gemini_strong_model")
    @classmethod
    def qualify_gemini_model(cls, value: str) -> str:
        """Accept legacy .env model names while recording the OpenRouter model ID."""
        return f"google/{value}" if value.startswith("gemini-") else value

    @field_validator("anthropic_model")
    @classmethod
    def validate_anthropic_model(cls, value: str) -> str:
        stripped = value.strip()
        if value and not stripped:
            raise ValueError("ANTHROPIC_MODEL must be a non-empty model ID")
        return stripped

    @property
    def draft_model(self) -> str:
        return self.anthropic_model or self.gemini_model


@lru_cache
def get_settings() -> Settings:
    return Settings()
