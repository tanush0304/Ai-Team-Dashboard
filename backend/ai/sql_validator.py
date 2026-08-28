import re
# ============================================================
# SQL operations that are never allowed
# ============================================================
FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "MERGE",
    "UPSERT",
    "CALL",
    "EXEC",
    "EXECUTE",
]

# ============================================================
# Tables that the AI is allowed to query
# ============================================================
ALLOWED_TABLES = {
    "team_members",
    "projects",
    "daily_updates",
}

def validate_sql(sql: str) -> bool:
    """
    Validate LLM-generated SQL.

    This validator is intentionally focused on read-only,
    single-statement SELECT queries.

    Returns:
        True  -> SQL is considered safe
        False -> SQL should not be executed
    """
    if not sql:
        return False
    sql = sql.strip()
    # --------------------------------------------------------
    # Remove a single trailing semicolon
    # --------------------------------------------------------
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    if not sql:
        return False
    upper_sql = sql.upper()

    # --------------------------------------------------------
    # 1. Query must start with SELECT
    # --------------------------------------------------------
    if not re.match(r"^\s*SELECT\b", upper_sql):
        return False

    # --------------------------------------------------------
    # 2. Prevent multiple SQL statements
    # --------------------------------------------------------
    if ";" in sql:
        return False

    # --------------------------------------------------------
    # 3. Block SQL comments
    # --------------------------------------------------------
    if "--" in sql:
        return False
    if "/*" in sql or "*/" in sql:
        return False

    # --------------------------------------------------------
    # 4. Block dangerous SQL operations
    # --------------------------------------------------------
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(
            rf"\b{keyword}\b",
            upper_sql
        ):
            return False

    # --------------------------------------------------------
    # 5. Block transaction/control statements
    # --------------------------------------------------------
    forbidden_patterns = [
        r"\bBEGIN\b",
        r"\bCOMMIT\b",
        r"\bROLLBACK\b",
        r"\bSAVEPOINT\b",
        r"\bSET\b",
        r"\bRESET\b",
        r"\bDO\b",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, upper_sql):
            return False

    # --------------------------------------------------------
    # 6. Prevent obvious system/catalog access
    # --------------------------------------------------------
    forbidden_system_objects = [
        "PG_CATALOG",
        "INFORMATION_SCHEMA",
        "PG_CLASS",
        "PG_TABLES",
        "PG_USER",
        "PG_ROLES",
        "PG_SETTINGS",
    ]
    for object_name in forbidden_system_objects:
        if re.search(
            rf"\b{object_name}\b",
            upper_sql
        ):
            return False

    # --------------------------------------------------------
    # 7. Check referenced tables
    # --------------------------------------------------------
    #
    # We look at FROM and JOIN clauses.
    #
    # Example:
    #
    # FROM daily_updates du
    # JOIN team_members tm
    #
    # -------------------------------------------------------
    table_matches = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql,
        flags=re.IGNORECASE
    )

    for table in table_matches:
        table_name = table.lower()
        if table_name not in ALLOWED_TABLES:
            return False

    # --------------------------------------------------------
    # 8. Make sure a FROM clause exists
    # --------------------------------------------------------
    if not re.search(
        r"\bFROM\b",
        upper_sql
    ):
        return False

    # --------------------------------------------------------
    # 9. Prevent incomplete FROM clause
    # --------------------------------------------------------
    if re.search(
        r"\bFROM\s*$",
        upper_sql
    ):
        return False

    # --------------------------------------------------------
    # 10. Prevent incomplete JOIN clauses
    # --------------------------------------------------------
    if re.search(
        r"\bJOIN\s*$",
        upper_sql
    ):
        return False

    # --------------------------------------------------------
    # 11. Prevent incomplete WHERE clause
    # --------------------------------------------------------
    if re.search(
        r"\bWHERE\s*$",
        upper_sql
    ):
        return False

    # --------------------------------------------------------
    # 12. Prevent obvious unrestricted SELECT *
    # --------------------------------------------------------
    #
    # We don't completely forbid SELECT * because it is
    # technically safe, but we can allow the SQL pipeline
    # to handle row limiting.
    #
    # Therefore this is intentionally NOT blocked.
    # --------------------------------------------------------
    return True