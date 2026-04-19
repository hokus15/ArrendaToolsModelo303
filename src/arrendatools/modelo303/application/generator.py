from __future__ import annotations

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.schema import SchemaSpec
from arrendatools.modelo303.infrastructure.schema_renderer import render_schema


class Modelo303Generator:
    def __init__(self, fiscal_year: int, schema: SchemaSpec):
        """Initialize generator for a fiscal year and schema."""
        self.fiscal_year = fiscal_year
        self.schema = schema

    def generate(self, data: Modelo303Data) -> str:
        model = Modelo303Model.from_data(data, fiscal_year=self.fiscal_year)
        return render_schema(self.schema, model)
