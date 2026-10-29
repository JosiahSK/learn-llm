"""
01_prompt_basics.py — Prompt Comparison Experiment
==================================================
Demonstrates the concrete impact of prompt structure:
  - Naive prompt vs Structured Prompt with Constraints
  - Zero-Shot vs Few-Shot Prompting
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from learn_llm.config import get_config


def main():
    print("=" * 60)
    print("Module 04: Prompt Engineering Laboratory")
    print("=" * 60)

    # 1. Compare Naive vs Constrained Prompting
    naive_prompt = "Tell me about Python lists."
    
    engineered_prompt = (
        "Explain Python lists to a complete beginner.\n"
        "Constraints:\n"
        "1. Exactly three bullet points.\n"
        "2. Include one line of code demonstrating list creation.\n"
        "3. Do not exceed 60 words total."
    )

    print("\n[EXPERIMENT 1] Naive vs Engineered Prompt")
    print("\n--- Naive Prompt ---")
    print(naive_prompt)
    print("\n--- Engineered Prompt ---")
    print(engineered_prompt)

    # 2. Compare Zero-Shot vs Few-Shot Classification
    zero_shot = (
        "Classify the sentiment of this review as POSITIVE, NEGATIVE, or NEUTRAL:\n"
        "'The battery lasted 45 minutes before dying completely.'"
    )

    few_shot = (
        "Classify customer feedback into POSITIVE, NEGATIVE, or NEUTRAL.\n\n"
        "Review: 'Arrived two days early and works like a charm.'\n"
        "Sentiment: POSITIVE\n\n"
        "Review: 'Color is slightly different than shown, but decent.'\n"
        "Sentiment: NEUTRAL\n\n"
        "Review: 'The battery lasted 45 minutes before dying completely.'\n"
        "Sentiment:"
    )

    print("\n" + "=" * 60)
    print("[EXPERIMENT 2] Zero-Shot vs Few-Shot Pattern")
    print("\n--- Few-Shot Demonstration ---")
    print(few_shot)
    print("=" * 60)
    print("\n[Takeaway] Few-shot examples anchor the output distribution, enforcing strict formatting.")


if __name__ == "__main__":
    main()
