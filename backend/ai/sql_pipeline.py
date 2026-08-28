import json
from ai.prompts import (
    SQL_PROMPT,
    SQL_RESULT_PROMPT
)
from ai.sql_validator import validate_sql
from ai.sql_executor import execute_sql
from services.groq import chat_completion
from utils.sql import supabase


def run_sql(question: str, history: str = ""):
    # -----------------------------
    # Step 1: Generate SQL
    # -----------------------------
    sql_response = chat_completion(
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
    # Step 2: Validate SQL
    # -----------------------------
    if not validate_sql(generated_sql):

        print("\n========== INVALID GENERATED SQL ==========")
        print(generated_sql)
        print("===========================================\n")

        raise Exception(
            f"Unsafe SQL generated.\n\nGenerated SQL:\n{generated_sql}"
        )

    # --------------------------------------------------
    # Basic SQL completeness check
    # --------------------------------------------------
    upper_sql = generated_sql.upper().strip()

    if upper_sql.endswith("FROM"):

        print("\n========== INCOMPLETE GENERATED SQL ==========")
        print(generated_sql)
        print("===============================================\n")

        raise Exception(
            f"Incomplete SQL generated.\n\nGenerated SQL:\n{generated_sql}"
        )

    # --------------------------------------------------
    # Alias / JOIN validation
    # --------------------------------------------------

    if "TM." in upper_sql and "JOIN TEAM_MEMBERS TM" not in upper_sql:

        raise Exception(
            "Invalid SQL: tm alias used without team_members join.\n\n"
            f"Generated SQL:\n{generated_sql}"
        )


    if "P." in upper_sql and "JOIN PROJECTS P" not in upper_sql:

        raise Exception(
            "Invalid SQL: p alias used without projects join.\n\n"
            f"Generated SQL:\n{generated_sql}"
        )


    if "DU." in upper_sql and "FROM DAILY_UPDATES DU" not in upper_sql:

        raise Exception(
            "Invalid SQL: du alias used without daily_updates alias.\n\n"
            f"Generated SQL:\n{generated_sql}"
        )


    # -----------------------------
    # Step 3: Execute SQL
    # -----------------------------

    try:

        rows = execute_sql(generated_sql)

        MAX_ROWS_FOR_LLM = 30

        if len(rows) > MAX_ROWS_FOR_LLM:
            rows_for_llm = rows[:MAX_ROWS_FOR_LLM]
        else:
            rows_for_llm = rows

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
    # Step 4: Explain Results
    # -----------------------------

    result_context = json.dumps(
        rows_for_llm,
        indent=2,
        default=str
    )

    explanation = chat_completion(
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
    # Step 5: Save History
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