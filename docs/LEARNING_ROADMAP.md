# 🗺️ Learning Roadmap

A structured guide through all 22 modules of the **learn-llm** course, from absolute beginner to advanced LLM practitioner.

---

## Course Overview

This course is designed as a **progressive, hands-on journey** through modern large language model development. Each module builds on the previous ones, introducing new concepts through runnable Jupyter notebooks with real API calls.

The course is divided into three broad phases:

| Phase | Modules | Focus |
|-------|---------|-------|
| **Foundations** | 00–06 | Environment setup, core APIs, prompt engineering, basic chains |
| **Intermediate** | 07–13 | Agents, RAG, embeddings, memory, structured output |
| **Advanced** | 14–21 | LangGraph, fine-tuning, production patterns, multimodal, evals |

You do **not** need to complete every module. Use the [learning paths](#learning-paths) below to find the right route for your goals.

---

## Module Table

| # | Module Name | Key Topics | Est. Time | Status in Academy |
|---|-------------|------------|-----------|-------------------|
| 00 | **Foundations** | AI vs ML vs DL, LLMs, training vs inference, hallucinations | 2 h | ✅ Available (`00_foundations/`) |
| 01 | **Python & Dev Environment** | Virtual environments, packages, HTTP, environment variables | 2 h | ✅ Available (`docs/SETUP.md`) |
| 02 | **LLM Fundamentals** | Transformers, attention, temperature, context windows | 3 h | ✅ Available (`02_llm_fundamentals/`) |
| 03 | **Model APIs** | Direct API calls, auth, error handling, Gemini & OpenRouter | 3 h | ✅ Available (`03_model_apis/`) |
| 04 | **Prompt Engineering** | Few-shot, constraints, prompt injection defense | 3 h | ✅ Available (`04_prompt_engineering/`) |
| 05 | **Messages & Chat History** | Message roles, stateful chatbot, context limits | 2 h | ✅ Available (`05_messages_and_chat_history/`) |
| 06 | **Streaming & Batch** | First-token latency, SSE, chunk handling, recovery | 3 h | ✅ Available (`06_streaming_and_batch/`) |
| 07 | **LangChain Fundamentals** | Chat models, prompt templates, runnables, LCEL | 4 h | ✅ Available (`07_langchain_fundamentals/`) |
| 08 | **Structured Outputs** | JSON mode, schemas, Pydantic validation | 3 h | 📋 Planned |
| 09 | **Function Calling & Tools** | JSON tool schemas, dispatching tools safely | 4 h | 📋 Planned |
| 10 | **Agents** | ReAct pattern, tool loops, stop conditions, bounds | 5 h | ✅ Available (`10_agents/`) |
| 11 | **Tokens & Tokenization** | Subwords, token IDs, vocabulary, cost calculation | 3 h | ✅ Available (`11_tokens_and_tokenization/`) |
| 12 | **Embeddings & Vector Search** | Vector space, cosine similarity, semantic search | 3 h | ✅ Available (`12_embeddings_and_vector_search/`) |
| 13 | **RAG Fundamentals** | Chunking, indexing, retrieval, prompt assembly | 4 h | ✅ Available (`13_rag_fundamentals/`) |
| 14 | **RAG Applications** | Multi-document Q&A, metadata filtering, citations | 5 h | 📋 Planned (Implemented in Project 09) |
| 15 | **RAG Evaluation** | Retrieval metrics, precision/recall, grounding checks | 5 h | 📋 Planned |
| 16 | **Advanced RAG** | Hybrid search, reranking, query rewriting | 5 h | 📋 Planned |
| 17 | **Local LLMs & Ollama** | Offline inference, GGUF, local embeddings | 4 h | 📋 Planned (Covered in Provider Setup & Projects) |
| 18 | **LangGraph & Workflows** | State graphs, cycles, conditional branches | 6 h | 📋 Planned |
| 19 | **Multimodal LLMs** | Vision, image inputs, document parsing | 5 h | 📋 Planned |
| 20 | **Deployment & Observability** | Telemetry, logging without leaks, latency metrics | 5 h | 📋 Planned |
| 21 | **Security & Responsible AI** | Prompt injection, output validation, abuse prevention | 4 h | ✅ Available (`docs/SECURITY.md`) |

---

## Learning Paths

### 🟢 Beginner Path — "I'm New to LLMs"

**Goal:** Get comfortable making API calls, writing effective prompts, and producing structured outputs.

**Total estimated time: 17–27 hours**

```
Module 00 → 02 → 03 → 04 → 05 → 06
```

| Step | Module | Time |
|------|--------|------|
| 1 | 00 — Environment Setup | 2 h |
| 2 | 02 — First API Call | 2 h |
| 3 | 03 — Prompt Engineering I | 3 h |
| 4 | 04 — Prompt Engineering II | 3 h |
| 5 | 05 — Chat & Conversation | 2 h |
| 6 | 06 — Structured Output | 3 h |

**Project to build after this path:** A command-line chatbot with a system prompt that answers questions about a topic of your choice and returns structured JSON summaries.

---

### 🟡 Intermediate Path — "I Can Make API Calls, Now What?"

**Goal:** Build retrieval-augmented generation (RAG) systems, use tool calling, and chain LLM calls together.

**Builds on beginner path. Additional estimated time: 24–37 hours**

```
(Beginner path) → 07 → 08 → 09 → 10 → 11 → 12 → 13
```

| Step | Module | Time |
|------|--------|------|
| 7 | 07 — Tool Calling | 4 h |
| 8 | 08 — Embeddings | 3 h |
| 9 | 09 — Vector Stores | 3 h |
| 10 | 10 — RAG I | 4 h |
| 11 | 11 — RAG II | 5 h |
| 12 | 12 — Memory & State | 4 h |
| 13 | 13 — LangChain Chains | 4 h |

**Project to build after this path:** A document Q&A system that accepts PDF uploads, chunks them into a vector store, and answers questions using RAG with conversation memory.

---

### 🔴 Advanced Path — "I Want to Build Production-Grade LLM Apps"

**Goal:** Build multi-agent systems with LangGraph, evaluate RAG quality, explore fine-tuning, and deploy.

**Builds on intermediate path. Additional estimated time: 30–45 hours**

```
(Intermediate path) → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21
```

| Step | Module | Time |
|------|--------|------|
| 14 | 14 — Agents with LangChain | 5 h |
| 15 | 15 — LangGraph I | 5 h |
| 16 | 16 — LangGraph II | 6 h |
| 17 | 17 — Multimodal LLMs | 5 h |
| 18 | 18 — Evaluation & Evals | 6 h |
| 19 | 19 — Fine-Tuning Concepts | 8 h |
| 20 | 20 — Production Patterns | 6 h |
| 21 | 21 — Capstone Project | 8 h |

**Project to build after this path:** The capstone (Module 21) — a fully evaluated, multi-agent RAG system with a web interface, production-grade error handling, and an automated evaluation suite.

---

## Time Estimates

| Difficulty Level | Per-Module Range | What's Included |
|-----------------|-----------------|-----------------|
| **Beginner** (00–06) | 2–4 hours | Reading, running notebooks, exercises |
| **Intermediate** (07–13) | 3–5 hours | Concepts + building mini-projects |
| **Advanced** (14–21) | 4–8 hours | Complex systems, debugging, evaluation |

> These are estimates for learners who are comfortable with Python. Add ~50% more time if you are newer to Python or software development.

---

## Offline / Free Options

Many modules can be completed **without spending any money** by using free-tier providers or running models locally.

| Module Range | Free Option Available | Notes |
|---|---|---|
| All modules | ✅ Google Gemini free tier | `gemini-3.8-flash` is free with rate limits. See [PROVIDER_SETUP.md](PROVIDER_SETUP.md) |
| All modules | ✅ OpenRouter free models | Models with `:free` suffix; list changes. See [PROVIDER_SETUP.md](PROVIDER_SETUP.md) |
| 01, 02, 05–15 | ✅ Ollama (fully offline) | Run Llama 3.2, Qwen, etc. locally. Needs 8 GB+ RAM for 7B models |
| 08–11 | ✅ Ollama embedding models | `nomic-embed-text`, `mxbai-embed-large` — no API key needed |
| 17 (Multimodal) | ⚠️ Limited offline support | Gemini free tier supports images; local multimodal models need significant VRAM |
| 19 (Fine-Tuning) | ⚠️ Needs GPU or Colab | Google Colab free tier has limited GPU. Unsloth + LoRA reduces requirements |

---

## What to Build After Each Module

| Module | Recommended Mini-Project |
|--------|--------------------------|
| 00 | Verify your setup: run a "Hello LLM" script against each provider |
| 01 | Write a provider comparison script that calls the same prompt on Gemini, OpenRouter, and Ollama |
| 02 | Build a streaming CLI tool that displays tokens as they arrive |
| 03 | Prompt comparison notebook: test 5 different prompt styles on the same task |
| 04 | Chain-of-thought math solver with self-consistency voting |
| 05 | Multi-turn customer support chatbot with a persistent chat history |
| 06 | Receipt parser: extract line items from a receipt description as structured JSON |
| 07 | Weather + calculator agent that picks the right tool based on user query |
| 08 | Semantic search over a list of 100 documents; show top-5 results |
| 09 | Build a local ChromaDB index from a folder of `.txt` files |
| 10 | PDF Q&A: load a PDF, chunk it, index it, answer questions |
| 11 | Compare BM25 vs. embedding-based retrieval on the same corpus |
| 12 | Chatbot with summarization memory that never forgets the user's name |
| 13 | LCEL pipeline: translate → summarize → extract keywords in one chain |
| 14 | Research agent that searches the web (via tool) and writes a report |
| 15 | Two-node LangGraph flow: classify a query, then route to the right handler |
| 16 | Supervisor + 2 worker agents that collaborate to answer complex questions |
| 17 | Image captioning pipeline that generates alt text for uploaded images |
| 18 | RAG eval suite using RAGAS: faithfulness, answer relevance, context recall |
| 19 | Fine-tune a 1B model on a custom Q&A dataset using LoRA |
| 20 | Add caching, exponential-backoff retries, and structured logging to Module 14 |
| 21 | Full capstone: end-to-end multi-agent RAG app with evaluation dashboard |

---

## Related Documentation

- [PROVIDER_SETUP.md](PROVIDER_SETUP.md) — How to configure Gemini, OpenRouter, and Ollama
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common errors and fixes
- [GLOSSARY.md](GLOSSARY.md) — Definitions for all key terms used in the course
- [../README.md](../README.md) — Repository overview and quick start

---

*Last updated: 2026-10-30*
