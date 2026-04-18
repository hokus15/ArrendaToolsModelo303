"""Tests de alineación entre catálogo, layouts y modelo."""

from dataclasses import fields

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.catalog import FIELD_CATALOG
from arrendatools.modelo303.infrastructure.layout_registry import LAYOUTS

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
        model_fields = {item.name for item in fields(Modelo303Model)}
        data_fields_in_catalog = {
            name
            for name in FIELD_CATALOG.keys()
            if not name.startswith("casilla_")
            and not name.startswith("reserved_")
            and not name.startswith("reservado_")
            and name not in LITERAL_FIELDS
        }

        missing = sorted(data_fields_in_catalog - model_fields)

        assert not missing, (
            "Campos de datos del catálogo sin atributo explícito en Modelo303Model:\n"
            + "\n".join(missing)
        )

    def test_all_layout_fields_exist_in_catalog(self):
        missing: list[str] = []

        for layout in LAYOUTS.values():
            for page in layout.pages:
                for field_name in page.fields:
                    if field_name not in FIELD_CATALOG:
                        missing.append(field_name)

        assert not missing, (
            "Campos presentes en layout pero ausentes en FIELD_CATALOG:\n"
            + "\n".join(sorted(set(missing)))
        )

    def test_model_and_catalog_can_render_every_catalog_field(self):
        model = _build_model(2026)

        unresolved: list[str] = []
        for field_name in FIELD_CATALOG.keys():
            try:
                raw_value = getattr(model, field_name, None)
                FIELD_CATALOG[field_name].render(field_name, raw_value)
            except ValueError:
                unresolved.append(field_name)

        assert not unresolved, (
            "Campos en FIELD_CATALOG sin resolver/renderizar por modelo+catálogo:\n"
            + "\n".join(sorted(unresolved))
        )

    def test_layouts_have_expected_years(self):
        assert 2025 in LAYOUTS
        assert 2026 in LAYOUTS

    def test_layout_pages_non_empty(self):
        for fiscal_year, layout in LAYOUTS.items():
            assert layout.pages, f"El layout {fiscal_year} no tiene páginas"
            for page in layout.pages:
                assert page.name.strip(), f"Página sin nombre en layout {fiscal_year}"
