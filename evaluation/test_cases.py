EVALUATION_CASES = [
    {
        "name": "direct_diabetes_symptoms",
        "question": "What are the symptoms of diabetes?",
        "history": [],
        "expected": "retrieve",
        "description": "Direct factual question supported by the medical book.",
    },
    {
        "name": "diabetes_type_2_follow_up",
        "question": "What about type 2?",
        "history": [
            {
                "role": "user",
                "content": "What are the symptoms of diabetes?",
            },
            {
                "role": "assistant",
                "content": (
                    "Diabetes can cause excessive thirst "
                    "and frequent urination."
                ),
            },
        ],
        "expected": "retrieve",
        "description": "Follow-up question requiring query rewriting.",
    },
    {
        "name": "diabetes_prevention_follow_up",
        "question": "How can it be prevented?",
        "history": [
            {
                "role": "user",
                "content": "What are the symptoms of diabetes?",
            },
            {
                "role": "assistant",
                "content": (
                    "Diabetes can cause excessive thirst "
                    "and frequent urination."
                ),
            },
        ],
        "expected": "retrieve",
        "description": "Vague follow-up requiring topic resolution.",
    },
    
    {
        "name": "out_of_context",
        "question": "What is the capital of France?",
        "history": [],
        "expected": "no_retrieval",
        "description": "Question outside the medical knowledge base.",
    },
    {
        "name": "greeting",
        "question": "hello",
        "history": [],
        "expected": "greeting",
        "description": "Greeting should bypass retrieval.",
    },
    {
        "name": "greeting_variant",
        "question": "hii",
        "history": [],
        "expected": "greeting",
        "description": "Greeting variant should bypass retrieval.",
    },
]