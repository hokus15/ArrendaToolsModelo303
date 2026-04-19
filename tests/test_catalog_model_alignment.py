"""Tests de alineación entre schemas y modelo."""

from dataclasses import fields

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.schema_registry import (
    SUPPORTED_SCHEMAS,
    get_schema,
)
from arrendatools.modelo303.infrastructure.schema_renderer import (
    _build_context,
    _render_field,
    _resolve_value,
)

LITERAL_FIELDS = {
    "registro_general_open",
    "registro_general_close",
    "modelo",
    "discriminante",
    "tipo_y_cierre",
    "aux_open",
    "aux_close",
    "did_open",
    "did_close",
    "dp30304_open",
    "dp30304_close",
    "dp30305_open",
    "dp30305_close",
    "dp30301_open",
    "dp30301_close",
    "dp30303_open",
    "dp30303_close",
}


def _build_model(fiscal_year: int = 2026) -> Modelo303Model:
    data = Modelo303Data(
        periodo=Period.THIRD_QUARTER,
        version="v1.0",
        nif_empresa_desarrollo="12345678X",
        razon_social="DE LOS PALOTES PERICO",
        nif_contribuyente="12345678E",
        iban="ES0012341234123412341234",
        base_imponible=2000,
    )
    return Modelo303Model.from_data(data, fiscal_year=fiscal_year)


class TestCatalogModelAlignment:
    def test_all_data_fields_exist_explicitly_in_model(self):
        """All non-literal, non-casilla, non-reserved schema fields must exist in Modelo303Model."""
        model_fields = {item.name for item in fields(Modelo303Model)}

        schema_data_fields: set[str] = set()
        for fiscal_year in SUPPORTED_SCHEMAS:
            schema = get_schema(fiscal_year)
            for page in schema.pages:
                for field_spec in page.fields:
                    if field_spec.source.value not in (
                        "constant",
                        "default",
                        "builtin",
                        "formula",
                    ):
                        effective = field_spec.name
                        if (
                            not effective.startswith("casilla_")
                            and not effective.startswith("reserved_")
                            and not effective.startswith("reservado_")
                            and effective not in LITERAL_FIELDS
                        ):
                            schema_data_fields.add(effective)

        missing = sorted(schema_data_fields - model_fields)

        assert not missing, (
            "Campos de datos del schema sin atributo explícito en Modelo303Model:\n"
            + "\n".join(missing)
        )

    def test_all_schema_fields_render_without_error(self):
        """Every field in every schema must render without error against a real model."""
        unresolved: list[str] = []

        for fiscal_year in SUPPORTED_SCHEMAS:
            schema = get_schema(fiscal_year)
            model = _build_model(fiscal_year)
            context = _build_context(model)
            for page in schema.pages:
                for field_spec in page.fields:
                    try:
                        raw_value = _resolve_value(field_spec, model, context)
                        _render_field(field_spec, raw_value)
                    except Exception as exc:  # noqa: BLE001
                        unresolved.append(f"{fiscal_year}/{field_spec.field_id}: {exc}")

        assert not unresolved, (
            "Campos del schema que fallan al renderizar:\n"
            + "\n".join(sorted(unresolved))
        )

    def test_schemas_have_expected_years(self):
        assert 2025 in SUPPORTED_SCHEMAS
        assert 2026 in SUPPORTED_SCHEMAS

    def test_schema_pages_non_empty(self):
        for fiscal_year in SUPPORTED_SCHEMAS:
            schema = get_schema(fiscal_year)
            assert schema.pages, f"El schema {fiscal_year} no tiene páginas"
            for page in schema.pages:
                assert page.id.strip(), f"Página sin id en schema {fiscal_year}"
