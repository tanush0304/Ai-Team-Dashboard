import re
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
]

def validate_sql(sql: str) -> bool:
    """
    Returns True only for safe SELECT queries.
    """
    if not sql:
        return False
    sql = sql.strip()
    # Remove trailing semicolon
    if sql.endswith(";"):
        sql = sql[:-1]
    upper_sql = sql.upper()
    # Must start with SELECT
    if not upper_sql.startswith("SELECT"):
        return False
    # Reject forbidden SQL keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            return False
    return True