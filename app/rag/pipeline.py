from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model
from app.llm.groq import generate_answer
from app.rag.intent import get_greeting_response
from app.rag.query_rewriter import rewrite_query

VECTORSTORE_PATH = "vectorstore"

MEDICAL_DISCLAIMER = (
    "This information is for educational purposes only and is not "
    "a substitute for professional medical advice, diagnosis, or treatment."
)


# Load embedding model once when the application imports this module
embedding_model = get_embedding_model()

# Load FAISS vector store once
vector_store = FAISS.load_local(
    VECTORSTORE_PATH,
    embedding_model,
    allow_dangerous_deserialization=True,
)


def retrieve_documents(
    question: str,
    k: int = 3,
    score_threshold: float = 0.85,
):
    candidate_k = max(k * 3, 10)

    results = vector_store.similarity_search_with_score(
        question,
        k=candidate_k,
    )

    documents = []

    seen_pages = set()

    for document, score in results:
        if score > score_threshold:
            continue

        page = document.metadata.get("page")

        # Avoid returning multiple chunks from the same page.
        if page in seen_pages:
            continue

        seen_pages.add(page)
        documents.append(document)

        if len(documents) >= k:
            break

    return documents

def build_context(documents) -> str:
    context_parts = []

    for index, document in enumerate(documents, start=1):
        page = document.metadata.get("page")

        if page is not None:
            page_number = page + 1
        else:
            page_number = "Unknown"

        context_parts.append(
            f"SOURCE {index}\n"
            f"Page: {page_number}\n"
            f"{'-' * 40}\n"
            f"{document.page_content.strip()}"
        )

    return "\n\n".join(context_parts)

def build_sources(documents) -> list[str]:
    """
    Build human-readable source references.
    """
    sources = []

    for document in documents:
        page = document.metadata.get("page")

        if page is not None:
            sources.append(
                f"The Gale Encyclopedia of Medicine — Page {page + 1}"
            )

    return list(dict.fromkeys(sources))

def answer_question(
    question: str,
    history: list[dict] | None = None,
    k: int = 3,
):
    greeting_response = get_greeting_response(question)

    if greeting_response:
        return greeting_response, []

    history = history or []

    search_query = rewrite_query(
        question=question,
        history=history,
    )

    documents = retrieve_documents(
        search_query,
        k=k,
    )

    if not documents:
        return (
            "The available medical context does not provide enough "
            "information to answer this question.",
            [],
        )

    context = build_context(documents)

    answer = generate_answer(
        context=context,
        question=question,
    )

    answer = f"{answer}\n\n{MEDICAL_DISCLAIMER}"

    sources = build_sources(documents)

    return answer, sources