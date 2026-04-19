"""Infrastructure layer exports for schema and field metadata."""

from .schema import FieldSpec, FieldType, PageSpec, SchemaSpec, Source
from .schema_registry import SUPPORTED_SCHEMAS, get_schema, list_supported_years

__all__ = [
    "FieldType",
    "FieldSpec",
    "PageSpec",
    "SchemaSpec",
    "Source",
    "SUPPORTED_SCHEMAS",
    "get_schema",
    "list_supported_years",
]
