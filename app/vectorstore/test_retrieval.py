from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model


VECTORSTORE_PATH = "vectorstore"


def main():
    print("Loading embedding model...")
    embedding_model = get_embedding_model()

    print("Loading FAISS vector store...")
    vector_store = FAISS.load_local(
        VECTORSTORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    query = "What are the symptoms of diabetes?"

    print(f"\nQuery: {query}")
    print("\nSearching...\n")

    results = vector_store.similarity_search(query, k=3)

    for i, document in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(f"Page: {document.metadata.get('page')}")
        print(f"Source: {document.metadata.get('source')}")
        print(document.page_content[:1000])
        print()


if __name__ == "__main__":
    main()