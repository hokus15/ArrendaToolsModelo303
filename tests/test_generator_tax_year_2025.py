from golden_helper import load_golden

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.domain.enums import Period


def _base_valid_data() -> dict:
    return {
        "periodo": Period.FIRST_QUARTER,
        "version": "1.00",
        "nif_empresa_desarrollo": "12345678X",
        "razon_social": "DE LOS PALOTES PERICO",
        "nif_contribuyente": "12345678E",
        "base_imponible": 2000.00,
    }


def test_generate_model_1t2t3t_amount_positive():
    expected_result = load_golden(2025, "1T2T3T/positive")
    valid_data = _base_valid_data()
    valid_data["iban"] = "ES0012341234123412341234"

    model_data = Modelo303Data(**valid_data)
    generator = get_generator(2025)
    generated_data = generator.generate(model_data)
    assert generated_data == expected_result


def test_generate_model_1t2t3t_amount_negative():
    expected_result = load_golden(2025, "1T2T3T/negative")
    valid_data = _base_valid_data()
    valid_data["iban"] = "ES0012341234123412341234"
    valid_data["base_gastos_bienes_y_servicios"] = 2500.0
    valid_data["cuota_gastos_bienes_y_servicios"] = 525.0

    model_data = Modelo303Data(**valid_data)
    generator = get_generator(2025)
    generated_data = generator.generate(model_data)
    assert generated_data == expected_result


def test_generate_model_4t_amount_positive():
    expected_result = load_golden(2025, "4T/positive")
    valid_data = _base_valid_data()
    valid_data["iban"] = "ES0012341234123412341234"
    valid_data["periodo"] = Period.FOURTH_QUARTER
    valid_data["volumen_anual_operaciones"] = 6000.0

    model_data = Modelo303Data(**valid_data)
    generator = get_generator(2025)
    generated_data = generator.generate(model_data)
    assert generated_data == expected_result


def test_generate_model_4t_amount_negative():
    expected_result = load_golden(2025, "4T/negative")
    valid_data = _base_valid_data()
    valid_data["iban"] = "ES0012341234123412341234"
    valid_data["periodo"] = Period.FOURTH_QUARTER
    valid_data["base_gastos_bienes_y_servicios"] = 2500.0
    valid_data["cuota_gastos_bienes_y_servicios"] = 525.0
    valid_data["volumen_anual_operaciones"] = 6000.0

    model_data = Modelo303Data(**valid_data)
    generator = get_generator(2025)
    generated_data = generator.generate(model_data)
    assert generated_data == expected_result


def test_generate_model_without_iban():
    expected_result = load_golden(2025, "without_iban")
    valid_data = _base_valid_data()

    model_data = Modelo303Data(**valid_data)
    generator = get_generator(2025)
    generated_data = generator.generate(model_data)
    assert generated_data == expected_result
