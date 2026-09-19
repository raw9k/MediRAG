from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model


VECTORSTORE_PATH = "vectorstore"


def test_diabetes_retrieval():
    embedding_model = get_embedding_model()

    vector_store = FAISS.load_local(
        VECTORSTORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    query = "What are the symptoms of diabetes?"

    results = vector_store.similarity_search(query, k=3)

    assert len(results) == 3

    for document in results:
        assert document.page_content.strip()
        assert "page" in document.metadata
        assert "source" in document.metadata

    combined_text = " ".join(
        document.page_content.lower() for document in results
    )

    assert "symptoms" in combined_text
    assert "diabetes" in combined_text