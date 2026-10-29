"""
learn_llm — shared utilities for the LLM Learning Academy.

Import helpers from this package in lessons and projects.
All public functions have clear docstrings and type hints.
"""

from .config import get_config, LLMConfig

__all__ = ["get_config", "LLMConfig"]
__version__ = "0.1.0"
