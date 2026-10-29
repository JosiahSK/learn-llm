# Project 02 — Multi-Provider Interactive Chatbot

Build a real, interactive chat session in the terminal that lets you switch between AI providers *mid-conversation* without losing your chat history.

---

## What This Project Does

`app.py` drops you into a persistent terminal chat loop. You type messages; the model replies. At any time you can:

- Switch to a different provider (`switch gemini`, `switch openrouter`, `switch ollama`).
- Clear the conversation history (`clear`).
- See available commands (`help`).
- Exit cleanly (`quit` or Ctrl-C).

The full message history is preserved across provider switches, so the new model has full context of what was said before.

---

## Learning Objectives

1. Maintain a mutable `messages` list and append both user and assistant turns.
2. Understand how different providers share the same chat-completions API contract.
3. Switch provider clients at runtime without restarting the application.
4. Implement a clean REPL (Read-Eval-Print Loop) with robust error handling.
5. Use Ollama as a fully offline fallback that requires zero credentials.

---

## Setup

### 1 — Create your `.env`

```bash
cp projects/02_multimodel_chatbot/.env.example projects/02_multimodel_chatbot/.env
```

Fill in the keys for the providers you want to use.  Ollama requires no key — just a running local server.

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### 3 — (Optional) Start Ollama

```bash
ollama serve          # starts the server
ollama pull llama3    # download the default model
```

---

## Run

```bash
python projects/02_multimodel_chatbot/app.py
```

Start with a specific provider:

```bash
LLM_PROVIDER=ollama python projects/02_multimodel_chatbot/app.py
```

---

## Commands

| Command | Effect |
|---|---|
| `quit` / `exit` | Exit the chatbot |
| `clear` | Erase conversation history |
| `help` | Show available commands |
| `switch gemini` | Switch to Google Gemini |
| `switch openrouter` | Switch to OpenRouter |
| `switch ollama` | Switch to local Ollama |

---

## Expected Output

```
╔══════════════════════════════════════════╗
║    Multi-Provider Interactive Chatbot    ║
╚══════════════════════════════════════════╝
Active provider : gemini  (gemini-3.8-flash)
Type 'help' for commands.

You: What is a token in the context of LLMs?
[gemini] A token is the basic unit of text that an LLM processes...

You: switch ollama
✓ Switched to ollama (llama3)

You: Summarise what I just asked about.
[ollama] You asked about tokens in large language models...

You: quit
Goodbye!
```

---

## Exercises

**Exercise 1 — Observe provider personality differences (easy)**

Ask the same question of all three providers by switching between them. Which one is more verbose? More concise? More creative?

**Exercise 2 — Persistent history across a switch (medium)**

After a few turns with Gemini, switch to Ollama and ask: *"What did we talk about so far?"* Does Ollama correctly summarise the earlier conversation? Why or why not?

**Exercise 3 — Add a `/save` command (harder)**

Add a `save` command that writes the current conversation to a JSON file (`chat_history_<timestamp>.json`). Each turn should be stored as `{"role": "...", "content": "..."}`. Add a corresponding `load <filename>` command to restore a previous session.

---

## How It Works

```
User input → command parser → (switch / clear / help) OR send to LLM
                                                            ↓
                                              append to messages list
                                                            ↓
                                              active provider client
                                                            ↓
                                              print streamed response
                                                            ↓
                                              append assistant reply
```

The `messages` list is the single source of truth for the conversation.  Because every provider accepts the same `[{"role": "...", "content": "..."}]` format, switching is just a matter of swapping the client object — the history travels intact.

---

## No API Key? Use Ollama

If you don't have API keys yet, start the script with `LLM_PROVIDER=ollama`.  All you need is a machine with [Ollama](https://ollama.com) installed and a pulled model (`ollama pull llama3`).  No internet connection required during the chat session.
