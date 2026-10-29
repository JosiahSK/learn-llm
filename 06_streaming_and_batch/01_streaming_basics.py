"""
01_streaming_basics.py — Streaming vs Non-Streaming Benchmark
============================================================
Compares traditional blocked responses against streamed chunks,
measuring Time To First Token (TTFT) and total generation time.
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def run_simulated_stream():
    """Runs an offline streaming demonstration without network calls."""
    print("\n[OFFLINE SIMULATION] Demonstrating incremental chunk streaming:")
    text = (
        "Streaming delivers content incrementally via chunked transfer encoding. "
        "This keeps users engaged while the model continues generating complex reasoning steps."
    )
    tokens = text.split(" ")
    start_time = time.perf_counter()
    first_token_time = None

    print("Stream > ", end="", flush=True)
    for token in tokens:
        time.sleep(0.04)  # Simulate network latency
        if first_token_time is None:
            first_token_time = time.perf_counter()
        print(token + " ", end="", flush=True)

    total_time = time.perf_counter() - start_time
    ttft = (first_token_time - start_time) * 1000 if first_token_time else 0
    print(f"\n\n[Stats: TTFT = {ttft:.1f}ms | Total Duration = {total_time:.2f}s]")


def main():
    print("=" * 60)
    print("Module 06: Streaming & Batch Latency Benchmark")
    print("=" * 60)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        run_simulated_stream()
        print("\nTo test with real cloud APIs, add GEMINI_API_KEY to your .env file.")
        return

    try:
        from google import genai
    except ImportError:
        run_simulated_stream()
        return

    client = genai.Client(api_key=api_key)
    model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    prompt = "Write an informative paragraph explaining why token streaming matters in generative AI."

    # 1. Non-streaming request
    print("\n--- 1. Testing Non-Streaming (Blocking) Request ---")
    start = time.perf_counter()
    resp = client.models.generate_content(model=model_id, contents=prompt)
    blocked_time = time.perf_counter() - start
    print(f"Response received in {blocked_time:.2f}s (All-at-once delivery)")

    # 2. Streaming request
    print("\n--- 2. Testing Streaming Request ---")
    start = time.perf_counter()
    first_token = None
    chunks_count = 0

    print("Live Stream: ", end="", flush=True)
    for chunk in client.models.generate_content_stream(model=model_id, contents=prompt):
        if first_token is None:
            first_token = time.perf_counter()
        if chunk.text:
            print(chunk.text, end="", flush=True)
            chunks_count += 1

    total_stream_time = time.perf_counter() - start
    ttft = (first_token - start) * 1000 if first_token else 0

    print(f"\n\n[Benchmark Summary]")
    print(f"Non-Streaming Wait Time: {blocked_time:.2f}s")
    print(f"Streaming TTFT:           {ttft:.1f}ms (Perceived latency)")
    print(f"Streaming Total Time:     {total_stream_time:.2f}s ({chunks_count} chunks)")


if __name__ == "__main__":
    main()
