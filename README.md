# LLM API Calling & Learning

A repository containing experiments and notebooks for exploring Large Language Model (LLM) APIs, LangChain, Google GenAI, and OpenAI/OpenRouter integrations.

## Contents

- **`ai_agent/learn_llm.ipynb`**: Interactive notebook walking through LLM API calls, prompting, LangChain models, and streaming responses.
- **`main.py`**: Python script demonstrating direct API calls with Google GenAI.
- **`requirements.txt`**: Project dependencies.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JosiahSK/learn-llm.git
   cd learn-llm
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```
