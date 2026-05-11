from api.schema_routes import _load_schema
from services.schema_formatter import format_schema_as_text
from services.prompt_guard import detect_injection as guard_detect_injection


SYSTEM_INSTRUCTIONS = """You are a SQL expert assistant. Your task is to convert natural language questions into valid SQLite SQL queries.

STRICT RULES:
1. Generate ONLY a single SQL SELECT statement — nothing else, no explanations, no markdown, no code blocks
2. Use ONLY the tables and columns provided in the schema below
3. Never invent tables, columns, or relationships that do not exist in the schema
4. Always use proper SQLite syntax
5. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, ATTACH, or PRAGMA statements
6. Only use JOINs when explicitly needed and when the schema shows the relationship
7. Do not wrap SQL in backticks, quotes, or any formatting characters
8. Return ONLY the SQL query text, starting with SELECT

SCHEMA:"""


def build_prompt(user_prompt: str) -> str:
    tables = _load_schema()
    schema_text = format_schema_as_text(tables)

    full_prompt = f"""{SYSTEM_INSTRUCTIONS}

{schema_text}

USER QUESTION:
{user_prompt}

SQL QUERY:"""

    return full_prompt


def detect_injection(prompt: str) -> tuple[bool, str | None]:
    return guard_detect_injection(prompt)
