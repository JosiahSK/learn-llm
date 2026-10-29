# 🛠️ Troubleshooting Guide

A reference for common errors encountered in the **learn-llm** course, organized by category.

> [!TIP]
> Use **Ctrl+F / Cmd+F** to search for a specific error message.

---

## Table of Contents

1. [Installation Issues](#1-installation-issues)
2. [API Key Issues](#2-api-key-issues)
3. [Model ID Issues](#3-model-id-issues)
4. [Rate Limiting](#4-rate-limiting)
5. [Network Issues](#5-network-issues)
6. [Notebook Issues](#6-notebook-issues)
7. [Ollama Issues](#7-ollama-issues)
8. [LangChain Issues](#8-langchain-issues)
9. [RAG Issues](#9-rag-issues)

---

## 1. Installation Issues

### 1.1 `pip install` Fails

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement langchain (from versions: none)
ERROR: No matching distribution found for langchain
```

**Likely causes:**
- Outdated `pip`
- Wrong Python environment active
- No internet connection or corporate firewall blocking PyPI

**Fix:**
```bash
# Step 1: Upgrade pip
python -m pip install --upgrade pip

# Step 2: Verify you are in the correct virtual environment
which python        # macOS/Linux
where python        # Windows
# Should point to your venv, not the system Python

# Step 3: If behind a corporate proxy, set proxy:
pip install langchain --proxy http://user:pass@proxy.company.com:8080

# Step 4: If PyPI is blocked, try an alternative index:
pip install langchain -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 1.2 Conflicting Package Versions

**Symptom:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages...
langchain 0.3.x requires pydantic>=2.0, but you have pydantic 1.10 installed.
```
or:
```
ImportError: cannot import name 'BaseModel' from 'pydantic'
```

**Likely cause:** Multiple projects sharing the same Python environment with incompatible dependencies.

**Fix:**
```bash
# Step 1: Create a fresh virtual environment for this course
python -m venv .venv

# Step 2: Activate it
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows PowerShell

# Step 3: Install only from the course requirements file
pip install -r requirements.txt

# Step 4: Verify the environment is clean
pip check   # Reports any dependency conflicts
```

> [!IMPORTANT]
> Always use a dedicated virtual environment per project. Never install course packages into your system Python.

---

### 1.3 Python Version Issues

**Symptom:**
```
SyntaxError: f-string expression part cannot include a backslash
# or
ModuleNotFoundError: No module named 'tomllib'
```

**Likely cause:** Using Python 3.8 or older. This course requires **Python 3.10+**.

**Fix:**
```bash
# Check your Python version
python --version

# If below 3.10, install a newer version:
# Windows: Download from https://python.org/downloads/
# macOS: brew install python@3.12
# Linux: sudo apt install python3.12

# On Windows, if multiple versions are installed:
py -3.12 -m venv .venv
```

---

## 2. API Key Issues

### 2.1 Key Not Set or Still a Placeholder

**Symptom:**
```
KeyError: 'GOOGLE_API_KEY'
# or
google.auth.exceptions.DefaultCredentialsError
# or (if using a placeholder from the .env.example)
400 Bad Request: API key not valid. Please pass a valid API key.
```

**Likely cause:** The environment variable was never set, or the `.env` file contains the example placeholder `your-api-key-here`.

**Fix:**
```bash
# Step 1: Verify the variable is set in your shell
echo $GOOGLE_API_KEY         # macOS/Linux
echo $env:GOOGLE_API_KEY     # Windows PowerShell
# Should print your actual key (starts with AIza...)

# Step 2: If empty, set it:
export GOOGLE_API_KEY="AIza..."           # macOS/Linux
$env:GOOGLE_API_KEY = "AIza..."          # Windows PowerShell

# Step 3: If using a .env file, ensure load_dotenv() is called BEFORE the client is created:
from dotenv import load_dotenv
load_dotenv()   # Must come before: client = genai.Client(...)

# Step 4: Confirm the .env file has no quotes around the value:
# CORRECT:   GOOGLE_API_KEY=AIzaXXXXXXX
# INCORRECT: GOOGLE_API_KEY="AIzaXXXXXXX"  (may work, but quotes can cause issues)
```

---

### 2.2 API Key Rejected (401 Unauthorized)

**Symptom:**
```
google.api_core.exceptions.PermissionDenied: 403 API key not valid
# or
openai.AuthenticationError: 401 Incorrect API key provided: sk-or-...
```

**Likely cause:** Key was deleted, regenerated, or restricted in the provider console.

**Fix:**
1. Go to your provider's key management page:
   - Gemini: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   - OpenRouter: [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Check whether the key still exists and is active
3. If the key was deleted, create a new one and update your `.env` file
4. Check that no extra whitespace or newline characters were introduced when copying:
   ```python
   import os
   key = os.environ["GOOGLE_API_KEY"]
   print(repr(key))  # Should show no \n or leading/trailing spaces
   ```

---

### 2.3 Account Not Verified / Access Restricted

**Symptom:**
```
403 PERMISSION_DENIED: Gemini API has not been used in project XXX before or it is disabled.
# or (OpenRouter)
402 Payment Required: You need to add a payment method to access this model.
```

**Fix for Gemini:**
1. Go to [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
2. Search for "Generative Language API"
3. Click **Enable**
4. Wait ~1 minute for the change to propagate

**Fix for OpenRouter:**
1. Verify your email address in the OpenRouter account settings
2. For models requiring payment, add a small credit ($5) at [https://openrouter.ai/credits](https://openrouter.ai/credits)
3. Switch to a `:free` model: [https://openrouter.ai/models?q=:free](https://openrouter.ai/models?q=:free)

---

## 3. Model ID Issues

### 3.1 404 Model Not Found

**Symptom:**
```
google.api_core.exceptions.NotFound: 404 models/gemini-pro is not found for API version v1beta
# or
openai.NotFoundError: 404 No endpoints found for model "gpt-4"
```

**Likely cause:** Using an outdated, incorrect, or deprecated model ID.

**Fix:**
1. Use the correct model ID from the table below
2. Do not add version suffixes unless specified (e.g., don't write `gemini-3.8-flash-001` unless you want to pin to a specific version)

---

### 3.2 Valid Gemini Model IDs *(verified 2026-10-30)*

Use these exact strings with the `google-genai` SDK:

| Model ID | Type | Free Tier | Best For |
|----------|------|-----------|----------|
| `gemini-3.8-flash` | Text + Multimodal | ✅ Yes | Default for all course modules |
| `gemini-3.8-flash-lite` | Text | ✅ Yes | High-volume, low-latency tasks |
| `gemini-3.8-flash-thinking-exp` | Reasoning | ✅ Limited | Complex reasoning tasks |
| `gemini-1.5-flash` | Text + Multimodal | ✅ Yes | Legacy free-tier fallback |
| `gemini-1.5-pro` | Text + Multimodal | ❌ Paid | Long context, complex tasks |
| `gemini-2.5-pro` | Text + Multimodal | ❌ Paid | Highest capability |

**Embedding models:**
| Model ID | Dimensions | Free Tier |
|----------|-----------|-----------|
| `text-embedding-004` | 768 | ✅ Yes |

> [!WARNING]
> `gemini-pro`, `gemini-1.0-pro`, and `chat-bison` are **deprecated** and will return 404. Always use the IDs from the table above.

**Where to find current model IDs:**
- Gemini: [https://ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
- OpenRouter: [https://openrouter.ai/models](https://openrouter.ai/models)
- Ollama: [https://ollama.com/library](https://ollama.com/library)

---

## 4. Rate Limiting

### 4.1 429 Too Many Requests

**Symptom:**
```
google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted
# or
openai.RateLimitError: 429 Too Many Requests
```

**Likely cause:** Exceeded the requests-per-minute (RPM) or tokens-per-minute (TPM) limit for your tier.

**Gemini Rate Limits and Tier Structure:**
Rate limits in the Gemini API are **dynamic** and **model-specific**. There is no single universal limit:
- Limits depend on the **model** (Flash vs Pro vs Flash-Lite), the **account/project tier** (Google AI Studio free tier vs Google Cloud Pay-As-You-Go), and regional policies.
- Check current allocations and quotas in official documentation:
  - **Models Overview:** [https://ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
  - **Pricing & Tier Quotas:** [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
  - **Rate Limits Guide:** [https://ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- Check your actual live quota in Google AI Studio under **API keys / Usage** or the Google Cloud Console under **APIs & Services → Quotas**.

**Fix — Quick (pace requests with delays):**
```python
import time

for i, chunk in enumerate(my_documents):
    response = client.models.generate_content(...)
    time.sleep(2)  # Pause between successive calls to avoid bursts
```

**Fix — Robust (exponential backoff):**
```python
import time
import random
from google.api_core.exceptions import ResourceExhausted

def call_with_backoff(fn, max_retries=5):
    for attempt in range(max_retries):
        try:
            return fn()
        except ResourceExhausted:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Waiting {wait:.1f}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
    raise RuntimeError("Max retries exceeded")

result = call_with_backoff(lambda: client.models.generate_content(...))
```

**Fix — Upgrade:**
If you need higher limits without paying, try:
- Switching between providers (use OpenRouter or Ollama while Gemini cools down)
- Processing your dataset in batches across multiple sessions

---

## 5. Network Issues

### 5.1 Timeout Errors

**Symptom:**
```
requests.exceptions.Timeout: HTTPSConnectionPool: Read timed out.
# or
httpx.ReadTimeout: timed out
```

**Likely cause:** Slow network, large request payload, or the API server is under load.

**Fix:**
```python
# Increase the timeout for the google-genai client:
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"],
    http_options=types.HttpOptions(timeout=60_000),  # 60 seconds in ms
)

# For the openai SDK:
from openai import OpenAI
client = OpenAI(timeout=60.0)  # seconds
```

---

### 5.2 SSL Certificate Errors

**Symptom:**
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Likely cause:** Corporate network with SSL inspection, or outdated CA bundle.

**Fix:**
```bash
# Update certifi:
pip install --upgrade certifi

# macOS (Python.org installer): Run the Install Certificates script
open /Applications/Python\ 3.12/Install\ Certificates.command

# Temporary workaround (NOT for production):
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

> [!CAUTION]
> Disabling SSL verification is a security risk. Use it only as a temporary diagnostic step, never in production code.

---

### 5.3 Proxy Configuration

**Symptom:** Requests hang or fail silently in a corporate environment with a proxy.

**Fix:**
```bash
# Set proxy environment variables (used by most HTTP libraries):
export HTTPS_PROXY=http://user:password@proxy.company.com:8080
export HTTP_PROXY=http://user:password@proxy.company.com:8080

# Windows PowerShell:
$env:HTTPS_PROXY = "http://user:password@proxy.company.com:8080"

# Or configure in Python:
import httpx
client = httpx.Client(proxies={"https://": "http://proxy.company.com:8080"})
```

---

## 6. Notebook Issues

### 6.1 Kernel Not Found

**Symptom:**
```
No kernel found. Please select a kernel.
# or
jupyter: command not found (when running from the notebook directory)
```

**Fix:**
```bash
# Step 1: Install Jupyter in your virtual environment
pip install jupyter ipykernel

# Step 2: Register the venv as a kernel
python -m ipykernel install --user --name=learn-llm --display-name="Learn LLM"

# Step 3: Launch Jupyter
jupyter notebook
# or for VS Code: select the kernel "Learn LLM" from the kernel picker in the top-right
```

---

### 6.2 Execution Order Issues

**Symptom:**
```
NameError: name 'client' is not defined
# or variable holds a stale value from a previous run
```

**Likely cause:** Cells executed out of order, or the kernel was restarted without re-running setup cells.

**Fix:**
1. **Kernel → Restart & Run All** — re-runs all cells from top to bottom
2. Check that import and setup cells (API key loading, client initialization) come before the cells that use them
3. Use **Cell → Run All Above** to catch up to your current cell

---

### 6.3 Output Too Large / Notebook Freezes

**Symptom:** Notebook becomes unresponsive after a cell produces many MB of output (e.g., printing thousands of embeddings).

**Fix:**
```python
# Truncate large outputs before printing:
print(str(embeddings)[:500])  # First 500 chars only

# Or suppress output for bulk operations:
results = []
for doc in documents:
    results.append(process(doc))
    # Don't print inside the loop
print(f"Processed {len(results)} documents")

# Clear cell output: Right-click cell → Clear Output
```

---

## 7. Ollama Issues

### 7.1 Server Not Running

**Symptom:**
```
httpx.ConnectError: [Errno 111] Connection refused (http://localhost:11434)
# or
ollama.ResponseError: connection refused
```

**Fix:**
```bash
# Start the Ollama server:
ollama serve

# Verify it's running:
curl http://localhost:11434/api/tags

# On Windows, check the system tray for the Ollama icon
# On Linux, check the service:
sudo systemctl status ollama
sudo systemctl start ollama
```

---

### 7.2 Model Not Installed

**Symptom:**
```
ollama.ResponseError: model "llama3.2" not found, try pulling it first
```

**Fix:**
```bash
# Pull the model (requires internet connection):
ollama pull llama3.2

# List installed models:
ollama list

# If disk space is low, remove unused models:
ollama rm mistral:7b
```

---

### 7.3 Slow Inference

**Symptom:** Responses take 30+ seconds per response on a 7B model.

**Likely causes:**
- Model is running on CPU (no GPU detected)
- Not enough RAM, causing heavy disk swapping
- Model is too large for your hardware

**Fix:**
```bash
# Check if GPU is being used (look for "gpu_layers" > 0):
ollama ps

# Try a smaller model:
ollama pull llama3.2:1b   # Much faster than 8B on CPU

# Increase the number of GPU layers if you have a GPU:
OLLAMA_NUM_GPU=99 ollama serve   # macOS/Linux, pushes all layers to GPU
```

---

### 7.4 CUDA / GPU Not Detected

**Symptom:**
```
# ollama ps shows gpu_layers = 0 despite having an NVIDIA GPU
```

**Fix:**
```bash
# Step 1: Verify CUDA is installed
nvidia-smi

# Step 2: Check Ollama detects the GPU
ollama run llama3.2 "test"
# Should show GPU memory usage in nvidia-smi during generation

# Step 3: If CUDA not found, reinstall Ollama after installing CUDA toolkit:
# https://developer.nvidia.com/cuda-downloads

# Step 4: For AMD GPUs (ROCm), ensure ROCm 5.7+ is installed
```

---

## 8. LangChain Issues

### 8.1 ImportError for LangChain Components

**Symptom:**
```
ImportError: cannot import name 'ChatGoogleGenerativeAI' from 'langchain'
# or
ModuleNotFoundError: No module named 'langchain_google_genai'
```

**Likely cause:** LangChain has split into multiple packages. Community integrations are in separate packages.

**Fix:**
```bash
# Install the specific integration package:
pip install langchain-google-genai      # For Gemini
pip install langchain-openai            # For OpenAI / OpenRouter / Ollama via OpenAI SDK
pip install langchain-ollama            # For Ollama
pip install langchain-community         # For misc. integrations (PDFLoader, etc.)
pip install langchain-chroma            # For ChromaDB vector store
```

```python
# Correct import paths:
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
```

---

### 8.2 Deprecated API Usage

**Symptom:**
```
LangChainDeprecationWarning: The class `LLMChain` was deprecated...
# or
DeprecationWarning: ConversationChain is deprecated. Use RunnableWithMessageHistory instead.
```

**Likely cause:** Tutorial or notebook was written for LangChain v0.1 (before LCEL was the standard).

**Fix:** Migrate to LCEL (the pipe `|` operator):

```python
# OLD (deprecated):
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(input="hello")

# NEW (LCEL):
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "hello"})
```

Refer to [LangChain migration guide](https://python.langchain.com/docs/versions/migrating_chains/) for specific chain migrations.

---

### 8.3 Chain Not Working / Returns Unexpected Output

**Symptom:** Chain runs without error but output is empty, wrong type, or the output parser raises an error.

**Fix — Debug the chain step by step:**
```python
# Test each component individually:
formatted_prompt = prompt.invoke({"question": "What is RAG?"})
print(formatted_prompt)  # Check the prompt looks right

raw_response = llm.invoke(formatted_prompt)
print(raw_response)      # Check the LLM response

parsed = output_parser.invoke(raw_response)
print(parsed)            # Check parsing succeeds
```

**Fix — Enable verbose logging:**
```python
from langchain.globals import set_verbose, set_debug
set_verbose(True)   # Shows chain steps
set_debug(True)     # Shows full inputs/outputs at each step
```

---

## 9. RAG Issues

### 9.1 Poor Retrieval Quality

**Symptom:** The model retrieves irrelevant chunks and gives wrong or hallucinated answers.

**Likely causes:**
- Chunks are too large or too small
- Embedding model mismatch between indexing and querying
- Not enough retrieved chunks (`k` too low)
- Query phrasing doesn't match document language

**Fix:**
```python
# Try different chunk sizes (experiment with your data):
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Try 300, 500, 1000
    chunk_overlap=50,      # Overlap helps with context at boundaries
)

# Increase k to retrieve more candidates:
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})  # Default is 4

# Use a hypothetical document embedding (HyDE) to improve query matching:
# Generate a hypothetical answer, then embed that instead of the raw query

# Add MMR (Max Marginal Relevance) for diversity:
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20},
)
```

---

### 9.2 PDF Text Extraction Fails

**Symptom:**
```
Error loading PDF: PdfReadError: EOF marker not found
# or extracted text is garbled/empty
```

**Likely cause:** Scanned PDF (image-only), corrupted file, or password-protected PDF.

**Fix:**
```bash
# Install additional loaders:
pip install pypdf pymupdf pdfminer.six

# Try PyMuPDF (more robust than pypdf):
from langchain_community.document_loaders import PyMuPDFLoader
loader = PyMuPDFLoader("document.pdf")
docs = loader.load()

# For scanned PDFs (requires Tesseract OCR):
pip install pytesseract pdf2image
# Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki (Windows)
#                   brew install tesseract (macOS)

# Check if PDF is password-protected:
import pypdf
with open("document.pdf", "rb") as f:
    reader = pypdf.PdfReader(f)
    print(reader.is_encrypted)  # True = needs password
```

---

### 9.3 Embedding Dimension Mismatch

**Symptom:**
```
chromadb.errors.InvalidDimensionException: Embedding dimension 1536 does not match collection dimensionality 768
# or
ValueError: shapes (768,) and (1536,) not aligned
```

**Likely cause:** The embedding model was changed after the vector store was already created with a different model.

**Fix:**
```python
# You must delete and recreate the collection when changing embedding models.
# Option 1: Delete the ChromaDB directory and re-index:
import shutil
shutil.rmtree("./chroma_db")  # Delete old index

# Option 2: Use a new collection name:
vectorstore = Chroma(
    collection_name="my_docs_v2",  # New name = new empty collection
    embedding_function=new_embeddings,
    persist_directory="./chroma_db",
)

# To avoid future confusion, embed the model name in the collection name:
collection_name = "docs_nomic-embed-text_v1"
```

> [!IMPORTANT]
> Always use the **same embedding model** for indexing documents and for embedding queries at retrieval time. Mixing models produces meaningless similarity scores.

---

## Related Documentation

- [PROVIDER_SETUP.md](PROVIDER_SETUP.md) — Provider configuration and API keys
- [GLOSSARY.md](GLOSSARY.md) — Definitions for technical terms
- [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) — Course structure and module order

---

*Last updated: 2026-10-30*
