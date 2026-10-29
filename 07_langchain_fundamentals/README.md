# Module 07 — LangChain Fundamentals

> **Goal:** Understand what LangChain is, when it adds value over direct SDK usage, and how to use its core building blocks (ChatModels, PromptTemplates, OutputParsers, and chains).

---

## 1. What is LangChain?

LangChain is an open-source framework that provides **composable abstractions** for building LLM-powered applications. Instead of writing glue code yourself (format a prompt → call the API → parse the output → pass to the next step), LangChain gives you reusable pieces you snap together.

```
prompt template  →  chat model  →  output parser
     ↓                  ↓               ↓
  formats           calls API         cleans
  the prompt        & streams         the text
```

LangChain supports many providers (OpenAI, Google, Anthropic, Ollama, …) behind a **unified interface**, so switching providers is often a one-line change.

### When to use LangChain

| Use LangChain when… | Use the direct SDK when… |
|---------------------|--------------------------|
| Building multi-step pipelines | Making a single API call |
| Switching between providers | Locked to one provider |
| Need built-in retry / fallback logic | Simple scripts or prototypes |
| Building RAG or agent workflows | Full control over every API option |
| Reusing prompt templates across a codebase | One-off experiments |

---

## 2. Core Concepts

### 2.1 ChatModel

A `ChatModel` wraps an LLM API. It takes a list of messages and returns a message.

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
response = model.invoke("What is the capital of France?")
print(response.content)  # "Paris"
```

Every LangChain chat model exposes the same three methods:

| Method | Returns | Use for |
|--------|---------|---------|
| `invoke(input)` | `AIMessage` | Single synchronous call |
| `stream(input)` | Iterator of `AIMessageChunk` | Streaming responses |
| `batch(inputs)` | List of `AIMessage` | Multiple inputs at once |

### 2.2 PromptTemplate

A `PromptTemplate` is a reusable, parameterised prompt with named placeholders.

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teacher explaining {topic} in {language}."),
    ("human", "Explain {topic} in simple terms."),
])

# Fill in the variables
messages = template.invoke({"topic": "recursion", "language": "English"})
```

Templates are **lazy** — they don't call the model. They just format the messages.

### 2.3 OutputParser

An `OutputParser` transforms the raw `AIMessage` into a more useful Python type.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
text = parser.invoke(ai_message)  # extracts .content as a plain str
```

Other parsers: `JsonOutputParser`, `PydanticOutputParser`, `CommaSeparatedListOutputParser`.

### 2.4 Runnable

Almost everything in LangChain implements the `Runnable` interface: prompts, models, parsers, even custom functions. Any `Runnable` exposes `invoke`, `stream`, and `batch`.

This is the key design decision that makes LCEL work.

### 2.5 Chain

A **chain** is a sequence of Runnables. Chains are built with the pipe operator `|`.

```python
chain = template | model | parser

result = chain.invoke({"topic": "recursion", "language": "English"})
print(result)  # plain string output
```

---

## 3. LangChain Expression Language (LCEL)

LCEL is the syntax for composing Runnables using `|`. Think of it like Unix pipes:

```bash
# Unix pipes
echo "hello" | tr '[:lower:]' '[:upper:]' | rev
```

```python
# LCEL
chain = prompt | model | parser
result = chain.invoke({"topic": "sorting", "language": "Python"})
```

LCEL chains automatically support:
- `.invoke()` — synchronous single call
- `.stream()` — streaming output
- `.batch()` — parallel execution over a list of inputs
- `.ainvoke()` / `.astream()` / `.abatch()` — async versions

You get all four for free from any chain you build.

---

## 4. Provider Integrations

### ChatGoogleGenerativeAI

```bash
pip install langchain-google-genai
```

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.7,
    # google_api_key="..." or set GOOGLE_API_KEY env var
)
```

### ChatOpenAI (also works with OpenRouter)

```bash
pip install langchain-openai
```

```python
from langchain_openai import ChatOpenAI

# Direct OpenAI
model = ChatOpenAI(model="gpt-4o-mini")

# Via OpenRouter
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

---

## 5. When NOT to Use LangChain

LangChain is powerful, but adds complexity. Avoid it when:

- You only need a single `generate_content()` call — the direct SDK is simpler.
- You need bleeding-edge API features that LangChain hasn't wrapped yet.
- You're debugging latency issues — LangChain's abstraction layers can make tracing hard.
- Your team isn't familiar with it — the learning curve is real.

> **Simple scripts don't need LangChain.** Start with the direct SDK; add LangChain when you feel the pain of managing prompts, parsers, and chains manually.

---

## 6. ⚠️ Warning: Version Changes and Deprecated APIs

LangChain's API has changed significantly across versions. Watch out for:

| Old (deprecated) | New (current) |
|-----------------|---------------|
| `from langchain.chat_models import ChatOpenAI` | `from langchain_openai import ChatOpenAI` |
| `from langchain.prompts import ChatPromptTemplate` | `from langchain_core.prompts import ChatPromptTemplate` |
| `LLMChain(llm=..., prompt=...)` | `prompt \| model \| parser` (LCEL) |
| `initialize_agent(...)` | `create_react_agent(...)` + `AgentExecutor` |

Always check which version of `langchain`, `langchain-core`, and `langchain-community` you have installed:

```bash
pip show langchain langchain-core langchain-openai langchain-google-genai
```

The examples in this module target **LangChain ≥ 0.2** with LCEL syntax.

---

## 7. Exercises

### Exercise 1 — Swap the Model
In `01_chat_models.py`, change from `ChatGoogleGenerativeAI` to `ChatOpenAI` (OpenRouter). Notice that the rest of the code doesn't change.

### Exercise 2 — Add a System Prompt
Modify `02_prompt_templates.py` to add a second system message that sets the tone: "Always answer in bullet points." See how it affects the output.

### Exercise 3 — Build a Translation Chain
Create a chain that: takes `{"text": ..., "target_language": ...}` → formats a translation prompt → calls the model → returns the plain-string translation.

### Exercise 4 — Batch Invoke
Call your translation chain with `.batch([...])` and translate 5 sentences at once. Compare timing with sequential `.invoke()` calls.

### Exercise 5 — Stream Output
Swap `.invoke()` for `.stream()` in any chain and print chunks as they arrive. Notice that `StrOutputParser` works seamlessly with streaming.

---

## Key Takeaways

- LangChain provides a **unified interface** across providers.
- LCEL's `|` operator makes composing steps elegant and explicit.
- Every component is a `Runnable` — same `invoke`/`stream`/`batch` API everywhere.
- LangChain has a history of breaking changes — always pin versions in production.
- Don't use it for simple scripts; do use it when building pipelines with multiple steps.
