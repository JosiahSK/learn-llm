# Project 04 — Streaming Chatbot with Latency Telemetry

This project implements a terminal streaming interface displaying tokens in real-time as they are emitted from the inference server, capturing Time To First Token (TTFT) and total generation metrics.

---

## 1. Features

- True incremental chunk rendering without terminal flickering.
- Millisecond-accurate telemetry for perceived vs actual latency.
- Graceful `Ctrl+C` interrupt handling without crashing the Python process.
- Seamless fallback to an offline generator simulation when API keys are absent.

---

## 2. Running the Project

```bash
python projects/04_streaming_chat/app.py
```
