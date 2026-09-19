import re


def get_previous_user_question(history: list[dict]) -> str | None:
    """Return the most recent user question from conversation history."""

    for message in reversed(history):
        if message.get("role") == "user":
            content = message.get("content", "").strip()

            if content:
                return content

    return None


def extract_topic(question: str) -> str | None:
    """
    Extract the main topic from the previous user question.

    The function is intentionally conservative. If a clear topic
    cannot be identified, it returns None.
    """

    question = question.strip().rstrip("?.")

    patterns = [
        r"(?:symptoms|signs)\s+of\s+(.+)",
        r"(?:causes|cause)\s+of\s+(.+)",
        r"(?:treatment|treatments)\s+for\s+(.+)",
        r"(?:prevention|prevent)\s+(?:of|for)?\s*(.+)",
        r"(?:risk factors)\s+for\s+(.+)",
        r"(?:what is|what are)\s+(.+)",
        r"(?:about)\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            question,
            re.IGNORECASE,
        )

        if match:
            topic = match.group(1).strip()

            if topic:
                return topic

    return None


def rewrite_query(
    question: str,
    history: list[dict],
) -> str:
    """
    Rewrite short follow-up questions using the previous user question.

    Examples:

        What about type 2?
        -> What about type 2 diabetes?

        How can it be prevented?
        -> How can diabetes be prevented?

        What about children?
        -> What about children regarding asthma?

    If the question is not a follow-up or the previous topic
    cannot be identified, the original question is returned.
    """

    question = question.strip()

    # No conversation history
    if not history:
        return question

    previous_question = get_previous_user_question(history)

    # No previous user question
    if not previous_question:
        return question

    normalized_question = question.lower()

    topic = extract_topic(previous_question)

    # ---------------------------------------------------------
    # 1. Explicit "type 1" follow-up
    # ---------------------------------------------------------
    if re.search(
        r"\btype\s*1\b",
        normalized_question,
    ):
        if topic:
            return re.sub(
                r"\btype\s*1\b",
                f"type 1 {topic}",
                question,
                flags=re.IGNORECASE,
            )

    # ---------------------------------------------------------
    # 2. Explicit "type 2" follow-up
    # ---------------------------------------------------------
    if re.search(
        r"\btype\s*2\b",
        normalized_question,
    ):
        if topic:
            return re.sub(
                r"\btype\s*2\b",
                f"type 2 {topic}",
                question,
                flags=re.IGNORECASE,
            )

    # ---------------------------------------------------------
    # 3. Vague references:
    #    it, this, that, these, those, they, them, its
    # ---------------------------------------------------------
    if re.search(
        r"\b(it|this|that|these|those|they|them|its)\b",
        normalized_question,
    ):
        if topic:
            rewritten_question = re.sub(
                r"\b(it|this|that|these|those|they|them|its)\b",
                topic,
                question,
                flags=re.IGNORECASE,
            )

            return rewritten_question

    # ---------------------------------------------------------
    # 4. "What about..." / "How about..." follow-up
    # ---------------------------------------------------------
    if re.match(
        r"^(what about|how about)\b",
        normalized_question,
    ):
        if topic:
            return f"{question} regarding {topic}"

    # ---------------------------------------------------------
    # 5. No rewrite required
    # ---------------------------------------------------------
    return question