from services.prompt_builder import build_prompt, detect_injection
from services.llm_service import call_gemini, extract_sql
from services.sql_explainer import explain_sql
from services.sql_validator import validate_query
from services.query_executor import executor


class QueryWorkflow:
    """
    Orchestrates the full AI query workflow:
    1. Generate SQL from natural language using Gemini
    2. Extract and clean the SQL from LLM response
    3. Validate the SQL
    4. Generate a human-readable explanation
    5. Execute on explicit approval
    """

    def preview(self, prompt: str) -> dict:
        """
        Steps 1-4: Generate, validate, and explain SQL.
        Does NOT execute — user must call execute() explicitly.
        """
        is_injection, inject_error = detect_injection(prompt)
        if is_injection:
            return {
                "success": False,
                "user_prompt": prompt,
                "generated_sql": "",
                "explanation": "",
                "valid": False,
                "error": inject_error,
            }

        full_prompt = build_prompt(prompt)

        raw_response, api_error = call_gemini(full_prompt)
        if api_error or raw_response is None:
            return {
                "success": False,
                "user_prompt": prompt,
                "generated_sql": "",
                "explanation": "",
                "valid": False,
                "error": api_error or "Empty response from Gemini",
            }

        sql, extract_error = extract_sql(raw_response)
        if extract_error or sql is None:
            return {
                "success": False,
                "user_prompt": prompt,
                "generated_sql": "",
                "explanation": "",
                "valid": False,
                "error": f"AI output could not be parsed: {extract_error}",
            }

        is_valid, validation_error = validate_query(sql)
        explanation = explain_sql(sql) if is_valid else ""

        return {
            "success": True,
            "user_prompt": prompt,
            "generated_sql": sql,
            "explanation": explanation,
            "valid": is_valid,
            "error": validation_error if not is_valid else None,
        }

    def execute(self, query: str) -> dict:
        """
        Step 5: Execute a user-approved SQL query.
        Always re-validates before execution — never trusts frontend state.
        """
        is_valid, validation_error = validate_query(query)
        if not is_valid:
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "count": 0,
                "error": validation_error,
            }

        result = executor.execute(query)
        return {
            "success": result["success"],
            "columns": result["columns"],
            "rows": result["rows"],
            "count": result["count"],
            "error": result.get("error"),
        }


workflow = QueryWorkflow()