from sqlalchemy import inspect

from database.connection import engine
from schemas.schema_response import ColumnInfo, RelationshipInfo, TableInfo


def _get_table_columns(table_name: str, fk_map: dict) -> list[ColumnInfo]:
    """
    Inspect all columns of a table and annotate each with FK info.
    fk_map: {(table, column): (ref_table, ref_col)}
    """
    inspector = inspect(engine)
    columns = []
    for col in inspector.get_columns(table_name):
        col_name = col["name"]
        key = (table_name, col_name)
        ref = fk_map.get(key)
        columns.append(ColumnInfo(
            name=col_name,
            type=str(col["type"]),
            nullable=col.get("nullable", True),
            primary_key=col.get("primary", False),
            foreign_key=ref is not None,
            foreign_key_ref=f"{ref[0]}.{ref[1]}" if ref else None,
        ))
    return columns


def _build_fk_map() -> dict:
    """
    Build a dict mapping (table, column) -> (referenced_table, referenced_column).
    Works for both SQLite and PostgreSQL/MySQL via SQLAlchemy's inspector.
    """
    inspector = inspect(engine)
    fk_map = {}
    for table_name in inspector.get_table_names():
        for fk in inspector.get_foreign_keys(table_name):
            for col in fk["constrained_columns"]:
                fk_map[(table_name, col)] = (fk["referred_table"], fk["referred_columns"][0])
    return fk_map


def _infer_relationships(fk_map: dict, table_columns: dict) -> list[RelationshipInfo]:
    """
    Build human-readable relationship descriptions from FK map.
    E.g. orders.customer_id → customers.id becomes:
         "orders belongs to customers via customer_id"
         "customers has many orders via customer_id"
    """
    relationships = []
    for (src_table, src_col), (tgt_table, tgt_col) in fk_map.items():
        relationships.append(RelationshipInfo(
            source_table=src_table,
            source_column=src_col,
            target_table=tgt_table,
            target_column=tgt_col,
            description=f"{src_table} belongs to {tgt_table} via {src_col}",
        ))
        relationships.append(RelationshipInfo(
            source_table=tgt_table,
            source_column=tgt_col,
            target_table=src_table,
            target_column=src_col,
            description=f"{tgt_table} has many {src_table} via {src_col}",
        ))
    return relationships


def read_schema() -> list[TableInfo]:
    """
    Full database introspection: returns a list of TableInfo with columns and relationships.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    fk_map = _build_fk_map()
    all_rels = _infer_relationships(fk_map, {})

    tables = []
    for table_name in table_names:
        columns = _get_table_columns(table_name, fk_map)
        table_rels = [r for r in all_rels if r.source_table == table_name]
        tables.append(TableInfo(
            name=table_name,
            columns=columns,
            relationships=table_rels,
        ))

    return tables