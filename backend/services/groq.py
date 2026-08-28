import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Models
FAST_MODEL = "openai/gpt-oss-20b"
DEFAULT_MODEL = "openai/gpt-oss-120b"


def chat_completion(
    messages,
    model=DEFAULT_MODEL,
    temperature=0,
    max_tokens=500
):
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )

    print("\n========== GROQ DEBUG ==========")
    print("Model:", model)
    print("Finish reason:", response.choices[0].finish_reason)
    print(
        "Message content:",
        repr(response.choices[0].message.content)
    )
    print(
        "Reasoning:",
        repr(
            getattr(
                response.choices[0].message,
                "reasoning",
                None
            )
        )
    )
    print("================================\n")

    return response