"""
openrouter.py — OpenRouter provider wrapper.

OpenRouter provides access to many models (including free ones) via
an OpenAI-compatible API endpoint.

Free models: https://openrouter.ai/models?q=:free  (availability changes)
Docs: https://openrouter.ai/docs
API keys: https://openrouter.ai/keys

Verified: 2026-10-30

IMPORTANT: Free model availability changes. Always check the current list
before depending on a specific free model. A model listed as free today
may require payment tomorrow, or may be removed.
"""

from typing import Iterator
from .base import BaseProvider


class OpenRouterProvider(BaseProvider):
    """
    Thin wrapper around the OpenRouter API (OpenAI-compatible).

    Example:
        from learn_llm.providers import OpenRouterProvider
        provider = OpenRouterProvider(
            api_key="...",
            model="google/gemma-4-31b-it:free"
        )
        print(provider.chat("Hello!"))
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        api_key: str,
        model: str = "google/gemma-4-31b-it:free",
        base_url: str = BASE_URL,
    ) -> None:
        """
        Parameters:
            api_key:  Your OpenRouter API key.
            model:    Model identifier (include `:free` suffix for free models).
            base_url: Override the API base URL (rarely needed).
        """
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "openai is not installed. Run: pip install openai"
            ) from exc

        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def chat(self, prompt: str, system: str = "") -> str:
        """Send a prompt to OpenRouter and return the full response text."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
        )
        return response.choices[0].message.content or ""

    def stream(self, prompt: str, system: str = "") -> Iterator[str]:
        """Stream response chunks from OpenRouter."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        with self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            stream=True,
        ) as stream:
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content
