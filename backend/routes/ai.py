import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

from utils.sql import supabase

from ai.classifier import classify
from ai.sql_pipeline import run_sql
from ai.rag_pipeline import run_rag
from ai.hybrid_pipeline import run_hybrid

from services.groq import chat_completion

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)

# ============================================================
# GROQ CLIENT
# ============================================================
api_key = os.getenv("GROQ_API_KEY")

client = (
    Groq(api_key=api_key)
    if api_key
    else None
)

# ============================================================
# REQUEST SCHEMA
# ============================================================
class ChatRequest(BaseModel):
    message: str

# ============================================================
# CHAT HISTORY HELPER
# ============================================================
def get_recent_history():

    history_text = ""

    try:
        response = (
            supabase
            .table("ai_chat_history")
            .select("question, ai_response")
            .order(
                "created_at",
                desc=True
            )
            .limit(5)
            .execute()
        )

        history_data = response.data or []

        for chat in reversed(history_data):

            history_text += (
                f"User: {chat.get('question', '')}\n"
                f"Assistant: {chat.get('ai_response', '')}\n\n"
            )

    except Exception as e:
        print(
            "History error:",
            e
        )
    return history_text

# ============================================================
# SAVE CHAT HISTORY
# ============================================================
def save_chat_history(
    question,
    response,
    generated_sql=None
):
    try:
        supabase.table(
            "ai_chat_history"
        ).insert(
            {
                "question": question,
                "generated_sql": generated_sql,
                "ai_response": response
            }
        ).execute()

    except Exception as e:
        print(
            "Chat history error:",
            e
        )

# ============================================================
# CHAT PIPELINE
# ============================================================
def run_chat(
    question,
    history=""
):
    response = chat_completion(
        temperature=0.3,
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": """
You are a friendly AI assistant for an internal
Team Management Dashboard.

Answer casual and conversational questions naturally.

You can respond to greetings, small talk, thanks,
and general conversational questions.

Do not invent team, project, update, or database information.

If the user asks for dashboard data, that question
should normally be handled by the SQL, RAG, or HYBRID
pipelines.
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
    save_chat_history(
        question=question,
        response=answer,
        generated_sql=None
    )
    return {
        "response": answer,
        "generated_sql": None,
        "rows": []
    }

# ============================================================
# AI CHAT ENDPOINT
# ============================================================
@router.post("/chat")
async def chat_with_assistant(
    payload: ChatRequest
):

    # --------------------------------------------------------
    # Check Groq API key
    # --------------------------------------------------------
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured."
        )
    try:

        # ----------------------------------------------------
        # Step 1: Get conversation history
        # ----------------------------------------------------
        history_text = get_recent_history()

        # ----------------------------------------------------
        # Step 2: Classify question
        # ----------------------------------------------------
        route = classify(
            payload.message,
            history_text
        )
        print(
            "=================================="
        )
        print(
            f"Question: {payload.message}"
        )
        print(
            f"Route: {route}"
        )
        print(
            "=================================="
        )

        # ====================================================
        # CHAT
        # ====================================================
        if route == "CHAT":
            return run_chat(
                payload.message,
                history_text
            )

        # ====================================================
        # SQL
        # ====================================================
        elif route == "SQL":
            return run_sql(
                payload.message,
                history_text
            )

        # ====================================================
        # RAG
        # ====================================================
        elif route == "RAG":
            return run_rag(
                payload.message,
                history_text
            )

        # ====================================================
        # HYBRID
        # ====================================================
        elif route == "HYBRID":
            return run_hybrid(
                payload.message,
                history_text
            )

        # ====================================================
        # UNKNOWN ROUTE
        # ====================================================
        else:
            print(
                f"Unknown route received: {route}"
            )
            # Safe fallback to SQL for dashboard questions
            return run_sql(
                payload.message,
                history_text
            )

    # --------------------------------------------------------
    # Error handling
    # --------------------------------------------------------
    except Exception as e:
        print(
            f"Error in /ai/chat: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ============================================================
# GET CHAT HISTORY
# ============================================================
@router.get("/history")
async def get_chat_history():
    try:
        response = (
            supabase
            .table("ai_chat_history")
            .select("*")
            .order(
                "created_at",
                desc=False
            )
            .execute()
        )
        return {
            "history": response.data or []
        }
    except Exception as e:
        print(
            f"Error fetching chat history: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )