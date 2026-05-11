import re


def explain_sql(sql: str) -> str:
    """
    Generates a human-readable explanation of a SQL query.
    Uses rule-based pattern matching — no LLM required.
    """
    if not sql or not sql.strip():
        return "No SQL query provided."

    parts = []

    # Detect SELECT vs CTE
    sql_stripped = sql.strip().upper()
    if sql_stripped.startswith("WITH"):
        return "This query uses a common table expression (CTE) to structure complex data retrieval."

    if not sql_stripped.startswith("SELECT"):
        return "This query performs a database operation on the database."

    # Extract components (using original case for user-friendly output)
    from_match = re.search(r"\bFROM\s+(\w+)", sql, re.IGNORECASE)
    select_match = re.search(r"\bSELECT\s+(.*?)\s+FROM\b", sql, re.IGNORECASE | re.DOTALL)
    where_match = re.search(r"\bWHERE\s+(.*?)(?:\bGROUP|\bORDER|\bLIMIT|$)", sql, re.IGNORECASE | re.DOTALL)
    group_match = re.search(r"\bGROUP\s+BY\s+(.*?)(?:\bHAVING|\bORDER|\bLIMIT|$)", sql, re.IGNORECASE)
    having_match = re.search(r"\bHAVING\s+(.*?)(?:\bORDER|\bLIMIT|$)", sql, re.IGNORECASE | re.DOTALL)
    order_match = re.search(r"\bORDER\s+BY\s+(.*?)(?:\bLIMIT|$)", sql, re.IGNORECASE | re.DOTALL)
    limit_match = re.search(r"\bLIMIT\s+(\d+)", sql, re.IGNORECASE)
    join_match = re.search(r"\bJOIN\s+(\w+)", sql, re.IGNORECASE)

    from_table = from_match.group(1) if from_match else "table"
    select_cols = select_match.group(1).strip() if select_match else "*"
    where_cond = where_match.group(1).strip() if where_match else None
    group_by = group_match.group(1).strip() if group_match else None
    having_cond = having_match.group(1).strip() if having_match else None
    order_by = order_match.group(1).strip() if order_match else None
    limit_n = limit_match.group(1) if limit_match else None
    joined_table = join_match.group(1) if join_match else None

    # Detect aggregate queries
    agg_patterns = [
        r"\bCOUNT\s*\(\s*\*?\s*\)",
        r"\bSUM\s*\(",
        r"\bAVG\s*\(",
        r"\bMAX\s*\(",
        r"\bMIN\s*\(",
    ]
    is_aggregate = any(re.search(p, sql, re.IGNORECASE) for p in agg_patterns)

    # Build explanation
    if is_aggregate:
        agg_map = {
            "COUNT(": "counts rows in",
            "SUM(": "sums values in",
            "AVG(": "averages values in",
            "MAX(": "finds the maximum value in",
            "MIN(": "finds the minimum value in",
        }
        for fn, label in agg_map.items():
            if fn.lower() in sql.lower():
                if group_by:
                    parts.append(f"Groups rows by {group_by} and {label} {from_table}")
                else:
                    parts.append(f"Calculates a value from all rows in {from_table}")
                break
        else:
            parts.append(f"Performs an aggregate calculation on {from_table}")
    else:
        cols = [c.strip() for c in select_cols.replace("\n", " ").split(",")]
        if len(cols) == 1 and cols[0].upper() == "*":
            parts.append(f"Retrieves all columns from {from_table}")
        else:
            col_names = ", ".join(cols[:3])
            suffix = " and other columns" if len(cols) > 3 else ""
            parts.append(f"Retrieves {col_names}{suffix} from {from_table}")

    if joined_table:
        parts.append(f"joining with {joined_table}")

    if where_cond:
        cond = re.sub(r"\s+", " ", where_cond).strip()
        cond = re.sub(r"\bAND\b", "and", cond, flags=re.IGNORECASE)
        cond = re.sub(r"\bOR\b", "or", cond, flags=re.IGNORECASE)
        parts.append(f"where {cond}")

    if having_cond:
        cond = re.sub(r"\s+", " ", having_cond).strip()
        parts.append(f"having {cond}")

    if group_by and not is_aggregate:
        parts.append(f"grouped by {group_by}")

    if order_by:
        direction = "descending" if re.search(r"\bDESC\b", sql, re.IGNORECASE) else "ascending"
        parts.append(f"ordered by {order_by} in {direction} order")

    if limit_n:
        parts.append(f"limited to {limit_n} result{'s' if int(limit_n) != 1 else ''}")

    result = ". ".join(parts).strip()
    if result:
        result = result[0].upper() + result[1:]
        if not result.endswith("."):
            result += "."
        return result

    return f"Retrieves data from {from_table}."
