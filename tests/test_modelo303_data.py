import pytest
from pydantic import ValidationError

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period


def _base_valid_data() -> dict:
    return {
        "periodo": Period.THIRD_QUARTER,
        "version": "v1.0",
        "nif_empresa_desarrollo": "12345678X",
        "razon_social": "DE LOS PALOTES PERICO",
        "nif_contribuyente": "12345678E",
        "base_imponible": 2000.00,
    }


def test_generate_model_4t_annual_volume_none():
    datos_validos = _base_valid_data()
    datos_validos["periodo"] = Period.FOURTH_QUARTER

    with pytest.raises(
        ValueError,
        match="El volumen anual de operaciones es obligatorio en el 4º trimestre",
    ):
        Modelo303Data(**datos_validos)


def test_generate_model_4t_annual_volume_ok():
    datos_validos = _base_valid_data()
    datos_validos["periodo"] = Period.FOURTH_QUARTER
    datos_validos["volumen_anual_operaciones"] = 10000.0

    datos = Modelo303Data(**datos_validos)
    assert datos.volumen_anual_operaciones == 10000.0


def test_generate_model_non_4t_annual_volume_none():
    datos_validos = _base_valid_data()
    datos_validos["periodo"] = Period.FIRST_QUARTER
    datos_validos["volumen_anual_operaciones"] = None

    datos = Modelo303Data(**datos_validos)
    assert datos.volumen_anual_operaciones is None


def test_generate_model_4t_annual_volume_zero_is_valid():
    datos_validos = _base_valid_data()
    datos_validos["periodo"] = Period.FOURTH_QUARTER
    datos_validos["volumen_anual_operaciones"] = 0.0

    datos = Modelo303Data(**datos_validos)
    assert datos.volumen_anual_operaciones == 0.0


def test_generate_model_defaults_for_optional_amounts():
    datos = Modelo303Data(**_base_valid_data())

    assert datos.base_gastos_bienes_y_servicios == 0
    assert datos.cuota_gastos_bienes_y_servicios == 0
    assert datos.base_adquisiones_bienes_inversion == 0
    assert datos.cuota_adquisiones_bienes_inversion == 0


def test_generate_model_period_invalid():
    datos_validos = _base_valid_data()
    datos_validos["periodo"] = "5T"

    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "periodo" in str(excinfo.value)


def test_generate_model_dev_nif_long():
    datos_validos = _base_valid_data()
    datos_validos["nif_empresa_desarrollo"] = (
        "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "nif_empresa_desarrollo" in str(excinfo.value)


def test_generate_model_dev_nif_short():
    datos_validos = _base_valid_data()
    datos_validos["nif_empresa_desarrollo"] = "1234"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "nif_empresa_desarrollo" in str(excinfo.value)


def test_generate_model_taxpayer_nif_long():
    datos_validos = _base_valid_data()
    datos_validos["nif_contribuyente"] = "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "nif_contribuyente" in str(excinfo.value)


def test_generate_model_taxpayer_nif_short():
    datos_validos = _base_valid_data()
    datos_validos["nif_contribuyente"] = "1234"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "nif_contribuyente" in str(excinfo.value)


def test_generate_model_version_long():
    datos_validos = _base_valid_data()
    datos_validos["version"] = "1.234"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "version" in str(excinfo.value)


def test_generate_model_legal_name_long():
    datos_validos = _base_valid_data()
    datos_validos["razon_social"] = (
        "DE LOS PALOTES PERICO PERO QUE SEA MAYOR DE LO PERMITIDO POR LA AGENCIA TRIBUTARIA"
    )
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "razon_social" in str(excinfo.value)


def test_generate_model_iban_long():
    datos_validos = _base_valid_data()
    datos_validos["iban"] = "ES001234123412341234123412345678901"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "iban" in str(excinfo.value)


def test_generate_model_iban_short():
    datos_validos = _base_valid_data()
    datos_validos["iban"] = "ES0012"
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "iban" in str(excinfo.value)


def test_generate_model_iban_exact_length_ok():
    datos_validos = _base_valid_data()
    datos_validos["iban"] = "ES0012341234123412341234"

    datos = Modelo303Data(**datos_validos)
    assert datos.iban == "ES0012341234123412341234"


def test_generate_model_iban_none_ok():
    datos_validos = _base_valid_data()
    datos_validos["iban"] = None

    datos = Modelo303Data(**datos_validos)
    assert datos.iban is None


def test_generate_model_taxable_base_negative():
    datos_validos = _base_valid_data()
    datos_validos["base_imponible"] = -1000.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "base_imponible" in str(excinfo.value)


def test_generate_model_goods_services_expenses_negative():
    datos_validos = _base_valid_data()
    datos_validos["base_gastos_bienes_y_servicios"] = -500.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "base_gastos_bienes_y_servicios" in str(excinfo.value)


def test_generate_model_vat_goods_services_expenses_negative():
    datos_validos = _base_valid_data()
    datos_validos["cuota_gastos_bienes_y_servicios"] = -100.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "cuota_gastos_bienes_y_servicios" in str(excinfo.value)


def test_generate_model_investment_goods_purchases_negative():
    datos_validos = _base_valid_data()
    datos_validos["base_adquisiones_bienes_inversion"] = -200.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "base_adquisiones_bienes_inversion" in str(excinfo.value)


def test_generate_model_vat_investment_goods_purchases_negative():
    datos_validos = _base_valid_data()
    datos_validos["cuota_adquisiones_bienes_inversion"] = -50.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "cuota_adquisiones_bienes_inversion" in str(excinfo.value)


def test_generate_model_annual_operations_volume_negative():
    datos_validos = _base_valid_data()
    datos_validos["volumen_anual_operaciones"] = -10000.00
    with pytest.raises(ValidationError) as excinfo:
        Modelo303Data(**datos_validos)
    assert "volumen_anual_operaciones" in str(excinfo.value)


def test_generate_model_boundary_lengths_ok():
    datos_validos = _base_valid_data()
    datos_validos["version"] = "v1.0"
    datos_validos["nif_empresa_desarrollo"] = "12345678X"
    datos_validos["nif_contribuyente"] = "12345678E"
    datos_validos["razon_social"] = "A" * 80

    datos = Modelo303Data(**datos_validos)
    assert datos.version == "v1.0"
    assert datos.nif_empresa_desarrollo == "12345678X"
    assert datos.nif_contribuyente == "12345678E"
    assert datos.razon_social == "A" * 80
