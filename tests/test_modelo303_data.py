import unittest

from pydantic import ValidationError

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period


class TestModelo303Data(unittest.TestCase):
    def setUp(self):
        # Datos base válidos
        self.datos_validos = {
            "ejercicio": Period.THIRD_QUARTER,
            "version": "v1.0",
            "nif_empresa_desarrollo": "12345678X",
            "razon_social": "DE LOS PALOTES PERICO",
            "nif_contribuyente": "12345678E",
            "base_imponible": 2000.00,
        }

    def test_generate_model_4T_annual_volume_none(self):
        self.datos_validos["ejercicio"] = Period.FOURTH_QUARTER

        with self.assertRaisesRegex(
            ValidationError,
            "El volumen anual de operaciones es obligatorio en el 4º trimestre*",
        ):
            Modelo303Data(**self.datos_validos)

    def test_generate_model_4T_annual_volume_ok(self):
        self.datos_validos["ejercicio"] = Period.FOURTH_QUARTER
        self.datos_validos["volumen_anual_operaciones"] = 10000.0

        datos = Modelo303Data(**self.datos_validos)
        self.assertEqual(datos.volumen_anual_operaciones, 10000.0)

    def test_generate_model_non_4T_annual_volume_none(self):
        self.datos_validos["ejercicio"] = Period.FIRST_QUARTER
        self.datos_validos["volumen_anual_operaciones"] = None

        datos = Modelo303Data(**self.datos_validos)
        self.assertIsNone(datos.volumen_anual_operaciones)

    def test_generate_model_4T_annual_volume_zero_is_valid(self):
        self.datos_validos["ejercicio"] = Period.FOURTH_QUARTER
        self.datos_validos["volumen_anual_operaciones"] = 0.0

        datos = Modelo303Data(**self.datos_validos)
        self.assertEqual(datos.volumen_anual_operaciones, 0.0)

    def test_generate_model_defaults_for_optional_amounts(self):
        datos = Modelo303Data(**self.datos_validos)

        self.assertEqual(datos.base_gastos_bienes_y_servicios, 0)
        self.assertEqual(datos.cuota_gastos_bienes_y_servicios, 0)
        self.assertEqual(datos.base_adquisiones_bienes_inversion, 0)
        self.assertEqual(datos.cuota_adquisiones_bienes_inversion, 0)

    def test_generate_model_period_invalid(self):
        self.datos_validos["ejercicio"] = "5T"

        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("ejercicio", str(cm.exception))

    def test_generate_model_dev_nif_long(self):
        self.datos_validos["nif_empresa_desarrollo"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generate_model_dev_nif_short(self):
        self.datos_validos["nif_empresa_desarrollo"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("nif_empresa_desarrollo", str(cm.exception))

    def test_generate_model_taxpayer_nif_long(self):
        self.datos_validos["nif_contribuyente"] = (
            "12345678XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generate_model_taxpayer_nif_short(self):
        self.datos_validos["nif_contribuyente"] = "1234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("nif_contribuyente", str(cm.exception))

    def test_generate_model_version_long(self):
        self.datos_validos["version"] = "1.234"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("version", str(cm.exception))

    def test_generate_model_legal_name_long(self):
        self.datos_validos["razon_social"] = (
            "DE LOS PALOTES PERICO PERO QUE SEA MAYOR DE LO PERMITIDO POR LA AGENCIA TRIBUTARIA"
        )
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("razon_social", str(cm.exception))

    def test_generate_model_iban_long(self):
        self.datos_validos["iban"] = "ES001234123412341234123412345678901"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("iban", str(cm.exception))

    def test_generate_model_iban_short(self):
        self.datos_validos["iban"] = "ES0012"
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("iban", str(cm.exception))

    def test_generate_model_iban_exact_length_ok(self):
        self.datos_validos["iban"] = "ES0012341234123412341234"

        datos = Modelo303Data(**self.datos_validos)
        self.assertEqual(datos.iban, "ES0012341234123412341234")

    def test_generate_model_iban_none_ok(self):
        self.datos_validos["iban"] = None

        datos = Modelo303Data(**self.datos_validos)
        self.assertIsNone(datos.iban)

    def test_generate_model_taxable_base_negative(self):
        self.datos_validos["base_imponible"] = -1000.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("base_imponible", str(cm.exception))

    def test_generate_model_goods_services_expenses_negative(self):
        self.datos_validos["base_gastos_bienes_y_servicios"] = -500.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("base_gastos_bienes_y_servicios", str(cm.exception))

    def test_generate_model_vat_goods_services_expenses_negative(self):
        self.datos_validos["cuota_gastos_bienes_y_servicios"] = -100.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("cuota_gastos_bienes_y_servicios", str(cm.exception))

    def test_generate_model_investment_goods_purchases_negative(self):
        self.datos_validos["base_adquisiones_bienes_inversion"] = -200.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("base_adquisiones_bienes_inversion", str(cm.exception))

    def test_generate_model_vat_investment_goods_purchases_negative(self):
        self.datos_validos["cuota_adquisiones_bienes_inversion"] = -50.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("cuota_adquisiones_bienes_inversion", str(cm.exception))

    def test_generate_model_annual_operations_volume_negative(self):
        self.datos_validos["volumen_anual_operaciones"] = -10000.00
        with self.assertRaises(ValidationError) as cm:
            Modelo303Data(**self.datos_validos)
        self.assertIn("volumen_anual_operaciones", str(cm.exception))

    def test_generate_model_boundary_lengths_ok(self):
        self.datos_validos["version"] = "v1.0"
        self.datos_validos["nif_empresa_desarrollo"] = "12345678X"
        self.datos_validos["nif_contribuyente"] = "12345678E"
        self.datos_validos["razon_social"] = "A" * 80

        datos = Modelo303Data(**self.datos_validos)
        self.assertEqual(datos.version, "v1.0")
        self.assertEqual(datos.nif_empresa_desarrollo, "12345678X")
        self.assertEqual(datos.nif_contribuyente, "12345678E")
        self.assertEqual(datos.razon_social, "A" * 80)


if __name__ == "__main__":
    unittest.main()
