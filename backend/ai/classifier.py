import os

from groq import Groq

from ai.prompts import ROUTER_PROMPT

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def classify(question, history=""):
    """
    Classifies a user question into one of:
        - RAG
        - SQL
        - HYBRID
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=5,
        messages=[
            {
                "role": "system",
                "content": ROUTER_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
                Previous Conversation:

                {history}

                Current Question:

                {question}
                """
            }
        ],
    )

    route = (
        response.choices[0]
        .message.content
        .strip()
        .upper()
    )

    print("Classifier raw output:", repr(route))

    if route not in ["RAG", "SQL", "HYBRID"]:
        return "RAG"

    return route