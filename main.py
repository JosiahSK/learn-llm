"""
main.py — First LLM Request (Beginner Entry Point)
====================================================
This script demonstrates the simplest possible LLM API call using Google Gemini.
It handles the most common errors so you can diagnose problems quickly.

Usage:
    1. Copy .env.example to .env and add your GEMINI_API_KEY
    2. Run:  python main.py

Free API key:  https://aistudio.google.com/apikey
Pricing info:  https://ai.google.dev/pricing
Current model IDs: https://ai.google.dev/gemini-api/docs/models
"""

import os
import sys
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Minimal fallback parser if python-dotenv is not yet installed
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def validate_config() -> str:
    """
    Read and validate the GEMINI_API_KEY from the environment.
    Returns the key, or exits with a clear error message if missing.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print(
            "\n[ERROR] GEMINI_API_KEY is not set.\n"
            "  1. Copy .env.example to .env\n"
            "  2. Open .env and add your key (free at https://aistudio.google.com/apikey)\n"
        )
        sys.exit(1)
    if key == "your_gemini_api_key_here":
        print(
            "\n[ERROR] GEMINI_API_KEY is still the placeholder value.\n"
            "  Open .env and replace 'your_gemini_api_key_here' with your real key.\n"
        )
        sys.exit(1)
    return key


def make_llm_request(api_key: str, prompt: str) -> str:
    """
    Send a single text prompt to the Gemini API and return the response text.

    Parameters:
        api_key: Your Google Gemini API key.
        prompt:  The question or instruction for the model.

    Returns:
        The model's response text.

    Raises:
        ImportError: If the google-genai package is not installed.
        Exception:   On API errors (key invalid, quota exceeded, network, etc.)
    """
    try:
        from google import genai
    except ImportError:
        print(
            "\n[ERROR] google-genai is not installed.\n"
            "  Run:  pip install -r requirements.txt\n"
        )
        sys.exit(1)

    # IMPORTANT: Verify the model ID is current before using it.
    # Model IDs can change. Check: https://ai.google.dev/gemini-api/docs/models
    model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
        )
    except Exception as exc:
        # Surface the error clearly rather than silently failing
        error_str = str(exc)
        if "API_KEY_INVALID" in error_str or "401" in error_str:
            print(
                "\n[ERROR] API key was rejected.\n"
                "  - Check your GEMINI_API_KEY in .env\n"
                "  - Generate a new key at: https://aistudio.google.com/apikey\n"
            )
        elif "quota" in error_str.lower() or "429" in error_str:
            print(
                "\n[ERROR] Quota exceeded or rate-limited.\n"
                "  - Wait a moment and try again\n"
                "  - Check your quota at: https://aistudio.google.com/\n"
            )
        elif "NOT_FOUND" in error_str or "404" in error_str:
            print(
                f"\n[ERROR] Model '{model_id}' not found.\n"
                "  - Check GEMINI_MODEL in .env\n"
                "  - Current models: https://ai.google.dev/gemini-api/docs/models\n"
            )
        else:
            print(f"\n[ERROR] API request failed:\n  {exc}\n")
        sys.exit(1)

    return response.text


def main() -> None:
    """Run a single demonstraton LLM request."""
    api_key = validate_config()

    prompt = "Explain what a large language model is in 2–3 sentences, for a beginner."

    print(f"\nSending prompt to Gemini...\nPrompt: {prompt!r}\n")
    print("-" * 60)

    answer = make_llm_request(api_key, prompt)
    print(answer)
    print("-" * 60)
    print("\nSuccess! See the ai_agent/ notebooks for more examples.")


if __name__ == "__main__":
    main()