# Project Catalog

This catalog documents every implemented project in the `projects/` directory. Each project is a self-contained, runnable application that demonstrates one or more LLM concepts in a practical context.

> [!TIP]
> Projects build on each other. If you're new, start with **Project 01** and work forward. Each project lists what you'll learn and which provider is required.

---

## Project 01 — Basic LLM Chat

**The "Hello, World!" of LLM programming.** Sends a single request to a language model, displays the response, and handles errors gracefully.

| Feature | Status |
|---------|--------|
| Single-turn request/response | ✅ Implemented |
| Gemini provider | ✅ Implemented |
| OpenRouter provider | ✅ Implemented |
| Ollama (local) provider | ✅ Implemented |
| Graceful API error handling | ✅ Implemented |
| `.env`-based config | ✅ Implemented |

**Directory:** [`projects/01_basic_llm_chat/`](../projects/01_basic_llm_chat/)

**Providers:** Google Gemini, OpenRouter, Ollama

**Requirements:** A free Gemini or OpenRouter API key, **or** Ollama installed locally with any model pulled.

**Run:**

```bash
python projects/01_basic_llm_chat/app.py
```

**What you'll learn:**

- How to authenticate with an LLM API using environment variables
- The basic request/response cycle (prompt → completion)
- How to handle common API errors (auth failure, rate limit, network timeout)
- How to read configuration from `.env` using `python-dotenv`
- The differences between calling a cloud API vs. a local Ollama endpoint

---

## Project 02 — Multi-Provider Chatbot

**An interactive terminal chatbot** that maintains conversation history and can switch between multiple LLM providers mid-session.

| Feature | Status |
|---------|--------|
| Interactive REPL loop | ✅ Implemented |
| Multi-turn conversation history | ✅ Implemented |
| Provider switching at runtime | ✅ Implemented |
| Gemini provider | ✅ Implemented |
| OpenRouter provider | ✅ Implemented |
| Ollama provider | ✅ Implemented |
| `/help` and `/quit` commands | ✅ Implemented |
| `/switch <provider>` command | ✅ Implemented |

**Directory:** [`projects/02_multimodel_chatbot/`](../projects/02_multimodel_chatbot/)

**Run:**

```bash
python projects/02_multimodel_chatbot/app.py
```

**What you'll learn:**

- How to build an abstract provider interface so your application code is independent of any specific API
- How to manage and pass conversation history (`messages` list) across turns
- How token limits interact with long conversations (context window management)
- How to design a simple CLI REPL for interactive LLM applications

---

## Project 04 — Streaming Chat

**Displays response tokens as they arrive** rather than waiting for the full completion. Demonstrates the streaming API pattern and how to handle interruptions gracefully.

| Feature | Status |
|---------|--------|
| Token-by-token streaming output | ✅ Implemented |
| Graceful Ctrl+C interruption | ✅ Implemented |
| Gemini streaming | ✅ Implemented |
| OpenRouter streaming | ✅ Implemented |
| Ollama streaming | ✅ Implemented |
| Time-to-first-token measurement | ✅ Implemented |
| Tokens-per-second display | ✅ Implemented |

**Directory:** [`projects/04_streaming_chat/`](../projects/04_streaming_chat/)

**Run:**

```bash
python projects/04_streaming_chat/app.py
```

**What you'll learn:**

- How streaming APIs differ from standard completion APIs (generator vs. single response)
- Why streaming improves perceived latency for end users
- How to handle `KeyboardInterrupt` cleanly in a streaming loop (flush partial output, exit cleanly)
- How to measure time-to-first-token (TTFT) and throughput (tokens/sec)
- The tradeoffs between streaming and non-streaming for different use cases

---

## Project 09 — Chat with PDF

**A complete Retrieval-Augmented Generation (RAG) pipeline.** Upload any PDF, ask questions in natural language, and receive answers with citations pointing back to the source pages.

| Feature | Status |
|---------|--------|
| PDF text extraction (pypdf) | ✅ Implemented |
| Text chunking with boundary overlap | ✅ Implemented |
| Page number & filename provenance | ✅ Implemented |
| Lexical term-overlap retrieval | ✅ Implemented |
| Answer generation with citations | ✅ Implemented |
| Unsupported query rejection | ✅ Implemented |
| Bundled offline sample document | ✅ Implemented |
| Dense vector embeddings (ChromaDB / Ollama) | 📋 Planned (Module 14) |
| CLI `--pdf` argument | ✅ Implemented |

**Directory:** [`projects/09_chat_with_pdf/`](../projects/09_chat_with_pdf/)

**Current Implementation:**
- **Retrieval:** Lexical term-overlap scoring (stopword filtered) over in-memory chunk store.
- **Answer Generation:** Cloud LLM (Gemini) when configured; deterministic grounded excerpt fallback in offline mode.
- **Grounding & Provenance:** Chunks preserve source filename, page number, and chunk ID, formatted into `[Source: <filename>, Page <X>]`. Note: a citation assertion confirms metadata preservation, not full semantic validation.

**Run (offline demo with bundled sample):**

```bash
python projects/09_chat_with_pdf/app.py
```

**Run (with custom PDF):**

```bash
python projects/09_chat_with_pdf/app.py --pdf yourfile.pdf
```

**What you'll learn:**

- The complete RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- Why chunking strategy (size, overlap) matters for retrieval quality
- How vector similarity search works at an intuitive level
- How to attribute answers back to source documents (grounded generation)
- The difference between embedding models and generation models
- How to swap cloud and local components in the same pipeline

---

## Quick Reference

| # | Project | Key Concept | Cloud | Local |
|---|---------|-------------|-------|-------|
| 01 | Basic LLM Chat | API basics | Gemini / OpenRouter | Ollama |
| 02 | Multi-Provider Chatbot | Provider abstraction | Gemini / OpenRouter | Ollama |
| 04 | Streaming Chat | Streaming APIs | Gemini / OpenRouter | Ollama |
| 09 | Chat with PDF | RAG pipeline | Gemini | Ollama |

---

## Project Conventions

All projects follow the same structural conventions:

```
projects/NN_project_name/
├── app.py           # Main runnable entry point
├── README.md        # Project-specific documentation
├── requirements.txt # Additional dependencies (if any beyond root requirements.txt)
└── ...              # Supporting modules
```

Every `app.py`:
- Loads configuration from `.env` via `python-dotenv`
- Prints a clear error message if required environment variables are missing
- Has a `if __name__ == "__main__":` guard
- Includes a `--help` flag describing usage
