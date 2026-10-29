"""
01_rag_pipeline.py — End-to-End Minimal RAG Pipeline
===================================================
A self-contained implementation walking through each stage of RAG:
  Ingest -> Chunk -> Embed -> Index -> Retrieve -> Grounded Generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from learn_llm.utils.text import chunk_text


def main():
    print("=" * 60)
    print("Module 13: Retrieval-Augmented Generation (RAG) Pipeline")
    print("=" * 60)

    # 1. Source Knowledge Document
    raw_document = (
        "The Gemini 3.6 Flash model is optimized for high-frequency, low-latency agentic tasks. "
        "It supports multimodal inputs including audio, video, images, and text. "
        "The context window accommodates up to 1,000,000 tokens in standard production tiers. "
        "For offline local development, Ollama enables running quantized GGUF weights directly on CPU or GPU."
    )

    print("\n[Step 1: Document Ingestion]")
    print(f"Loaded source text ({len(raw_document)} characters)")

    # 2. Chunking
    chunks = chunk_text(raw_document, chunk_size=120, chunk_overlap=20)
    print(f"\n[Step 2: Chunking]")
    for i, c in enumerate(chunks):
        print(f"  Chunk [{i}]: '{c}'")

    # 3. Simulated Retrieval for User Query
    query = "What is the context window of Gemini 3.6 Flash?"
    print(f"\n[Step 3: Query & Retrieval]")
    print(f"User Query: '{query}'")

    # Rank chunks by simple keyword overlap heuristic for transparent offline demo
    query_terms = set(query.lower().split())
    scored = []
    for idx, c in enumerate(chunks):
        score = sum(1 for term in query_terms if term in c.lower())
        scored.append((score, idx, c))
    scored.sort(key=lambda x: x[0], reverse=True)

    top_chunk = scored[0]
    print(f"Retrieved Most Relevant Chunk (ID #{top_chunk[1]}):")
    print(f"  '{top_chunk[2]}'")

    # 4. Augmented Generation Prompt
    augmented_prompt = (
        f"You are a helpful assistant. Use ONLY the provided context to answer the question.\n"
        f"Context: {top_chunk[2]}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

    print("\n[Step 4: Augmented Prompt Assembly]")
    print("-" * 50)
    print(augmented_prompt)
    print("-" * 50)

    print("\n[Step 5: Grounded Answer Synthesis]")
    print("Grounded Answer: According to the provided context, the context window accommodates up to 1,000,000 tokens.")
    print("\n[Key Takeaway] RAG eliminates hallucinations by grounding answers strictly in retrieved evidence.")


if __name__ == "__main__":
    main()
