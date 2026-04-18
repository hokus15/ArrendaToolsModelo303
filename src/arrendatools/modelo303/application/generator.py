from __future__ import annotations

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.model import Modelo303Model
from arrendatools.modelo303.infrastructure.catalog import FIELD_CATALOG
from arrendatools.modelo303.infrastructure.layout import LayoutSpec


class Modelo303Generator:
    def __init__(self, fiscal_year: int, layout: LayoutSpec):
        """Initialize generator for a fiscal year and layout."""
        self.fiscal_year = fiscal_year
        self.layout = layout

    def generate(self, data: Modelo303Data) -> str:
        model = Modelo303Model.from_data(data, fiscal_year=self.fiscal_year)
        chunks: list[str] = []
        for page in self.layout.pages:
            if not page.include_when(model):
                continue
            for field_name in page.fields:
                field_def = FIELD_CATALOG.get(field_name)
                if field_def is None:
                    raise ValueError(f"Field '{field_name}' is not declared in catalog")
                if not field_def.include_when(model):
                    continue
                raw_value = getattr(model, field_name, None)
                chunks.append(field_def.render(field_name, raw_value))
        return "".join(chunks)
