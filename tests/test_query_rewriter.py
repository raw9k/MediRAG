from app.rag.query_rewriter import rewrite_query


def test_type_2_follow_up():
    history = [
        {
            "role": "user",
            "content": "What are the symptoms of diabetes?",
        },
        {
            "role": "assistant",
            "content": "Diabetes can cause excessive thirst.",
        },
    ]

    result = rewrite_query(
        "What about type 2?",
        history,
    )

    assert result == "What about type 2 diabetes?"


def test_vague_follow_up():
    history = [
        {
            "role": "user",
            "content": "What are the symptoms of diabetes?",
        },
        {
            "role": "assistant",
            "content": "Diabetes can cause excessive thirst.",
        },
    ]

    result = rewrite_query(
        "How can it be prevented?",
        history,
    )

    assert result == "How can diabetes be prevented?"


def test_different_medical_topic():
    history = [
        {
            "role": "user",
            "content": "What are the symptoms of asthma?",
        },
        {
            "role": "assistant",
            "content": "Asthma may cause breathing difficulties.",
        },
    ]

    result = rewrite_query(
        "How can it be prevented?",
        history,
    )

    assert result == "How can asthma be prevented?"


def test_what_about_follow_up():
    history = [
        {
            "role": "user",
            "content": "What are the symptoms of asthma?",
        },
        {
            "role": "assistant",
            "content": "Asthma may cause breathing difficulties.",
        },
    ]

    result = rewrite_query(
        "What about children?",
        history,
    )

    assert "asthma" in result.lower()


def test_no_history():
    result = rewrite_query(
        "What are the symptoms of diabetes?",
        [],
    )

    assert result == "What are the symptoms of diabetes?"


def test_non_follow_up_question():
    history = [
        {
            "role": "user",
            "content": "What are the symptoms of diabetes?",
        },
        {
            "role": "assistant",
            "content": "Diabetes can cause excessive thirst.",
        },
    ]

    result = rewrite_query(
        "What are the symptoms of asthma?",
        history,
    )

    assert result == "What are the symptoms of asthma?"