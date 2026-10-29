"""
Project 01 — Basic LLM Chat
============================
This is the entry-point for every other project in the learn-llm course.

What it does
------------
1. Reads configuration (provider, model, API key) from environment variables or
   a .env file in this directory.
2. Creates the appropriate LLM client for the selected provider.
3. Sends a single user message and prints the model's reply.

Supported providers
-------------------
- gemini      : Google Gemini via the google-genai SDK
- openrouter  : Any model hosted on OpenRouter (OpenAI-compatible)
- ollama      : A locally-running Ollama server (OpenAI-compatible)

Environment variables
---------------------
LLM_PROVIDER        : "gemini" | "openrouter" | "ollama"  (default: gemini)
GEMINI_API_KEY      : Your Google AI Studio key (required for gemini)
OPENROUTER_API_KEY  : Your OpenRouter key (required for openrouter)
GEMINI_MODEL        : Override the Gemini model name
OPENROUTER_MODEL    : Override the OpenRouter model name
OLLAMA_MODEL        : Override the Ollama model name
OLLAMA_BASE_URL     : Ollama server URL (default: http://localhost:11434/v1)
LLM_SYSTEM_PROMPT   : Optional system-role message prepended to every request

Usage
-----
    python projects/01_basic_llm_chat/app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Load .env from *this* directory first, then the repo root.
# We do this manually so the script works even if the learn_llm package is not
# installed in the current Python environment.
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv  # type: ignore

    _here = Path(__file__).parent
    load_dotenv(_here / ".env", override=False)          # project-level .env
    load_dotenv(_here.parent.parent / ".env", override=False)  # repo-root .env
except ImportError:
    pass  # python-dotenv not available; rely on shell environment

# ---------------------------------------------------------------------------
# Try to use the shared config module; fall back to raw os.environ reads.
# ---------------------------------------------------------------------------
try:
    from learn_llm.config import get_config  # type: ignore

    _cfg = get_config()
    PROVIDER = _cfg.provider
    GEMINI_API_KEY = _cfg.gemini_api_key or ""
    OPENROUTER_API_KEY = _cfg.openrouter_api_key or ""
    GEMINI_MODEL = _cfg.gemini_model
    OPENROUTER_MODEL = _cfg.openrouter_model
    OLLAMA_MODEL = _cfg.ollama_model
    OLLAMA_BASE_URL = _cfg.ollama_base_url
    SYSTEM_PROMPT = _cfg.system_prompt or ""
except Exception:
    # Fallback: read directly from environment
    PROVIDER = os.environ.get("LLM_PROVIDER", "gemini").strip().lower()
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    SYSTEM_PROMPT = os.environ.get("LLM_SYSTEM_PROMPT", "")

# ---------------------------------------------------------------------------
# The prompt we send in this demo.  Edit this to experiment!
# ---------------------------------------------------------------------------
PROMPT = "Explain what a large language model is in exactly two sentences."


# ---------------------------------------------------------------------------
# Provider helpers
# ---------------------------------------------------------------------------

def _run_gemini(prompt: str) -> str:
    """Send *prompt* to Google Gemini and return the response text."""
    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "google-genai is not installed.  Run: pip install google-genai"
        ) from exc

    if not GEMINI_API_KEY:
        raise SystemExit(
            "GEMINI_API_KEY is not set.  "
            "Copy .env.example → .env and add your key."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    contents: list = []
    if SYSTEM_PROMPT:
        # Gemini uses a system_instruction field rather than a role message.
        pass  # handled via system_instruction below

    contents.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )

    config_kwargs: dict = {}
    if SYSTEM_PROMPT:
        config_kwargs["system_instruction"] = SYSTEM_PROMPT

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None,
    )
    return response.text


def _run_openai_compat(prompt: str, *, base_url: str, api_key: str, model: str) -> str:
    """Send *prompt* to any OpenAI-compatible endpoint and return response text."""
    try:
        from openai import OpenAI  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "openai is not installed.  Run: pip install openai"
        ) from exc

    client = OpenAI(base_url=base_url, api_key=api_key or "not-needed")

    messages: list[dict] = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(model=model, messages=messages)
    content = completion.choices[0].message.content
    if content is None:
        raise ValueError("The model returned an empty response.")
    return content


def _run_openrouter(prompt: str) -> str:
    """Send *prompt* to OpenRouter."""
    if not OPENROUTER_API_KEY:
        raise SystemExit(
            "OPENROUTER_API_KEY is not set.  "
            "Copy .env.example → .env and add your key."
        )
    return _run_openai_compat(
        prompt,
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model=OPENROUTER_MODEL,
    )


def _run_ollama(prompt: str) -> str:
    """Send *prompt* to a local Ollama server."""
    return _run_openai_compat(
        prompt,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama ignores the key but the client requires one
        model=OLLAMA_MODEL,
    )


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------
_PROVIDERS: dict[str, tuple[str, callable]] = {
    "gemini":      (GEMINI_MODEL,      _run_gemini),
    "openrouter":  (OPENROUTER_MODEL,  _run_openrouter),
    "ollama":      (OLLAMA_MODEL,      _run_ollama),
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== Basic LLM Chat ===")

    if PROVIDER not in _PROVIDERS:
        raise SystemExit(
            f"Unknown provider '{PROVIDER}'.  "
            f"Choose one of: {', '.join(_PROVIDERS)}"
        )

    model_name, runner = _PROVIDERS[PROVIDER]

    print(f"Provider : {PROVIDER}")
    print(f"Model    : {model_name}")
    print(f"Prompt   : {PROMPT}")
    if SYSTEM_PROMPT:
        print(f"System   : {SYSTEM_PROMPT}")
    print()

    try:
        response_text = runner(PROMPT)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        print(f"Error calling {PROVIDER}: {exc}", file=sys.stderr)
        sys.exit(1)

    print("--- Response ---")
    print(response_text)
    print("----------------")
    print("Done.")


if __name__ == "__main__":
    main()
