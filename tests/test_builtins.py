"""Tests for builtins.py."""

from decimal import Decimal

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.builtins import BUILTIN_REGISTRY


def _build_model(
    periodo: Period, base_imponible: Decimal = Decimal("0.00"), iban: str = ""
) -> Modelo303Model:
    data = Modelo303Data(
        periodo=periodo,
        version="v1.0",
        nif_empresa_desarrollo="12345678X",
        razon_social="EMPRESA TEST SL",
        nif_contribuyente="12345678E",
        iban=iban or None,
        base_imponible=base_imponible,
        **(
            {"volumen_anual_operaciones": Decimal("10000.00")}
            if periodo == Period.FOURTH_QUARTER
            else {}
        ),
    )
    return Modelo303Model.from_data(data, fiscal_year=2025)


class TestBuiltinRegistry:
    def test_registry_contains_expected_keys(self):
        assert "tipo_declaracion" in BUILTIN_REGISTRY
        assert "exencion_390" in BUILTIN_REGISTRY
        assert "operaciones_no_cero" in BUILTIN_REGISTRY
        assert "sepa" in BUILTIN_REGISTRY

    def test_declaration_type_zero_amount(self):
        model = _build_model(Period.FIRST_QUARTER, base_imponible=Decimal("0.00"))
        result = BUILTIN_REGISTRY["tipo_declaracion"](model)
        assert result == "N"

    def test_declaration_type_positive_with_iban(self):
        model = _build_model(
            Period.FIRST_QUARTER,
            base_imponible=Decimal("1000.00"),
            iban="ES0012341234123412341234",
        )
        result = BUILTIN_REGISTRY["tipo_declaracion"](model)
        assert result == "U"

    def test_declaration_type_positive_without_iban(self):
        model = _build_model(Period.FIRST_QUARTER, base_imponible=Decimal("1000.00"))
        result = BUILTIN_REGISTRY["tipo_declaracion"](model)
        assert result == "I"

    def test_declaration_type_negative_non_q4(self):
        model = _build_model(Period.SECOND_QUARTER, base_imponible=Decimal("0.00"))
        # Inject negative amount manually
        model.casilla_29 = Decimal("99999.00")
        result = BUILTIN_REGISTRY["tipo_declaracion"](model)
        assert result == "C"

    def test_exoneracion_modelo_390_q1_returns_0(self):
        model = _build_model(Period.FIRST_QUARTER)
        result = BUILTIN_REGISTRY["exencion_390"](model)
        assert result == "0"

    def test_exoneracion_modelo_390_q4_returns_1(self):
        model = _build_model(Period.FOURTH_QUARTER)
        result = BUILTIN_REGISTRY["exencion_390"](model)
        assert result == "1"

    def test_operaciones_no_0_q2_returns_0(self):
        model = _build_model(Period.SECOND_QUARTER)
        result = BUILTIN_REGISTRY["operaciones_no_cero"](model)
        assert result == "0"

    def test_operaciones_no_0_q4_returns_1(self):
        model = _build_model(Period.FOURTH_QUARTER)
        result = BUILTIN_REGISTRY["operaciones_no_cero"](model)
        assert result == "1"

    def test_marca_sepa_returns_0(self):
        model = _build_model(Period.FIRST_QUARTER, iban="ES0012341234123412341234")
        result = BUILTIN_REGISTRY["sepa"](model)
        assert result == "0"
