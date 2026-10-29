"""
01_token_explorer.py — Tokens, Subwords, and Cost Computation
============================================================
Teaches how subword tokenizers (like Byte-Pair Encoding) partition text,
why word counts differ from token counts, and how token metrics affect pricing.
Runs completely offline!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def simple_bpe_tokenize(text: str) -> list[str]:
    """A clear educational heuristic demonstrating subword slicing when tiktoken is absent."""
    tokens = []
    for word in text.split(" "):
        if len(word) > 5:
            tokens.append(word[:4])
            tokens.append(word[4:])
        else:
            tokens.append(word)
    return tokens


def main():
    print("=" * 60)
    print("Module 11: Token Explorer & Subword Mechanics")
    print("=" * 60)

    sample_strings = [
        "Artificial Intelligence",
        "def compute_fibonacci(n: int) -> int:",
        "Special characters: [API_KEY] <eos> #LLM",
        "unconstitutional",
    ]

    try:
        import tiktoken
        encoder = tiktoken.get_encoding("cl100k_base")
        use_tiktoken = True
        print("[Engine: tiktoken (cl100k_base)]\n")
    except ImportError:
        use_tiktoken = False
        print("[Engine: Standalone Educational Tokenizer (Install tiktoken for exact BPE)]\n")

    for sample in sample_strings:
        if use_tiktoken:
            token_ids = encoder.encode(sample)
            subwords = [encoder.decode([tid]) for tid in token_ids]
        else:
            subwords = simple_bpe_tokenize(sample)
            token_ids = [hash(s) % 100000 for s in subwords]

        print(f"Text: '{sample}'")
        print(f"  Character Count: {len(sample)}")
        print(f"  Word Count:      {len(sample.split(' '))}")
        print(f"  Token Count:     {len(token_ids)}")
        print(f"  Tokens Slices:   {subwords}")
        print(f"  Token IDs:       {token_ids}")
        print("-" * 50)


if __name__ == "__main__":
    main()
