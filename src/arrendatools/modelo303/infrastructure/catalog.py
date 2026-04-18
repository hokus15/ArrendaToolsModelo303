from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from typing import Callable

from arrendatools.modelo303.infrastructure.formatting import format_signed_numeric


class FieldType(Enum):
    ALPHABETICAL = auto()
    ALPHANUMERIC = auto()
    NUMERIC = auto()
    NUMERIC_SIGNED = auto()


@dataclass(frozen=True, slots=True)
class FieldDef:
    length: int
    field_type: FieldType
    strict_type: bool = True
    default_value: str | None = None
    scale_to_cents: bool = True
    include_when: Callable[[object], bool] = lambda _model: True

    def render(self, name: str, raw_value: str | Decimal | int | float | None) -> str:
        value = self._normalize_value(raw_value)
        if len(value) > self.length:
            raise ValueError(
                f"Field '{name}' exceeds length {self.length}: {len(value)}"
            )
        if self.strict_type:
            _validate_type(name, value, self.field_type)
        align_right = self.field_type in {FieldType.NUMERIC, FieldType.NUMERIC_SIGNED}
        pad_char = "0" if align_right else " "
        padding = self.length - len(value)
        if align_right:
            return (pad_char * padding) + value
        return value + (pad_char * padding)

    def _normalize_value(self, raw_value: str | Decimal | int | float | None) -> str:
        if raw_value is None:
            return self.default_value or ""

        if isinstance(raw_value, str):
            return raw_value

        if (
            isinstance(raw_value, (Decimal, int, float))
            and self.scale_to_cents
            and self.field_type in {FieldType.NUMERIC, FieldType.NUMERIC_SIGNED}
        ):
            return format_signed_numeric(raw_value, self.length)

        return str(raw_value)


def _validate_type(name: str, value: str, field_type: FieldType) -> None:
    if field_type == FieldType.ALPHABETICAL and not re.fullmatch(r"[A-Za-z ]*", value):
        raise ValueError(f"Field '{name}' only allows letters and spaces")
    if field_type == FieldType.ALPHANUMERIC and not re.fullmatch(
        r"[A-Za-z0-9 ]*", value
    ):
        raise ValueError(
            f"Field '{name}' only allows alphanumeric characters and spaces"
        )
    if field_type == FieldType.NUMERIC and not re.fullmatch(r"\d*", value):
        raise ValueError(f"Field '{name}' only allows digits")
    if field_type == FieldType.NUMERIC_SIGNED:
        if not re.fullmatch(r"N?\d*", value):
            raise ValueError(
                f"Field '{name}' only allows digits with optional leading N"
            )
        if "N" in value and not value.startswith("N"):
            raise ValueError(f"Field '{name}' requires N at first position")


def build_catalog() -> dict[str, FieldDef]:
    catalog: dict[str, FieldDef] = {
        "registro_general_open": FieldDef(
            2, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T"
        ),
        "registro_general_close": FieldDef(
            3, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T"
        ),
        "modelo": FieldDef(3, FieldType.NUMERIC, default_value="303", scale_to_cents=False),
        "discriminante": FieldDef(1, FieldType.NUMERIC, default_value="0", scale_to_cents=False),
        "ejercicio": FieldDef(4, FieldType.NUMERIC, scale_to_cents=False),
        "periodo": FieldDef(2, FieldType.ALPHANUMERIC),
        "tipo_y_cierre": FieldDef(
            5, FieldType.ALPHANUMERIC, strict_type=False, default_value="0000>"
        ),
        "aux_open": FieldDef(
            5, FieldType.ALPHANUMERIC, strict_type=False, default_value="<AUX>"
        ),
        "aux_close": FieldDef(
            6, FieldType.ALPHANUMERIC, strict_type=False, default_value="</AUX>"
        ),
        "version": FieldDef(4, FieldType.ALPHANUMERIC, strict_type=False),
        "developer_nif": FieldDef(9, FieldType.ALPHANUMERIC),
        "did_open": FieldDef(
            11, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T303DID00>"
        ),
        "did_close": FieldDef(
            12, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T303DID00>"
        ),
        "swift": FieldDef(11, FieldType.ALPHANUMERIC),
        "iban": FieldDef(34, FieldType.ALPHANUMERIC),
        "bank_name": FieldDef(70, FieldType.ALPHANUMERIC),
        "bank_address": FieldDef(35, FieldType.ALPHANUMERIC),
        "bank_city": FieldDef(30, FieldType.ALPHANUMERIC),
        "bank_country": FieldDef(2, FieldType.ALPHANUMERIC),
        "sepa": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "dp30304_open": FieldDef(
            11, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T30304000>"
        ),
        "dp30304_close": FieldDef(
            12, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T30304000>"
        ),
        "dp30305_open": FieldDef(
            11, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T30305000>"
        ),
        "dp30305_close": FieldDef(
            12, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T30305000>"
        ),
        "dp30301_open": FieldDef(
            11, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T30301000>"
        ),
        "dp30301_close": FieldDef(
            12, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T30301000>"
        ),
        "dp30303_open": FieldDef(
            11, FieldType.ALPHANUMERIC, strict_type=False, default_value="<T30303000>"
        ),
        "dp30303_close": FieldDef(
            12, FieldType.ALPHANUMERIC, strict_type=False, default_value="</T30303000>"
        ),
        "pagina_complementaria": FieldDef(1, FieldType.ALPHABETICAL),
        "codigo_actividad_principal": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_principal": FieldDef(4, FieldType.NUMERIC, scale_to_cents=False),
        "codigo_actividad_1": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_1": FieldDef(4, FieldType.ALPHANUMERIC),
        "codigo_actividad_2": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_2": FieldDef(4, FieldType.ALPHANUMERIC),
        "codigo_actividad_3": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_3": FieldDef(4, FieldType.ALPHANUMERIC),
        "codigo_actividad_4": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_4": FieldDef(4, FieldType.ALPHANUMERIC),
        "codigo_actividad_5": FieldDef(3, FieldType.ALPHANUMERIC),
        "epigrafe_iae_5": FieldDef(4, FieldType.ALPHANUMERIC),
        "marque_operaciones_terceras": FieldDef(1, FieldType.ALPHABETICAL),
        "tipo_declaracion": FieldDef(1, FieldType.ALPHANUMERIC),
        "nif": FieldDef(9, FieldType.ALPHANUMERIC),
        "razon_social": FieldDef(80, FieldType.ALPHANUMERIC, strict_type=False),
        "tributacion_foral": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "registro_devolucion": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "solo_rg": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "autoliquidacion_conjunta": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "criterio_caja": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "destinatario_caja": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "prorrata_especial": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "revocacion_prorrata": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "concurso": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "fecha_concurso": FieldDef(8, FieldType.NUMERIC, scale_to_cents=False),
        "tipo_auto_concurso": FieldDef(1, FieldType.ALPHANUMERIC),
        "sii": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "exencion_390": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "operaciones_no_cero": FieldDef(1, FieldType.NUMERIC, scale_to_cents=False),
        "indicador_pago_gasolina": FieldDef(
            1,
            FieldType.NUMERIC,
            scale_to_cents=False,
        ),
        "sin_actividad": FieldDef(1, FieldType.ALPHANUMERIC),
        "rectificativa": FieldDef(1, FieldType.ALPHANUMERIC),
        "num_justificante": FieldDef(13, FieldType.ALPHANUMERIC),
        "baja_domiciliacion": FieldDef(1, FieldType.ALPHANUMERIC),
        "motivo_rectificacion": FieldDef(1, FieldType.ALPHANUMERIC),
        "motivo_discrepancia": FieldDef(1, FieldType.ALPHANUMERIC),
        "reserved_4": FieldDef(4, FieldType.ALPHANUMERIC),
        "reserved_70": FieldDef(70, FieldType.ALPHANUMERIC),
        "reserved_213": FieldDef(213, FieldType.ALPHANUMERIC),
        "reserved_617": FieldDef(617, FieldType.ALPHANUMERIC),
        "reservado_13": FieldDef(13, FieldType.ALPHANUMERIC),
        "reservado_120": FieldDef(120, FieldType.ALPHANUMERIC),
        "reservado_443": FieldDef(443, FieldType.ALPHANUMERIC),
        "reservado_521": FieldDef(521, FieldType.ALPHANUMERIC),
        "reservado_522": FieldDef(522, FieldType.ALPHANUMERIC),
        "reservado_546": FieldDef(546, FieldType.ALPHANUMERIC),
        "reservado_600": FieldDef(600, FieldType.ALPHANUMERIC),
        "reservado_672": FieldDef(672, FieldType.ALPHANUMERIC),
        "casilla_01": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_02": FieldDef(5, FieldType.NUMERIC),
        "casilla_03": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_04": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_05": FieldDef(5, FieldType.NUMERIC),
        "casilla_06": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_07": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_08": FieldDef(5, FieldType.NUMERIC),
        "casilla_09": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_10": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_11": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_12": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_13": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_14": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_15": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_16": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_17": FieldDef(5, FieldType.NUMERIC),
        "casilla_18": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_19": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_20": FieldDef(5, FieldType.NUMERIC),
        "casilla_21": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_22": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_23": FieldDef(5, FieldType.NUMERIC),
        "casilla_24": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_25": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_26": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_27": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_28": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_29": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_30": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_31": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_32": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_33": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_34": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_35": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_36": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_37": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_38": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_39": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_40": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_41": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_42": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_43": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_44": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_45": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_46": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_47": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_48": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_49": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_50": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_51": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_52": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_53": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_54": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_55": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_56": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_57": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_58": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_59": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_60": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_61": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_62": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_63": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_64": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_65": FieldDef(5, FieldType.NUMERIC),
        "casilla_66": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_67": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_68": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_69": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_70": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_71": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_72": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_73": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_74": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_75": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_76": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_77": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_78": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_79": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_80": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_81": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_82": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_83": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_84": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_85": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_86": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_87": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_88": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_89": FieldDef(5, FieldType.NUMERIC),
        "casilla_90": FieldDef(5, FieldType.NUMERIC),
        "casilla_91": FieldDef(5, FieldType.NUMERIC),
        "casilla_92": FieldDef(5, FieldType.NUMERIC),
        "casilla_93": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_94": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_95": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_96": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_97": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_98": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_99": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_100": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_101": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_102": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_103": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_104": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_105": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_106": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_107": FieldDef(5, FieldType.NUMERIC),
        "casilla_108": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_109": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_110": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_111": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_112": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_113": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_114": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_115": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_116": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_117": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_118": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_119": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_120": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_121": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_122": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_123": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_124": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_125": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_126": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_127": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_128": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_129": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_130": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_131": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_132": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_133": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_134": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_135": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_136": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_137": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_138": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_139": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_140": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_141": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_142": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_143": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_144": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_145": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_146": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_147": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_148": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_149": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_150": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_151": FieldDef(5, FieldType.NUMERIC),
        "casilla_152": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_153": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_154": FieldDef(5, FieldType.NUMERIC),
        "casilla_155": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_156": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_157": FieldDef(5, FieldType.NUMERIC),
        "casilla_158": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_159": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_160": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_161": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_162": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_163": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_164": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_165": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_166": FieldDef(5, FieldType.NUMERIC),
        "casilla_167": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_168": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_169": FieldDef(5, FieldType.NUMERIC),
        "casilla_170": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_171": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_500": FieldDef(3, FieldType.ALPHANUMERIC),
        "casilla_501": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_502": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_503": FieldDef(1, FieldType.ALPHABETICAL),
        "casilla_504": FieldDef(5, FieldType.NUMERIC),
        "casilla_505": FieldDef(3, FieldType.ALPHANUMERIC),
        "casilla_506": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_507": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_508": FieldDef(1, FieldType.ALPHABETICAL),
        "casilla_509": FieldDef(5, FieldType.NUMERIC),
        "casilla_510": FieldDef(3, FieldType.ALPHANUMERIC),
        "casilla_511": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_512": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_513": FieldDef(1, FieldType.ALPHABETICAL),
        "casilla_514": FieldDef(5, FieldType.NUMERIC),
        "casilla_515": FieldDef(3, FieldType.ALPHANUMERIC),
        "casilla_516": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_517": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_518": FieldDef(1, FieldType.ALPHABETICAL),
        "casilla_519": FieldDef(5, FieldType.NUMERIC),
        "casilla_520": FieldDef(3, FieldType.ALPHANUMERIC),
        "casilla_521": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_522": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_523": FieldDef(1, FieldType.ALPHABETICAL),
        "casilla_524": FieldDef(5, FieldType.NUMERIC),
        "casilla_700": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_701": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_702": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_703": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_704": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_705": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_706": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_707": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_708": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_709": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_710": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_711": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_712": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_713": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_714": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_715": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_716": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_717": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_718": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_719": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_720": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_721": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_722": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_723": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_724": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_725": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_726": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_727": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_728": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_729": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_730": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_731": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_732": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_733": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_734": FieldDef(17, FieldType.NUMERIC_SIGNED),
        "casilla_735": FieldDef(17, FieldType.NUMERIC_SIGNED),
    }

    return catalog


FIELD_CATALOG = build_catalog()
