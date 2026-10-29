"""
app.py — Project 02: Multi-Model Interactive Chatbot
===================================================
A unified CLI chatbot that lets the user switch between providers
(Gemini, OpenRouter, Ollama) on the fly while retaining conversation history.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from learn_llm.providers import GeminiProvider, OpenRouterProvider, OllamaProvider


def main():
    print("=" * 65)
    print("Project 02: Multi-Provider Chatbot")
    print("Commands: 'switch gemini' | 'switch openrouter' | 'switch ollama' | 'clear' | 'exit'")
    print("=" * 65)

    current_provider_name = os.getenv("LLM_PROVIDER", "gemini").lower()
    print(f"\nActive Provider: [{current_provider_name.upper()}]")
    print("Type your message to begin chatting (or switch provider anytime):\n")

    conversation = []

    while True:
        try:
            user_msg = input(f"You ({current_provider_name}) > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if not user_msg:
            continue

        if user_msg.lower() in ("exit", "quit"):
            print("Chat session terminated.")
            break

        if user_msg.lower() == "clear":
            conversation = []
            print("[Conversation history cleared]\n")
            continue

        if user_msg.lower().startswith("switch "):
            target = user_msg.split(" ")[1].lower()
            if target in ("gemini", "openrouter", "ollama"):
                current_provider_name = target
                print(f"[Switched active provider to: {target.upper()}]\n")
            else:
                print(f"[Invalid provider: '{target}'. Options: gemini, openrouter, ollama]\n")
            continue

        conversation.append({"role": "user", "content": user_msg})

        # Mock or execute depending on active provider credentials
        reply = None
        if current_provider_name == "gemini":
            key = os.getenv("GEMINI_API_KEY")
            if key and key != "your_gemini_api_key_here":
                try:
                    p = GeminiProvider(api_key=key, model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"))
                    reply = p.chat(user_msg)
                except Exception as e:
                    reply = f"[Gemini Error: {e}]"
            else:
                reply = f"(Demo - Gemini key missing) Echoing: {user_msg}"

        elif current_provider_name == "openrouter":
            key = os.getenv("OPENROUTER_API_KEY")
            if key and key != "your_openrouter_api_key_here":
                try:
                    p = OpenRouterProvider(api_key=key, model=os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free"))
                    reply = p.chat(user_msg)
                except Exception as e:
                    reply = f"[OpenRouter Error: {e}]"
            else:
                reply = f"(Demo - OpenRouter key missing) Echoing: {user_msg}"

        elif current_provider_name == "ollama":
            p = OllamaProvider(model=os.getenv("OLLAMA_MODEL", "llama3.2"))
            if p.is_available():
                try:
                    reply = p.chat(user_msg)
                except Exception as e:
                    reply = f"[Ollama Error: {e}]"
            else:
                reply = "(Demo - Ollama server not reachable at localhost:11434)"

        conversation.append({"role": "assistant", "content": reply})
        print(f"\nAssistant > {reply}\n")


if __name__ == "__main__":
    main()
