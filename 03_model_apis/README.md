# Module 03 — Model APIs and Direct Provider Access

Before adopting high-level frameworks like LangChain, developers must understand what happens underneath: HTTP requests, JSON payloads, authentication tokens, status codes, and raw JSON responses.

---

## 1. Objectives

- Connect directly to cloud and local LLM endpoints without framework bloat.
- Master authentication patterns via environment variables.
- Understand request schemas: System vs User vs Assistant messages.
- Implement resilient error handlers for rate limits (HTTP 429), timeouts, and auth errors (HTTP 401).

---

## 2. Lessons in this Module

1. [`01_first_request_gemini.py`](./01_first_request_gemini.py): Direct API connection to Google Gemini (`google-genai`).
2. [`02_first_request_openrouter.py`](./02_first_request_openrouter.py): Querying free models on OpenRouter (`openai` client).

---

## 3. Verified Provider Endpoints (2026-10-30)

| Provider | Endpoint | SDK | Verified Free Model |
|---|---|---|---|
| Google Gemini | `https://generativelanguage.googleapis.com` | `google-genai` | `gemini-3.8-flash` |
| OpenRouter | `https://openrouter.ai/api/v1` | `openai` | `google/gemma-4-31b-it:free` |
| Ollama | `http://localhost:11434/v1` | `openai` / `urllib` | `llama3.2` |
