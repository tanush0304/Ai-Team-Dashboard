import os
import json

from groq import Groq

from ai.prompts import (
    SQL_PROMPT,
    SQL_RESULT_PROMPT
)

from ai.sql_validator import validate_sql
from ai.sql_executor import execute_sql

from utils.sql import supabase


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def run_sql(question: str, history: str = ""):
    # -----------------------------
    # Step 1 : Generate SQL
    # -----------------------------

    sql_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=300,
        messages=[
    {
        "role": "system",
        "content": SQL_PROMPT
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

    generated_sql = (
        sql_response
        .choices[0]
        .message
        .content
        .strip()
    )

    generated_sql = generated_sql.replace("```sql", "")
    generated_sql = generated_sql.replace("```", "")
    generated_sql = generated_sql.strip()
    if generated_sql.endswith(";"):
        generated_sql = generated_sql[:-1]
    # -----------------------------
    # Step 2 : Validate SQL
    # -----------------------------

    if not validate_sql(generated_sql):

        raise Exception(
            "Unsafe SQL generated."
        )

    # -----------------------------
    # Step 3 : Execute SQL
    # -----------------------------

    try:
        rows = execute_sql(generated_sql)
        print("\n========== GENERATED SQL ==========")
        print(generated_sql)

        print("\n========== SQL ROWS ==========")
        print(rows)
        print("==================================\n")
    except Exception as e:
        raise Exception(
        f"SQL Execution Error:\n{e}\n\nGenerated SQL:\n{generated_sql}"
    )

    # -----------------------------
    # Step 4 : Explain Results
    # -----------------------------

    result_context = json.dumps(
        rows,
        indent=2,
        default=str
    )

    explanation = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=700,
        messages=[
            {
                "role": "system",
                "content": SQL_RESULT_PROMPT
            },
            {
                "role": "user",
                "content": f"""

Previous Conversation:

{history}
                
Question:

{question}

SQL Result:

{result_context}
"""
            }
        ]
    )

    answer = (
    explanation
    .choices[0]
    .message
    .content
    .strip()
    )

    # -----------------------------
    # Step 5 : Save History
    # -----------------------------

    try:

        supabase.table(
            "ai_chat_history"
        ).insert(
            {
                "question": question,
                "generated_sql": generated_sql,
                "ai_response": answer
            }
        ).execute()

    except Exception as e:

        print(e)

    return {
        "response": answer,
        "generated_sql": generated_sql,
        "rows": rows
    }