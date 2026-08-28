import os

from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


DEFAULT_MODEL = "openai/gpt-oss-120b"

FAST_MODEL = "openai/gpt-oss-20b"


def chat_completion(
    messages,
    temperature=0,
    max_tokens=500,
    model=DEFAULT_MODEL
):

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )

    return response