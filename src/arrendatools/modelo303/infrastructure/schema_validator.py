from __future__ import annotations

import ast

from arrendatools.modelo303.infrastructure.schema import FieldSpec, SchemaSpec, Source

VALID_PAGE_INCLUDE_WHEN = {"always", "fourth_quarter"}


class SchemaValidationError(ValueError):
    pass


def validate_schema(schema: SchemaSpec) -> None:
    """Validate a SchemaSpec for structural correctness. Raises SchemaValidationError."""
    _check_no_duplicate_pages(schema)
    for page in schema.pages:
        _check_page_include_when(page)
        _check_no_duplicate_fields(page)
        for field_spec in page.fields:
            _check_field(field_spec)


def _check_no_duplicate_pages(schema: SchemaSpec) -> None:
    seen: set[str] = set()
    for page in schema.pages:
        if page.id in seen:
            raise SchemaValidationError(f"Duplicate page id: {page.id!r}")
        seen.add(page.id)


def _check_page_include_when(page) -> None:
    if page.include_when not in VALID_PAGE_INCLUDE_WHEN:
        raise SchemaValidationError(
            f"Page '{page.id}': invalid include_when: {page.include_when!r}. "
            f"Valid values: {sorted(VALID_PAGE_INCLUDE_WHEN)}"
        )


def _check_no_duplicate_fields(page) -> None:
    seen: set[str] = set()
    for field_spec in page.fields:
        if field_spec.field_id in seen:
            raise SchemaValidationError(
                f"Page '{page.id}': duplicate field id: {field_spec.field_id!r}"
            )
        seen.add(field_spec.field_id)


def _check_field(field_spec: FieldSpec) -> None:
    fid = field_spec.field_id
    if field_spec.position < 1:
        raise SchemaValidationError(
            f"Field '{fid}': position must be >= 1, got {field_spec.position}"
        )
    if field_spec.length < 1:
        raise SchemaValidationError(
            f"Field '{fid}': length must be >= 1, got {field_spec.length}"
        )
    _check_source(field_spec)


def _check_source(field_spec: FieldSpec) -> None:
    fid = field_spec.field_id
    source = field_spec.source
    if source in (Source.CONSTANT, Source.DEFAULT):
        if field_spec.value is None:
            raise SchemaValidationError(
                f"Field '{fid}': source={source.value!r} requires 'value' to be set"
            )
    elif source == Source.MODEL:
        pass  # attr defaults to name when absent
    elif source == Source.BUILTIN:
        if not field_spec.function:
            raise SchemaValidationError(
                f"Field '{fid}': source='builtin' requires 'function'"
            )
    elif source == Source.FORMULA:
        if not field_spec.expr:
            raise SchemaValidationError(
                f"Field '{fid}': source='formula' requires 'expr'"
            )
        _check_formula_syntax(fid, field_spec.expr)


def _check_formula_syntax(field_id: str, expr: str) -> None:
    try:
        ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise SchemaValidationError(
            f"Field '{field_id}': unparseable formula {expr!r}"
        ) from exc
