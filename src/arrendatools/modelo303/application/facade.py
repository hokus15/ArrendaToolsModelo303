from arrendatools.modelo303.infrastructure.schema_registry import get_schema

from .generator import Modelo303Generator


def get_generator(fiscal_year: int) -> Modelo303Generator:
    schema = get_schema(fiscal_year)
    return Modelo303Generator(fiscal_year=fiscal_year, schema=schema)
