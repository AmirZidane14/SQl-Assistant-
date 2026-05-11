import re

ALLOWED_PREFIXES = ["SELECT", "WITH"]

BLOCKED_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "TRUNCATE", "EXEC", "EXECUTE", "CREATE", "GRANT",
    "REVOKE", "DENY", "ATTACH", "DETACH", "PRAGMA",
    "REINDEX", "ANALYZE", "VACUUM",
]

MULTI_STMT_PATTERN = re.compile(r";\s*[A-Z]", re.IGNORECASE)
SINGLE_LINE_COMMENT_PATTERN = re.compile(r"--.*$", re.MULTILINE)
MULTI_LINE_COMMENT_PATTERN = re.compile(r"/\*[\s\S]*?\*/")

INJECTION_PATTERNS = [
    re.compile(r"\bUNION\s+SELECT\b", re.IGNORECASE),
    re.compile(r"\bOR\s+1\s*=\s*1\b", re.IGNORECASE),
    re.compile(r"\bOR\s+\w+\s*=\s*\w+\b", re.IGNORECASE),
    re.compile(r"';?\s*(DROP|INSERT|UPDATE|DELETE)\b", re.IGNORECASE),
    re.compile(r"<[^>]*>"),
    re.compile(r"\\x[0-9a-fA-F]{2}"),
]

MAX_QUERY_LENGTH = 5000
MAX_JOINS = 5
MAX_NESTED_SELECT = 3


class SQLValidator:
    def __init__(self, query: str):
        self.original = query.strip()
        self.cleaned = self._remove_comments(self.original)

    def _remove_comments(self, sql: str) -> str:
        sql = SINGLE_LINE_COMMENT_PATTERN.sub("", sql)
        sql = MULTI_LINE_COMMENT_PATTERN.sub("", sql)
        return sql.strip()

    def validate(self) -> tuple[bool, str | None]:
        if "--" in self.original or "/*" in self.original:
            return False, "SQL comments are not allowed"

        if not self.cleaned:
            return False, "Query cannot be empty"

        if len(self.original) > MAX_QUERY_LENGTH:
            return False, f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters"

        first_word = self.cleaned.split()[0].upper()
        if first_word not in ALLOWED_PREFIXES:
            return False, f"Query must start with SELECT or WITH. Found: {first_word}"

        for keyword in BLOCKED_KEYWORDS:
            pattern = re.compile(rf"\b{keyword}\b", re.IGNORECASE)
            if pattern.search(self.cleaned):
                return False, f"Blocked keyword '{keyword}' is not allowed"

        if MULTI_STMT_PATTERN.search(self.cleaned):
            return False, "Multiple statements are not allowed. Submit one query at a time"

        for pattern in INJECTION_PATTERNS:
            if pattern.search(self.cleaned):
                return False, "Suspicious pattern detected — possible injection attempt"

        join_count = len(re.findall(r"\bJOIN\b", self.cleaned, re.IGNORECASE))
        if join_count > MAX_JOINS:
            return False, f"Query has too many JOINs (max {MAX_JOINS})"

        nested_count = len(re.findall(r"\bSELECT\b", self.cleaned, re.IGNORECASE))
        if nested_count > MAX_NESTED_SELECT:
            return False, f"Query has too many nested SELECTs (max {MAX_NESTED_SELECT})"

        if re.search(r"\\x[0-9a-fA-F]{4,}", self.original):
            return False, "Suspicious encoded content detected"

        return True, None


def validate_query(query: str) -> tuple[bool, str | None]:
    validator = SQLValidator(query)
    return validator.validate()
