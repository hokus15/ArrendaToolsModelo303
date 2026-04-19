from __future__ import annotations

from functools import lru_cache
from importlib.resources import files

from arrendatools.modelo303.infrastructure.schema import SchemaSpec
from arrendatools.modelo303.infrastructure.schema_loader import load_schema
from arrendatools.modelo303.infrastructure.schema_validator import validate_schema

# Single source of truth for supported fiscal years.
# To add a new year: add the entry here.
# To retire a year: remove the entry (the YAML file may remain in the repo).
SUPPORTED_SCHEMAS: dict[int, str] = {
    2025: "2025.1.yaml",
    2026: "2026.1.yaml",
}


def list_supported_years() -> tuple[int, ...]:
    return tuple(sorted(SUPPORTED_SCHEMAS.keys()))


@lru_cache(maxsize=None)
def get_schema(fiscal_year: int) -> SchemaSpec:
    """Load, validate and return the SchemaSpec for the given fiscal year."""
    filename = SUPPORTED_SCHEMAS.get(fiscal_year)
    if filename is None:
        raise ValueError(f"No existe un schema para el ejercicio {fiscal_year}")
    traversable = files("arrendatools.modelo303.infrastructure.schemas").joinpath(
        filename
    )
    schema = load_schema(traversable)
    validate_schema(schema)
    return schema
