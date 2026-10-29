# Module 10 — Agents

> **Goal:** Understand what an LLM agent is, how tool calling works, the ReAct reasoning pattern, and the safety considerations that matter most when giving a model the ability to take actions.

---

## 1. What is an Agent?

A **chain** is a fixed sequence of steps: prompt → model → parser → done.

An **agent** is different: the model itself decides which steps to take, in what order, and when to stop. The model has access to a set of **tools** (functions) and can call them repeatedly until it has enough information to answer.

```
User question
     ↓
  [Model reasons]
     ↓
  "I need to call tool X"  ←── decision made by the model
     ↓
  [Tool executes]
     ↓
  [Model sees result]
     ↓
  "I need to call tool Y"  ←── another decision
     ↓
  [Tool executes]
     ↓
  "I have enough info to answer"
     ↓
  Final answer to user
```

Agents unlock tasks that are **open-ended** or require **multiple steps with unknown structure**.

### Agents vs Simple Chains

| Feature | Chain | Agent |
|---------|-------|-------|
| Step order | Fixed at code time | Decided by model at runtime |
| Tools | None (usually) | Yes, can call 0–N times |
| Loops | No | Yes, iterates until done |
| Predictability | High | Lower |
| Appropriate for | Well-defined tasks | Open-ended tasks |

---

## 2. Tool Calling

Modern LLMs support **function/tool calling** natively. You describe tools in a schema, and the model responds with a structured JSON object specifying which tool to call and with what arguments.

### How the Model Requests a Tool

```json
{
  "tool_calls": [
    {
      "name": "get_current_time",
      "arguments": {"city": "Tokyo"}
    }
  ]
}
```

The model does **not** execute the tool — your code does. The model only produces the request.

### How Your Code Executes It

```python
tool_name = response.tool_calls[0]["name"]
tool_args = response.tool_calls[0]["arguments"]

# Dispatch to the right function
result = tools_registry[tool_name](**tool_args)

# Feed the result back to the model
messages.append(ToolMessage(content=str(result), tool_call_id=...))
```

The result is appended to the conversation so the model can use it in its next reasoning step.

---

## 3. The ReAct Pattern

**ReAct** = **Re**ason + **Act**

Originally described in the 2022 paper *"ReAct: Synergizing Reasoning and Acting in Language Models"*, this pattern interleaves reasoning steps with action steps:

```
Thought: I need to find the current time in Tokyo.
Action: get_current_time(city="Tokyo")
Observation: 2024-01-15 14:32:00 JST

Thought: Now I have the time. I can answer.
Action: Final Answer: It is 2:32 PM in Tokyo.
```

Each **Thought** is the model reflecting on what it knows. Each **Action** is a tool call. Each **Observation** is the tool result fed back in.

LangChain's `create_react_agent` implements this pattern automatically.

---

## 4. Stop Conditions

Without stop conditions, an agent could loop forever (or until your API bill is astronomical). Always define at least one:

| Stop Condition | How to implement |
|---------------|-----------------|
| **Max iterations** | `AgentExecutor(max_iterations=5)` |
| **Success signal** | Model outputs `Final Answer:` |
| **Timeout** | Wrap in `asyncio.wait_for(..., timeout=30)` |
| **Budget limit** | Track token usage, stop when exceeded |

A well-designed agent should hit "success" most of the time. If it often hits `max_iterations`, the task might be too complex or the tools are insufficient.

---

## 5. State and Memory in Agents

By default, each agent run is stateless. Memory comes in two flavours:

### In-Context Memory (short-term)
Pass previous turns as messages:

```python
messages = [
    HumanMessage("My name is Alice."),
    AIMessage("Hello Alice!"),
    HumanMessage("What's my name?"),  # model can answer from context
]
```

Limited by the model's **context window**. Works for short conversations.

### External Memory (long-term)
Store and retrieve facts from a database, vector store, or simple dict. Inject relevant memories into the prompt at query time. This is the foundation of personalisation and RAG (see Module 13).

---

## 6. Observability: Logging Tool Calls

Agent behaviour can be opaque — you need visibility into what the model decided to do and why. At minimum, log:

- Which tool was called
- What arguments were used
- What the tool returned
- How many iterations were taken

```python
# LangChain AgentExecutor with verbose=True
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

With `verbose=True`, LangChain prints each Thought, Action, and Observation to stdout. In production, use a proper logging framework or a tracing tool like LangSmith.

---

## 7. When to Use an Agent vs a Deterministic Workflow

Agents are powerful but unpredictable. Prefer a **deterministic workflow** (a fixed chain or script) when:

- You know exactly what steps are needed.
- Reproducibility is critical (e.g., financial calculations).
- Failure modes of incorrect tool calls are severe.

Use an **agent** when:
- The user's intent is open-ended ("help me research X").
- The number of tool calls required varies per request.
- You want the model to handle edge cases by reasoning.

> **Practical rule:** Start with a deterministic workflow. Upgrade to an agent only when the workflow becomes too complex to enumerate.

---

## 8. ⚠️ WARNING: Never Give Agents Unrestricted Shell Access

Agents will do exactly what the model decides — including unintended or harmful actions if given the wrong tools.

**Never expose these to an agent without extreme sandboxing:**
- `subprocess` / shell execution
- File system write access to sensitive paths
- Database `DELETE` / `DROP` operations
- External API calls that have side effects (send email, charge card, etc.)

**Instead:**
- Give agents read-only tools where possible.
- Require human approval before any destructive action.
- Run agents in sandboxed environments (containers with no network, read-only filesystems).
- Log every tool call so you can audit what the agent did.

> 🔴 **A language model deciding to run `rm -rf /` is not a hypothetical — it has happened in research settings. Design defensively.**

---

## 9. Exercises

### Exercise 1 — Run the Agent
Run `01_simple_agent.py` with `verbose=True`. Ask it: *"What time is it in London, and how many words is your answer?"*. Read every Thought/Action/Observation step.

### Exercise 2 — Add a New Tool
Add a `get_weather(city: str)` tool that returns a hardcoded weather string. Register it and ask a question that requires both time and weather.

### Exercise 3 — Hit the Max Iterations Limit
Ask a question that the tools cannot possibly answer (e.g., "What is the population of every country?"). Watch the agent hit `max_iterations`. What does it say?

### Exercise 4 — Break the Calculator
Try to pass `__import__('os').system('echo pwned')` as the expression to `calculate()`. Verify that the `ast.literal_eval` guard rejects it. Contrast with what `eval()` would do.

### Exercise 5 — Memory
Modify the agent to maintain a list of previous messages across two calls:
1. Call 1: "My name is Alice."
2. Call 2: "What's my name?"
The agent should answer correctly by seeing the prior message.

---

## Key Takeaways

- An agent lets the **model decide** which tools to call and when to stop.
- ReAct (Reason → Act → Observe) is the foundational pattern.
- Always set a `max_iterations` guard.
- Log every tool call — agents are opaque without observability.
- Never give an agent unrestricted access to the shell, filesystem, or destructive APIs.
