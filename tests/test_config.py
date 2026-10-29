"""
test_config.py — tests for configuration loading and validation.

All tests run without real API keys. They test validation logic only.
"""

import os
import pytest
from unittest.mock import patch


class TestLLMConfig:
    """Tests for the LLMConfig dataclass."""

    def test_default_provider_is_gemini(self):
        from learn_llm.config import LLMConfig
        cfg = LLMConfig()
        assert cfg.provider == "gemini"

    def test_default_gemini_model(self):
        from learn_llm.config import LLMConfig
        cfg = LLMConfig()
        assert cfg.gemini_model == "gemini-3.8-flash"

    def test_config_fields_exist(self):
        """Ensure all expected fields exist on LLMConfig."""
        from learn_llm.config import LLMConfig
        cfg = LLMConfig()
        required_fields = [
            "provider", "gemini_api_key", "gemini_model",
            "openrouter_api_key", "openrouter_model",
            "ollama_base_url", "ollama_model",
        ]
        for field in required_fields:
            assert hasattr(cfg, field), f"LLMConfig missing field: {field}"


class TestGetConfig:
    """Tests for the get_config() function."""

    def test_unsupported_provider_exits(self):
        """An invalid LLM_PROVIDER value should call sys.exit."""
        with patch.dict(os.environ, {"LLM_PROVIDER": "invalid_provider"}):
            with pytest.raises(SystemExit):
                # Need fresh import to re-read env
                import importlib
                import learn_llm.config as cfg_module
                importlib.reload(cfg_module)
                cfg_module.get_config()

    def test_missing_gemini_key_exits(self, monkeypatch):
        """Missing GEMINI_API_KEY with provider=gemini should exit."""
        monkeypatch.setenv("LLM_PROVIDER", "gemini")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        from learn_llm import config
        import importlib
        importlib.reload(config)

        with pytest.raises(SystemExit):
            config.get_config()

    def test_placeholder_gemini_key_exits(self, monkeypatch):
        """Placeholder GEMINI_API_KEY value should exit."""
        monkeypatch.setenv("LLM_PROVIDER", "gemini")
        monkeypatch.setenv("GEMINI_API_KEY", "your_gemini_api_key_here")

        from learn_llm import config
        import importlib
        importlib.reload(config)

        with pytest.raises(SystemExit):
            config.get_config()

    def test_ollama_provider_needs_no_key(self, monkeypatch):
        """Ollama provider requires no API key — should not exit."""
        monkeypatch.setenv("LLM_PROVIDER", "ollama")
        monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        from learn_llm import config
        import importlib
        importlib.reload(config)

        # Should not raise
        cfg = config.get_config()
        assert cfg.provider == "ollama"
