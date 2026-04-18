"""Year-specific overrides for fiscal year 2026.

This module defines:
- Simple field value overrides
- Custom calculator functions for fields that vary by year
"""

from decimal import Decimal
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from arrendatools.modelo303.domain.model import Modelo303Model

Calculator = Callable[["Modelo303Model"], Decimal]

# Simple value overrides that apply uniformly
CASILLA_DEFAULTS: dict[str, Decimal] = {
    "casilla_17": Decimal("0"),
    "casilla_23": Decimal("5.2"),
}


# Calculator functions that override the default compute_casilla_* methods
# Each receives the model instance and returns the computed value
CASILLA_CALCULATORS: dict[str, Calculator] = {
    # In 2026: casilla_71 = casilla_69 - casilla_70 + casilla_109 - casilla_112
    # (DOES subtract casilla_112, unlike 2025)
    "casilla_71": lambda model: model.compute_casilla_69()
    - model.casilla_70
    + model.casilla_109
    - model.casilla_112,
}
