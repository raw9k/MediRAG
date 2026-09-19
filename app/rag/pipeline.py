from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model
from app.llm.grok import generate_answer


VECTORSTORE_PATH = "vectorstore"


def retrieve_documents(question: str, k: int = 3):
    embedding_model = get_embedding_model()

    vector_store = FAISS.load_local(
        VECTORSTORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    return vector_store.similarity_search(question, k=k)


def build_context(documents) -> str:
    return "\n\n".join(
        f"Source page: {doc.metadata.get('page')}\n{doc.page_content}"
        for doc in documents
    )


def answer_question(question: str, k: int = 3) -> str:
    documents = retrieve_documents(question, k=k)
    context = build_context(documents)

    return generate_answer(
        context=context,
        question=question,
    )