# 🔧 Provider Setup Guide

Configure your LLM providers for the learn-llm course. This guide covers **Google Gemini**, **OpenRouter**, and **Ollama** (local).

> [!TIP]
> You only need **one provider** to get started. Gemini's free tier is the easiest starting point for most learners.

---

## Table of Contents

- [Google Gemini](#google-gemini)
- [OpenRouter](#openrouter)
- [Ollama (Local)](#ollama-local)
- [Provider Comparison Table](#provider-comparison-table)

---

## Google Gemini

**Best for:** Getting started quickly with a free API key and access to state-of-the-art models.

### Step 1 — Get a Free API Key

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API key"**
4. Select an existing Google Cloud project, or click **"Create API key in new project"**
5. Copy the key — it starts with `AIza...`
6. Store it safely; you won't be able to view it again in full

> [!CAUTION]
> Never commit your API key to Git. Always load it from an environment variable or a `.env` file that is listed in `.gitignore`.

### Step 2 — Set the Environment Variable

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "AIza..."
# Or to persist across sessions:
[System.Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "AIza...", "User")
```

**macOS / Linux:**
```bash
export GOOGLE_API_KEY="AIza..."
# Add to ~/.bashrc or ~/.zshrc to persist
```

**`.env` file (recommended for notebooks):**
```
GOOGLE_API_KEY=AIza...
```
Then load with:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

### Rate Limits & Tier Details

Rate limits and free allowances in the Gemini API are **dynamic** and **model-specific**. They are not universal fixed numbers; instead, they depend on:
1. **The Model:** Different models (e.g., Flash vs Pro vs Flash-Lite) have distinct throughput caps.
2. **Account & Project Tier:** Google AI Studio provides free-of-charge allowances for experimentation, while Google Cloud projects with pay-as-you-go billing have separate, higher rate tiers.
3. **Regional Availability:** Specific models or free allowances may vary depending on account geography and organizational policy.

> [!IMPORTANT]
> Because Google updates rate limits and model allocations dynamically, **do not rely on hardcoded RPM (requests per minute), TPM (tokens per minute), or RPD (requests per day) assumptions**.
> Consult the official, up-to-date documentation:
> - **Models Overview:** [https://ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
> - **Pricing & Usage Tiers:** [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
> - **Rate Limits Guide:** [https://ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)

### How to Check Your Actual Rate Limits & Usage

- **Google AI Studio Dashboard:** Visit [https://aistudio.google.com](https://aistudio.google.com) → click the **API keys / Usage** view to inspect your active quotas.
- **Google Cloud Console:** If using a linked GCP project, check **APIs & Services → Quotas & System Limits** for exact per-minute and per-day ceilings.

---

### The `google-genai` SDK

The course uses the **new `google-genai` SDK** (package name: `google-genai`), which replaces the older `google-generativeai` package.

```bash
pip install google-genai
```

> [!WARNING]
> Do **not** use `google-generativeai` for new code — it is deprecated. The new SDK has a different API surface. See [Module 02](../02-first-api-call/) for a full migration guide.

### Code Example

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain what a transformer model is in 2 sentences.",
)

print(response.text)
```

**Streaming example:**
```python
for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Tell me a short story about a robot.",
):
    print(chunk.text, end="", flush=True)
```

---

### Common Errors & Fixes

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `google.auth.exceptions.DefaultCredentialsError` | API key not set | Set `GOOGLE_API_KEY` env variable |
| `400 API key not valid` | Wrong or truncated key | Re-copy the key from AI Studio |
| `403 PERMISSION_DENIED` | Key doesn't have Gemini API enabled | Enable "Generative Language API" in Google Cloud Console |
| `429 RESOURCE_EXHAUSTED` | Hit rate limit | Wait 60 seconds; add `time.sleep()` between calls |
| `404 models/... not found` | Wrong model ID | Use `gemini-3.8-flash`, not `gemini-pro` or old IDs |
| `ModuleNotFoundError: google.genai` | Wrong package installed | `pip install google-genai` (not `google-generativeai`) |

**Links:**
- Pricing & free tier: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
- API key management: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- SDK documentation: [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)

---

## OpenRouter

**Best for:** Accessing many different models (including GPT-4, Claude, Llama) through one API with free options.

### Step 1 — Get an API Key

1. Go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign in or create a free account
3. Click **"Create Key"** and give it a name
4. Copy the key — it starts with `sk-or-...`
5. Optionally set a credit limit on the key for cost control

### Step 2 — Set the Environment Variable

```bash
# .env file
OPENROUTER_API_KEY=sk-or-...
```

```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ["OPENROUTER_API_KEY"]
```

---

### Free Models

OpenRouter offers models with a `:free` suffix that cost $0 per token. **The list of free models changes frequently** — models may be added, removed, or converted to paid at any time.

**To see the current list of free models:**
→ [https://openrouter.ai/models?q=:free](https://openrouter.ai/models?q=:free)

Some historically available free models (verify current availability at the link above):

| Model ID | Notes |
|----------|-------|
| `meta-llama/llama-3.2-3b-instruct:free` | Small, fast Llama model |
| `meta-llama/llama-3.1-8b-instruct:free` | Good general-purpose model |
| `google/gemma-2-9b-it:free` | Google's Gemma 2 instruction-tuned |
| `microsoft/phi-3-mini-128k-instruct:free` | Compact model with large context |
| `mistralai/mistral-7b-instruct:free` | Reliable general-purpose model |
| `qwen/qwen-2-7b-instruct:free` | Strong multilingual model |

> [!WARNING]
> Free models on OpenRouter may be **rate-limited more aggressively**, have lower priority during peak times, or be removed entirely. Do not rely on a specific free model for production use. Always have a fallback.

### Rate Limits on Free Models

- Free models typically allow **~20 requests per minute**
- Daily limits vary by model
- No cost, but OpenRouter may require account verification (email) to access free models
- Adding a small credit balance ($5+) often unlocks higher rate limits even on free models

---

### OpenAI-Compatible Endpoint

OpenRouter is **fully compatible with the OpenAI SDK**. Just change the `base_url`:

```bash
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.2-3b-instruct:free",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is retrieval-augmented generation?"},
    ],
)

print(response.choices[0].message.content)
```

**With optional headers (recommended for OpenRouter):**
```python
client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/your-repo",  # Optional
        "X-Title": "learn-llm course",                    # Optional
    },
)
```

### Common Errors & Fixes

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `401 Unauthorized` | Wrong API key | Confirm key starts with `sk-or-` |
| `402 Payment Required` | Model is not free; no credits | Switch to a `:free` model or add credits |
| `429 Too Many Requests` | Rate limit hit | Add `time.sleep(3)` between calls |
| `404 No endpoints found for model` | Model ID wrong or removed | Check [openrouter.ai/models](https://openrouter.ai/models) for current IDs |
| `Model is not free` | Free model removed | Browse to find current free alternatives |

**Links:**
- Documentation: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- API key management: [https://openrouter.ai/keys](https://openrouter.ai/keys)
- Current free models: [https://openrouter.ai/models?q=:free](https://openrouter.ai/models?q=:free)

---

## Ollama (Local)

**Best for:** Fully offline use, privacy-sensitive data, no API costs, and learning about local model inference.

> [!NOTE]
> Ollama runs models entirely on your machine. **No data is sent to any external server.** This makes it ideal for working with private documents.

### Installation

**Windows:**
1. Download the installer from [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. Run the `.exe` installer
3. Ollama starts automatically as a background service

**macOS:**
```bash
# Option 1: Download from https://ollama.com/download/mac
# Option 2: Homebrew
brew install ollama
ollama serve  # Start the server
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
# The service starts automatically via systemd
```

---

### Pull a Model

```bash
ollama pull llama3.2          # 2B parameter model (~1.3 GB)
ollama pull llama3.2:3b       # 3B parameter model (~2 GB)
ollama pull llama3.1:8b       # 8B parameter model (~4.7 GB)
ollama pull qwen2.5:7b        # Qwen 2.5 7B (~4.4 GB)
ollama pull mistral:7b        # Mistral 7B (~4.1 GB)
```

---

### RAM Requirements

| Model Size | Minimum RAM | Recommended RAM | Example Models |
|------------|-------------|-----------------|----------------|
| 1B | 4 GB | 6 GB | `llama3.2:1b` |
| 3B | 6 GB | 8 GB | `llama3.2:3b`, `phi3:mini` |
| 7B | 8 GB | 12 GB | `llama3.1:8b`, `mistral:7b`, `qwen2.5:7b` |
| 13B | 16 GB | 24 GB | `llama2:13b` |
| 70B | 48 GB | 64 GB | `llama3.1:70b` (needs GPU or very high RAM) |

> [!TIP]
> If you have a GPU, Ollama will automatically use it for much faster inference. NVIDIA GPUs with CUDA, AMD GPUs with ROCm, and Apple Silicon (M1/M2/M3) are all supported.

---

### Starting the Ollama Server

On Windows and macOS, Ollama runs as a background service automatically after installation.

**Manual start (if needed):**
```bash
ollama serve
```

**Verify the server is running:**
```bash
curl http://localhost:11434/api/tags
```

Expected response:
```json
{
  "models": [
    {
      "name": "llama3.2:latest",
      "model": "llama3.2:latest",
      ...
    }
  ]
}
```

---

### Using Ollama in Python

**OpenAI-compatible API (recommended):**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Required by the SDK, but ignored by Ollama
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "What is a vector database?"},
    ],
)

print(response.choices[0].message.content)
```

**Native Ollama Python library:**
```bash
pip install ollama
```
```python
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "What is RAG?"}],
)
print(response["message"]["content"])
```

---

### Embedding Models

Ollama supports embedding models for use in RAG pipelines:

```bash
ollama pull nomic-embed-text      # 137M params, 768 dimensions — great general purpose
ollama pull mxbai-embed-large     # 335M params, 1024 dimensions — higher quality
ollama pull all-minilm            # 23M params, 384 dimensions — very fast/lightweight
```

**Using with LangChain:**
```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector = embeddings.embed_query("What is machine learning?")
print(f"Embedding dimension: {len(vector)}")  # 768
```

---

### Privacy Benefits

- ✅ All inference happens on your local machine
- ✅ No API keys required
- ✅ No usage data sent to any third party
- ✅ Works completely offline after model download
- ✅ Suitable for sensitive documents (medical, legal, financial)

**Model library:** [https://ollama.com/library](https://ollama.com/library)

---

## Provider Comparison Table

| Feature | Google Gemini | OpenRouter | Ollama (Local) |
|---------|:---:|:---:|:---:|
| **Setup complexity** | 1 (Easy) | 1 (Easy) | 2 (Moderate) |
| **Free access** | ✅ Yes (rate-limited) | ✅ Limited (`:free` models) | ✅ Yes (unlimited local) |
| **Streaming** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Structured output (JSON)** | ✅ Yes | ⚠️ Partial (model-dependent) | ⚠️ Partial (model-dependent) |
| **Tool / function calling** | ✅ Yes | ⚠️ Partial (model-dependent) | ⚠️ Partial (model-dependent) |
| **Embedding models** | ✅ Yes | ⚠️ Limited | ✅ Yes |
| **Multimodal (image/audio)** | ✅ Yes | ⚠️ Model-dependent | ⚠️ Limited (some models) |
| **Works offline** | ❌ No | ❌ No | ✅ Yes |
| **No data leaves your machine** | ❌ No | ❌ No | ✅ Yes |
| **Best for** | General use, production | Multi-model comparison | Privacy, offline, zero cost |

**Setup complexity scale:** 1 = Sign up and copy a key, 2 = Install software + download models, 3 = Requires infrastructure setup

---

> [!NOTE]
> **Verification note:** Free tier details, rate limits, and model availability were verified on **2026-10-30**. LLM provider offerings change frequently. Always check the official provider documentation for the most current information before starting a project.

---

## Related Documentation

- [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) — Which modules use which providers
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Provider-specific error fixes
- [GLOSSARY.md](GLOSSARY.md) — Definitions for provider-related terms

*Last updated: 2026-10-30*
