"""
02_first_request_openrouter.py — Direct API Call with OpenRouter
===============================================================
Demonstrates how to use an OpenAI-compatible SDK (`openai`) to make
direct API calls to OpenRouter's free and open-source models.

OpenRouter Free Models:
  Models tagged with `:free` (e.g. `google/gemma-4-31b-it:free`) are free to query.
  Verify current free models at: https://openrouter.ai/models?q=:free
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


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_api_key_here":
        print("[ERROR] OPENROUTER_API_KEY is not set.")
        print("  1. Copy .env.example to .env")
        print("  2. Get a key at: https://openrouter.ai/keys")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("[ERROR] 'openai' package not installed. Run: pip install openai")
        sys.exit(1)

    # Free model identifier verified as of 2026-10-30
    model_id = os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    print(f"Connecting to OpenRouter ({base_url}) with model '{model_id}'...")
    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = "State one advantage and one limitation of token-based pricing."
    print(f"\nUser Prompt:\n  {prompt}\n")

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        print("OpenRouter Response:")
        print("-" * 60)
        print(answer)
        print("-" * 60)
    except Exception as exc:
        print(f"\n[ERROR] Request failed: {exc}")
        sys.exit(1)

    print("\n[SUCCESS] Lesson 02 complete!")


if __name__ == "__main__":
    main()
