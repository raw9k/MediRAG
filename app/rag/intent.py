GREETING_RESPONSES = {
    "hi": "Hello! How can I help you with a medical question?",
    "hii": "Hello! How can I help you with a medical question?",
    "hiii": "Hello! How can I help you with a medical question?",
    "hello": "Hello! How can I help you with a medical question?",
    "hey": "Hey! How can I help you with a medical question?",
    "heyy": "Hey! How can I help you with a medical question?",
    "good morning": "Good morning! How can I help you with a medical question?",
    "good afternoon": "Good afternoon! How can I help you with a medical question?",
    "good evening": "Good evening! How can I help you with a medical question?",
}

def get_greeting_response(question: str) -> str | None:
    """
    Return a greeting response if the input is a simple greeting.
    Otherwise return None.
    """
    normalized_question = question.strip().lower()

    return GREETING_RESPONSES.get(normalized_question)