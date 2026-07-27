from ai.sql_pipeline import run_sql


def run_hybrid(question: str):
    """
    Hybrid pipeline:
    Currently uses the SQL pipeline and returns the result.

    Later we can enhance it by combining SQL analytics with
    RAG summaries.
    """

    result = run_sql(question)

    return {
        "response": result["response"],
        "generated_sql": result["generated_sql"],
    }