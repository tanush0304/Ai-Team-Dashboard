from ai.context_builder import build_database_context
from ai.prompts import RAG_PROMPT
from services.groq import chat_completion


def run_rag(question: str, history: str = ""):

    context = build_database_context()

    response = chat_completion(
        temperature=0.2,
        max_tokens=700,
        messages=[
            {
                "role": "system",
                "content": f"""
{RAG_PROMPT}

DATABASE CONTEXT:

{context}
"""
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
        ]
    )

    answer = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return {
        "response": answer,
        "generated_sql": None,
        "rows": []
    }