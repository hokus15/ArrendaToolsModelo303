from decimal import Decimal
from pathlib import Path

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.domain.enums import Period

ejercicio = 2025
period = Period.FIRST_QUARTER
nif_empresa_desarrollo = "12345678X"
version = "1.00"
# nif_empresa_desarrollo = "Q2826000H"
# razon_social = "MORELL BOSCH JORGE"
razon_social = "DE LOS PALOTES PERICO"
# nif_contribuyente = "43103839E"
nif_contribuyente = "12345678E"
# iban = "ES3614650100961700091074"
iban = "ES0012341234123412341234"
# iban = None
base_imponible = Decimal("2000.00")
base_gastos_bienes_y_servicios = Decimal("2500.0")
cuota_gastos_bienes_y_servicios = Decimal("525.0")
base_adquisiones_bienes_inversion = Decimal("0.0")
cuota_adquisiones_bienes_inversion = Decimal("0.0")
volumen_anual_operaciones = Decimal("6000.0")

datos_modelo = Modelo303Data(
    ejercicio=period,
    nif_empresa_desarrollo=nif_empresa_desarrollo,
    version=version,
    razon_social=razon_social,
    nif_contribuyente=nif_contribuyente,
    iban=iban,
    base_imponible=base_imponible,
    base_gastos_bienes_y_servicios=base_gastos_bienes_y_servicios,
    cuota_gastos_bienes_y_servicios=cuota_gastos_bienes_y_servicios,
    base_adquisiones_bienes_inversion=base_adquisiones_bienes_inversion,
    cuota_adquisiones_bienes_inversion=cuota_adquisiones_bienes_inversion,
    volumen_anual_operaciones=volumen_anual_operaciones,
)

modelo = get_generator(ejercicio)

datos_fichero = modelo.generate(datos_modelo)
print(datos_fichero)

output_path = Path(f"{nif_contribuyente}_{ejercicio}_{period.value}.303")
output_path.write_text(datos_fichero, encoding="utf-8")
