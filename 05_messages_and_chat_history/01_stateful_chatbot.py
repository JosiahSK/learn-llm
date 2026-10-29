"""
01_stateful_chatbot.py — Terminal Chatbot with Conversational History
=====================================================================
Demonstrates how to build a stateful conversational loop around a stateless
API, showing message appending, role assignment, and history bounds.
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

from learn_llm.utils.text import count_words


def main():
    print("=" * 60)
    print("Module 05: Stateful Terminal Chatbot")
    print("Commands: 'exit' to quit | 'clear' to reset history | 'history' to view")
    print("=" * 60)

    # Initialize message log with a system rule
    messages = [
        {"role": "system", "content": "You are a concise, helpful programming mentor."}
    ]

    print("\nChatbot initialized. Type a message to begin:\n")

    # Offline simulation / fallback loop if no keys configured
    api_key = os.getenv("GEMINI_API_KEY")

    while True:
        try:
            user_input = input("You > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Session ended.")
            break

        if user_input.lower() == "clear":
            messages = [messages[0]]
            print("[History cleared]\n")
            continue

        if user_input.lower() == "history":
            print("\n--- Current Transcript ---")
            for idx, msg in enumerate(messages):
                print(f"[{idx}] {msg['role'].upper()}: {msg['content']}")
            print("--------------------------\n")
            continue

        # Append user turn
        messages.append({"role": "user", "content": user_input})

        # Calculate rough size of history
        total_chars = sum(len(m["content"]) for m in messages)
        total_words = sum(count_words(m["content"]) for m in messages)

        # Mock reply if offline, or execute via API if key present
        if api_key and api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
                # Format transcript for Gemini
                transcript = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
                resp = client.models.generate_content(model=model_id, contents=transcript)
                bot_reply = resp.text
            except Exception as e:
                bot_reply = f"[API Error: {e}]"
        else:
            bot_reply = f"(Demo Mode) Echoing response with context. History length: {len(messages)} turns."

        messages.append({"role": "assistant", "content": bot_reply})
        print(f"\nAssistant > {bot_reply}")
        print(f"[Context Stats: {total_words} words | ~{total_chars} chars across {len(messages)} messages]\n")


if __name__ == "__main__":
    main()
