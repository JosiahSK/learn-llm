# Module 12 — Embeddings and Vector Search

> **Goal:** Understand what an embedding is, how models map text to vectors that encode meaning, what cosine similarity measures, and when to use vector search vs keyword search.

---

## 1. What is an Embedding?

An **embedding** is a list of numbers (a vector) that represents the *meaning* of a piece of text in a high-dimensional space.

```
"The cat sat on the mat."
         ↓  embedding model
[0.023, -0.451, 0.817, 0.003, -0.192, ..., 0.341]
         ↑ typically 768 to 3072 numbers
```

The key insight: **semantically similar texts produce numerically similar vectors.**

```
distance("The cat sat on the mat.", "A feline rested on the rug.") → small
distance("The cat sat on the mat.", "Neural networks backpropagate.") → large
```

The embedding model has learned during training that cats and felines refer to similar concepts, so it places their vectors close together in the high-dimensional space.

---

## 2. How Embedding Models Map Text to Vector Space

The process is:

1. Tokenise the input text.
2. Pass tokens through a transformer model (typically an encoder-only model like BERT or a bi-encoder).
3. Pool the token representations (often mean-pooling or CLS-token).
4. Output a fixed-length vector regardless of input length.

Unlike chat models that generate new tokens, embedding models are **deterministic** — the same text always produces the same vector (given the same model version).

Popular embedding models:

| Model | Dimensions | Provider |
|-------|-----------|---------|
| `text-embedding-3-small` | 1536 | OpenAI |
| `text-embedding-3-large` | 3072 | OpenAI |
| `models/text-embedding-004` | 768 | Google |
| `nomic-embed-text` | 768 | Ollama (local) |
| `all-MiniLM-L6-v2` | 384 | HuggingFace (local) |

---

## 3. Cosine Similarity Explained Intuitively

Cosine similarity measures the **angle** between two vectors, not the distance between their endpoints.

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)
```

- Result is always between **-1** and **1**.
- **1.0** → identical direction (same meaning).
- **0.0** → perpendicular (unrelated).
- **-1.0** → opposite direction (opposite meaning).

Why cosine and not Euclidean distance? Because we care about direction, not magnitude. A long document and a short document about the same topic should be considered similar — cosine handles this naturally.

```
"I love pizza"  →  [0.8, 0.2, ...]
"Pizza is my favourite food"  →  [0.75, 0.25, ...]
cosine_similarity → 0.97  ✅  very similar

"I love pizza"  →  [0.8, 0.2, ...]
"The stock market crashed"  →  [-0.1, 0.9, ...]
cosine_similarity → 0.12  ✅  unrelated
```

---

## 4. Why Similar Sentences Have Similar Vectors

Embedding models are trained on enormous corpora with objectives that force semantically related text to cluster. Common training methods:

- **Contrastive learning:** pairs of similar sentences are pulled closer; dissimilar pairs are pushed apart.
- **MNLI fine-tuning:** model learns which sentences entail or contradict each other.
- **RLHF-based methods:** human preference data guides similarity judgements.

The result: the model encodes **concepts**, not just surface-level words. Synonyms, paraphrases, and translations of the same idea end up near each other.

---

## 5. Dimensionality and What It Means

An embedding with **768 dimensions** lives in a 768-dimensional space. Each dimension (loosely) encodes some latent feature of meaning — though unlike hand-crafted features, the dimensions are not individually interpretable.

Higher dimensionality:
- ✅ Can encode more nuanced distinctions
- ✅ Better recall on hard retrieval tasks
- ❌ More storage per vector
- ❌ Slower similarity search at scale

For most applications, **768–1536 dimensions** is a practical sweet spot.

---

## 6. Chunking Trade-offs for Embeddings

Embedding models have their own token limits (typically 512–8192 tokens). Long documents must be split into **chunks** before embedding.

| Chunk size | Pros | Cons |
|-----------|------|------|
| Small (128 tokens) | High precision retrieval | May lose context; more chunks to manage |
| Medium (256–512 tokens) | Good balance | Standard choice |
| Large (1024+ tokens) | More context per chunk | Dilutes the embedding; harder to retrieve specific info |

**Overlap** between chunks (e.g., 50-token overlap) prevents information from being cut off at boundaries.

---

## 7. When to Use Vector Search vs Keyword Search

| Situation | Use vector search | Use keyword search |
|-----------|------------------|--------------------|
| Semantic queries ("feelings of loneliness") | ✅ | ❌ |
| Exact term lookup ("invoice #12345") | ❌ | ✅ |
| Paraphrase matching | ✅ | ❌ |
| Boolean filters (date range, category) | ❌ needs hybrid | ✅ |
| Cross-lingual search | ✅ | ❌ |
| Fast exact matching at scale | ❌ | ✅ (inverted index) |

**Hybrid search** (BM25 + vector) often outperforms either alone. Most production RAG systems use hybrid.

---

## 8. ⚠️ Embedding Model Compatibility

**You must use the same embedding model for both indexing and querying.** If you embed your documents with `text-embedding-3-small` and then query with `text-embedding-3-large`, the vectors live in different spaces and similarity scores are meaningless.

> This also applies to model versions. If the provider updates `text-embedding-3-small`, your existing vectors may silently become incompatible. Pin your embedding model version in production.

---

## 9. Exercises

### Exercise 1 — Similarity Explorer
Run `01_embedding_explorer.py`. Find two sentences that you expect to be similar. Are they? Find two that look superficially similar but mean different things.

### Exercise 2 — ASCII Heatmap
Study the heatmap output. Which sentence cluster is the tightest? Which sentences are most isolated?

### Exercise 3 — Query Ranking
Change the query sentence in the script. How does the ranking change? Does the top result always make intuitive sense?

### Exercise 4 — Real Embeddings (Ollama)
If you have Ollama installed, run `ollama pull nomic-embed-text` and enable the real-embedding path in the script. Compare the similarity rankings against the mock embeddings.

### Exercise 5 — Chunking
Write a function that takes a long paragraph, splits it into overlapping chunks of 50 words with a 10-word overlap, and prints each chunk with its chunk index.

---

## Key Takeaways

- An embedding is a **vector of numbers encoding meaning**, not just keywords.
- **Cosine similarity** measures how semantically similar two texts are (1 = identical, 0 = unrelated).
- Higher dimensionality = more expressive but slower to search.
- Chunk documents before embedding; chunk size is a trade-off between precision and context.
- Always use the **same model** for indexing and querying.
- Vector search excels at semantic/paraphrase retrieval; keyword search wins for exact matches.
