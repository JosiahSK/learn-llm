# Project 01 — Basic LLM Chat

A minimal, single-file introduction to calling a Large Language Model API from Python. You send one message; the model replies. That's it — but every component you'll use in more advanced projects starts right here.

---

## What This Project Does

`app.py` loads your API credentials, picks a provider (Gemini, OpenRouter, or Ollama), sends a hard-coded prompt, and prints the model's response to the terminal. No web server, no database, no complexity — just the raw request/response cycle.

---

## Learning Objectives

By the end of this project you will be able to:

1. Configure provider credentials via a `.env` file.
2. Instantiate an LLM client programmatically.
3. Construct a minimal `messages` payload and fire a chat-completion request.
4. Read the response text from the returned object.
5. Understand why the same code works across different providers (OpenAI-compatible API).

---

## Setup

### 1 — Copy the example environment file

```bash
cp projects/01_basic_llm_chat/.env.example projects/01_basic_llm_chat/.env
```

On Windows (PowerShell):

```powershell
Copy-Item projects\01_basic_llm_chat\.env.example projects\01_basic_llm_chat\.env
```

### 2 — Add your API key

Open `projects/01_basic_llm_chat/.env` and fill in the key for the provider you want to use:

| Provider | Where to get a key |
|---|---|
| **Gemini** | [aistudio.google.com](https://aistudio.google.com) → *Get API key* |
| **OpenRouter** | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Ollama** | No key needed — just install [Ollama](https://ollama.com) and run `ollama pull llama3` |

Set `LLM_PROVIDER` to `gemini`, `openrouter`, or `ollama`.

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python projects/01_basic_llm_chat/app.py
```

To override the provider without editing `.env`:

```bash
LLM_PROVIDER=ollama python projects/01_basic_llm_chat/app.py
```

---

## Expected Output

```
=== Basic LLM Chat ===
Provider : gemini
Model    : gemini-3.8-flash
Prompt   : Explain what a large language model is in exactly two sentences.

--- Response ---
A large language model (LLM) is a type of artificial intelligence trained on
vast amounts of text data to understand and generate human-like language.
It works by predicting the most likely next word (or token) given everything
that came before it, allowing it to write, summarise, translate, and answer
questions.
----------------
Done.
```

---

## Exercises

**Exercise 1 — Change the prompt (easy)**

Edit the `PROMPT` constant in `app.py` to ask something different, such as:

```
"What are three practical uses for LLMs in software development?"
```

Run the script and observe how the response changes.

**Exercise 2 — Try all three providers (medium)**

Run the script three times, once with each provider, by changing `LLM_PROVIDER` in your `.env` (or as an environment variable). Note the differences in:
- Response wording
- Speed
- Default model name shown

**Exercise 3 — Add a system prompt (harder)**

Modify `app.py` to include a `system` role message before the user message. Give the model a persona, e.g. *"You are a pirate who explains technology in nautical metaphors."* Compare the responses before and after. Then try making the system prompt changeable via an environment variable `LLM_SYSTEM_PROMPT`.

---

## How It Works

```
.env  →  config loader  →  provider client  →  API call  →  print response
```

1. **Config** — `python-dotenv` reads your `.env` file into `os.environ`.
2. **Client** — A thin wrapper picks the right SDK (`google-genai` for Gemini, `openai` for OpenRouter/Ollama).
3. **Request** — A list of message dicts (`[{"role": "user", "content": "..."}]`) is sent.
4. **Response** — The API returns a completion object; we extract `.choices[0].message.content` (or the Gemini equivalent).

All three providers follow the OpenAI chat-completions schema, which is why nearly the same code works for all of them.

---

## API Keys & Free Tier Notes

- **Gemini** offers a free tier via AI Studio with generous rate limits (suitable for all exercises in this course).
- **OpenRouter** provides free access to several models (look for the `(free)` tag on [openrouter.ai/models](https://openrouter.ai/models)). Credit-based billing kicks in only after you exhaust the free quota.
- **Ollama** is completely free and runs locally — no internet required after the initial model download. Requires a machine with at least 8 GB RAM for 7 B-parameter models.

> **Never commit your `.env` file.** The `.gitignore` at the repository root already excludes `*.env` and `.env` files.
