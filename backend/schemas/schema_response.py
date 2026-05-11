from pydantic import BaseModel


class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    primary_key: bool
    foreign_key: bool
    foreign_key_ref: str | None = None


class RelationshipInfo(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    description: str


class TableInfo(BaseModel):
    name: str
    columns: list[ColumnInfo]
    relationships: list[RelationshipInfo]


class SchemaResponse(BaseModel):
    tables: list[TableInfo]
    total_tables: int
    total_columns: int


class SchemaTextResponse(BaseModel):
    schema_text: str
    table_count: int
    cached: bool


class SchemaRefreshResponse(BaseModel):
    success: bool
    message: str
    table_count: int