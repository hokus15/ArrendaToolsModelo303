"""Infrastructure layer exports for layout and field metadata."""

from .catalog import FIELD_CATALOG, FieldDef, FieldType
from .layout import LayoutSpec, PageSpec
from .layout_registry import LAYOUTS, get_layout, list_supported_years

__all__ = [
    "FieldType",
    "FieldDef",
    "FIELD_CATALOG",
    "PageSpec",
    "LayoutSpec",
    "LAYOUTS",
    "get_layout",
    "list_supported_years",
]
