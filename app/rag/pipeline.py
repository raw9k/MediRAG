from langchain_community.vectorstores import FAISS

from app.embeddings.embedder import get_embedding_model
from app.llm.groq import generate_answer


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
    score_threshold: float = 0.80,
):
    """
    Retrieve relevant documents using FAISS similarity search
    and filter out documents above the distance threshold.
    """
    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    documents = [
        document
        for document, score in results
        if score <= score_threshold
    ]

    return documents


def build_context(documents) -> str:
    """
    Build the context passed to the LLM.
    """
    return "\n\n".join(
        f"Source page: {doc.metadata.get('page')}\n"
        f"{doc.page_content}"
        for doc in documents
    )


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


def answer_question(question: str, k: int = 3):
    """
    Retrieve relevant medical context and generate
    an evidence-grounded answer.
    """
    documents = retrieve_documents(
        question,
        k=k,
    )

    # Handle questions for which the knowledge base
    # does not contain sufficiently relevant information.
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

    # Add a deterministic medical disclaimer.
    answer = f"{answer}\n\n{MEDICAL_DISCLAIMER}"

    sources = build_sources(documents)

    return answer, sources