import unittest

from arrendatools.modelo303.datos import Modelo303Datos, Periodo
from arrendatools.modelo303.factory import Modelo303Factory
from arrendatools.modelo303.generadores.generador_ejercicio_2023 import (
    GeneradorEjercicio2023,
)
from arrendatools.modelo303.generadores.generador_ejercicio_2024 import (
    GeneradorEjercicio2024,
)
from arrendatools.modelo303.generadores.generador_ejercicio_2025 import (
    GeneradorEjercicio2025,
)
from arrendatools.modelo303.generadores.generador_ejercicio_2026 import (
    GeneradorEjercicio2026,
)


class Modelo303FactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.datos = Modelo303Datos(
            periodo=Periodo.PRIMER_TRIMESTRE,
            base_imponible=1000,
            version="v1.0",
            nif_empresa_desarrollo="12345678X",
            nif_contribuyente="12345678E",
            nombre_fiscal_contribuyente="DE LOS PALOTES PERICO",
        )

    def test_get_modelo_303_2023(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2023)
        self.assertIsInstance(modelo, GeneradorEjercicio2023)

    def test_get_modelo_303_2024(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2024)
        self.assertIsInstance(modelo, GeneradorEjercicio2024)

    def test_get_modelo_303_2025(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2025)
        self.assertIsInstance(modelo, GeneradorEjercicio2025)

    def test_get_modelo_303_2026(self):
        modelo = Modelo303Factory.obtener_generador_modelo303(2026)
        self.assertIsInstance(modelo, GeneradorEjercicio2026)

    def test_get_modelo_303_invalid_year(self):
        with self.assertRaises(ValueError):
            Modelo303Factory.obtener_generador_modelo303(2022)

    def test_load_class_invalid_format(self):
        with self.assertRaises(ImportError):
            Modelo303Factory._load_class(
                "modulo_sin_clase", Modelo303Factory._SAFE_MODULES
            )

    def test_load_class_invalid_class_name(self):
        with self.assertRaises(ValueError):
            Modelo303Factory._load_class(
                "arrendatools.modelo303.generadores.generador_ejercicio_2023.123Bad",
                Modelo303Factory._SAFE_MODULES,
            )

    def test_load_class_module_not_whitelisted(self):
        with self.assertRaises(ImportError):
            Modelo303Factory._load_class(
                "arrendatools.modelo303.generadores.generador_ejercicio_2099.GeneradorEjercicio2099",
                Modelo303Factory._SAFE_MODULES,
            )

    def test_load_class_missing_class(self):
        with self.assertRaises(ImportError):
            Modelo303Factory._load_class(
                "arrendatools.modelo303.generadores.generador_ejercicio_2023.ClaseInexistente",
                Modelo303Factory._SAFE_MODULES,
            )


if __name__ == "__main__":
    unittest.main()
