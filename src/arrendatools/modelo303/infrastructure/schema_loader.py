from __future__ import annotations

from pathlib import Path
from typing import Union

import yaml

from arrendatools.modelo303.infrastructure.schema import (
    FieldMetadata,
    FieldSpec,
    FieldType,
    PageSpec,
    SchemaSpec,
    Source,
)


def load_schema(source: Union[Path, str, object]) -> SchemaSpec:
    """Load a SchemaSpec from a YAML file path or importlib.resources Traversable."""
    if hasattr(source, "read_text"):
        content = source.read_text(encoding="utf-8")
    else:
        with open(source, encoding="utf-8") as fh:
            content = fh.read()
    data = yaml.safe_load(content)
    return _parse_schema(data)


def _parse_schema(data: dict) -> SchemaSpec:
    pages = tuple(_parse_page(p) for p in data.get("pages", []))
    return SchemaSpec(
        schema_id=str(data["schema_id"]),
        fiscal_year=int(data["fiscal_year"]),
        revision=str(data["revision"]),
        specification_date=str(data["specification_date"]),
        source_file=str(data.get("source_file", "")),
        pages=pages,
    )


def _parse_page(data: dict) -> PageSpec:
    fields = tuple(_parse_field(f) for f in data.get("fields") or [])
    return PageSpec(
        id=str(data["id"]),
        include_when=str(data.get("include_when", "always")),
        fields=fields,
    )


def _parse_field(data: dict) -> FieldSpec:
    meta_raw = data.get("metadata") or {}
    return FieldSpec(
        field_id=str(data["id"]),
        name=str(data["name"]),
        position=int(data["position"]),
        length=int(data["length"]),
        field_type=FieldType(str(data["field_type"])),
        source=Source(str(data["source"])),
        value=_nullable_str(data.get("value")),
        function=_nullable_str(data.get("function")),
        expr=_nullable_str(data.get("expr")),
        metadata=FieldMetadata(
            tipo=str(meta_raw.get("tipo") or ""),
            descripcion=str(meta_raw.get("descripcion") or ""),
            validacion=str(meta_raw.get("validacion") or ""),
            contenido=str(meta_raw.get("contenido") or ""),
        ),
    )


def _nullable_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
