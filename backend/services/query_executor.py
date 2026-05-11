from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.connection import SessionLocal
from services.sql_validator import validate_query


class QueryExecutor:
    """
    Executes validated SQL queries against the database.
    All queries are validated first — this class assumes validation already passed.
    """

    def execute(self, query: str) -> dict:
        """
        Validates and executes a SQL query, returning results as a dict.

        Args:
            query: The SQL query string (should already be validated)

        Returns:
            A dict with:
              - success: bool
              - columns: list[str] (empty on error)
              - rows: list[list] (empty on error)
              - count: int (0 on error)
              - error: str | None (set on failure)
        """
        is_valid, error = validate_query(query)
        if not is_valid:
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "count": 0,
                "error": error,
            }

        db = SessionLocal()
        try:
            result = db.execute(text(query))
            rows = result.fetchall()

            columns = list(result.keys()) if result.keys() else []
            rows_data = [[cell for cell in row] for row in rows]

            return {
                "success": True,
                "columns": columns,
                "rows": rows_data,
                "count": len(rows_data),
                "error": None,
            }

        except SQLAlchemyError as e:
            # Map common errors to user-friendly messages
            error_msg = str(e).split("\n")[0]

            if "syntax error" in error_msg.lower():
                return {
                    "success": False,
                    "columns": [],
                    "rows": [],
                    "count": 0,
                    "error": f"SQL syntax error: {error_msg}",
                }

            return {
                "success": False,
                "columns": [],
                "rows": [],
                "count": 0,
                "error": f"Query execution failed: {error_msg}",
            }

        finally:
            db.close()


executor = QueryExecutor()