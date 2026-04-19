from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FieldType(Enum):
    ALPHABETICAL = "alphabetical"
    ALPHANUMERIC = "alphanumeric"
    NUMERIC = "numeric"
    NUMERIC_SIGNED = "numeric_signed"


class Source(Enum):
    CONSTANT = "constant"
    DEFAULT = "default"
    MODEL = "model"
    BUILTIN = "builtin"
    FORMULA = "formula"


@dataclass
class FieldMetadata:
    tipo: str = ""
    descripcion: str = ""
    validacion: str = ""
    contenido: str = ""


@dataclass
class FieldSpec:
    field_id: str
    name: str
    position: int
    length: int
    field_type: FieldType
    source: Source
    value: str | None = None
    function: str | None = None
    expr: str | None = None
    metadata: FieldMetadata = field(default_factory=FieldMetadata)


@dataclass
class PageSpec:
    id: str
    include_when: str
    fields: tuple[FieldSpec, ...]


@dataclass
class SchemaSpec:
    schema_id: str
    fiscal_year: int
    revision: str
    specification_date: str
    source_file: str
    pages: tuple[PageSpec, ...]


__all__ = [
    "FieldMetadata",
    "FieldSpec",
    "FieldType",
    "PageSpec",
    "SchemaSpec",
    "Source",
]
