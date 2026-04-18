from arrendatools.modelo303.infrastructure.layout_registry import LAYOUTS

from .generator import Modelo303Generator


def get_generator(fiscal_year: int) -> Modelo303Generator:
    layout = LAYOUTS.get(fiscal_year)
    if layout is None:
        raise ValueError(f"No existe un generador para el ejercicio {fiscal_year}")
    return Modelo303Generator(fiscal_year=fiscal_year, layout=layout)
