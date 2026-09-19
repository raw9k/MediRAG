import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def generate_answer(context: str, question: str) -> str:
    client = get_groq_client()

    prompt = f"""
You are a medical information assistant.

Answer the user's question using ONLY the provided medical context.

If the context does not contain enough information to answer the question,
say that the available context does not provide enough information.

Medical context:
{context}

User question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You provide concise, evidence-grounded medical information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=500,
    )

    return response.choices[0].message.content