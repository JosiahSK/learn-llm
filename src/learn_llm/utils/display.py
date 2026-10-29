"""
display.py — output helpers for lesson notebooks and scripts.
"""

from typing import Iterator
import sys


def print_stream(chunks: Iterator[str], end: str = "\n", flush: bool = True) -> str:
    """
    Print streaming response chunks to stdout as they arrive.

    Parameters:
        chunks: An iterator of text chunks (from provider.stream(...)).
        end:    String printed after the final chunk.
        flush:  Whether to flush stdout after each chunk.

    Returns:
        The complete concatenated response string.

    Example:
        full_response = print_stream(provider.stream("Tell me a story"))
    """
    collected: list[str] = []
    for chunk in chunks:
        print(chunk, end="", flush=flush)
        collected.append(chunk)
    print(end, end="")
    return "".join(collected)
