from services.schema_reader import read_schema


def format_schema_as_text(tables: list) -> str:
    """
    Convert the schema structure into a clean, LLM-friendly text format.
    This string is injected into the AI prompt so it knows the DB structure.
    """
    lines = []
    lines.append("DATABASE SCHEMA")
    lines.append("=" * 40)
    lines.append("")

    for table in tables:
        lines.append(f"TABLE {table.name}:")
        for col in table.columns:
            parts = [f"{col.name} ({col.type.upper()}"]
            if col.primary_key:
                parts.append("PRIMARY KEY")
            if col.foreign_key:
                parts.append(f"FOREIGN KEY → {col.foreign_key_ref}")
            if not col.nullable and not col.primary_key:
                parts.append("NOT NULL")
            parts[-1] = parts[-1] + ")"
            lines.append("  - " + ", ".join(parts).replace("  - ", "  - "))

        if table.columns:
            pass

        if table.relationships:
            lines.append("")
            lines.append("  RELATIONSHIPS:")
            seen = set()
            for rel in table.relationships:
                key = (rel.source_table, rel.target_table, rel.description)
                if key not in seen:
                    seen.add(key)
                    lines.append(f"    • {rel.description}")

        lines.append("")

    return "\n".join(lines)


def build_llm_schema_context(tables: list) -> str:
    """
    High-level entry point that reads the schema and returns a formatted string.
    """
    schema = read_schema() if not tables else tables
    return format_schema_as_text(schema)