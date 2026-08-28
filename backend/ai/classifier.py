from ai.prompts import ROUTER_PROMPT
from services.groq import chat_completion, FAST_MODEL

def classify(question, history=""):
    response = chat_completion(
        model=FAST_MODEL,
        temperature=0,
        max_tokens=200,
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
        .message
        .content
        .strip()
        .upper()
    )
    print("Classifier raw output:", repr(route))
    if "HYBRID" in route:
        return "HYBRID"
    if "SQL" in route:
        return "SQL"
    if "RAG" in route:
        return "RAG"
    if "CHAT" in route:
        return "CHAT"
    return "SQL"