import unittest

from golden_helper import load_golden

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.domain.enums import Period


class TestTaxYear2026Generator(unittest.TestCase):
    def setUp(self):
        self.fiscal_year = 2026
        # Datos base válidos
        self.valid_data = {
            "version": "1.00",
            "nif_empresa_desarrollo": "12345678X",
            "razon_social": "DE LOS PALOTES PERICO",
            "nif_contribuyente": "12345678E",
            "base_imponible": 2000.00,
        }

    def test_generate_model_1T2T3T_amount_positive(self):
        expected_result = load_golden(2026, "1T2T3T/positive")
        self.valid_data["iban"] = "ES0012341234123412341234"
        self.valid_data["ejercicio"] = Period.FIRST_QUARTER

        model_data = Modelo303Data(**self.valid_data)
        generator = get_generator(self.fiscal_year)
        generated_data = generator.generate(model_data)
        self.assertEqual(generated_data, expected_result)

    def test_generate_model_1T2T3T_amount_negative(self):
        expected_result = load_golden(2026, "1T2T3T/negative")
        self.valid_data["iban"] = "ES0012341234123412341234"
        self.valid_data["ejercicio"] = Period.FIRST_QUARTER
        self.valid_data["base_gastos_bienes_y_servicios"] = 2500.0
        self.valid_data["cuota_gastos_bienes_y_servicios"] = 525.0

        model_data = Modelo303Data(**self.valid_data)
        generator = get_generator(self.fiscal_year)
        generated_data = generator.generate(model_data)
        self.assertEqual(generated_data, expected_result)

    def test_generate_model_4T_amount_positive(self):
        expected_result = load_golden(2026, "4T")
        self.valid_data["iban"] = "ES0012341234123412341234"
        self.valid_data["ejercicio"] = Period.FOURTH_QUARTER
        self.valid_data["volumen_anual_operaciones"] = 6000.0

        model_data = Modelo303Data(**self.valid_data)
        generator = get_generator(self.fiscal_year)
        generated_data = generator.generate(model_data)
        self.assertEqual(generated_data, expected_result)

    def test_generate_model_without_iban(self):
        expected_result = load_golden(2026, "without_iban")

        self.valid_data["ejercicio"] = Period.SECOND_QUARTER
        model_data = Modelo303Data(**self.valid_data)
        generator = get_generator(self.fiscal_year)
        generated_data = generator.generate(model_data)
        self.assertEqual(generated_data, expected_result)


if __name__ == "__main__":
    unittest.main()
