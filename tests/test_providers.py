"""
test_providers.py — tests for provider wrappers using mocks.

No real API calls are made and no optional third-party packages (openai, google-genai)
are required to run these unit tests. sys.modules is pre-populated with mocks so that
the test suite can execute deterministically on any machine.
"""

import sys
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture(autouse=True)
def mock_sdk_modules():
    """Ensure mock modules for google.genai and openai are present in sys.modules."""
    mock_google = MagicMock()
    mock_genai = MagicMock()
    mock_google.genai = mock_genai

    mock_openai_module = MagicMock()

    modules_to_patch = {
        "google": mock_google,
        "google.genai": mock_genai,
        "openai": mock_openai_module,
    }

    with patch.dict(sys.modules, modules_to_patch):
        yield {
            "genai": mock_genai,
            "openai": mock_openai_module,
        }


class TestGeminiProvider:
    """Tests for GeminiProvider — mocked at the google.genai level."""

    def test_chat_calls_generate_content(self, fake_gemini_key, mock_sdk_modules):
        mock_response = MagicMock()
        mock_response.text = "Paris is the capital of France."
        mock_sdk_modules["genai"].Client.return_value.models.generate_content.return_value = mock_response

        from learn_llm.providers.gemini import GeminiProvider
        provider = GeminiProvider(api_key=fake_gemini_key)
        result = provider.chat("What is the capital of France?")

        assert result == "Paris is the capital of France."

    def test_chat_with_system_message(self, fake_gemini_key, mock_sdk_modules):
        mock_response = MagicMock()
        mock_response.text = "Bonjour!"
        mock_sdk_modules["genai"].Client.return_value.models.generate_content.return_value = mock_response

        from learn_llm.providers.gemini import GeminiProvider
        provider = GeminiProvider(api_key=fake_gemini_key)
        result = provider.chat("Say hello", system="You always respond in French.")

        assert result == "Bonjour!"
        call_kwargs = mock_sdk_modules["genai"].Client.return_value.models.generate_content.call_args
        assert "config" in call_kwargs.kwargs or any("config" in str(a) for a in call_kwargs.args)

    def test_import_error_raised_when_package_missing(self, fake_gemini_key):
        with patch.dict(sys.modules, {"google": None, "google.genai": None}):
            with pytest.raises(ImportError):
                from learn_llm.providers import gemini as gm
                import importlib
                importlib.reload(gm)
                gm.GeminiProvider(api_key=fake_gemini_key)


class TestOpenRouterProvider:
    """Tests for OpenRouterProvider — mocked at the openai level."""

    def test_chat_returns_response(self, fake_openrouter_key, mock_sdk_modules):
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "42"
        mock_sdk_modules["openai"].OpenAI.return_value.chat.completions.create.return_value = mock_completion

        from learn_llm.providers.openrouter import OpenRouterProvider
        provider = OpenRouterProvider(
            api_key=fake_openrouter_key,
            model="google/gemma-4-31b-it:free",
        )
        result = provider.chat("What is 6 times 7?")

        assert result == "42"

    def test_system_message_prepended(self, fake_openrouter_key, mock_sdk_modules):
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "Yes!"
        mock_sdk_modules["openai"].OpenAI.return_value.chat.completions.create.return_value = mock_completion

        from learn_llm.providers.openrouter import OpenRouterProvider
        provider = OpenRouterProvider(api_key=fake_openrouter_key)
        provider.chat("Are you a helpful assistant?", system="Be concise.")

        call_args = mock_sdk_modules["openai"].OpenAI.return_value.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args.args[0]
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 1
        assert system_msgs[0]["content"] == "Be concise."


class TestOllamaProvider:
    """Tests for OllamaProvider."""

    def test_is_available_returns_false_when_server_down(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
            from learn_llm.providers.ollama import OllamaProvider
            provider = OllamaProvider(model="llama3.2")
            assert provider.is_available() is False

    def test_list_models_returns_empty_on_error(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
            from learn_llm.providers.ollama import OllamaProvider
            provider = OllamaProvider()
            assert provider.list_models() == []
