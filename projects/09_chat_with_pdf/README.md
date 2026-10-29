# Project 09 — Chat with PDF & Provenance Citation Engine

A foundational, self-contained Retrieval-Augmented Generation (RAG) assistant that parses documents, tracks page metadata, segments text with boundary overlap, retrieves relevant passages, and produces answers with exact source citations.

---

## 1. Pipeline Architecture

```
[ PDF Document / Text Sample ]
       │
       ▼ (pypdf: extract text preserving page numbers)
[ Page Chunks ] ── (attach provenance: source filename, page_number, chunk_id)
       │
       ▼ (learn_llm.utils.text.chunk_text: sliding window with overlap)
[ Text Chunks ]
       │
       ▼ (Current implementation: Lexical Term-Overlap Retrieval)
[ In-Memory Index ] ◄── (Planned: Dense vector embeddings via ChromaDB / nomic-embed-text)
       │
   (User Query) ──► [ Lexical Scorer (Stopword-filtered term intersection) ]
                               │
                               ▼
               [ Evidence Passages (Top-K) ]
                               │
                               ▼
               [ Grounded Answer + [Source: file, Page X] Citations ]
```

---

## 2. Retrieval Implementation Details & Honesty

- **Current Retrieval Backend:** **Lexical / Term-Overlap Retrieval**. The current implementation tokenizes queries into content words (filtering common English stopwords) and computes keyword overlap intersections against document chunks.
- **Why Lexical Demo First?** It runs completely offline without downloading 500MB embedding weights or requiring vector database binaries, guaranteeing reproducible testing across all operating systems.
- **Limitation:** Lexical retrieval relies on word overlap; it cannot detect conceptual synonyms (e.g., querying "canine" won't match "dog" without shared vocabulary).
- **Roadmap Extension:** Module 12 (`12_embeddings_and_vector_search/`) introduces dense embedding spaces, and Module 14 will migrate this pipeline to ChromaDB with local embeddings.
- **Grounding Disclaimer:** A formatted citation string `[Source: file, Page X]` demonstrates that provenance metadata was preserved and formatted; it does **not** constitute mathematical proof of factual grounding. Always evaluate response truthfulness against source text.

---

## 3. Requirements & Usage

```bash
# Run with the included sample corpus (offline demo, no PDF required):
python projects/09_chat_with_pdf/app.py

# Run with your own PDF:
python projects/09_chat_with_pdf/app.py --pdf path/to/document.pdf
```
