from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from arrendatools.modelo303.domain.enums import Period

NIF_LENGTH = 9
MAX_VERSION_LENGTH = 4
MAX_TAXPAYER_LEGAL_NAME_LENGTH = 80
IBAN_LENGTH = 24


class Modelo303Data(BaseModel):
    ejercicio: Period = Field(..., description="Trimestre en formato 1T, 2T, 3T o 4T")
    version: str = Field(..., max_length=MAX_VERSION_LENGTH, description="Version")
    nif_empresa_desarrollo: str = Field(
        ...,
        min_length=NIF_LENGTH,
        max_length=NIF_LENGTH,
        description="NIF de la empresa desarrolladora",
    )
    razon_social: str = Field(
        ...,
        max_length=MAX_TAXPAYER_LEGAL_NAME_LENGTH,
        description="Nombre fiscal del contribuyente",
    )
    nif_contribuyente: str = Field(
        ...,
        min_length=NIF_LENGTH,
        max_length=NIF_LENGTH,
        description="NIF del contribuyente",
    )
    iban: str | None = Field(
        None,
        min_length=IBAN_LENGTH,
        max_length=IBAN_LENGTH,
        description="IBAN de la cuenta bancaria",
    )
    base_imponible: Decimal = Field(..., ge=0, description="Base imponible")
    base_gastos_bienes_y_servicios: Decimal = Field(
        Decimal("0"), ge=0, description="Gastos en bienes y servicios"
    )
    cuota_gastos_bienes_y_servicios: Decimal = Field(
        Decimal("0"), ge=0, description="IVA soportado en bienes y servicios"
    )
    base_adquisiones_bienes_inversion: Decimal = Field(
        Decimal("0"), ge=0, description="Adquisiciones de bienes de inversion"
    )
    cuota_adquisiones_bienes_inversion: Decimal = Field(
        Decimal("0"), ge=0, description="IVA soportado en bienes de inversion"
    )
    volumen_anual_operaciones: Decimal | None = Field(
        None, ge=0, description="Volumen anual de operaciones"
    )

    @model_validator(mode="after")
    def check_volumen_anual_operaciones(self):
        if (
            self.ejercicio == Period.FOURTH_QUARTER
            and self.volumen_anual_operaciones is None
        ):
            raise ValueError(
                "El volumen anual de operaciones es obligatorio en el 4º trimestre (4T)"
            )
        return self
