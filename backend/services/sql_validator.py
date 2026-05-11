import re

# SQL keywords that are allowed in a query
ALLOWED_PREFIXES = [
    "SELECT",
    "WITH",        # CTEs (WITH ... AS SELECT) are allowed
]

# SQL keywords that are BLOCKED — any query containing these is rejected
BLOCKED_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "EXEC",
    "EXECUTE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "DENY",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "REINDEX",
    "ANALYZE",
    "VACUUM",
]

# Patterns for multi-statement detection (semicolon followed by SQL)
MULTI_STMT_PATTERN = re.compile(r";\s*[A-Z]", re.IGNORECASE)

# Patterns for SQL comment detection
SINGLE_LINE_COMMENT_PATTERN = re.compile(r"--.*$", re.MULTILINE)
MULTI_LINE_COMMENT_PATTERN = re.compile(r"/\*[\s\S]*?\*/")

# Patterns for common injection attacks
INJECTION_PATTERNS = [
    re.compile(r"\bUNION\s+SELECT\b", re.IGNORECASE),
    re.compile(r"\bOR\s+1\s*=\s*1\b", re.IGNORECASE),
    re.compile(r"\bOR\s+\w+\s*=\s*\w+\b", re.IGNORECASE),
    re.compile(r"';?\s*(DROP|INSERT|UPDATE|DELETE)\b", re.IGNORECASE),
    re.compile(r"<[^>]*>"),                    # HTML tags
    re.compile(r"\\x[0-9a-fA-F]{2}"),          # Hex-encoded bytes
]


class SQLValidator:
    """
    Validates incoming SQL queries to ensure only safe, read-only operations are executed.
    This is a defense-in-depth layer — the AI generation layer should also produce safe queries,
    but manual query input must be validated here as well.
    """

    def __init__(self, query: str):
        # Normalize: strip leading/trailing whitespace
        self.original = query.strip()
        self.cleaned = self._remove_comments(self.original)

    def _remove_comments(self, sql: str) -> str:
        """Strip both single-line (--) and block (/* */) comments from the query."""
        sql = SINGLE_LINE_COMMENT_PATTERN.sub("", sql)
        sql = MULTI_LINE_COMMENT_PATTERN.sub("", sql)
        return sql.strip()

    def validate(self) -> tuple[bool, str | None]:
        """
        Returns (True, None) if the query is safe.
        Returns (False, error_message) if the query is blocked.

        Validation order:
        1. Empty query
        2. SQL comment detection (rejected — not stripped)
        3. Allowed prefix check
        4. Blocked keywords
        5. Multi-statement detection
        6. Injection pattern detection
        """
        # 0. Pre-check on original: reject if it contains SQL comments (not just strip them)
        if "--" in self.original or "/*" in self.original:
            return False, "SQL comments are not allowed"

        # 1. Empty query
        if not self.cleaned:
            return False, "Query cannot be empty"

        # 2. Must start with SELECT or WITH
        first_word = self.cleaned.split()[0].upper()
        if first_word not in ALLOWED_PREFIXES:
            return False, f"Query must start with SELECT or WITH. Found: {first_word}"

        # 3. Check for blocked keywords anywhere in the query
        for keyword in BLOCKED_KEYWORDS:
            pattern = re.compile(rf"\b{keyword}\b", re.IGNORECASE)
            if pattern.search(self.cleaned):
                return False, f"Blocked keyword '{keyword}' is not allowed"

        # 4. Block multiple statements (semicolon followed by more SQL)
        if MULTI_STMT_PATTERN.search(self.cleaned):
            return False, "Multiple statements are not allowed. Submit one query at a time"

        # 5. Block injection attack patterns
        for pattern in INJECTION_PATTERNS:
            if pattern.search(self.cleaned):
                return False, "Suspicious pattern detected — possible injection attempt"

        return True, None


def validate_query(query: str) -> tuple[bool, str | None]:
    """
    Convenience function. Validates a SQL query string.
    Returns (is_valid, error_message).
    """
    validator = SQLValidator(query)
    return validator.validate()