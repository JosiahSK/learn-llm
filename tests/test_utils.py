"""
test_utils.py — tests for text processing utilities.

All tests run without network access or API keys.
"""

import pytest


class TestChunkText:
    """Tests for the chunk_text utility."""

    def test_empty_string_returns_empty_list(self):
        from learn_llm.utils.text import chunk_text
        assert chunk_text("") == []

    def test_whitespace_only_returns_empty_list(self):
        from learn_llm.utils.text import chunk_text
        assert chunk_text("   \n  ") == []

    def test_short_text_returns_single_chunk(self):
        from learn_llm.utils.text import chunk_text
        text = "Hello world"
        chunks = chunk_text(text, chunk_size=500)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_chunks_cover_all_words(self, sample_text):
        """All words in the input should appear in the output chunks."""
        from learn_llm.utils.text import chunk_text
        chunks = chunk_text(sample_text, chunk_size=100, chunk_overlap=20)
        # Joining chunks won't be identical (overlap), but all unique words should appear
        all_chunk_text = " ".join(chunks)
        for word in sample_text.split():
            assert word in all_chunk_text

    def test_chunk_size_respected(self, sample_text):
        """Individual chunks should not greatly exceed the requested size."""
        from learn_llm.utils.text import chunk_text
        chunk_size = 100
        chunks = chunk_text(sample_text, chunk_size=chunk_size, chunk_overlap=10)
        for chunk in chunks:
            # Allow a modest overshoot from word boundary rounding
            assert len(chunk) <= chunk_size + 50

    def test_returns_list_of_strings(self, sample_text):
        from learn_llm.utils.text import chunk_text
        chunks = chunk_text(sample_text)
        assert isinstance(chunks, list)
        assert all(isinstance(c, str) for c in chunks)


class TestCountWords:
    def test_empty_string(self):
        from learn_llm.utils.text import count_words
        assert count_words("") == 0

    def test_single_word(self):
        from learn_llm.utils.text import count_words
        assert count_words("hello") == 1

    def test_multiple_words(self):
        from learn_llm.utils.text import count_words
        assert count_words("hello world foo bar") == 4


class TestTruncateText:
    def test_short_text_unchanged(self):
        from learn_llm.utils.text import truncate_text
        text = "Short text"
        assert truncate_text(text, max_chars=100) == text

    def test_long_text_truncated(self):
        from learn_llm.utils.text import truncate_text
        text = "word " * 100
        result = truncate_text(text, max_chars=20)
        assert len(result) <= 25  # 20 + len("...")
        assert result.endswith("...")
