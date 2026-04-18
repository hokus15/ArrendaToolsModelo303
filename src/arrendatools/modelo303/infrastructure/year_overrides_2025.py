"""Year-specific overrides for fiscal year 2025.

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
CASILLA_DEFAULTS: dict[str, Decimal] = {}


# Calculator functions that override the default compute_casilla_* methods
# Each receives the model instance and returns the computed value
CASILLA_CALCULATORS: dict[str, Calculator] = {}
