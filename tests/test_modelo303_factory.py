import pytest

from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.application.generator import Modelo303Generator


def test_get_model303_2023_not_supported():
    with pytest.raises(ValueError):
        get_generator(2023)


def test_get_model303_2024_not_supported():
    with pytest.raises(ValueError):
        get_generator(2024)


def test_get_model303_2025():
    modelo = get_generator(2025)
    assert isinstance(modelo, Modelo303Generator)
    assert modelo.fiscal_year == 2025


def test_get_model303_2026():
    modelo = get_generator(2026)
    assert isinstance(modelo, Modelo303Generator)
    assert modelo.fiscal_year == 2026


def test_get_model303_invalid_year():
    with pytest.raises(ValueError):
        get_generator(2022)
