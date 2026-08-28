import json

from ai.prompts import (
    SQL_PROMPT,
    SQL_RESULT_PROMPT
)

from ai.sql_validator import validate_sql
from ai.sql_executor import execute_sql
from services.groq import chat_completion
from utils.sql import supabase


MAX_SQL_ATTEMPTS = 2
MAX_ROWS_FOR_LLM = 30


def clean_sql(sql: str) -> str:
    """
    Clean common formatting returned by the LLM.
    """

    if not sql:
        return ""

    sql = sql.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```SQL", "")
    sql = sql.replace("```", "")

    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    return sql.strip()


def validate_generated_sql(sql: str):
    """
    Perform application-level validation on generated SQL.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    if not validate_sql(sql):
        return (
            False,
            "SQL failed the safety validation. "
            "Only safe SELECT queries are allowed."
        )

    upper_sql = sql.upper().strip()

    # --------------------------------------------------
    # Incomplete FROM clause
    # --------------------------------------------------

    if upper_sql.endswith("FROM"):
        return (
            False,
            "SQL is incomplete. The FROM clause is missing "
            "a table."
        )

    # --------------------------------------------------
    # Alias validation
    # --------------------------------------------------

    if (
        "TM." in upper_sql
        and "JOIN TEAM_MEMBERS TM" not in upper_sql
    ):
        return (
            False,
            "The query uses the tm alias but does not "
            "join team_members as tm."
        )

    if (
        "P." in upper_sql
        and "JOIN PROJECTS P" not in upper_sql
    ):
        return (
            False,
            "The query uses the p alias but does not "
            "join projects as p."
        )

    if (
        "DU." in upper_sql
        and "FROM DAILY_UPDATES DU" not in upper_sql
    ):
        return (
            False,
            "The query uses the du alias but does not "
            "define daily_updates as du."
        )

    # --------------------------------------------------
    # Basic JOIN validation
    # --------------------------------------------------

    if "JOIN TEAM_MEMBERS TM" in upper_sql:
        if "ON DU.MEMBER_ID = TM.ID" not in upper_sql:
            return (
                False,
                "The team_members join is missing the required "
                "ON condition."
            )

    if "JOIN PROJECTS P" in upper_sql:
        if "ON DU.PROJECT_ID = P.ID" not in upper_sql:
            return (
                False,
                "The projects join is missing the required "
                "ON condition."
            )

    return True, None


def generate_sql(question: str, history: str = ""):
    """
    Generate SQL using the LLM.
    """

    response = chat_completion(
        temperature=0,
        max_tokens=1000,
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

    sql = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return clean_sql(sql)


def repair_sql(
    question: str,
    generated_sql: str,
    error_message: str,
    history: str = ""
):
    """
    Ask the LLM to correct an invalid SQL query.
    """

    repair_prompt = f"""
You are repairing a PostgreSQL query generated for
an internal Team Management Dashboard.

The previous SQL query was invalid.

USER QUESTION:
{question}

PREVIOUS CONVERSATION:
{history}

PREVIOUS SQL:
{generated_sql}

VALIDATION / DATABASE ERROR:
{error_message}

Your task is to generate a corrected SQL query.

IMPORTANT RULES:

1. Return ONLY the corrected SQL query.
2. Return exactly ONE SELECT query.
3. Do not explain anything.
4. Do not use markdown.
5. Do not use ```sql.
6. Do not use INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, GRANT, or REVOKE.
7. Use only tables and columns defined in the original
   SQL schema.
8. Make sure every table alias used in SELECT, WHERE,
   ORDER BY, GROUP BY, or JOIN actually exists.
9. Every JOIN must contain a valid ON condition.
10. Make sure the query is complete and executable.
11. Use the minimum number of tables required.
12. Preserve the user's original intent.

Return ONLY the corrected SQL query.
"""

    response = chat_completion(
        temperature=0,
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": SQL_PROMPT
            },
            {
                "role": "user",
                "content": repair_prompt
            }
        ]
    )

    repaired_sql = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return clean_sql(repaired_sql)


def run_sql(question: str, history: str = ""):

    # ==================================================
    # Step 1: Generate + Validate SQL
    # ==================================================

    generated_sql = ""
    last_error = ""

    for attempt in range(1, MAX_SQL_ATTEMPTS + 1):

        print(
            f"\n========== SQL ATTEMPT {attempt} =========="
        )

        try:

            if attempt == 1:

                generated_sql = generate_sql(
                    question,
                    history
                )

            else:

                generated_sql = repair_sql(
                    question,
                    generated_sql,
                    last_error,
                    history
                )

            print("\nGenerated SQL:")
            print(generated_sql)

            # ------------------------------------------
            # Validate SQL
            # ------------------------------------------

            is_valid, validation_error = (
                validate_generated_sql(
                    generated_sql
                )
            )

            if not is_valid:

                last_error = validation_error

                print(
                    "\nSQL VALIDATION FAILED:"
                )
                print(last_error)

                if attempt < MAX_SQL_ATTEMPTS:
                    print(
                        "\nAttempting SQL correction..."
                    )
                    continue

                raise Exception(
                    f"SQL validation failed after "
                    f"{MAX_SQL_ATTEMPTS} attempts.\n\n"
                    f"Last error:\n{last_error}\n\n"
                    f"Generated SQL:\n{generated_sql}"
                )

            # ------------------------------------------
            # Execute SQL
            # ------------------------------------------

            try:

                rows = execute_sql(
                    generated_sql
                )

                print(
                    "\nSQL EXECUTION SUCCESSFUL"
                )

                print(
                    "\n========== SQL ROWS =========="
                )
                print(rows)
                print(
                    "==================================\n"
                )

                # --------------------------------------
                # Successful SQL
                # --------------------------------------

                break

            except Exception as db_error:

                last_error = (
                    f"Database execution failed: "
                    f"{db_error}"
                )

                print(
                    "\nSQL EXECUTION FAILED:"
                )
                print(last_error)

                if attempt < MAX_SQL_ATTEMPTS:

                    print(
                        "\nAttempting SQL correction..."
                    )

                    continue

                raise Exception(
                    f"SQL Execution Error after "
                    f"{MAX_SQL_ATTEMPTS} attempts:\n"
                    f"{last_error}\n\n"
                    f"Generated SQL:\n"
                    f"{generated_sql}"
                )

        except Exception:

            if attempt >= MAX_SQL_ATTEMPTS:
                raise

    # ==================================================
    # Step 2: Limit rows sent to LLM
    # ==================================================

    if len(rows) > MAX_ROWS_FOR_LLM:

        rows_for_llm = rows[
            :MAX_ROWS_FOR_LLM
        ]

    else:

        rows_for_llm = rows

    # ==================================================
    # Step 3: Explain Results
    # ==================================================

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

    # ==================================================
    # Step 4: Save History
    # ==================================================

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

        print(
            "Warning: Failed to save chat history:",
            e
        )

    # ==================================================
    # Step 5: Return
    # ==================================================

    return {
        "response": answer,
        "generated_sql": generated_sql,
        "rows": rows
    }