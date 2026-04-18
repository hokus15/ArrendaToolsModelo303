from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import ClassVar

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.infrastructure.year_overrides import (
    get_year_calculators,
    get_year_defaults,
)


@dataclass(slots=True)
class Modelo303Model:
    _NO_ES_4T: ClassVar[str] = "0"
    _SI: ClassVar[str] = "1"
    _NO: ClassVar[str] = "2"
    _ES_T: ClassVar[str] = "0"
    _NO_SOLO_RG: ClassVar[str] = "3"
    _CODIGO_ACTIVIDAD: ClassVar[str] = "A01"
    _EPIGRAFE_IAE: ClassVar[str] = "8612"

    ejercicio: str = ""
    periodo: str = ""
    version: str = ""
    developer_nif: str = ""
    swift: str = ""
    iban: str = ""
    bank_name: str = ""
    bank_address: str = ""
    bank_city: str = ""
    bank_country: str = ""
    sepa: str = ""
    pagina_complementaria: str = ""
    codigo_actividad_principal: str = ""
    epigrafe_iae_principal: str = ""
    codigo_actividad_1: str = ""
    epigrafe_iae_1: str = ""
    codigo_actividad_2: str = ""
    epigrafe_iae_2: str = ""
    codigo_actividad_3: str = ""
    epigrafe_iae_3: str = ""
    codigo_actividad_4: str = ""
    epigrafe_iae_4: str = ""
    codigo_actividad_5: str = ""
    epigrafe_iae_5: str = ""
    marque_operaciones_terceras: str = ""
    tipo_declaracion: str = ""
    nif: str = ""
    razon_social: str = ""
    tributacion_foral: str = ""
    registro_devolucion: str = ""
    solo_rg: str = ""
    autoliquidacion_conjunta: str = ""
    criterio_caja: str = ""
    destinatario_caja: str = ""
    prorrata_especial: str = ""
    revocacion_prorrata: str = ""
    concurso: str = ""
    fecha_concurso: str = ""
    tipo_auto_concurso: str = ""
    sii: str = ""
    exencion_390: str = ""
    operaciones_no_cero: str = ""
    indicador_pago_gasolina: str = ""
    sin_actividad: str = ""
    rectificativa: str = ""
    num_justificante: str = ""
    baja_domiciliacion: str = ""
    motivo_rectificacion: str = ""
    motivo_discrepancia: str = ""
    casilla_01: Decimal = Decimal("0.00")
    casilla_02: Decimal = Decimal("4.00")
    casilla_03: Decimal = Decimal("0.00")
    casilla_04: Decimal = Decimal("0.00")
    casilla_05: Decimal = Decimal("10.00")
    casilla_06: Decimal = Decimal("0.00")
    casilla_07: Decimal = Decimal("0.00")
    casilla_08: Decimal = Decimal("21.00")
    casilla_09: Decimal = Decimal("0.00")
    casilla_10: Decimal = Decimal("0.00")
    casilla_11: Decimal = Decimal("0.00")
    casilla_12: Decimal = Decimal("0.00")
    casilla_13: Decimal = Decimal("0.00")
    casilla_14: Decimal = Decimal("0.00")
    casilla_15: Decimal = Decimal("0.00")
    casilla_16: Decimal = Decimal("0.00")
    casilla_17: Decimal = Decimal("0.00")
    casilla_18: Decimal = Decimal("0.00")
    casilla_19: Decimal = Decimal("0.00")
    casilla_20: Decimal = Decimal("1.40")
    casilla_21: Decimal = Decimal("0.00")
    casilla_22: Decimal = Decimal("0.00")
    casilla_23: Decimal = Decimal("5.20")
    casilla_24: Decimal = Decimal("0.00")
    casilla_25: Decimal = Decimal("0.00")
    casilla_26: Decimal = Decimal("0.00")
    casilla_27: Decimal = Decimal("0.00")
    casilla_28: Decimal = Decimal("0.00")
    casilla_29: Decimal = Decimal("0.00")
    casilla_30: Decimal = Decimal("0.00")
    casilla_31: Decimal = Decimal("0.00")
    casilla_32: Decimal = Decimal("0.00")
    casilla_33: Decimal = Decimal("0.00")
    casilla_34: Decimal = Decimal("0.00")
    casilla_35: Decimal = Decimal("0.00")
    casilla_36: Decimal = Decimal("0.00")
    casilla_37: Decimal = Decimal("0.00")
    casilla_38: Decimal = Decimal("0.00")
    casilla_39: Decimal = Decimal("0.00")
    casilla_40: Decimal = Decimal("0.00")
    casilla_41: Decimal = Decimal("0.00")
    casilla_42: Decimal = Decimal("0.00")
    casilla_43: Decimal = Decimal("0.00")
    casilla_44: Decimal = Decimal("0.00")
    casilla_45: Decimal = Decimal("0.00")
    casilla_46: Decimal = Decimal("0.00")
    casilla_47: Decimal = Decimal("0.00")
    casilla_48: Decimal = Decimal("0.00")
    casilla_49: Decimal = Decimal("0.00")
    casilla_50: Decimal = Decimal("0.00")
    casilla_51: Decimal = Decimal("0.00")
    casilla_52: Decimal = Decimal("0.00")
    casilla_53: Decimal = Decimal("0.00")
    casilla_54: Decimal = Decimal("0.00")
    casilla_55: Decimal = Decimal("0.00")
    casilla_56: Decimal = Decimal("0.00")
    casilla_57: Decimal = Decimal("0.00")
    casilla_58: Decimal = Decimal("0.00")
    casilla_59: Decimal = Decimal("0.00")
    casilla_60: Decimal = Decimal("0.00")
    casilla_61: Decimal = Decimal("0.00")
    casilla_62: Decimal = Decimal("0.00")
    casilla_63: Decimal = Decimal("0.00")
    casilla_64: Decimal = Decimal("0.00")
    casilla_65: Decimal = Decimal("0.00")
    casilla_66: Decimal = Decimal("0.00")
    casilla_67: Decimal = Decimal("0.00")
    casilla_68: Decimal = Decimal("0.00")
    casilla_69: Decimal = Decimal("0.00")
    casilla_70: Decimal = Decimal("0.00")
    casilla_71: Decimal = Decimal("0.00")
    casilla_72: Decimal = Decimal("0.00")
    casilla_73: Decimal = Decimal("0.00")
    casilla_74: Decimal = Decimal("0.00")
    casilla_75: Decimal = Decimal("0.00")
    casilla_76: Decimal = Decimal("0.00")
    casilla_77: Decimal = Decimal("0.00")
    casilla_78: Decimal = Decimal("0.00")
    casilla_79: Decimal = Decimal("0.00")
    casilla_80: Decimal = Decimal("0.00")
    casilla_81: Decimal = Decimal("0.00")
    casilla_82: Decimal = Decimal("0.00")
    casilla_83: Decimal = Decimal("0.00")
    casilla_84: Decimal = Decimal("0.00")
    casilla_85: Decimal = Decimal("0.00")
    casilla_86: Decimal = Decimal("0.00")
    casilla_87: Decimal = Decimal("0.00")
    casilla_88: Decimal = Decimal("0.00")
    casilla_89: Decimal = Decimal("0.00")
    casilla_90: Decimal = Decimal("0.00")
    casilla_91: Decimal = Decimal("0.00")
    casilla_92: Decimal = Decimal("0.00")
    casilla_93: Decimal = Decimal("0.00")
    casilla_94: Decimal = Decimal("0.00")
    casilla_95: Decimal = Decimal("0.00")
    casilla_96: Decimal = Decimal("0.00")
    casilla_97: Decimal = Decimal("0.00")
    casilla_98: Decimal = Decimal("0.00")
    casilla_99: Decimal = Decimal("0.00")
    casilla_100: Decimal = Decimal("0.00")
    casilla_101: Decimal = Decimal("0.00")
    casilla_102: Decimal = Decimal("0.00")
    casilla_103: Decimal = Decimal("0.00")
    casilla_104: Decimal = Decimal("0.00")
    casilla_105: Decimal = Decimal("0.00")
    casilla_106: Decimal = Decimal("0.00")
    casilla_107: Decimal = Decimal("0.00")
    casilla_108: Decimal = Decimal("0.00")
    casilla_109: Decimal = Decimal("0.00")
    casilla_110: Decimal = Decimal("0.00")
    casilla_111: Decimal = Decimal("0.00")
    casilla_112: Decimal = Decimal("0.00")
    casilla_113: Decimal = Decimal("0.00")
    casilla_114: Decimal = Decimal("0.00")
    casilla_115: Decimal = Decimal("0.00")
    casilla_116: Decimal = Decimal("0.00")
    casilla_117: Decimal = Decimal("0.00")
    casilla_118: Decimal = Decimal("0.00")
    casilla_119: Decimal = Decimal("0.00")
    casilla_120: Decimal = Decimal("0.00")
    casilla_121: Decimal = Decimal("0.00")
    casilla_122: Decimal = Decimal("0.00")
    casilla_123: Decimal = Decimal("0.00")
    casilla_124: Decimal = Decimal("0.00")
    casilla_125: Decimal = Decimal("0.00")
    casilla_126: Decimal = Decimal("0.00")
    casilla_127: Decimal = Decimal("0.00")
    casilla_128: Decimal = Decimal("0.00")
    casilla_129: Decimal = Decimal("0.00")
    casilla_130: Decimal = Decimal("0.00")
    casilla_131: Decimal = Decimal("0.00")
    casilla_132: Decimal = Decimal("0.00")
    casilla_133: Decimal = Decimal("0.00")
    casilla_134: Decimal = Decimal("0.00")
    casilla_135: Decimal = Decimal("0.00")
    casilla_136: Decimal = Decimal("0.00")
    casilla_137: Decimal = Decimal("0.00")
    casilla_138: Decimal = Decimal("0.00")
    casilla_139: Decimal = Decimal("0.00")
    casilla_140: Decimal = Decimal("0.00")
    casilla_141: Decimal = Decimal("0.00")
    casilla_142: Decimal = Decimal("0.00")
    casilla_143: Decimal = Decimal("0.00")
    casilla_144: Decimal = Decimal("0.00")
    casilla_145: Decimal = Decimal("0.00")
    casilla_146: Decimal = Decimal("0.00")
    casilla_147: Decimal = Decimal("0.00")
    casilla_148: Decimal = Decimal("0.00")
    casilla_149: Decimal = Decimal("0.00")
    casilla_150: Decimal = Decimal("0.00")
    casilla_151: Decimal = Decimal("0.00")
    casilla_152: Decimal = Decimal("0.00")
    casilla_153: Decimal = Decimal("0.00")
    casilla_154: Decimal = Decimal("0.00")
    casilla_155: Decimal = Decimal("0.00")
    casilla_156: Decimal = Decimal("0.00")
    casilla_157: Decimal = Decimal("1.75")
    casilla_158: Decimal = Decimal("0.00")
    casilla_159: Decimal = Decimal("0.00")
    casilla_160: Decimal = Decimal("0.00")
    casilla_161: Decimal = Decimal("0.00")
    casilla_162: Decimal = Decimal("0.00")
    casilla_163: Decimal = Decimal("0.00")
    casilla_164: Decimal = Decimal("0.00")
    casilla_165: Decimal = Decimal("0.00")
    casilla_166: Decimal = Decimal("0.00")
    casilla_167: Decimal = Decimal("0.00")
    casilla_168: Decimal = Decimal("0.00")
    casilla_169: Decimal = Decimal("0.50")
    casilla_170: Decimal = Decimal("0.00")
    casilla_171: Decimal = Decimal("0.00")
    casilla_500: str = ""
    casilla_501: Decimal = Decimal("0.00")
    casilla_502: Decimal = Decimal("0.00")
    casilla_503: str = " "
    casilla_504: Decimal = Decimal("0.00")
    casilla_505: str = ""
    casilla_506: Decimal = Decimal("0.00")
    casilla_507: Decimal = Decimal("0.00")
    casilla_508: str = " "
    casilla_509: Decimal = Decimal("0.00")
    casilla_510: str = ""
    casilla_511: Decimal = Decimal("0.00")
    casilla_512: Decimal = Decimal("0.00")
    casilla_513: str = " "
    casilla_514: Decimal = Decimal("0.00")
    casilla_515: str = ""
    casilla_516: Decimal = Decimal("0.00")
    casilla_517: Decimal = Decimal("0.00")
    casilla_518: str = " "
    casilla_519: Decimal = Decimal("0.00")
    casilla_520: str = ""
    casilla_521: Decimal = Decimal("0.00")
    casilla_522: Decimal = Decimal("0.00")
    casilla_523: str = " "
    casilla_524: Decimal = Decimal("0.00")
    casilla_700: Decimal = Decimal("0.00")
    casilla_701: Decimal = Decimal("0.00")
    casilla_702: Decimal = Decimal("0.00")
    casilla_703: Decimal = Decimal("0.00")
    casilla_704: Decimal = Decimal("0.00")
    casilla_705: Decimal = Decimal("0.00")
    casilla_706: Decimal = Decimal("0.00")
    casilla_707: Decimal = Decimal("0.00")
    casilla_708: Decimal = Decimal("0.00")
    casilla_709: Decimal = Decimal("0.00")
    casilla_710: Decimal = Decimal("0.00")
    casilla_711: Decimal = Decimal("0.00")
    casilla_712: Decimal = Decimal("0.00")
    casilla_713: Decimal = Decimal("0.00")
    casilla_714: Decimal = Decimal("0.00")
    casilla_715: Decimal = Decimal("0.00")
    casilla_716: Decimal = Decimal("0.00")
    casilla_717: Decimal = Decimal("0.00")
    casilla_718: Decimal = Decimal("0.00")
    casilla_719: Decimal = Decimal("0.00")
    casilla_720: Decimal = Decimal("0.00")
    casilla_721: Decimal = Decimal("0.00")
    casilla_722: Decimal = Decimal("0.00")
    casilla_723: Decimal = Decimal("0.00")
    casilla_724: Decimal = Decimal("0.00")
    casilla_725: Decimal = Decimal("0.00")
    casilla_726: Decimal = Decimal("0.00")
    casilla_727: Decimal = Decimal("0.00")
    casilla_728: Decimal = Decimal("0.00")
    casilla_729: Decimal = Decimal("0.00")
    casilla_730: Decimal = Decimal("0.00")
    casilla_731: Decimal = Decimal("0.00")
    casilla_732: Decimal = Decimal("0.00")
    casilla_733: Decimal = Decimal("0.00")
    casilla_734: Decimal = Decimal("0.00")
    casilla_735: Decimal = Decimal("0.00")

    @classmethod
    def from_data(cls, data: Modelo303Data, fiscal_year: int) -> "Modelo303Model":
        model = cls()
        model.ejercicio = str(fiscal_year)
        model.periodo = data.periodo.value
        model.version = data.version
        model.developer_nif = data.nif_empresa_desarrollo
        model.iban = data.iban or ""
        model.sepa = model.marca_sepa(data.iban)
        model.pagina_complementaria = " "
        model.codigo_actividad_principal = cls._CODIGO_ACTIVIDAD
        model.epigrafe_iae_principal = cls._EPIGRAFE_IAE
        model.marque_operaciones_terceras = " "
        model.nif = data.nif_contribuyente
        model.razon_social = data.razon_social
        model.tributacion_foral = cls._NO
        model.registro_devolucion = cls._NO
        model.solo_rg = cls._NO_SOLO_RG
        model.autoliquidacion_conjunta = cls._NO
        model.criterio_caja = cls._NO
        model.destinatario_caja = cls._NO
        model.prorrata_especial = cls._NO
        model.revocacion_prorrata = cls._NO
        model.concurso = cls._NO
        model.sii = cls._NO
        model.exencion_390 = model.exoneracion_modelo_390(data.periodo)
        model.operaciones_no_cero = model.operaciones_no_0(data.periodo)
        model.indicador_pago_gasolina = cls._ES_T

        model.casilla_65 = Decimal("100.00")
        model.casilla_07 = data.base_imponible
        model.casilla_09 = (data.base_imponible * Decimal("0.21")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        model.casilla_28 = data.base_gastos_bienes_y_servicios

        # Apply year-specific simple value overrides (e.g., casilla_17, casilla_23)
        year_defaults = get_year_defaults(fiscal_year)
        for field_name, value in year_defaults.items():
            setattr(model, field_name, value)

        model.casilla_29 = data.cuota_gastos_bienes_y_servicios
        model.casilla_30 = data.base_adquisiones_bienes_inversion
        model.casilla_31 = data.cuota_adquisiones_bienes_inversion
        if data.volumen_anual_operaciones is not None:
            model.casilla_80 = data.volumen_anual_operaciones

        # Compute all calculated fields (uses any defaults set above)
        model.casilla_27 = model.compute_casilla_27()
        model.casilla_45 = model.compute_casilla_45()
        model.casilla_46 = model.compute_casilla_46()
        model.casilla_64 = model.compute_casilla_64()
        model.casilla_66 = model.compute_casilla_66()
        model.casilla_69 = model.compute_casilla_69()
        model.casilla_71 = model.compute_casilla_71()
        model.casilla_88 = model.compute_casilla_88()

        # Apply year-specific custom calculators (override computed values)
        year_calculators = get_year_calculators(fiscal_year)
        for field_name, calculator in year_calculators.items():
            setattr(model, field_name, calculator(model))

        if model.amount() < 0:
            model.iban = ""
        model.tipo_declaracion = model.declaration_type()
        return model

    def amount(self) -> Decimal:
        vat_accrued = (self.casilla_07 * Decimal("0.21")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        total_deductible_vat = (self.casilla_29 + self.casilla_31).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        return (vat_accrued - total_deductible_vat).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def declaration_type(self) -> str:
        amount = self.amount()
        if amount == 0:
            return "N"
        if amount < 0 and self.periodo != Period.FOURTH_QUARTER:
            return "C"
        if amount < 0 and self.periodo == Period.FOURTH_QUARTER:
            return "D"
        if amount > 0 and (self.iban or "") != "":
            return "U"
        return "I"

    def exoneracion_modelo_390(self, periodo: Period) -> str:
        if periodo != Period.FOURTH_QUARTER:
            return self._NO_ES_4T
        return self._SI

    def operaciones_no_0(self, periodo: Period) -> str:
        if periodo != Period.FOURTH_QUARTER:
            return self._NO_ES_4T
        return self._SI

    def marca_sepa(self, iban: str | None) -> str:
        return "0"

    def compute_casilla_27(self) -> Decimal:
        return (
            self.casilla_152
            + self.casilla_167
            + self.casilla_03
            + self.casilla_155
            + self.casilla_06
            + self.casilla_09
            + self.casilla_11
            + self.casilla_13
            + self.casilla_15
            + self.casilla_158
            + self.casilla_170
            + self.casilla_18
            + self.casilla_21
            + self.casilla_24
            + self.casilla_26
        )

    def compute_casilla_45(self) -> Decimal:
        return (
            self.casilla_29
            + self.casilla_31
            + self.casilla_33
            + self.casilla_35
            + self.casilla_37
            + self.casilla_39
            + self.casilla_41
            + self.casilla_42
            + self.casilla_43
            + self.casilla_44
        )

    def compute_casilla_46(self) -> Decimal:
        return self.compute_casilla_27() - self.compute_casilla_45()

    def compute_casilla_64(self) -> Decimal:
        return self.compute_casilla_46() + self.casilla_58 + self.casilla_76

    def compute_casilla_66(self) -> Decimal:
        return self.compute_casilla_64() * (self.casilla_65 / Decimal("100.00"))

    def compute_casilla_69(self) -> Decimal:
        return self.compute_casilla_66() + self.casilla_77 - self.casilla_78

    def compute_casilla_71(self) -> Decimal:
        return self.compute_casilla_69() - self.casilla_70 + self.casilla_109

    def compute_casilla_88(self) -> Decimal:
        return (
            self.casilla_80
            + self.casilla_81
            + self.casilla_93
            + self.casilla_94
            + self.casilla_83
            + self.casilla_84
            + self.casilla_125
            + self.casilla_126
            + self.casilla_127
            + self.casilla_128
            + self.casilla_86
            + self.casilla_95
            + self.casilla_96
            + self.casilla_97
            + self.casilla_98
            + self.casilla_79
            + self.casilla_99
        )
