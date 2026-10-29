"""
conftest.py — shared pytest fixtures for learn-llm tests.

All tests in the core suite run without real API credentials.
Tests requiring real APIs are marked with @pytest.mark.requires_api
and are skipped by default in CI.
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def fake_gemini_key() -> str:
    """A syntactically valid but fake Gemini API key for testing."""
    return "AIzaSyTESTKEY12345678901234567890123456"


@pytest.fixture
def fake_openrouter_key() -> str:
    """A syntactically valid but fake OpenRouter API key for testing."""
    return "sk-or-test-FAKEKEY12345678901234567890"


@pytest.fixture
def mock_gemini_response():
    """A mock Gemini API response object."""
    mock = MagicMock()
    mock.text = "This is a mock LLM response for testing."
    return mock


@pytest.fixture
def mock_openai_response():
    """A mock OpenAI-compatible API response object."""
    mock = MagicMock()
    mock.choices = [MagicMock()]
    mock.choices[0].message.content = "This is a mock LLM response for testing."
    return mock


@pytest.fixture
def sample_text() -> str:
    """A multi-sentence sample text for chunking and embedding tests."""
    return (
        "Large language models are a type of artificial intelligence trained on vast amounts "
        "of text data. They can generate, summarize, translate, and answer questions about "
        "text. Modern LLMs are based on the transformer architecture, which uses an "
        "attention mechanism to understand relationships between words in a sequence. "
        "The quality of an LLM's output depends on its training data, size, and the "
        "instructions given to it at inference time."
    )
