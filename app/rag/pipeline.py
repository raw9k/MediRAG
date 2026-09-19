from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model
from app.llm.groq import generate_answer


VECTORSTORE_PATH = "vectorstore"


# Load once when the application imports this module
embedding_model = get_embedding_model()

vector_store = FAISS.load_local(
    VECTORSTORE_PATH,
    embedding_model,
    allow_dangerous_deserialization=True,
)


def retrieve_documents(question: str, k: int = 3):
    return vector_store.similarity_search(question, k=k)


def build_context(documents) -> str:
    return "\n\n".join(
        f"Source page: {doc.metadata.get('page')}\n"
        f"{doc.page_content}"
        for doc in documents
    )


def build_sources(documents) -> list[str]:
    sources = []

    for document in documents:
        page = document.metadata.get("page")

        if page is not None:
            sources.append(
                f"The Gale Encyclopedia of Medicine — Page {page + 1}"
            )

    return list(dict.fromkeys(sources))


def answer_question(question: str, k: int = 3):
    documents = retrieve_documents(question, k=k)

    context = build_context(documents)

    answer = generate_answer(
        context=context,
        question=question,
    )

    sources = build_sources(documents)

    return answer, sources