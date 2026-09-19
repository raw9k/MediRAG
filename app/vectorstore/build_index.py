from pathlib import Path

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import split_documents
from app.vectorstore.faiss_store import create_vector_store


PDF_PATH = Path(
    "data/raw/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"
)

VECTORSTORE_PATH = "vectorstore"


def main():
    print("Loading PDF...")
    documents = load_pdf(str(PDF_PATH))

    print("Creating chunks...")
    chunks = split_documents(documents)

    print(f"Pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    print("Creating FAISS vector store...")
    vector_store = create_vector_store(chunks)

    print("Saving vector store...")
    vector_store.save_local(VECTORSTORE_PATH)

    print(f"Vector store saved to: {VECTORSTORE_PATH}")


if __name__ == "__main__":
    main()