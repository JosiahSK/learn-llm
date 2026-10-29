"""
app.py — Project 04: Real-Time Streaming Terminal Chat
=====================================================
Streams responses token-by-token with real-time latency monitoring.
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from learn_llm.providers import GeminiProvider, OpenRouterProvider


def simulate_stream(prompt: str):
    """Simulates a fast stream of tokens when API keys are unconfigured."""
    text = f"You asked: '{prompt}'. In streaming mode, data frames arrive as SSE chunks from the server."
    for word in text.split(" "):
        time.sleep(0.04)
        yield word + " "


def main():
    print("=" * 65)
    print("Project 04: Real-Time Streaming Chatbot")
    print("Type your question and press Enter. (Press Ctrl+C to abort a response)")
    print("=" * 65)

    api_key = os.getenv("GEMINI_API_KEY")
    use_cloud = bool(api_key and api_key != "your_gemini_api_key_here")

    if use_cloud:
        provider = GeminiProvider(api_key=api_key, model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"))
        print("[Engine: Google Gemini Live Stream]\n")
    else:
        print("[Engine: Offline Simulation Mode (Set GEMINI_API_KEY in .env for cloud API)]\n")

    while True:
        try:
            query = input("Prompt > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            break

        print("\nStreaming response: ", end="", flush=True)
        start_time = time.perf_counter()
        first_token_time = None
        chunk_count = 0

        try:
            stream_gen = provider.stream(query) if use_cloud else simulate_stream(query)
            for chunk in stream_gen:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                print(chunk, end="", flush=True)
                chunk_count += 1
        except KeyboardInterrupt:
            print("\n[Stream aborted by user]")
        except Exception as e:
            print(f"\n[Stream Error: {e}]")

        total_elapsed = time.perf_counter() - start_time
        ttft = (first_token_time - start_time) * 1000 if first_token_time else 0.0

        print(f"\n\n[Telemetry: TTFT = {ttft:.1f}ms | Total Duration = {total_elapsed:.2f}s | Chunks = {chunk_count}]\n")


if __name__ == "__main__":
    main()
