"""Tests for schema_validator.py."""

import pytest

from arrendatools.modelo303.infrastructure.schema import (
    FieldSpec,
    FieldType,
    PageSpec,
    SchemaSpec,
    Source,
)
from arrendatools.modelo303.infrastructure.schema_validator import (
    SchemaValidationError,
    validate_schema,
)


def _make_schema(*pages: PageSpec) -> SchemaSpec:
    return SchemaSpec(
        schema_id="test",
        fiscal_year=2099,
        revision="1.0",
        specification_date="2099-01-01",
        source_file="",
        pages=tuple(pages),
    )


def _make_page(
    page_id: str, *fields: FieldSpec, include_when: str = "always"
) -> PageSpec:
    return PageSpec(id=page_id, include_when=include_when, fields=tuple(fields))


def _const_field(name: str, pos: int = 1, length: int = 1) -> FieldSpec:
    return FieldSpec(
        field_id=f"test_{name}",
        name=name,
        position=pos,
        length=length,
        field_type=FieldType.ALPHANUMERIC,
        source=Source.CONSTANT,
        value="X",
    )


def _model_field(name: str, pos: int = 1, length: int = 17) -> FieldSpec:
    return FieldSpec(
        field_id=f"test_{name}",
        name=name,
        position=pos,
        length=length,
        field_type=FieldType.NUMERIC_SIGNED,
        source=Source.MODEL,
    )


class TestValidateSchema:
    def test_valid_schema_passes(self):
        schema = _make_schema(
            _make_page("p1", _const_field("f1"), _model_field("f2", pos=2))
        )
        validate_schema(schema)  # should not raise

    def test_duplicate_page_raises(self):
        schema = _make_schema(
            _make_page("dup", _const_field("f1")),
            _make_page("dup", _const_field("f2")),
        )
        with pytest.raises(SchemaValidationError, match="Duplicate page id"):
            validate_schema(schema)

    def test_invalid_page_include_when_raises(self):
        schema = _make_schema(
            _make_page("p1", _const_field("f1"), include_when="never")
        )
        with pytest.raises(SchemaValidationError, match="invalid include_when"):
            validate_schema(schema)

    def test_duplicate_field_in_page_raises(self):
        schema = _make_schema(
            _make_page("p1", _const_field("dup", 1), _const_field("dup", 2))
        )
        with pytest.raises(SchemaValidationError, match="duplicate field id"):
            validate_schema(schema)

    def test_position_zero_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=0,
            length=1,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.CONSTANT,
            value="X",
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="position must be >= 1"):
            validate_schema(schema)

    def test_length_zero_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=0,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.CONSTANT,
            value="X",
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="length must be >= 1"):
            validate_schema(schema)

    def test_constant_without_value_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=3,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.CONSTANT,
            value=None,
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="requires 'value'"):
            validate_schema(schema)

    def test_default_without_value_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=3,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.DEFAULT,
            value=None,
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="requires 'value'"):
            validate_schema(schema)

    def test_builtin_without_function_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=1,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.BUILTIN,
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="requires 'function'"):
            validate_schema(schema)

    def test_builtin_with_unknown_function_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=1,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.BUILTIN,
            function="unknown_builtin",
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="unknown builtin function"):
            validate_schema(schema)

    def test_model_field_without_attr_passes(self):
        schema = _make_schema(_make_page("p1", _model_field("casilla_07")))
        validate_schema(schema)

    def test_formula_without_expr_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=17,
            field_type=FieldType.NUMERIC_SIGNED,
            source=Source.FORMULA,
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="requires 'expr'"):
            validate_schema(schema)

    def test_formula_with_invalid_syntax_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="f1",
            position=1,
            length=17,
            field_type=FieldType.NUMERIC_SIGNED,
            source=Source.FORMULA,
            expr="casilla_69 ??? casilla_70",
        )
        schema = _make_schema(_make_page("p1", f))
        with pytest.raises(SchemaValidationError, match="unparseable formula"):
            validate_schema(schema)

    def test_fourth_quarter_include_when_is_valid(self):
        schema = _make_schema(
            _make_page("p1", _const_field("f1"), include_when="fourth_quarter")
        )
        validate_schema(schema)  # should not raise

    def test_real_2025_schema_is_valid(self):
        from arrendatools.modelo303.infrastructure.schema_registry import get_schema

        schema = get_schema(2025)
        validate_schema(schema)

    def test_real_2026_schema_is_valid(self):
        from arrendatools.modelo303.infrastructure.schema_registry import get_schema

        schema = get_schema(2026)
        validate_schema(schema)
