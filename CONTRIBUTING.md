# Contributing to learn-llm

Thank you for your interest in contributing! This guide explains everything you need to set up your development environment, follow the project's coding standards, and get your changes merged.

---

## Table of Contents

1. [Setting Up the Dev Environment](#1-setting-up-the-dev-environment)
2. [Coding Standards](#2-coding-standards)
3. [How to Add a New Lesson](#3-how-to-add-a-new-lesson)
4. [How to Add a New Project](#4-how-to-add-a-new-project)
5. [Testing Requirements](#5-testing-requirements)
6. [Pull Request Process](#6-pull-request-process)
7. [What Good Lessons Look Like](#7-what-good-lessons-look-like)
8. [Reporting Bugs or Security Issues](#8-reporting-bugs-or-security-issues)

---

## 1. Setting Up the Dev Environment

**Prerequisites:** Python 3.11 or later, Git.

```bash
# 1. Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/learn-llm.git
cd learn-llm

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install all dependencies including dev extras
pip install -r requirements.txt
pip install pytest pytest-cov

# 4. Set up your local environment file
cp .env.example .env
# Edit .env with your API keys (never commit this file)

# 5. Verify the test suite passes without API keys
pytest tests/ -v
```

You're ready to contribute.

---

## 2. Coding Standards

### Type Hints

All function signatures must include type hints. Use `from __future__ import annotations` at the top of files targeting Python 3.9 compatibility.

```python
# ✅ Good
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    ...

# ❌ Bad — no hints
def chunk_text(text, chunk_size=500, overlap=50):
    ...
```

### Docstrings

Every public function, class, and module must have a docstring. Use Google style:

```python
def embed_text(text: str, model: str = "text-embedding-004") -> list[float]:
    """Generate an embedding vector for the given text.

    Args:
        text: The input string to embed. Must be non-empty.
        model: The Gemini embedding model ID.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        ValueError: If `text` is empty.
        APIError: If the embedding request fails.
    """
```

### Error Handling

- **Never** use bare `except:` or `except Exception:` without logging.
- Catch the most specific exception type possible.
- Always provide a user-friendly message; log the full traceback at `DEBUG` level.

```python
# ✅ Good
try:
    response = client.generate(prompt)
except AuthenticationError as e:
    logger.debug("Auth failure detail: %s", e)
    raise SystemExit("Authentication failed. Check your API key in .env.") from e

# ❌ Bad
try:
    response = client.generate(prompt)
except:
    pass
```

### General Style

- Follow [PEP 8](https://peps.python.org/pep-0008/). Run `ruff check .` before committing.
- Maximum line length: **100 characters**.
- Use `pathlib.Path` for all filesystem operations, not `os.path`.
- Use `logging` (not `print`) in library code under `src/`. Scripts and notebooks may use `print`.
- All string literals in user-facing messages should be natural English sentences.

---

## 3. How to Add a New Lesson

Lessons live in `modules/NN_module_name/lessons/`. Each lesson is a folder:

```
modules/NN_module_name/lessons/NN_lesson_name/
├── README.md          # Lesson narrative (required)
├── lesson.ipynb       # Interactive notebook (required)
└── exercise.ipynb     # Hands-on exercise with blanks (optional but encouraged)
```

### Step-by-Step

**1. Create the lesson folder:**

```bash
mkdir -p modules/06_rag/lessons/03_chunking_strategies
```

**2. Write `README.md`** — the lesson narrative. Structure it as:

```markdown
# Lesson Title

Brief one-paragraph overview of what this lesson covers and why it matters.

## Learning Objectives

By the end of this lesson you will be able to:
- [ ] Objective 1
- [ ] Objective 2

## Background

Conceptual explanation with diagrams or code snippets as needed.

## Hands-On

Instructions pointing to `lesson.ipynb`.

## Key Takeaways

- Bullet point summary of the most important concepts.

## Next Steps

Link to the next lesson or exercise.
```

**3. Create `lesson.ipynb`** — follow the notebook template structure:

- **Cell 1 (Markdown):** Title and learning objectives.
- **Cell 2 (Markdown):** Concept explanation with any necessary background.
- **Cell 3 (Code):** Imports and setup (load `.env`, configure logging).
- **Subsequent cells:** Step-by-step implementation with a Markdown explanation cell before each code cell.
- **Final cell (Markdown):** Summary and next steps.

**4. Create `exercise.ipynb`** (optional):

- Copy `lesson.ipynb`, then replace key implementation sections with `# YOUR CODE HERE` comments.
- Include expected output as a reference in a hidden/collapsed cell.

**5. Register the lesson** in the module's `README.md` lesson table.

**6. Run the tests:**

```bash
pytest tests/ -v
```

---

## 4. How to Add a New Project

Projects live in `projects/NN_project_name/`. Follow the conventions in [`docs/PROJECT_CATALOG.md`](docs/PROJECT_CATALOG.md).

**Checklist:**

- [ ] `app.py` is the single runnable entry point (`python projects/NN_project_name/app.py`)
- [ ] `app.py` has a `if __name__ == "__main__":` guard
- [ ] `app.py` uses `argparse` for any command-line arguments and implements `--help`
- [ ] All configuration comes from `.env` via `python-dotenv`; no hardcoded keys
- [ ] A `README.md` documents the project: description, requirements, run instructions, what you'll learn
- [ ] Any dependencies beyond the root `requirements.txt` are listed in a local `requirements.txt`
- [ ] At least one unit test exists in `tests/test_NN_project_name.py` that does **not** require an API key
- [ ] The project is added to `docs/PROJECT_CATALOG.md`

---

## 5. Testing Requirements

> [!IMPORTANT]
> **All tests must pass without any API keys configured.** Tests that call real APIs are not permitted in the test suite. Use mocking.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src/learn_llm --cov-report=term-missing

# Run a specific test file
pytest tests/test_config.py -v
```

### Writing Tests

- Place tests in `tests/test_<module_name>.py`.
- Use `unittest.mock.patch` or `pytest-mock` to mock all API calls.
- Test both the happy path and error cases (e.g., missing env var, API failure).
- Test names should describe the scenario: `test_load_config_raises_when_api_key_missing`.

```python
from unittest.mock import patch, MagicMock
from src.learn_llm.config import load_config

def test_load_config_raises_when_api_key_missing(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
        load_config()
```

---

## 6. Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/06-rag-chunking-lesson
   ```

2. **Make your changes.** Commit often with clear messages following [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat(lessons): add chunking strategies lesson to module 06
   fix(project-01): handle missing GEMINI_API_KEY gracefully
   docs(security): add prompt injection example
   ```

3. **Before opening the PR:**
   - [ ] `pytest tests/ -v` passes with zero failures
   - [ ] `ruff check .` reports no errors
   - [ ] Notebook output cells are cleared
   - [ ] No API keys or PII in any file
   - [ ] `CHANGELOG.md` updated under `[Unreleased]`

4. **Open the PR** against `main`. Fill in the PR template:
   - What does this change do?
   - Why is it needed?
   - How was it tested?
   - Any screenshots or example output?

5. **Review:** At least one maintainer approval is required before merging. Address review comments on the same branch with additional commits (do not force-push during review).

6. **Merge:** Maintainers will squash-merge to keep the main branch history clean.

---

## 7. What Good Lessons Look Like

Good lessons in this repository follow the design principles established in [`docs/LEARNING_ROADMAP.md`](docs/LEARNING_ROADMAP.md):

### Progressive Disclosure

Start with the simplest possible working example. Add complexity only after the learner has seen it work. Every lesson should have a runnable "minimal example" in the first few cells.

### Concept Before Code

Each code cell should be preceded by a Markdown cell explaining *what* the code does and *why*. Learners should understand the concept before they see the implementation.

### Show the Why, Not Just the How

Bad lesson: "Here is how to split text into chunks."
Good lesson: "Here is *why* chunking matters (context windows, retrieval quality), and here is how to implement it."

### Exercises With Meaningful Blanks

Exercises should ask learners to make real decisions, not just fill in function names. Blanks should require understanding, not just memorization.

### Provider Agnosticism

Where possible, lessons should work with both a cloud provider (Gemini, OpenRouter) and a local provider (Ollama), demonstrating the abstraction.

### Tested Claims

If a lesson makes a claim like "chunking with overlap improves retrieval," it should demonstrate this empirically (e.g., show retrieval quality with and without overlap on a sample document).

---

## 8. Reporting Bugs or Security Issues

### Bugs

Open a [GitHub Issue](../../issues/new) with:
- A clear title describing the problem
- Steps to reproduce (minimal example preferred)
- Expected behaviour vs. actual behaviour
- Python version, OS, and relevant package versions (`pip list | grep langchain`)

### Security Issues

> [!CAUTION]
> **Do not open a public GitHub issue for security vulnerabilities.**

If you discover a security issue — such as an API key accidentally committed, a prompt injection vulnerability in a project, or a dependency with a known CVE — please report it privately:

1. Go to the repository's **Security** tab on GitHub.
2. Click **"Report a vulnerability"** to open a private advisory.
3. Describe the issue, its potential impact, and steps to reproduce.

We will acknowledge the report within 48 hours and aim to release a fix within 7 days for critical issues. See [`docs/SECURITY.md`](docs/SECURITY.md) for the full security policy.
