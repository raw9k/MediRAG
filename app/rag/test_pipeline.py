from app.rag.pipeline import answer_question


if __name__ == "__main__":
    question = "What are the symptoms of diabetes?"

    answer, sources = answer_question(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    for source in sources:
        print(f"- {source}")