# Module 11 — Tokens and Tokenization

> **Goal:** Understand what a token is, why tokens ≠ words, how this affects cost and context limits, and how to estimate token counts in your applications.

---

## 1. What is Tokenization?

Before an LLM can process text, it must convert that text into a sequence of **token IDs** — integers that the model's neural network can work with. The process of splitting text into tokens is called **tokenization**.

```
"Hello, world!" 
     ↓  tokenizer
[9906, 11, 1917, 0]
     ↓  embedding lookup
[[0.12, -0.34, ...], [0.56, 0.78, ...], ...]
     ↓  transformer layers
...
```

The tokenizer runs **before** the model and **after** the model outputs (to decode integer IDs back to text).

---

## 2. Why Tokens ≠ Words

Most modern LLMs use **subword tokenization** (Byte-Pair Encoding / BPE or SentencePiece). This means:

- Common words are often **one token**: `" the"` → `[1820]`
- Rare words are split into **multiple tokens**: `" tokenization"` → `[4037`, `2065]`
- Numbers can be split digit-by-digit: `"1234"` → `["1"`, `"2"`, `"3"`, `"4"]`
- Emojis are usually **multiple tokens**: `"🚀"` → `[9468`, `248`, `222]`
- Leading spaces matter: `"hello"` and `" hello"` can be different tokens

```python
# This will surprise you:
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

print(enc.encode("hello"))        # [15339]       — 1 token
print(enc.encode(" hello"))       # [24748]       — 1 token, but different!
print(enc.encode("Hello"))        # [9906]        — 1 token
print(enc.encode("HELLO"))        # [13855, 3843] — 2 tokens
print(enc.encode("🚀"))           # [9468, 248, 222] — 3 tokens
```

---

## 3. How Token IDs Work

Each tokenizer has a **vocabulary** — a fixed mapping from subword strings to integer IDs.

```
Vocabulary (excerpt):
   0 → "<|endoftext|>"
   1 → "!"
   2 → "\""
   ...
 256 → "a"
 ...
9906 → "Hello"
```

When the model generates text, it outputs a **probability distribution over the whole vocabulary** at each step. The highest-probability token ID is selected (or sampled), decoded back to a string, appended to the output, and the process repeats.

---

## 4. Vocabulary Size

Different models use different tokenizers with different vocabulary sizes:

| Tokenizer | Used by | Vocab size |
|-----------|---------|-----------|
| `cl100k_base` | GPT-4, GPT-3.5-turbo | ~100,000 |
| `o200k_base` | GPT-4o | ~200,000 |
| SentencePiece | Gemini, PaLM, LLaMA | ~32,000–256,000 |
| WordPiece | BERT | ~30,000 |

Larger vocabularies → fewer tokens per sentence → faster generation and larger effective context.

---

## 5. Cost Implications: Pricing is Per Token

LLM APIs charge by the token, not by the word or character:

```
Cost = (input_tokens × input_price) + (output_tokens × output_price)
```

Example (illustrative, not current):

| Model | Input $/1M tokens | Output $/1M tokens |
|-------|------------------|-------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o mini | $0.15 | $0.60 |
| Gemini 1.5 Flash | $0.075 | $0.30 |

This means:
- A 1,000-word essay ≈ 1,300 tokens of output. At $10/1M, that's $0.013.
- Process 10,000 such essays → $130 just in output tokens.
- Verbose system prompts add to **every** request's input cost.

> **Tip:** Short, precise prompts save money. Measure token counts in development, especially for system prompts that appear in every request.

---

## 6. Context Window Limits in Tokens

Every model has a **context window** — the maximum number of tokens it can process at once (input + output combined):

| Model | Context window |
|-------|---------------|
| GPT-3.5-turbo | 16,384 tokens |
| GPT-4o | 128,000 tokens |
| Gemini 1.5 Pro | 2,000,000 tokens |
| LLaMA 3.1 70B | 128,000 tokens |

If your input exceeds the context window, the API returns an error. You must then either:
- Truncate the input
- Summarise older content
- Use a chunking strategy (see Module 13 — RAG)

A rough rule of thumb: **1 token ≈ 0.75 English words**, or **100 tokens ≈ 75 words**.

---

## 7. Different Tokenizers Produce Different Results

You **cannot** use tiktoken (OpenAI's tokenizer) to count tokens for Gemini — they use different tokenizers and will give different counts.

For exact counts:
- **OpenAI / OpenRouter (OpenAI models):** use `tiktoken`
- **Gemini:** use `client.models.count_tokens()`
- **Anthropic:** use `client.messages.count_tokens()`

For **estimates** (when you don't need exact counts), tiktoken's `cl100k_base` is a reasonable approximation for English text across most models.

---

## 8. How to Estimate Token Count

### Using tiktoken (OpenAI-compatible models)

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
tokens = enc.encode(text)
print(f"Token count: {len(tokens)}")
```

### Using the Gemini SDK

```python
result = client.models.count_tokens(
    model="gemini-3.8-flash",
    contents=text,
)
print(f"Token count: {result.total_tokens}")
```

### Rule-of-thumb estimate

```python
def rough_token_estimate(text: str) -> int:
    """~1 token per 4 characters for English text."""
    return len(text) // 4
```

---

## 9. Exercises

### Exercise 1 — Token Explorer
Run `01_token_explorer.py`. Enter your own sentences and observe:
- How many tokens does each take?
- What happens to non-English text?
- How does code tokenize differently from prose?

### Exercise 2 — Surprising Tokens
Find a word that tokenizes into more tokens than you'd expect. Hint: try long compound words, URLs, or identifiers with underscores like `my_variable_name`.

### Exercise 3 — Cost Calculator
Using placeholder pricing, calculate the cost to summarise 1,000 news articles if each is 500 words of input and the summary is 50 words of output.

### Exercise 4 — Context Window
Write a function that takes a list of messages and a max-token budget, and truncates the oldest messages to stay within budget.

### Exercise 5 — Compare Tokenizers
Use tiktoken to count tokens in a paragraph. Then use the Gemini SDK's `count_tokens`. How different are the counts? What does this tell you about cross-tokenizer estimation?

---

## Key Takeaways

- Text is converted to integer token IDs before reaching the model.
- Tokens ≠ words — common words may be 1 token; rare words, emojis, and code may be many.
- API pricing is **per token** — measure your prompts.
- Context window limits are in **tokens**, not words or characters.
- Use the correct tokenizer for each model; tiktoken is a reasonable cross-model estimator for English.
