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

Use ONLY the provided medical context to answer the user's question.

Rules:
1. Do not diagnose the user.
2. Do not prescribe medications or recommend specific treatments
   beyond what is explicitly stated in the provided context.
3. Do not invent or add medical facts that are not present in the context.
4. If the context does not contain enough information, clearly say:
   "The available medical context does not provide enough information
   to answer this question."
5. Keep the answer concise and easy to understand.
6. Distinguish general medical information from personalized medical advice.
7. For potentially serious symptoms, advise the user to seek professional
   medical care rather than making a diagnosis.

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
                    "You provide concise, evidence-grounded medical "
                    "information. You do not diagnose patients."
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