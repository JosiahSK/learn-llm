# Setup and Environment Guide

Welcome to **learn-llm**! This guide details how to set up your Python environment, configure dependencies, and verify everything works.

---

## 1. System Requirements

- **Python Version:** Python 3.11 or higher (Tested on Python 3.11.4).
- **Operating Systems:** Windows 10/11, macOS (Intel/Apple Silicon), or modern Linux.
- **Hardware Requirements:**
  - For Cloud API usage: Minimal (any standard PC/laptop with internet access).
  - For Local Models (Ollama): 8GB RAM minimum (16GB recommended for 7B/8B models).

---

## 2. Step-by-Step Installation

### Step A: Clone the Repository
```bash
git clone https://github.com/JosiahSK/learn-llm.git
cd learn-llm
```

### Step B: Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step C: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Configuration & API Keys

1. Copy the example environment template:
   ```bash
   # Windows:
   copy .env.example .env

   # macOS / Linux:
   cp .env.example .env
   ```

2. Open `.env` in your text editor and add at least one key:
   - **Google Gemini:** Free tier available at [Google AI Studio](https://aistudio.google.com/apikey). Set `GEMINI_API_KEY`.
   - **OpenRouter:** Free models available at [OpenRouter](https://openrouter.ai/keys). Set `OPENROUTER_API_KEY`.
   - **Ollama:** Completely local and free at [ollama.com](https://ollama.com/). No key required!

---

## 4. Verification

Run the automated offline test suite to ensure the environment is correctly configured:

```bash
# Windows PowerShell:
$env:PYTHONPATH="src;projects/09_chat_with_pdf"; pytest -v tests

# macOS / Linux:
PYTHONPATH="src:projects/09_chat_with_pdf" pytest -v tests
```

Expected output: **36 passed in < 1s**!

Next, run the beginner entry point:
```bash
python main.py
```
If keys are not yet configured, `main.py` will display helpful setup instructions.
