from pathlib import Path

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import split_documents


PDF_PATH = Path("data/raw/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf")


def test_pdf_exists():
    assert PDF_PATH.exists()


def test_pdf_loading():
    documents = load_pdf(str(PDF_PATH))

    assert len(documents) > 0
    assert documents[0].page_content.strip()


def test_document_chunking():
    documents = load_pdf(str(PDF_PATH))
    chunks = split_documents(documents)

    assert len(chunks) > len(documents)
    assert all(chunk.page_content.strip() for chunk in chunks)