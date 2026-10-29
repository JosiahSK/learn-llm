"""
ollama.py — Ollama local model provider wrapper.

Ollama runs LLMs locally on your machine — no API key, no cloud costs.

Install Ollama: https://ollama.com/
Model library:  https://ollama.com/library

Before using:
    1. Install Ollama
    2. Run: ollama pull llama3.2  (or your preferred model)
    3. Ensure Ollama is running (it starts a local server at :11434)

RAM requirements:
    - 7B parameter models:  ~8 GB RAM
    - 13B parameter models: ~16 GB RAM
    - 70B parameter models: ~40+ GB RAM

Verified: 2026-10-30
"""

from typing import Iterator
from .base import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Thin wrapper around the Ollama local API.

    The Ollama server must be running before you use this.
    Check with: curl http://localhost:11434/api/tags

    Example:
        from learn_llm.providers import OllamaProvider
        provider = OllamaProvider(model="llama3.2")
        print(provider.chat("What is Python?"))
    """

    def __init__(
        self,
        model: str = "llama3.2",
        base_url: str = "http://localhost:11434",
    ) -> None:
        """
        Parameters:
            model:    The Ollama model name (must be pulled first).
            base_url: Ollama server URL (default: http://localhost:11434).
        """
        try:
            from openai import OpenAI  # Ollama exposes an OpenAI-compatible API
        except ImportError as exc:
            raise ImportError(
                "openai is not installed. Run: pip install openai"
            ) from exc

        # Ollama's OpenAI-compatible endpoint
        self._client = OpenAI(
            api_key="ollama",  # Ollama ignores the key, but the client requires one
            base_url=f"{base_url.rstrip('/')}/v1",
        )
        self._model = model
        self._base_url = base_url

    def is_available(self) -> bool:
        """Check if the Ollama server is reachable."""
        try:
            import urllib.request
            req = urllib.request.Request(f"{self._base_url}/api/tags", headers={"User-Agent": "learn-llm"})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """Return a list of models currently installed in Ollama."""
        try:
            import json
            import urllib.request
            req = urllib.request.Request(f"{self._base_url}/api/tags", headers={"User-Agent": "learn-llm"})
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    return [m["name"] for m in data.get("models", [])]
                return []
        except Exception:
            return []

    def chat(self, prompt: str, system: str = "") -> str:
        """Send a prompt to the local Ollama model and return the response."""
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
        """Stream response chunks from the local Ollama model."""
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
