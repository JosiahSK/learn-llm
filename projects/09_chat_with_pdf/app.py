"""
app.py — Project 09: Chat with PDF & Citations Engine
=====================================================
A complete RAG application with:
  1. PDF text extraction tracking page numbers
  2. Overlapping chunk segmentation
  3. Vector retrieval with metadata attribution
  4. Grounded answer generation citing source filename and page numbers
  5. Built-in fallback demo document so it runs out-of-the-box
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from learn_llm.utils.text import chunk_text


class DocumentChunk:
    """Represents a text chunk with provenance metadata."""
    def __init__(self, text: str, source: str, page: int, chunk_id: int):
        self.text = text
        self.source = source
        self.page = page
        self.chunk_id = chunk_id


def load_pdf(pdf_path: Path) -> list[DocumentChunk]:
    """Extracts text page-by-page from a PDF, segmenting each page into chunks."""
    try:
        import pypdf
    except ImportError:
        print("[WARNING] 'pypdf' is not installed. Run: pip install pypdf")
        return []

    chunks = []
    chunk_counter = 0

    try:
        reader = pypdf.PdfReader(str(pdf_path))
        if len(reader.pages) == 0:
            print(f"[ERROR] PDF '{pdf_path.name}' contains no pages.")
            return []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue

            page_chunks = chunk_text(text, chunk_size=400, chunk_overlap=50)
            for pc in page_chunks:
                chunks.append(DocumentChunk(
                    text=pc,
                    source=pdf_path.name,
                    page=page_num,
                    chunk_id=chunk_counter
                ))
                chunk_counter += 1

        return chunks
    except Exception as exc:
        print(f"[ERROR] Failed to read PDF '{pdf_path}': {exc}")
        return []


def load_demo_chunks() -> list[DocumentChunk]:
    """Loads fallback sample document if no PDF is supplied."""
    sample_path = Path(__file__).resolve().parent.parent.parent / "data" / "sample_documents" / "llm_basics.txt"
    if sample_path.exists():
        raw_text = sample_path.read_text(encoding="utf-8")
    else:
        raw_text = (
            "Large language models use transformer neural networks. "
            "They calculate probabilistic next-token predictions across a vocabulary. "
            "Context windows define the limit of tokens processed in memory. "
            "RAG pipelines retrieve relevant text to ground generation and prevent hallucinations."
        )

    raw_chunks = chunk_text(raw_text, chunk_size=300, chunk_overlap=40)
    return [
        DocumentChunk(text=c, source="llm_basics.txt", page=(idx // 2) + 1, chunk_id=idx)
        for idx, c in enumerate(raw_chunks)
    ]


def retrieve_chunks(query: str, chunks: list[DocumentChunk], top_k: int = 3) -> list[DocumentChunk]:
    """Retrieves top_k relevant chunks using keyword/term overlap scoring.
    Returns an empty list if no query terms match the document.
    """
    stopwords = {"what", "is", "the", "in", "and", "a", "an", "of", "to", "how", "why", "does", "do", "for"}
    query_terms = set(query.lower().replace("?", "").replace(".", "").split()) - stopwords
    if not query_terms:
        query_terms = set(query.lower().replace("?", "").replace(".", "").split())

    scored = []
    for c in chunks:
        chunk_words = set(c.text.lower().split())
        score = len(query_terms.intersection(chunk_words))
        if score > 0:
            scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]


def generate_grounded_answer(query: str, retrieved: list[DocumentChunk]) -> str:
    """Constructs a strict grounding prompt with citation instructions.
    Gracefully handles unsupported queries when no chunks are retrieved.
    """
    if not retrieved:
        return "I cannot find the answer in the provided document."

    api_key = os.getenv("GEMINI_API_KEY")

    # Build formatted context block with citations
    context_blocks = []
    for c in retrieved:
        context_blocks.append(f"[{c.source} | Page {c.page}]:\n\"{c.text}\"")

    context_str = "\n\n".join(context_blocks)

    prompt = (
        "You are an evidence-grounded research assistant.\n"
        "Instructions:\n"
        "1. Answer the question relying ONLY on the provided context passages.\n"
        "2. For every factual claim, cite the source in the format: [Source: <filename>, Page <X>].\n"
        "3. If the context does not contain the answer, explicitly state: "
        "'I cannot find the answer in the provided document.' Do not guess.\n\n"
        f"Context:\n{context_str}\n\n"
        f"Question: {query}\n"
        "Grounded Answer:"
    )

    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
            resp = client.models.generate_content(model=model_id, contents=prompt)
            return resp.text
        except Exception as e:
            return (
                f"[Cloud LLM Error: {e}]\n"
                f"Fallback Grounded Citation: Found in [Source: {retrieved[0].source}, Page {retrieved[0].page}]"
            )
    else:
        # Transparent deterministic offline fallback: extract the most relevant complete sentence
        clean_text = retrieved[0].text.strip()
        sentences = [s.strip() for s in clean_text.split(".") if len(s.strip().split()) >= 4]
        if sentences:
            q_terms = set(query.lower().split())
            best_sentence = max(sentences, key=lambda s: len(q_terms.intersection(set(s.lower().split()))))
        else:
            best_sentence = clean_text[:120]
        return (
            f"{best_sentence}. [Source: {retrieved[0].source}, Page {retrieved[0].page}]"
        )


def main():
    parser = argparse.ArgumentParser(description="Chat with PDF and Citations Engine")
    parser.add_argument("--pdf", type=str, help="Path to a PDF file", default=None)
    args = parser.parse_args()

    print("=" * 65)
    print("Project 09: Chat with PDF & Source Citation Engine")
    print("=" * 65)

    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"[ERROR] File '{pdf_path}' not found.")
            sys.exit(1)
        print(f"Ingesting PDF: {pdf_path.name}...")
        chunks = load_pdf(pdf_path)
    else:
        print("[No --pdf provided: Loading bundled sample document (data/sample_documents/llm_basics.txt)]")
        chunks = load_demo_chunks()

    print(f"Indexed {len(chunks)} chunks across document pages.\n")
    print("Ask questions about the document (type 'exit' to quit):\n")

    while True:
        try:
            query = input("Ask > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            break

        retrieved = retrieve_chunks(query, chunks, top_k=2)
        answer = generate_grounded_answer(query, retrieved)

        print("\nAnswer:")
        print("-" * 60)
        print(answer)
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
