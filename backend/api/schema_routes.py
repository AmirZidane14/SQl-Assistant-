from fastapi import APIRouter, HTTPException

from schemas.schema_response import (
    SchemaResponse,
    SchemaTextResponse,
    SchemaRefreshResponse,
)
from services.schema_reader import read_schema
from services.schema_formatter import format_schema_as_text

router = APIRouter(prefix="/api", tags=["schema"])

# In-memory cache — refreshed on startup and via POST /schema/refresh
_schema_cache: list | None = None


def _load_schema() -> list:
    """Load schema from DB (or return cache if available)."""
    global _schema_cache
    if _schema_cache is None:
        _schema_cache = read_schema()
    return _schema_cache


@router.get("/schema", response_model=SchemaResponse)
def get_schema():
    """
    Returns the full database schema as a structured JSON object.
    Includes tables, columns, types, PK/FK flags, and relationships.
    """
    tables = _load_schema()
    total_columns = sum(len(t.columns) for t in tables)
    return SchemaResponse(
        tables=tables,
        total_tables=len(tables),
        total_columns=total_columns,
    )


@router.get("/schema/text", response_model=SchemaTextResponse)
def get_schema_text():
    """
    Returns a LLM-friendly plain-text version of the schema.
    Used by the AI generation prompt to provide DB context.
    """
    tables = _load_schema()
    schema_text = format_schema_as_text(tables)
    return SchemaTextResponse(
        schema_text=schema_text,
        table_count=len(tables),
        cached=_schema_cache is not None,
    )


@router.post("/schema/refresh", response_model=SchemaRefreshResponse)
def refresh_schema():
    """
    Forces a re-read of the database schema, invalidating the in-memory cache.
    Call this after the database schema changes.
    """
    global _schema_cache
    _schema_cache = None
    tables = _load_schema()
    return SchemaRefreshResponse(
        success=True,
        message="Schema cache refreshed successfully",
        table_count=len(tables),
    )