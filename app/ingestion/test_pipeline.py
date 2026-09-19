from pathlib import Path

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import split_documents


pdf_path = Path("data/raw/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf")

documents = load_pdf(str(pdf_path))
chunks = split_documents(documents)

print(f"Pages: {len(documents)}")
print(f"Chunks: {len(chunks)}")

print("\nFirst page metadata:")
print(documents[0].metadata)

print("\nFirst chunk:")
print(chunks[0].page_content)

print("\nFirst chunk metadata:")
print(chunks[0].metadata)

print("\n--- First Substantial Chunk ---")

for i, chunk in enumerate(chunks):
    if len(chunk.page_content) > 400:
        print(f"\n--- Chunk {i} ---")
        print(f"Page: {chunk.metadata.get('page')}")
        print(f"Length: {len(chunk.page_content)}")
        print(chunk.page_content)
        break