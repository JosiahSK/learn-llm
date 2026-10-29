"""
config.py — configuration loading and validation for learn-llm.

Loads settings from environment variables (via .env).
Provides a single LLMConfig dataclass used across modules.

Usage:
    from learn_llm.config import get_config
    cfg = get_config()
    print(cfg.provider)   # 'gemini' | 'openrouter' | 'ollama'
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Optional
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


SUPPORTED_PROVIDERS = ("gemini", "openrouter", "ollama")


@dataclass
class LLMConfig:
    """All runtime configuration for an LLM lesson or project."""

    # Active provider
    provider: str = "gemini"

    # Gemini
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-3.8-flash"

    # OpenRouter
    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "google/gemma-4-31b-it:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_embed_model: str = "nomic-embed-text"


def get_config() -> LLMConfig:
    """
    Read and validate configuration from environment variables.

    Returns:
        LLMConfig with values from the environment.

    Raises:
        SystemExit: If required values for the selected provider are missing.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower().strip()

    if provider not in SUPPORTED_PROVIDERS:
        print(
            f"[ERROR] LLM_PROVIDER='{provider}' is not supported.\n"
            f"  Supported values: {', '.join(SUPPORTED_PROVIDERS)}\n"
            "  Check your .env file."
        )
        sys.exit(1)

    cfg = LLMConfig(
        provider=provider,
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        openrouter_model=os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free"),
        openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        ollama_embed_model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
    )

    _validate_provider_config(cfg)
    return cfg


def _validate_provider_config(cfg: LLMConfig) -> None:
    """Exit with a clear message if required provider credentials are missing."""
    if cfg.provider == "gemini":
        if not cfg.gemini_api_key:
            _missing_key_error(
                "GEMINI_API_KEY",
                "Get a free key at: https://aistudio.google.com/apikey",
            )
        if cfg.gemini_api_key == "your_gemini_api_key_here":
            _placeholder_error("GEMINI_API_KEY")

    elif cfg.provider == "openrouter":
        if not cfg.openrouter_api_key:
            _missing_key_error(
                "OPENROUTER_API_KEY",
                "Get a key at: https://openrouter.ai/keys",
            )
        if cfg.openrouter_api_key == "your_openrouter_api_key_here":
            _placeholder_error("OPENROUTER_API_KEY")

    elif cfg.provider == "ollama":
        # No API key needed for Ollama — just a running server
        pass


def _missing_key_error(env_var: str, hint: str) -> None:
    print(
        f"\n[ERROR] {env_var} is not set.\n"
        f"  1. Copy .env.example to .env\n"
        f"  2. Set {env_var} in .env\n"
        f"  {hint}\n"
    )
    sys.exit(1)


def _placeholder_error(env_var: str) -> None:
    print(
        f"\n[ERROR] {env_var} is still the placeholder value.\n"
        "  Open .env and replace it with your real key.\n"
    )
    sys.exit(1)
