"""
text.py — text processing helpers for LLM lessons.
"""

from typing import Iterator


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[str]:
    """
    Split text into overlapping chunks for embedding and RAG.

    Splits on word boundaries to avoid cutting mid-word.

    Parameters:
        text:          The input text to split.
        chunk_size:    Target number of characters per chunk.
        chunk_overlap: Number of characters to repeat between adjacent chunks.
                       Overlap preserves context at chunk boundaries.

    Returns:
        A list of text chunks.

    Notes:
        - Chunk size and overlap are measured in characters, not tokens.
        - For production use, prefer token-based chunking to respect model limits.
        - Larger chunks preserve context but may exceed embedding model limits.
        - Smaller chunks improve recall precision but may lose context.

    Example:
        >>> chunks = chunk_text("Hello world this is a test", chunk_size=10, chunk_overlap=3)
    """
    if not text.strip():
        return []

    words = text.split()
    chunks: list[str] = []
    current_chunk: list[str] = []
    current_length = 0

    for word in words:
        word_len = len(word) + 1  # +1 for the space
        if current_length + word_len > chunk_size and current_chunk:
            chunk_text_str = " ".join(current_chunk)
            chunks.append(chunk_text_str)

            # Keep last few words as overlap
            overlap_text = chunk_text_str[-chunk_overlap:]
            current_chunk = overlap_text.split()
            current_length = sum(len(w) + 1 for w in current_chunk)

        current_chunk.append(word)
        current_length += word_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def count_words(text: str) -> int:
    """Return the number of whitespace-delimited words in a string."""
    return len(text.split())


def truncate_text(text: str, max_chars: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to max_chars and append a suffix if truncated.

    Useful for displaying long model responses in lessons without flooding output.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + suffix
