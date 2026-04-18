from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.domain.model import Modelo303Model


def _make_data(**overrides) -> Modelo303Data:
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


def _make_model(**overrides) -> Modelo303Model:
    fiscal_year = overrides.pop("fiscal_year", 2026)
    data = _make_data(**overrides)
    return Modelo303Model.from_data(data, fiscal_year=fiscal_year)


def test_amount_positive():
    model = _make_model(
        base_imponible=2000.0,
        cuota_gastos_bienes_y_servicios=100.0,
        cuota_adquisiones_bienes_inversion=50.0,
    )
    assert model.amount() == 270.0


def test_amount_zero():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=210.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.amount() == 0.0


def test_amount_negative():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=300.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.amount() == -90.0


def test_declaration_type_n_when_zero():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=210.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.declaration_type() == "N"


def test_declaration_type_c_when_negative_and_not_q4():
    model = _make_model(
        ejercicio=Period.THIRD_QUARTER,
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=300.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.declaration_type() == "C"


def test_declaration_type_d_when_negative_and_q4():
    model = _make_model(
        ejercicio=Period.FOURTH_QUARTER,
        volumen_anual_operaciones=1000.0,
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=300.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.declaration_type() == "D"


def test_declaration_type_u_when_positive_with_iban():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=0.0,
        cuota_adquisiones_bienes_inversion=0.0,
        iban="ES0012341234123412341234",
    )
    assert model.declaration_type() == "U"


def test_declaration_type_i_when_positive_without_iban():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=0.0,
        cuota_adquisiones_bienes_inversion=0.0,
    )
    assert model.declaration_type() == "I"


def test_declaration_type_i_when_positive_with_iban_none():
    model = _make_model(
        base_imponible=1000.0,
        cuota_gastos_bienes_y_servicios=0.0,
        cuota_adquisiones_bienes_inversion=0.0,
        iban=None,
    )
    assert model.declaration_type() == "I"


def test_modelo_390_exemption():
    model_q1 = _make_model(ejercicio=Period.FIRST_QUARTER)
    model_q4 = _make_model(
        ejercicio=Period.FOURTH_QUARTER,
        volumen_anual_operaciones=1000.0,
    )

    assert model_q1.exencion_390 == "0"
    assert model_q4.exencion_390 == "1"


def test_has_non_zero_operations():
    model_q2 = _make_model(ejercicio=Period.SECOND_QUARTER)
    model_q4 = _make_model(
        ejercicio=Period.FOURTH_QUARTER,
        volumen_anual_operaciones=1000.0,
    )

    assert model_q2.operaciones_no_cero == "0"
    assert model_q4.operaciones_no_cero == "1"


def test_sepa_flag_default():
    model = _make_model()
    assert model.sepa == "0"
