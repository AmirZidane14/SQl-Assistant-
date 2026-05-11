import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.connection import SessionLocal
from services.sql_validator import validate_query
from services.secret_filter import safe_error_message


QUERY_TIMEOUT_SECONDS = 5


class QueryExecutor:
    def execute(self, query: str) -> dict:
        is_valid, error = validate_query(query)
        if not is_valid:
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "count": 0,
                "error": error,
            }

        result_holder: dict = {"data": None, "error": None}

        def _run_query():
            db = SessionLocal()
            try:
                result = db.execute(text(query))
                rows = result.fetchall()
                columns = list(result.keys()) if result.keys() else []
                rows_data = [[cell for cell in row] for row in rows]
                result_holder["data"] = {
                    "columns": columns,
                    "rows": rows_data,
                    "count": len(rows_data),
                }
            except SQLAlchemyError as e:
                result_holder["error"] = safe_error_message(e)
            except Exception as e:
                result_holder["error"] = safe_error_message(e)
            finally:
                db.close()

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_query)
            try:
                future.result(timeout=QUERY_TIMEOUT_SECONDS)
            except FuturesTimeoutError:
                return {
                    "success": False,
                    "columns": [],
                    "rows": [],
                    "count": 0,
                    "error": f"Query timed out after {QUERY_TIMEOUT_SECONDS} seconds",
                }

        if result_holder["error"]:
            error_msg = result_holder["error"]
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

        data = result_holder["data"]
        return {
            "success": True,
            "columns": data["columns"],
            "rows": data["rows"],
            "count": data["count"],
            "error": None,
        }


executor = QueryExecutor()
