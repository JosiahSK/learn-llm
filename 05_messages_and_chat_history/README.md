# Module 05 — Messages and Chat History

LLM API calls are inherently **stateless**. Every HTTP POST request is evaluated in total isolation; the model remembers nothing from prior requests.

To build interactive assistants, client applications must manage conversational memory by storing and sending the message history with every subsequent turn.

---

## 1. Key Concepts

- **Stateless vs Stateful:** The model maintains no session. The client must store the transcript.
- **Message Roles:**
  - `system`: Rules and behavioral instructions.
  - `user`: Input from the human interlocutor.
  - `assistant`: Output produced by the model.
- **Context Window Management:** As the conversation grows, old tokens must be trimmed or summarized to avoid exceeding the model's maximum context limit.

---

## 2. Lessons

- [`01_stateful_chatbot.py`](./01_stateful_chatbot.py): A terminal chatbot that tracks message history, computes token approximations, and handles conversational resets.
