"""
test_pdf_rag.py — Comprehensive Unit & Integration Tests for RAG & PDF Processing
=================================================================================
Tests:
  1. PDF text extraction & page-number tracking
  2. Empty / corrupt / unreadable PDF handling
  3. Chunking & boundary overlap preservation
  4. Provenance metadata (source filename and page numbers)
  5. Retrieval & grounded citation construction
  6. Unsupported question detection
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure src and projects/09_chat_with_pdf are discoverable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "projects" / "09_chat_with_pdf"))

from app import DocumentChunk, load_pdf, load_demo_chunks, retrieve_chunks, generate_grounded_answer
from learn_llm.utils.text import chunk_text


class TestChunkingAndProvenance:
    """Tests chunking boundary logic and metadata retention."""

    def test_chunk_text_preserves_overlap(self):
        text = "Wordone wordtwo wordthree wordfour wordfive wordsix wordseven"
        chunks = chunk_text(text, chunk_size=30, chunk_overlap=10)
        assert len(chunks) >= 2
        # Verify that trailing words from chunk 0 appear in chunk 1
        last_word_c0 = chunks[0].split()[-1]
        assert last_word_c0 in chunks[1]

    def test_document_chunk_metadata_attributes(self):
        chunk = DocumentChunk(text="Sample content", source="test.pdf", page=3, chunk_id=12)
        assert chunk.text == "Sample content"
        assert chunk.source == "test.pdf"
        assert chunk.page == 3
        assert chunk.chunk_id == 12

    def test_load_demo_chunks_assigns_valid_pages(self):
        demo_chunks = load_demo_chunks()
        assert len(demo_chunks) > 0
        for c in demo_chunks:
            assert c.page >= 1
            assert c.source == "llm_basics.txt"
            assert len(c.text.strip()) > 0


class TestPDFExtractionAndErrorHandling:
    """Tests PDF parsing edge cases: missing, empty, or corrupt files."""

    def test_load_pdf_returns_empty_when_file_not_found(self):
        missing_path = Path("non_existent_file.pdf")
        chunks = load_pdf(missing_path)
        assert chunks == []

    def test_load_pdf_handles_empty_page_list(self):
        mock_pypdf = MagicMock()
        mock_reader = MagicMock()
        mock_reader.pages = []
        mock_pypdf.PdfReader.return_value = mock_reader
        with patch.dict("sys.modules", {"pypdf": mock_pypdf}):
            chunks = load_pdf(Path("empty.pdf"))
            assert chunks == []

    def test_load_pdf_handles_corrupt_stream(self):
        mock_pypdf = MagicMock()
        mock_pypdf.PdfReader.side_effect = Exception("Corrupt PDF header")
        with patch.dict("sys.modules", {"pypdf": mock_pypdf}):
            chunks = load_pdf(Path("corrupt.pdf"))
            assert chunks == []

    def test_load_pdf_extracts_and_preserves_page_numbers(self):
        page1 = MagicMock()
        page1.extract_text.return_value = "Page one content detailing neural networks."
        page2 = MagicMock()
        page2.extract_text.return_value = "Page two content discussing vector embeddings."

        mock_pypdf = MagicMock()
        mock_reader = MagicMock()
        mock_reader.pages = [page1, page2]
        mock_pypdf.PdfReader.return_value = mock_reader

        with patch.dict("sys.modules", {"pypdf": mock_pypdf}):
            chunks = load_pdf(Path("sample_doc.pdf"))
            assert len(chunks) >= 2
            assert chunks[0].page == 1
            assert "Page one" in chunks[0].text
            assert any(c.page == 2 for c in chunks)


class TestRetrievalAndCitations:
    """Tests retrieval precision, grounded citation construction, and unsupported query handling."""

    def test_retrieval_matches_relevant_chunk(self):
        chunks = [
            DocumentChunk(text="Transformers utilize attention mechanisms.", source="doc.pdf", page=1, chunk_id=0),
            DocumentChunk(text="Convolutional layers process visual images.", source="doc.pdf", page=2, chunk_id=1),
            DocumentChunk(text="Reinforcement learning relies on reward signals.", source="doc.pdf", page=3, chunk_id=2),
        ]
        results = retrieve_chunks("How does attention work in transformers?", chunks, top_k=1)
        assert len(results) == 1
        assert results[0].page == 1
        assert "Transformers" in results[0].text

    def test_retrieval_returns_empty_for_unrelated_query(self):
        chunks = [
            DocumentChunk(text="Python syntax uses significant indentation.", source="python.pdf", page=1, chunk_id=0),
        ]
        results = retrieve_chunks("quantum superposition Hamiltonian matrix", chunks, top_k=1)
        assert results == []

    def test_generate_grounded_answer_unsupported_query(self):
        answer = generate_grounded_answer("unsupported question", retrieved=[])
        assert answer == "I cannot find the answer in the provided document."

    def test_generate_grounded_answer_offline_includes_citation(self):
        chunk = DocumentChunk(
            text="The context window defines the maximum number of tokens. It operates as working memory.",
            source="manual.pdf",
            page=4,
            chunk_id=5
        )
        answer = generate_grounded_answer("context window", retrieved=[chunk])
        assert "[Source: manual.pdf, Page 4]" in answer
        assert "The context window defines the maximum number of tokens" in answer
