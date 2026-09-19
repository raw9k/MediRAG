from evaluation.test_cases import EVALUATION_CASES

from app.rag.pipeline import (
    answer_question,
    retrieve_documents,
)
from app.rag.query_rewriter import rewrite_query
from app.rag.intent import get_greeting_response


def test_evaluation_cases():
    for case in EVALUATION_CASES:
        question = case["question"]
        history = case["history"]
        expected = case["expected"]

        if expected == "greeting":
            response = get_greeting_response(question)

            assert response is not None, (
                f"Expected greeting for: {question}"
            )

        elif expected == "no_retrieval":
            documents = retrieve_documents(
                question,
                k=3,
            )

            assert documents == [], (
                f"Expected no retrieval for: {question}"
            )

            answer, sources = answer_question(
                question=question,
                history=history,
            )

            assert (
                "does not provide enough information"
                in answer.lower()
            )

            assert sources == []

        elif expected == "retrieve":
            documents = retrieve_documents(
                rewrite_query(
                    question,
                    history,
                ),
                k=3,
            )

            assert len(documents) > 0, (
                f"Expected retrieval for: {question}"
            )

            answer, sources = answer_question(
                question=question,
                history=history,
            )

            assert isinstance(answer, str)
            assert len(answer) > 0
            assert len(sources) > 0