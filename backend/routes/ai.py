import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from utils.sql import supabase
from ai.classifier import classify
from ai.sql_pipeline import run_sql
from ai.hybrid_pipeline import run_hybrid


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat_with_assistant(payload: ChatRequest):

    if client is None:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured in backend/.env"
        )

    try:
        history_text = ""

        try:
            history = (
                supabase.table("ai_chat_history")
                .select("question, ai_response")
                .order("created_at", desc=True)
                .limit(5)
                .execute()
            )

            for chat in reversed(history.data):
                history_text += (
                    f"User: {chat['question']}\n"
                    f"Assistant: {chat['ai_response']}\n\n"
                )

        except Exception as e:
            print("History error:", e)

        # Decide which pipeline to use
        route = classify(payload.message, history_text)

        print(f"Route: {route}")

        if route == "SQL":
            return run_sql(payload.message, history_text)
        elif route == "HYBRID":
            return run_hybrid(payload.message)

        # If RAG, continue with the existing code below

        # ============================
        # Fetch data from Supabase
        # ============================

        members_resp = supabase.table("team_members").select("*").execute()
        projects_resp = supabase.table("projects").select("*").execute()
        updates_resp = supabase.table("daily_updates").select("*").execute()

        team_members = members_resp.data or []
        projects = projects_resp.data or []
        updates = updates_resp.data or []

        # ...rest of your existing RAG code...
        # ============================
        # Create lookup dictionaries
        # ============================

        member_lookup = {
            member["id"]: member["full_name"]
            for member in team_members
        }

        project_lookup = {
            project["id"]: project["project_name"]
            for project in projects
        }

        # ============================
        # Format Team Members
        # ============================

        member_context = "\n".join(
            [
                f"""
Name: {m['full_name']}
Role: {m['role']}
Department: {m['department']}
Email: {m['email']}
"""
                for m in team_members
            ]
        )

        # ============================
        # Format Projects
        # ============================

        project_context = "\n".join(
            [
                f"""
Project: {p['project_name']}
Status: {p['status']}
Description: {p['description']}
"""
                for p in projects
            ]
        )

        # ============================
        # Format Daily Updates
        # ============================

        formatted_updates = []

        for update in updates:

            member_name = member_lookup.get(
                update["member_id"],
                "Unknown Member"
            )

            project_name = project_lookup.get(
                update["project_id"],
                "Unknown Project"
            )

            blockers = update.get("blockers")

            if (
                blockers is None
                or str(blockers).strip().lower()
                in ["", "no", "none", "nil"]
            ):
                blockers = "No blockers reported"

            formatted_updates.append(
                f"""
Team Member : {member_name}

Project : {project_name}

Date : {update['update_date']}

Task Completed :
{update['task_completed']}

Hours Worked :
{update['hours_worked']}

Current Status :
{update['status']}

Blockers :
{blockers}
"""
            )

        updates_context = "\n----------------------------------------\n".join(
            formatted_updates
        )

        # ============================
        # Build AI Context
        # ============================

        db_context = f"""
================ TEAM MEMBERS ================

{member_context}

================ PROJECTS ====================

{project_context}

================ DAILY UPDATES ===============

{updates_context}
"""

        # ============================
        # System Prompt
        # ============================

        system_prompt = f"""
You are an AI Assistant for an internal Team Management Dashboard.

You MUST answer ONLY using the supplied database context.

Guidelines:

- Never mention member IDs or project IDs unless explicitly asked.
- Always refer to people by their names.
- Always refer to projects by their names.
- Present responses professionally.
- Use bullet points or headings whenever appropriate.
- Summarize instead of copying raw data.
- If blockers are "No", "None", or empty, say "No blockers reported."
- Never expose Python dictionaries or JSON.
- Never make up information.
- If the requested information does not exist, politely say so.

Database Context:

{db_context}
"""

        # ============================
        # Ask Groq
        # ============================

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": payload.message
                }
            ],
            temperature=0.2,
            max_tokens=1024,
        )

        reply = completion.choices[0].message.content

        # ============================
        # Save Chat History
        # ============================

        try:

            supabase.table("ai_chat_history").insert(
                {
                    "question": payload.message,
                    "generated_sql": None,
                    "ai_response": reply,
                }
            ).execute()

        except Exception as db_err:
            print(f"Warning: Failed to save history: {db_err}")

        return {
            "response": reply
        }

    except Exception as e:
        print(f"Error in /ai/chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/history")
async def get_chat_history():

    try:

        response = (
            supabase.table("ai_chat_history")
            .select("*")
            .order("created_at", desc=False)
            .execute()
        )

        return {
            "history": response.data or []
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )