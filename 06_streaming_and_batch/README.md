# Module 06 — Streaming and Batch Processing

> **Goal:** Understand the difference between streaming and non-streaming responses, why streaming matters for user experience, and how batch processing lets you handle many requests efficiently.

---

## 1. What is Streaming vs Non-Streaming?

When you call an LLM API, the model generates tokens **one at a time** internally. The question is: when does the server send those tokens to your program?

| Mode | Behaviour | Analogy |
|------|-----------|---------|
| **Non-streaming** | Server waits until the full response is generated, then sends everything at once | Waiting for a letter to arrive in the post |
| **Streaming** | Server sends each token (or small chunk) as soon as it is generated | Watching someone type in real-time |

```python
# Non-streaming – you block until the whole answer is ready
response = client.models.generate_content(model=MODEL, contents=prompt)
print(response.text)  # appears all at once

# Streaming – chunks arrive incrementally
for chunk in client.models.generate_content_stream(model=MODEL, contents=prompt):
    print(chunk.text, end="", flush=True)  # appears token-by-token
```

---

## 2. First-Token Latency vs Total Latency

Two different measures of "how fast" an LLM is:

| Metric | Definition | Affected by |
|--------|-----------|-------------|
| **First-token latency (TTFT)** | Time until the first token arrives | Model size, server load, prompt length |
| **Total latency** | Time until the full response is complete | All of the above + response length |

In streaming mode:
- **TTFT** is the same whether you stream or not (the model still has to "think" before the first token).
- **Total latency** (wall-clock) is approximately the same — streaming doesn't make the model *faster*.
- **Perceived latency** is dramatically lower — users see progress immediately.

---

## 3. Why Streaming Improves User Experience

Imagine asking an LLM to write a 500-word essay.

- **Non-streaming:** User stares at a blank screen for 8 seconds, then the full essay appears.
- **Streaming:** Text starts appearing after ~0.5 seconds; user starts reading while the model is still writing.

This is why every chat interface (ChatGPT, Claude, Gemini) uses streaming. The model isn't faster — the *experience* is better.

> **Rule of thumb:** If the response could take more than ~1 second, use streaming in any user-facing application.

---

## 4. How Streaming Works Technically

### Server-Sent Events (SSE)

The most common transport for LLM streaming over HTTP. The server holds the connection open and pushes events:

```
data: {"text": "Once"}
data: {"text": " upon"}
data: {"text": " a"}
data: {"text": " time"}
data: [DONE]
```

Each `data:` line is a JSON object with a chunk of the response. Your HTTP client reads the stream line-by-line.

### Chunked Transfer Encoding

An HTTP/1.1 feature where the server sends the response body in pieces without knowing the total size upfront:

```
HTTP/1.1 200 OK
Transfer-Encoding: chunked

5\r\n
Hello\r\n
6\r\n
 World\r\n
0\r\n
\r\n
```

Most LLM SDKs hide these details behind a simple iterator:

```python
for chunk in stream:
    print(chunk.text, end="")
```

### What a "Chunk" Contains

Chunks are **not** guaranteed to be single tokens. A chunk might be:
- 1 token (`" the"`)
- Several tokens (`" quick brown fox"`)
- A partial word at token boundaries

Always use `end=""` and `flush=True` when printing chunks, otherwise you'll buffer output.

---

## 5. Batch Processing

Batch processing means sending **many requests** and collecting results — either sequentially or concurrently.

### Sequential Batch (simple but slow)

```python
prompts = ["Summarise topic A", "Summarise topic B", "Summarise topic C"]
results = []
for prompt in prompts:
    results.append(client.models.generate_content(model=MODEL, contents=prompt).text)
```

Total time = sum of all individual request times.

### Concurrent Batch (faster)

```python
import asyncio

async def fetch(prompt):
    # async SDK call
    ...

async def main():
    tasks = [fetch(p) for p in prompts]
    results = await asyncio.gather(*tasks)
```

Total time ≈ time of the slowest individual request (when requests don't hit rate limits).

---

## 6. Concurrency and Rate Limits

Running too many requests in parallel will hit **rate limits** — the API provider's cap on:

| Limit Type | Typical unit |
|-----------|-------------|
| Requests per minute (RPM) | Number of API calls |
| Tokens per minute (TPM) | Input + output tokens combined |
| Tokens per day (TPD) | Daily budget |

**Strategies for staying within limits:**

1. **Semaphore** — allow at most N concurrent requests:
   ```python
   sem = asyncio.Semaphore(5)  # max 5 in-flight at once
   async with sem:
       result = await fetch(prompt)
   ```

2. **Exponential back-off** — on `429 Too Many Requests`, wait and retry:
   ```python
   import time, random
   for attempt in range(5):
       try:
           return call_api()
       except RateLimitError:
           time.sleep(2 ** attempt + random.random())
   ```

3. **Token-aware batching** — estimate token count before sending and throttle accordingly.

---

## 7. Error Handling for Partial Responses

Streaming introduces a new failure mode: the connection drops **mid-stream**, leaving you with a partial response.

```python
full_text = []
try:
    for chunk in client.models.generate_content_stream(model=MODEL, contents=prompt):
        full_text.append(chunk.text)
        print(chunk.text, end="", flush=True)
except Exception as e:
    partial = "".join(full_text)
    print(f"\n[Stream interrupted after {len(partial)} chars]: {e}")
    # Decide: retry? use partial? fail?
```

**Best practices:**
- Always accumulate chunks so you have a partial result if the stream fails.
- Log the partial response for debugging.
- Implement retry logic with the accumulated text as context if needed.
- Set reasonable timeouts — a stream that sends no data for 30 seconds is probably dead.

---

## 8. Exercises

### Exercise 1 — Time Both Modes
Run `01_streaming_basics.py` and observe the timing output. Answer:
- What is the TTFT for each mode?
- Is total latency the same?
- Does the streaming response *feel* faster even if total time is similar?

### Exercise 2 — Count Chunks
Modify the script to count the number of chunks received and the average chunk size in characters. Is chunk size consistent?

### Exercise 3 — Mock Streaming Without an API
Run the offline section of `01_streaming_basics.py`. Adjust the `delay` parameter in `fake_stream()`. At what delay does streaming feel "too slow"?

### Exercise 4 — Batch Timing
Write a script that sends 5 identical prompts sequentially and then concurrently (using `asyncio`). Compare total wall-clock time for each approach.

### Exercise 5 — Rate Limit Simulation
Introduce artificial throttling: add `time.sleep(0.1)` between chunks in `fake_stream()`. Observe how a caller that buffers chunks is affected vs one that prints immediately.

---

## Key Takeaways

- Streaming does **not** make the model faster — it makes the *experience* faster.
- Always handle partial responses when streaming.
- Use concurrency for batch jobs, but respect rate limits.
- First-token latency (TTFT) is the metric that users feel most.
