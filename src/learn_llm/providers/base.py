"""
base.py — abstract base class for provider wrappers.

All providers implement the same interface so lessons can switch
between them without changing business logic.
"""

from abc import ABC, abstractmethod
from typing import Iterator


class BaseProvider(ABC):
    """Common interface for all LLM provider wrappers."""

    @abstractmethod
    def chat(self, prompt: str, system: str = "") -> str:
        """
        Send a single prompt and return the complete response text.

        Parameters:
            prompt: The user's question or instruction.
            system: Optional system/developer instruction.

        Returns:
            The model's response as a plain string.
        """

    @abstractmethod
    def stream(self, prompt: str, system: str = "") -> Iterator[str]:
        """
        Send a prompt and yield response text chunks as they arrive.

        Parameters:
            prompt: The user's question or instruction.
            system: Optional system/developer instruction.

        Yields:
            Text chunks from the model response.
        """
