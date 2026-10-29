# Module 04 — Prompt Engineering & Evaluation

Prompt engineering is not merely phrasing a query nicely; it is the discipline of structuring instructions, constraints, and context to maximize model determinism and ground output formatting.

---

## 1. Key Concepts

- **Clarity & Constraints:** Explicit boundaries (e.g., "Limit reply to 3 sentences", "Return valid JSON").
- **Few-Shot Prompting:** Providing input-output demonstration pairs inside the prompt to establish output patterns.
- **Role Assignment:** Conditioning the model's persona with a system message (e.g., "You are an expert compiler engineer").
- **Prompt Injection Defense:** Treating external and user-supplied data as untrusted text, wrapping it in clear XML/delimiter boundaries.

---

## 2. Lessons

- [`01_prompt_basics.py`](./01_prompt_basics.py): Side-by-side prompt comparisons testing zero-shot, few-shot, and constrained prompting.
