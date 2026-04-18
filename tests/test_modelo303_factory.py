import unittest

from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.application.generator import Modelo303Generator


class TestModelo303Api(unittest.TestCase):
    def test_get_model303_2023_not_supported(self):
        with self.assertRaises(ValueError):
            get_generator(2023)

    def test_get_model303_2024_not_supported(self):
        with self.assertRaises(ValueError):
            get_generator(2024)

    def test_get_model303_2025(self):
        modelo = get_generator(2025)
        self.assertIsInstance(modelo, Modelo303Generator)
        self.assertEqual(modelo.fiscal_year, 2025)

    def test_get_model303_2026(self):
        modelo = get_generator(2026)
        self.assertIsInstance(modelo, Modelo303Generator)
        self.assertEqual(modelo.fiscal_year, 2026)

    def test_get_model303_invalid_year(self):
        with self.assertRaises(ValueError):
            get_generator(2022)


if __name__ == "__main__":
    unittest.main()
