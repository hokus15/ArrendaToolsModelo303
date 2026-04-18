import unittest

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model


class TestBusinessRules(unittest.TestCase):
    def _make_data(self, **overrides) -> Modelo303Data:
        payload = {
            "ejercicio": Period.THIRD_QUARTER,
            "version": "v1.0",
            "nif_empresa_desarrollo": "12345678X",
            "razon_social": "DE LOS PALOTES PERICO",
            "nif_contribuyente": "12345678E",
            "base_imponible": 2000.0,
            "base_gastos_bienes_y_servicios": 0.0,
            "cuota_gastos_bienes_y_servicios": 0.0,
            "base_adquisiones_bienes_inversion": 0.0,
            "cuota_adquisiones_bienes_inversion": 0.0,
        }
        payload.update(overrides)
        return Modelo303Data(**payload)

    def _make_model(self, **overrides) -> Modelo303Model:
        fiscal_year = overrides.pop("fiscal_year", 2026)
        data = self._make_data(**overrides)
        return Modelo303Model.from_data(data, fiscal_year=fiscal_year)

    def test_amount_positive(self):
        model = self._make_model(
            base_imponible=2000.0,
            cuota_gastos_bienes_y_servicios=100.0,
            cuota_adquisiones_bienes_inversion=50.0,
        )
        self.assertEqual(model.amount(), 270.0)

    def test_amount_zero(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=210.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.amount(), 0.0)

    def test_amount_negative(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=300.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.amount(), -90.0)

    def test_declaration_type_n_when_zero(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=210.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.declaration_type(), "N")

    def test_declaration_type_c_when_negative_and_not_q4(self):
        model = self._make_model(
            ejercicio=Period.THIRD_QUARTER,
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=300.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.declaration_type(), "C")

    def test_declaration_type_d_when_negative_and_q4(self):
        model = self._make_model(
            ejercicio=Period.FOURTH_QUARTER,
            volumen_anual_operaciones=1000.0,
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=300.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.declaration_type(), "D")

    def test_declaration_type_u_when_positive_with_iban(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=0.0,
            cuota_adquisiones_bienes_inversion=0.0,
            iban="ES0012341234123412341234",
        )
        self.assertEqual(model.declaration_type(), "U")

    def test_declaration_type_i_when_positive_without_iban(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=0.0,
            cuota_adquisiones_bienes_inversion=0.0,
        )
        self.assertEqual(model.declaration_type(), "I")

    def test_declaration_type_i_when_positive_with_iban_none(self):
        model = self._make_model(
            base_imponible=1000.0,
            cuota_gastos_bienes_y_servicios=0.0,
            cuota_adquisiones_bienes_inversion=0.0,
            iban=None,
        )
        self.assertEqual(model.declaration_type(), "I")

    def test_modelo_390_exemption(self):
        model_q1 = self._make_model(ejercicio=Period.FIRST_QUARTER)
        model_q4 = self._make_model(
            ejercicio=Period.FOURTH_QUARTER,
            volumen_anual_operaciones=1000.0,
        )

        self.assertEqual(model_q1.exencion_390, "0")
        self.assertEqual(model_q4.exencion_390, "1")

    def test_has_non_zero_operations(self):
        model_q2 = self._make_model(ejercicio=Period.SECOND_QUARTER)
        model_q4 = self._make_model(
            ejercicio=Period.FOURTH_QUARTER,
            volumen_anual_operaciones=1000.0,
        )

        self.assertEqual(model_q2.operaciones_no_cero, "0")
        self.assertEqual(model_q4.operaciones_no_cero, "1")

    def test_sepa_flag_default(self):
        model = self._make_model()
        self.assertEqual(model.sepa, "0")


if __name__ == "__main__":
    unittest.main()
