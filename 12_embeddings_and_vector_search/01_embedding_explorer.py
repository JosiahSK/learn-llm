"""
01_embedding_explorer.py — Vector Similarity & Semantic Geometry
===============================================================
Demonstrates what embeddings represent, how semantic proximity is quantified,
and calculates cosine similarities across an offline text corpus.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Computes the cosine angle between two high-dimensional vectors."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def build_bow_embedding(text: str, vocab: list[str]) -> list[float]:
    """Simple term-frequency vector mapping for transparent offline mathematical demonstration."""
    words = text.lower().replace(".", "").replace(",", "").split()
    return [float(words.count(term)) for term in vocab]


def main():
    print("=" * 60)
    print("Module 12: Embeddings & Vector Similarity Space")
    print("=" * 60)

    corpus = [
        "The golden retriever ran across the sunny park.",
        "A playful puppy dashed through the grassy garden.",
        "Deep learning models require GPUs for accelerated matrix multiplication.",
        "NVIDIA graphics processors speed up neural network training.",
        "Apple pie recipes require fresh cinnamon and sugar.",
    ]

    # Shared vocabulary across all sentences
    all_words = sorted(list(set(" ".join(corpus).lower().replace(".", "").split())))
    vectors = [build_bow_embedding(doc, all_words) for doc in corpus]

    query = "training machine learning networks with hardware"
    query_vec = build_bow_embedding(query, all_words)

    print(f"Target Query: '{query}'\n")
    print("Ranked Documents by Semantic / Lexical Proximity:")
    print("-" * 60)

    scored = []
    for doc, vec in zip(corpus, vectors):
        sim = cosine_similarity(query_vec, vec)
        scored.append((sim, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    for rank, (score, doc) in enumerate(scored, 1):
        print(f"#{rank} [Score: {score:.3f}] {doc}")

    print("-" * 60)
    print("\n[Principle] High dimensional embeddings encode semantic meaning such that")
    print("synonyms and related concepts cluster nearby in vector space.")


if __name__ == "__main__":
    main()
