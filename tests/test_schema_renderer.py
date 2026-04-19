"""Tests for schema_renderer.py and the formula evaluator."""

from decimal import Decimal

import pytest

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.schema import (
    FieldSpec,
    FieldType,
    PageSpec,
    SchemaSpec,
    Source,
)
from arrendatools.modelo303.infrastructure.schema_renderer import (
    _build_context,
    _evaluate_formula,
    render_schema,
)


def _build_model(fiscal_year: int = 2025) -> Modelo303Model:
    data = Modelo303Data(
        periodo=Period.FIRST_QUARTER,
        version="v1.0",
        nif_empresa_desarrollo="12345678X",
        razon_social="EMPRESA TEST SL",
        nif_contribuyente="12345678E",
        iban="ES0012341234123412341234",
        base_imponible=Decimal("1000.00"),
    )
    return Modelo303Model.from_data(data, fiscal_year=fiscal_year)


def _make_schema(*pages: PageSpec, fiscal_year: int = 2025) -> SchemaSpec:
    return SchemaSpec(
        schema_id="test",
        fiscal_year=fiscal_year,
        revision="1.0",
        specification_date="2025-01-01",
        source_file="",
        pages=tuple(pages),
    )


def _make_page(
    page_id: str, *fields: FieldSpec, include_when: str = "always"
) -> PageSpec:
    return PageSpec(id=page_id, include_when=include_when, fields=tuple(fields))


class TestRenderConstant:
    def test_constant_field_renders_value(self):
        f = FieldSpec(
            field_id="p1_1",
            name="modelo",
            position=1,
            length=3,
            field_type=FieldType.NUMERIC,
            source=Source.CONSTANT,
            value="303",
        )
        schema = _make_schema(_make_page("p1", f))
        model = _build_model()
        result = render_schema(schema, model)
        assert result == "303"

    def test_constant_empty_value_renders_spaces(self):
        f = FieldSpec(
            field_id="p1_1",
            name="reserved_4",
            position=1,
            length=4,
            field_type=FieldType.ALPHANUMERIC,
            source=Source.CONSTANT,
            value="",
        )
        schema = _make_schema(_make_page("p1", f))
        model = _build_model()
        result = render_schema(schema, model)
        assert result == "    "  # 4 spaces


class TestRenderModel:
    def test_model_field_renders_attribute(self):
        f = FieldSpec(
            field_id="p1_1",
            name="ejercicio",
            position=1,
            length=4,
            field_type=FieldType.NUMERIC,
            source=Source.MODEL,
        )
        schema = _make_schema(_make_page("p1", f))
        model = _build_model(fiscal_year=2025)
        result = render_schema(schema, model)
        assert result == "2025"


class TestRenderPageIncludeWhen:
    def test_fourth_quarter_page_excluded_for_q1(self):
        f = FieldSpec(
            field_id="q4_1",
            name="modelo",
            position=1,
            length=3,
            field_type=FieldType.NUMERIC,
            source=Source.CONSTANT,
            value="303",
        )
        schema = _make_schema(_make_page("q4_only", f, include_when="fourth_quarter"))
        model = _build_model()  # Q1
        assert render_schema(schema, model) == ""

    def test_fourth_quarter_page_included_for_q4(self):
        data = Modelo303Data(
            periodo=Period.FOURTH_QUARTER,
            version="v1.0",
            nif_empresa_desarrollo="12345678X",
            razon_social="EMPRESA TEST SL",
            nif_contribuyente="12345678E",
            iban="ES0012341234123412341234",
            base_imponible=Decimal("500.00"),
            volumen_anual_operaciones=Decimal("10000.00"),
        )
        model = Modelo303Model.from_data(data, fiscal_year=2025)
        f = FieldSpec(
            field_id="q4_1",
            name="modelo",
            position=1,
            length=3,
            field_type=FieldType.NUMERIC,
            source=Source.CONSTANT,
            value="303",
        )
        schema = _make_schema(_make_page("q4_only", f, include_when="fourth_quarter"))
        assert render_schema(schema, model) == "303"

    def test_unknown_include_when_raises(self):
        f = FieldSpec(
            field_id="p1_1",
            name="modelo",
            position=1,
            length=3,
            field_type=FieldType.NUMERIC,
            source=Source.CONSTANT,
            value="303",
        )
        schema = _make_schema(_make_page("p1", f, include_when="never"))
        model = _build_model()
        with pytest.raises(ValueError, match="unknown include_when"):
            render_schema(schema, model)


class TestFormulaEvaluator:
    def _ctx(self, **kwargs) -> dict:
        model = _build_model()
        for k, v in kwargs.items():
            setattr(model, k, Decimal(str(v)))
        return _build_context(model)

    def test_addition(self):
        ctx = self._ctx(casilla_07=Decimal("100.00"), casilla_09=Decimal("21.00"))
        result = _evaluate_formula("casilla_07 + casilla_09", ctx)
        assert result == Decimal("121.00")

    def test_subtraction(self):
        ctx = self._ctx(casilla_69=Decimal("500.00"), casilla_70=Decimal("100.00"))
        result = _evaluate_formula("casilla_69 - casilla_70", ctx)
        assert result == Decimal("400.00")

    def test_complex_formula(self):
        ctx = self._ctx(
            casilla_69=Decimal("500.00"),
            casilla_70=Decimal("100.00"),
            casilla_109=Decimal("50.00"),
            casilla_112=Decimal("25.00"),
        )
        result = _evaluate_formula(
            "casilla_69 - casilla_70 + casilla_109 - casilla_112", ctx
        )
        assert result == Decimal("425.00")

    def test_unknown_variable_raises(self):
        ctx = _build_context(_build_model())
        with pytest.raises(ValueError, match="Unknown variable"):
            _evaluate_formula("casilla_99999 + casilla_07", ctx)

    def test_invalid_syntax_raises(self):
        ctx = _build_context(_build_model())
        with pytest.raises(ValueError, match="Invalid formula"):
            _evaluate_formula("casilla_07 ??? casilla_09", ctx)

    def test_no_eval_on_unsafe_node(self):
        ctx = _build_context(_build_model())
        with pytest.raises(ValueError):
            _evaluate_formula("__import__('os')", ctx)


class TestRenderFormula:
    def test_formula_field_renders_correctly(self):
        """casilla_71 via formula: casilla_69 - casilla_70 + casilla_109 - casilla_112."""
        f = FieldSpec(
            field_id="p1_1",
            name="casilla_71",
            position=1,
            length=17,
            field_type=FieldType.NUMERIC_SIGNED,
            source=Source.FORMULA,
            expr="casilla_69 - casilla_70 + casilla_109 - casilla_112",
        )
        schema = _make_schema(_make_page("p1", f))

        data = Modelo303Data(
            periodo=Period.FIRST_QUARTER,
            version="v1.0",
            nif_empresa_desarrollo="12345678X",
            razon_social="EMPRESA TEST SL",
            nif_contribuyente="12345678E",
            iban="ES0012341234123412341234",
            base_imponible=Decimal("0.00"),
        )
        model = Modelo303Model.from_data(data, fiscal_year=2026)
        # casilla_69 - 0 + 0 - 0 = 0
        assert render_schema(schema, model) == "0" * 17
