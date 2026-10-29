"""
01_first_request_gemini.py — First API Call with Google Gemini
=============================================================
This lesson demonstrates how to interact directly with Google Gemini
using the official unified `google-genai` SDK without third-party frameworks.

Prerequisites:
  1. Add your GEMINI_API_KEY to your .env file
  2. Run: pip install -r requirements.txt
  3. Execute: python 01_first_request_gemini.py
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path so we can import src modules if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("[ERROR] GEMINI_API_KEY is not set.")
        print("  1. Copy .env.example to .env")
        print("  2. Get a free key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("[ERROR] 'google-genai' is not installed. Run: pip install google-genai")
        sys.exit(1)

    # Verified model identifier (2026-10-30)
    model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    print(f"Connecting to Gemini API using model '{model_id}'...")
    client = genai.Client(api_key=api_key)

    prompt = "Explain in two sentences why Large Language Models are useful for software engineers."
    print(f"\nUser Prompt:\n  {prompt}\n")

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
        )
        print("Gemini Response:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
    except Exception as exc:
        print(f"\n[ERROR] API Call Failed: {exc}")
        sys.exit(1)

    print("\n[SUCCESS] Lesson 01 complete! Next step: explore message roles in 03_message_roles.py.")


if __name__ == "__main__":
    main()
