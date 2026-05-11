import re


BLOCKED_INJECTION_PATTERNS = [
    # Prompt injection
    re.compile(r"ignore\s+(all\s+)?(previous|your\s+)?instructions", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(previous|your\s+)?instructions", re.IGNORECASE),
    re.compile(r"new\s+instructions[:\s]", re.IGNORECASE),
    re.compile(r"ignore\s+the\s+rules", re.IGNORECASE),
    re.compile(r"disregard\s+the\s+rules", re.IGNORECASE),
    re.compile(r"forget\s+(all\s+)?(previous|your\s+)?(instructions|guidelines)", re.IGNORECASE),

    # System prompt extraction
    re.compile(r"(show|reveal|print|tell|what\s+is)\s+(my\s+|your\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"(show|reveal|print|tell)\s+(my\s+|your\s+)?(hidden\s+)?instructions", re.IGNORECASE),
    re.compile(r"what\s+(are\s+)?your\s+(system\s+)?(instructions|prompts|guidelines)", re.IGNORECASE),
    re.compile(r"repeat\s+(your\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"share\s+(your\s+)?(system\s+)?(prompt|instructions)", re.IGNORECASE),

    # Role-play / jailbreak
    re.compile(r"(act|pretend|roleplay)\s+as\s+(an?\s+)?unrestricted", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(an?\s+)?unrestricted", re.IGNORECASE),
    re.compile(r"developer\s+mode", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
    re.compile(r"bypass\s+(safety|security|content\s+filter)", re.IGNORECASE),
    re.compile(r"disable\s+(safety|security)\s+(filters?|checks?)", re.IGNORECASE),

    # API key / secret extraction
    re.compile(r"(return|reveal|show|extract)\s+(my|the|any)\s+(api|openai|gemini)\s*key", re.IGNORECASE),
    re.compile(r"(return|reveal|show)\s+.*token", re.IGNORECASE),
    re.compile(r"print\s+(env|environment)", re.IGNORECASE),
    re.compile(r"import\s+os.*getenv", re.IGNORECASE),

    # Accidental secret leaks in prompt
    re.compile(r"(api[_-]?key|secret|token|password)\s*=\s*['\"][A-Za-z0-9_\-]{8,}", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-]{16,}", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9_\-]{32,}", re.IGNORECASE),
    re.compile(r"AIza[A-Za-z0-9_\-]{20,}", re.IGNORECASE),

    # Recursive prompt extraction
    re.compile(r"previous\s+message\s+was:\s*['\"]", re.IGNORECASE),
    re.compile(r"start\s+with\s+['\"]system", re.IGNORECASE),
    re.compile(r"output\s+(all\s+)?your\s+(instructions?|system\s+prompt)", re.IGNORECASE),
]


def detect_injection(prompt: str) -> tuple[bool, str | None]:
    """
    Advanced prompt injection detection.
    Scans against a comprehensive list of attack patterns.
    Returns (is_injection, error_message).
    """
    if not prompt or not prompt.strip():
        return True, "Prompt cannot be empty"

    lowered = prompt.lower().strip()

    # Check each pattern
    for pattern in BLOCKED_INJECTION_PATTERNS:
        if pattern.search(prompt):
            return True, "Prompt contains potentially unsafe content and was rejected"

    # Check for extremely long prompts (DoS vector)
    if len(prompt) > 2000:
        return True, "Prompt exceeds maximum length"

    # Check for repeated tokens (spamming)
    tokens = lowered.split()
    if len(tokens) > 100:
        unique_ratio = len(set(tokens)) / len(tokens)
        if unique_ratio < 0.3:
            return True, "Prompt appears to be spam and was rejected"

    return False, None
