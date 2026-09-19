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
    
    
def test_retrieval_returns_relevant_documents():
    from app.rag.pipeline import retrieve_documents

    results = retrieve_documents(
        "What are the symptoms of diabetes?",
        k=5,
        score_threshold=0.80,
    )

    assert len(results) > 0
    assert len(results) <= 5

    combined_text = " ".join(
        document.page_content.lower()
        for document in results
    )

    assert "diabetes" in combined_text
    
def test_out_of_context_question():
    from app.rag.pipeline import answer_question

    answer, sources = answer_question(
        "What is the capital of France?"
    )

    assert (
        "does not provide enough information"
        in answer.lower()
    )

    assert sources == []
    
def test_greeting_response():
    from app.rag.pipeline import answer_question

    answer, sources = answer_question("hi")

    assert "hello" in answer.lower()
    assert sources == []
    
def test_hello_response():
    from app.rag.pipeline import answer_question

    answer, sources = answer_question("hello")

    assert "hello" in answer.lower()
    assert sources == []