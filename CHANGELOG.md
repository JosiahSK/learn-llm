# Changelog

All notable changes to the `learn-llm` repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-30

### Added
- **Repository Architecture & Documentation Suite:**
  - `docs/REPOSITORY_AUDIT.md`: In-depth audit of legacy codebase, security review, and migration map.
  - `docs/LEARNING_ROADMAP.md`: Pedagogical pathway spanning 22 modules with time estimates and learning paths.
  - `docs/SETUP.md`: OS-agnostic setup instructions, venv configuration, and verification steps.
  - `docs/PROVIDER_SETUP.md`: Verified free-tier guides for Google Gemini, OpenRouter (`:free`), and local Ollama.
  - `docs/GLOSSARY.md`: 40+ formal definitions and intuitive analogies for LLM engineering concepts.
  - `docs/TROUBLESHOOTING.md`: Exhaustive error resolution matrix covering network, quota, auth, and environment issues.
  - `docs/SECURITY.md`: Production LLM security rules, prompt injection defense, credential isolation, and tool safety.
  - `docs/PROJECT_CATALOG.md`: Index of hands-on capstone and milestone projects.
  - `CONTRIBUTING.md`: Contributing standards, test expectations, and PR guidelines.
- **Unified Core Package (`src/learn_llm`):**
  - `config.py`: Centralized environment loading and strict provider validation.
  - `providers/`: Abstract base class and concrete implementations for `GeminiProvider`, `OpenRouterProvider`, and `OllamaProvider`.
  - `utils/`: Reusable, deterministic text chunkers, word counters, text truncators, and terminal streaming displays.
- **Comprehensive Module Curricula:**
  - `00_foundations/`: Core conceptual taxonomy (AI, ML, DL, NLP, GenAI, hallucinations, and system boundaries).
  - `02_llm_fundamentals/`: Intuitive transformer breakdown, attention, temperature, and context windows.
  - `03_model_apis/`: Direct API calls across Gemini, OpenRouter, and local endpoints with complete error handling.
  - `04_prompt_engineering/`: Few-shot prompting, prompt decomposition, output schemas, and prompt injection defense.
  - `05_messages_and_chat_history/`: Message roles, conversational memory, sliding context windows, and stateful bots.
  - `06_streaming_and_batch/`: First-token latency (TTFT), SSE mechanics, batching, and stream error recovery.
  - `07_langchain_fundamentals/`: LCEL runnables, prompt templates, output parsers, and architectural trade-offs.
  - `10_agents/`: ReAct agent loops, safe tool dispatching, stop criteria, and execution boundaries.
  - `11_tokens_and_tokenization/`: Subword tokenization, vocabulary indexing, and cost/context calculation.
  - `12_embeddings_and_vector_search/`: Vector geometry, cosine similarity, dimensional indexing, and semantic search.
  - `13_rag_fundamentals/`: End-to-end RAG architecture, chunking, retrieval, prompt assembly, and citation synthesis.
- **Hands-On Real-World Projects:**
  - `projects/01_basic_llm_chat/`: Production-ready single-request client with resilient error handling.
  - `projects/02_multimodel_chatbot/`: Interactive CLI chatbot with dynamic runtime provider switching.
  - `projects/04_streaming_chat/`: Interactive streaming client with real-time TTFT and total latency benchmarks.
  - `projects/09_chat_with_pdf/`: Complete RAG pipeline supporting PDF ingestion, page metadata tracking, similarity retrieval, and rigorous source attribution.
  - `data/sample_documents/`: Included test corpus (`llm_basics.txt`) for offline and reproducible RAG verification.
- **Automated Testing Suite (`tests/`):**
  - 36 isolated, offline-safe unit tests covering configuration, provider clients, utility functions, chunking, and PDF RAG with zero network dependencies.

### Fixed
- **`main.py`:**
  - Repaired syntax error: missing closing parenthesis on `print(response.text)`.
  - Replaced legacy/deprecated model ID with verified stable `gemini-3.8-flash`.
  - Added strict credential validation and user-friendly error diagnostics for missing keys, 401s, 429s, and 404s.
- **`ai_agent/learn_llm.ipynb`:**
  - Replaced non-existent `langchain.agents.create_agent` with modern, verified `langgraph.prebuilt.create_react_agent`.
  - Resolved undefined `llm` references; unified model initialization across OpenRouter and Gemini.
  - Replaced invalid `openrouter/free` and `gemini-3.8-flash` IDs with verified models.
  - Added markdown documentation before code blocks and isolated cell execution flows.
- **`ai_agent/streaming.ipynb`:**
  - Completely implemented previously empty notebook with local mock streaming, live Gemini streaming, LangChain streaming, and performance measurement.
- **`requirements.txt` & `.gitignore`:**
  - Pinned core dependency groups; added security safeguards for vector databases, model caches, and local environments.
