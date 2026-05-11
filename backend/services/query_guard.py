import re

MAX_QUERY_LENGTH = 5000
MAX_JOINS = 5
MAX_NESTED_SELECT = 3
MAX_WHERE_CLAUSES = 20

BLOCKED_SQL_PATTERNS = [
    re.compile(r"\bUNION\s+SELECT\b", re.IGNORECASE),
    re.compile(r"\bUNION\s+ALL\s+SELECT\b", re.IGNORECASE),
    re.compile(r"\bOR\s+1\s*=\s*1\b", re.IGNORECASE),
    re.compile(r"\bOR\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?", re.IGNORECASE),
    re.compile(r"\bAND\s+1\s*=\s*1\b", re.IGNORECASE),
    re.compile(r"\bEXEC(\s|;|\()", re.IGNORECASE),
    re.compile(r"\bEXECUTE\s+", re.IGNORECASE),
    re.compile(r"\bxp_", re.IGNORECASE),
    re.compile(r"\bsp_\w+", re.IGNORECASE),
    re.compile(r"\bSLEEP\s*\(", re.IGNORECASE),
    re.compile(r"\bBENCHMARK\s*\(", re.IGNORECASE),
    re.compile(r"\bWAITFOR\s+DELAY", re.IGNORECASE),
    re.compile(r"\bPG_SLEEP", re.IGNORECASE),
    re.compile(r"\bATTACH\s+DATABASE", re.IGNORECASE),
    re.compile(r"\bATTACH\s+\w+\s+AS", re.IGNORECASE),
    re.compile(r"\bDETACH\s+DATABASE", re.IGNORECASE),
    re.compile(r"\bLOAD_EXTENSION", re.IGNORECASE),
    re.compile(r"\bsqlite_master\b", re.IGNORECASE),
    re.compile(r"\bsqlite_temp_master\b", re.IGNORECASE),
    re.compile(r"\binformation_schema\b", re.IGNORECASE),
    re.compile(r"--\s*$", re.MULTILINE),
    re.compile(r"/\*[\s\S]*?\*/"),
    re.compile(r"<[^>]*>"),
    re.compile(r"\\\x[0-9a-fA-F]{2}"),
]

SAFE_PREFIXES = ["SELECT", "WITH"]


def analyze_query_complexity(sql: str) -> tuple[bool, str | None]:
    """
    Check if a SQL query exceeds complexity limits.
    Returns (is_safe, error_message).
    """
    if len(sql) > MAX_QUERY_LENGTH:
        return False, f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters"

    join_count = len(re.findall(r"\bJOIN\b", sql, re.IGNORECASE))
    if join_count > MAX_JOINS:
        return False, f"Query has too many JOINs (max {MAX_JOINS})"

    nested_count = len(re.findall(r"\bSELECT\b", sql, re.IGNORECASE))
    if nested_count > MAX_NESTED_SELECT:
        return False, f"Query has too many nested SELECTs (max {MAX_NESTED_SELECT})"

    where_count = len(re.findall(r"\bWHERE\b", sql, re.IGNORECASE))
    if where_count > MAX_WHERE_CLAUSES:
        return False, f"Query has too many WHERE clauses (max {MAX_WHERE_CLAUSES})"

    return True, None


def detect_sql_injection(sql: str) -> tuple[bool, str | None]:
    """
    Advanced SQL injection detection for read-only queries.
    Returns (is_safe, error_message).
    """
    sql_stripped = sql.strip()

    # Must start with allowed prefix
    first_word = sql_stripped.split()[0].upper()
    if first_word not in SAFE_PREFIXES:
        return False, f"Only SELECT queries are allowed. Found: {first_word}"

    # Check blocked patterns
    for pattern in BLOCKED_SQL_PATTERNS:
        if pattern.search(sql):
            return False, f"Suspicious SQL pattern detected and blocked"

    # Check complexity
    is_complex, complex_error = analyze_query_complexity(sql)
    if not is_complex:
        return False, complex_error

    # Check for hex-encoded content (common in injection)
    if re.search(r"\\x[0-9a-fA-F]{4,}", sql):
        return False, "Suspicious encoded content detected"

    # Check for stacked queries (semicolon + SQL keyword)
    if re.search(r";\s*[A-Z]", sql, re.IGNORECASE):
        return False, "Multiple statements are not allowed"

    return True, None
