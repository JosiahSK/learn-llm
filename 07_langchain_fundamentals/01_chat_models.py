"""
01_chat_models.py — LangChain Chat Models and the LCEL Standard
==============================================================
Demonstrates how LangChain abstracts different LLM providers using
standardized ChatModel interfaces and LangChain Expression Language (LCEL).
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    print("=" * 60)
    print("Module 07: LangChain Fundamentals — Chat Models & LCEL")
    print("=" * 60)

    try:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
    except ImportError:
        print("[ERROR] LangChain core is not installed. Run: pip install langchain-core")
        sys.exit(1)

    print("\n1. Defining reusable ChatPromptTemplate with parameters...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on software engineering best practices. Be concise."),
        ("user", "Explain the concept of {concept} in two sentences.")
    ])

    print("2. Constructing an LCEL Runnable pipeline (Prompt | Model | Parser)...")
    parser = StrOutputParser()

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model = ChatGoogleGenerativeAI(
                model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
                google_api_key=api_key,
            )
            chain = prompt | model | parser
            print("\n3. Invoking Chain with concept='Inversion of Control'...")
            result = chain.invoke({"concept": "Inversion of Control"})
            print("\nResult:")
            print("-" * 50)
            print(result)
            print("-" * 50)
        except Exception as e:
            print(f"[API Error running LangChain]: {e}")
    else:
        print("\n[NOTE] No active GEMINI_API_KEY detected.")
        print("LangChain pipeline structure was compiled successfully:")
        print(f"  Pipe: {prompt.__class__.__name__} | <ChatModel> | {parser.__class__.__name__}")


if __name__ == "__main__":
    main()
