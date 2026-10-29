# Repository Audit — learn-llm

**Audit Date:** 2026-10-30  
**Repository:** https://github.com/JosiahSK/learn-llm  
**Commit audited:** `53ffba7` (Initial commit: LLM API calling notebook and scripts)

---

## 1. Original Repository Inventory

| File | Size | Description |
|---|---|---|
| `.gitignore` | 225 B | Covers `.env`, `venv/`, `__pycache__/` |
| `README.md` | 993 B | Minimal — no roadmap, truncated setup instructions |
| `requirements.txt` | 90 B | 6 unpinned packages |
| `main.py` | 289 B | Incomplete — invalid model ID, missing closing paren |
| `ai_agent/learn_llm.ipynb` | ~32 KB | Mixed API examples, several bugs |
| `ai_agent/streaming.ipynb` | ~320 B | **Completely empty** — single empty code cell |

---

## 2. Issues Found

### main.py

| Severity | Issue |
|---|---|
| 🔴 Bug | `model="gemini-3.6-flash"` — invalid model ID (does not exist as of 2026-10-30) |
| 🔴 Bug | `print(response.text` — missing closing parenthesis (syntax error) |
| 🟡 Missing | No error handling for missing API key |
| 🟡 Missing | No error handling for API errors (network, quota, auth) |
| 🟡 Missing | Runs an API call every time the script is executed with no guard |

### learn_llm.ipynb

| Severity | Issue |
|---|---|
| 🔴 Bug | `from langchain.agents import create_agent` — function does not exist in LangChain |
| 🔴 Bug | Uses `llm` variable (cells 54–57) but only `llm1` and `llm2` are defined |
| 🔴 Bug | `model="gemini-3.6-flash"` — invalid model ID |
| 🔴 Bug | `model="openrouter/free"` — not a valid model identifier |
| 🟡 Quality | No Markdown explanations — pure code cells with no context |
| 🟡 Quality | Cell execution order matters — cells 54+ depend on state from cell 1 |
| 🟡 Quality | Mixes two completely different SDKs (LangChain + Google GenAI) without separation |
| 🟡 Quality | Agent is displayed (visualized) before the tools and agent are properly set up |
| ⚪ Minor | Saved output includes verbose LangChain object representations |

### streaming.ipynb

| Severity | Issue |
|---|---|
| 🔴 Missing | **Completely empty** — no content at all |

### requirements.txt

| Severity | Issue |
|---|---|
| 🟡 Reliability | No version pins — `pip install` may select incompatible versions |
| 🟡 Missing | `langchain-google-genai` listed but `langchain-core`, `langgraph` missing |
| 🟡 Missing | No testing packages (`pytest`, `pytest-mock`) |
| 🟡 Missing | No document processing packages (`pypdf`) |
| 🟡 Missing | No vector search packages (`chromadb`) |
| ⚪ Minor | No Python version specification |

### .gitignore

| Severity | Issue |
|---|---|
| 🟡 Missing | `*.egg-info/`, `.pytest_cache/`, `.ipynb_checkpoints/` |
| 🟡 Missing | Model files (`*.gguf`, `*.safetensors`) |
| 🟡 Missing | Vector database dirs (`chroma_db/`, `faiss_index/`) |

### Security Scan

| Finding | Status |
|---|---|
| API keys in tracked files | **Not found** — keys loaded from environment |
| API keys in notebook outputs | **Not found** — outputs show `SecretStr('**********')` |
| `.env` file tracked | **Not found** — `.gitignore` correctly excludes it |
| `.env.example` with placeholders | **Missing** — added in this overhaul |

---

## 3. What Was Changed and Why

### Files Modified

| File | Change | Reason |
|---|---|---|
| `.gitignore` | Added patterns for `.ipynb_checkpoints/`, `*.gguf`, `chroma_db/`, `.pytest_cache/`, etc. | Prevent large/generated files from being committed |
| `requirements.txt` | Added version pins, grouped by purpose, added missing packages | Reproducible installation |
| `main.py` | Fixed model ID, fixed syntax error, added error handling and config validation | Script was broken and unsafe to run |
| `README.md` | Completely rewritten as a learning academy entry point | Original was 25 lines with no roadmap |

### Files Added

| File | Purpose |
|---|---|
| `.env.example` | Safe template for environment configuration |
| `pyproject.toml` | Standard project metadata and tool configuration |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CHANGELOG.md` | Change history |
| `docs/REPOSITORY_AUDIT.md` | This file |
| `docs/LEARNING_ROADMAP.md` | Full course progression |
| `docs/SETUP.md` | Detailed installation guide |
| `docs/PROVIDER_SETUP.md` | Provider-specific setup with verified info |
| `docs/GLOSSARY.md` | Key terms and concepts |
| `docs/TROUBLESHOOTING.md` | Common problems and solutions |
| `docs/SECURITY.md` | Security practices |
| `docs/PROJECT_CATALOG.md` | All projects with run instructions |
| `src/learn_llm/` | Shared library: config, provider wrappers, utilities |
| `tests/` | Automated test suite (runs without API keys) |
| `00_foundations/` | Module 00: AI/ML/LLM concepts |
| `02_llm_fundamentals/` | Module 02: Transformer architecture |
| `03_model_apis/` | Module 03: Direct API calls |
| `04_prompt_engineering/` | Module 04: Prompting techniques |
| `05_messages_and_chat_history/` | Module 05: Stateful chatbot |
| `06_streaming_and_batch/` | Module 06: Streaming (replaces empty notebook) |
| `07_langchain_fundamentals/` | Module 07: LangChain |
| `10_agents/` | Module 10: Agents (fixes original notebook) |
| `11_tokens_and_tokenization/` | Module 11: Tokenization |
| `12_embeddings_and_vector_search/` | Module 12: Embeddings |
| `13_rag_fundamentals/` | Module 13: RAG pipeline |
| `projects/01_basic_llm_chat/` | Project 1: First LLM request |
| `projects/02_multimodel_chatbot/` | Project 2: Multi-provider chatbot |
| `projects/04_streaming_chat/` | Project 4: Streaming chatbot |
| `projects/09_chat_with_pdf/` | Project 9: Chat with PDF + citations |

### Original Notebooks Preserved and Improved

- `ai_agent/learn_llm.ipynb` — Bugs fixed, markdown explanations added, separated into logical sections
- `ai_agent/streaming.ipynb` — Implemented from scratch (was completely empty)

---

## 4. Provider Verification (2026-10-30)

### Google Gemini
- **SDK:** `google-genai` (unified SDK — replaces legacy `google-generativeai`)
- **Default Stable Model:** `gemini-3.8-flash` (newest stable Flash model, configurable via `GEMINI_MODEL`)
- **Previous-Gen Model:** `gemini-3.6-flash` (retained for backward compatibility)
- **Account Tiers & Free Access:** Available via Google AI Studio with free-tier rate limits (RPM/TPM). Official documentation warns that free-tier quotas and eligible models vary by region/account and can change.
- **API key:** https://aistudio.google.com/apikey
- **Pricing & Quotas:** https://ai.google.dev/pricing
- **Rate Limits Guide:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Model list:** https://ai.google.dev/gemini-api/docs/models

### OpenRouter
- **API:** OpenAI-compatible at `https://openrouter.ai/api/v1`
- **Free models:** Multiple `:free` models available. List changes frequently.
- **Invalid model used in original:** `openrouter/free` (not a valid ID)
- **Example free model:** `google/gemma-4-31b-it:free` (verified 2026-10-30)
- **Source:** https://openrouter.ai/models?q=:free

### Ollama
- **Type:** Local inference — no API key, no cloud charges
- **Install:** https://ollama.com/
- **Embedding model:** `nomic-embed-text` (pull separately)

---

## 5. Test Status (2026-10-30)

| Test | Status | Notes |
|---|---|---|
| `tests/test_config.py` | ✅ Runnable | No API keys needed |
| `tests/test_utils.py` | ✅ Runnable | No API keys needed |
| `tests/test_providers.py` | ✅ Runnable | Mocked — no real API calls |
| Provider integration tests | ⚠️ Skipped | Require real keys — marked `@pytest.mark.requires_api` |
| Notebook execution | ⚠️ Not automated | Notebooks require Jupyter + API keys |

To run the test suite:
```bash
pip install pytest pytest-asyncio pytest-mock
pytest tests/ -v
```

---

## 6. Remaining Work (Future Milestones)

| Priority | Item |
|---|---|
| High | Modules 08, 09 (structured outputs, function calling) |
| High | Projects 05, 06, 07 (tool calling, token explorer, embedding explorer) |
| High | Projects 10, 11, 12, 13 (RAG with citations, evaluation, local) |
| Medium | Modules 14–16 (advanced RAG) |
| Medium | Module 17 (local models) |
| Medium | Module 18 (LangGraph) |
| Medium | Module 19 (multimodal) |
| Low | Modules 20–21 (deployment, security) |
| Low | GitHub Actions CI workflow |

---

*This audit document should be updated whenever significant changes are made to the repository.*
