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


class DraftChatOpenRouter(ChatOpenRouter):
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
