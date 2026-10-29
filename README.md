# 🎓 LLM Learning Academy — Foundational Milestone

A practical, hands-on learning resource for **Large Language Models, Generative AI, and real-world AI applications** — covering foundational concepts, provider APIs, streaming, agents, tokenization, embeddings, and document retrieval.

> **Status:** Foundational learning academy milestone. Core modules (00–07, 10–13) and reference projects are implemented and tested; advanced specialization modules (08–09, 14–20) are documented in the [Learning Roadmap](./docs/LEARNING_ROADMAP.md).

---

## Who This Is For

| Audience | What You'll Get |
|---|---|
| **Students** | A clear path from AI basics to production-ready RAG applications |
| **Developers** | Working implementations of LangChain, agents, embeddings, streaming, and RAG |
| **Trainers / Workshop leads** | Self-contained lessons with exercises and expected outputs |
| **Long-term reference** | Verified provider docs, architecture diagrams, a complete glossary |

---

## Prerequisites

- Python 3.11 or newer
- Basic Python knowledge (functions, variables, lists, dicts, exceptions)
- A free API key from [Google AI Studio](https://aistudio.google.com/apikey) **or** [Ollama](https://ollama.com/) installed for local use

No prior AI experience required for Module 00–03.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/JosiahSK/learn-llm.git
cd learn-llm

# 2. Create a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your environment
copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux
# Open .env and add your API key

# 5. Run your first LLM request
python main.py
```

---

## Free API Access

You can learn everything in this course **for free**:

| Provider | Setup | Free Access Details |
|---|---|---|
| **Google Gemini** | [Get key →](https://aistudio.google.com/apikey) | Free tier with generous quota. No credit card for free tier. Verify at [ai.google.dev/pricing](https://ai.google.dev/pricing) |
| **OpenRouter** | [Get key →](https://openrouter.ai/keys) | Many models marked `:free`. Availability changes — check [openrouter.ai/models?q=:free](https://openrouter.ai/models?q=:free) |
| **Ollama** | [Install →](https://ollama.com/) | Local inference, no API key, no cloud charges. Requires sufficient RAM |

> ⚠️ Free tier limits and model availability can change. Always check the provider's current pricing page rather than relying solely on this README.

---

## Learning Roadmap

```
BEGINNER ──────────────────────────────────────────────────────── ADVANCED
   │                                                                    │
   ▼                                                                    ▼
Module 00    Module 02    Module 03    Module 04    Module 05    Module 06
Foundations  LLM Basics   Model APIs   Prompting    Messages     Streaming
   │              │            │            │            │            │
   └──────────────┴────────────┴────────────┴────────────┴────────────┘
                                    │
                             Module 07: LangChain
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
         Module 10            Module 11–13           Module 17
          Agents             Embeddings/RAG        Local Models
              │                     │                     │
              └─────────────────────┴─────────────────────┘
                                    │
                            Module 18: LangGraph
```

---

## Module Navigation

| # | Module | Topics | Status |
|---|---|---|---|
| [00](./00_foundations/) | **Foundations** | AI vs ML vs DL, LLMs, training vs inference, hallucinations | ✅ Available |
| [01](./docs/SETUP.md) | **Python Environment** | Virtual environments, packages, HTTP, environment variables | ✅ Available |
| [02](./02_llm_fundamentals/) | **LLM Fundamentals** | Transformers, attention, temperature, context windows | ✅ Available |
| [03](./03_model_apis/) | **Model APIs** | Direct API calls, auth, error handling, Gemini & OpenRouter | ✅ Available |
| [04](./04_prompt_engineering/) | **Prompt Engineering** | Few-shot, constraints, structured output, injection | ✅ Available |
| [05](./05_messages_and_chat_history/) | **Messages & Chat History** | Message roles, stateful chatbot, context limits | ✅ Available |
| [06](./06_streaming_and_batch/) | **Streaming & Batch** | First-token latency, chunk handling, error recovery | ✅ Available |
| [07](./07_langchain_fundamentals/) | **LangChain** | Chat models, prompt templates, runnables, output parsers | ✅ Available |
| [10](./10_agents/) | **Agents** | Tool calling, multi-step execution, stop conditions | ✅ Available |
| [11](./11_tokens_and_tokenization/) | **Tokens & Tokenization** | Token IDs, cost estimation, tokenizer differences | ✅ Available |
| [12](./12_embeddings_and_vector_search/) | **Embeddings** | Vector representations, cosine similarity, semantic search | ✅ Available |
| [13](./13_rag_fundamentals/) | **RAG Fundamentals** | Document loading, chunking, indexing, retrieval, generation | ✅ Available |

> Modules 08, 09, 14–21 are planned — see [docs/LEARNING_ROADMAP.md](./docs/LEARNING_ROADMAP.md)

---

## Projects

| # | Project | Description | API Required | Local |
|---|---|---|---|---|
| [01](./projects/01_basic_llm_chat/) | **Basic LLM Chat** | Single request, key validation, error handling | Gemini or OpenRouter | Ollama |
| [02](./projects/02_multimodel_chatbot/) | **Multi-Provider Chatbot** | Same UI, switch between providers | Gemini or OpenRouter | Ollama |
| [04](./projects/04_streaming_chat/) | **Streaming Chat** | Display chunks as they arrive | Gemini or OpenRouter | Ollama |
| [09](./projects/09_chat_with_pdf/) | **Chat with PDF** | Upload → chunk → embed → retrieve → answer with citations | Gemini or OpenRouter | Ollama |

---

## Original Notebooks

The original notebooks from the initial commit are preserved and improved in:
- [`ai_agent/learn_llm.ipynb`](./ai_agent/learn_llm.ipynb) — API calls, LangChain basics, simple agent *(fixed and annotated)*
- [`ai_agent/streaming.ipynb`](./ai_agent/streaming.ipynb) — Streaming responses *(fully implemented)*

---

## Installation Details

```bash
# Core install (covers Modules 00–10)
pip install -r requirements.txt

# To run tests
pip install pytest pytest-asyncio pytest-mock
pytest tests/

# For Ollama (local models)
# 1. Install Ollama: https://ollama.com/
# 2. Pull a model:
ollama pull llama3.2         # ~2 GB, good for testing
ollama pull nomic-embed-text # ~274 MB, for embeddings
```

---

## Repository Structure

```
learn-llm/
├── README.md              ← You are here
├── main.py                ← Beginner entry point: first LLM request
├── requirements.txt       ← Dependencies (pinned)
├── pyproject.toml         ← Project metadata
├── .env.example           ← Safe config template (copy to .env)
│
├── docs/                  ← Guides and reference
│   ├── REPOSITORY_AUDIT.md
│   ├── LEARNING_ROADMAP.md
│   ├── SETUP.md
│   ├── PROVIDER_SETUP.md
│   ├── GLOSSARY.md
│   ├── TROUBLESHOOTING.md
│   └── SECURITY.md
│
├── 00_foundations/        ← What is AI, ML, LLMs?
├── 02_llm_fundamentals/   ← Transformers, temperature, context
├── 03_model_apis/         ← Direct API calls (Gemini, OpenRouter)
├── 04_prompt_engineering/ ← Prompting techniques
├── 05_messages_and_chat_history/ ← Stateful chatbot
├── 06_streaming_and_batch/       ← Streaming responses
├── 07_langchain_fundamentals/    ← LangChain patterns
├── 10_agents/             ← Tool calling, agents
├── 11_tokens_and_tokenization/   ← Tokenizers, cost
├── 12_embeddings_and_vector_search/ ← Embeddings, similarity
├── 13_rag_fundamentals/   ← Complete RAG pipeline
│
├── projects/              ← End-to-end projects
│   ├── 01_basic_llm_chat/
│   ├── 02_multimodel_chatbot/
│   ├── 04_streaming_chat/
│   └── 09_chat_with_pdf/
│
├── src/learn_llm/         ← Shared library (config, providers, utils)
├── tests/                 ← Automated tests
├── data/sample_documents/ ← Sample data for RAG lessons
└── ai_agent/              ← Original notebooks (improved)
```

---

## Testing

```bash
# Run all tests (no API keys needed)
pytest tests/ -v

# Run only fast unit tests
pytest tests/ -v -m "not requires_api and not slow"

# Run a specific test file
pytest tests/test_utils.py -v
```

---

## Security

- **Never** commit your `.env` file — it is in `.gitignore`
- **Never** put API keys directly in notebooks or Python files
- See [docs/SECURITY.md](./docs/SECURITY.md) for a full security guide
- If you accidentally commit a key, rotate it immediately at the provider's dashboard

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `GEMINI_API_KEY not set` | Copy `.env.example` to `.env` and add your key |
| `Model not found / 404` | Check the model ID — they change. See [docs/PROVIDER_SETUP.md](./docs/PROVIDER_SETUP.md) |
| `Quota exceeded / 429` | Wait and retry, or switch to Ollama for local testing |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Ollama connection refused | Start Ollama, then `ollama pull <model>` |

Full guide: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add lessons, fix bugs, or improve documentation.

---

## References

- [Google Gemini API docs](https://ai.google.dev/gemini-api/docs)
- [google-genai SDK](https://github.com/googleapis/python-genai)
- [LangChain documentation](https://python.langchain.com/docs/)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [OpenRouter documentation](https://openrouter.ai/docs)
- [Ollama documentation](https://ollama.com/docs)
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
