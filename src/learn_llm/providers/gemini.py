"""
gemini.py — Google Gemini provider wrapper.

Uses the google-genai SDK (the new unified SDK, NOT google-generativeai).

Free tier available at: https://aistudio.google.com/
Pricing: https://ai.google.dev/pricing
Model IDs: https://ai.google.dev/gemini-api/docs/models

Verified: 2026-10-30
"""

from typing import Iterator
from .base import BaseProvider


class GeminiProvider(BaseProvider):
    """
    Thin wrapper around the Google Gemini API.

    Example:
        from learn_llm.providers import GeminiProvider
        provider = GeminiProvider(api_key="...", model="gemini-3.8-flash")
        print(provider.chat("What is an LLM?"))
    """

    def __init__(self, api_key: str, model: str = "gemini-3.8-flash") -> None:
        """
        Parameters:
            api_key: Your Google Gemini API key.
            model:   Model identifier — verify at https://ai.google.dev/gemini-api/docs/models
        """
        try:
            from google import genai
        except ImportError as exc:
            raise ImportError(
                "google-genai is not installed. Run: pip install google-genai"
            ) from exc

        self._client = genai.Client(api_key=api_key)
        self._model = model

    def chat(self, prompt: str, system: str = "") -> str:
        """Send a prompt to Gemini and return the full response text."""
        contents: list = []
        if system:
            # Gemini uses a system_instruction field, not a message role
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config={"system_instruction": system},
            )
        else:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
            )
        return response.text

    def stream(self, prompt: str, system: str = "") -> Iterator[str]:
        """Stream response chunks from Gemini."""
        kwargs = {"model": self._model, "contents": prompt}
        if system:
            kwargs["config"] = {"system_instruction": system}

        for chunk in self._client.models.generate_content_stream(**kwargs):
            if chunk.text:
                yield chunk.text
