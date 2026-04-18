"""Year-specific field overrides registry for Modelo303Model.

This centralizes per-year configuration including simple value overrides and custom calculators for fields that
vary by fiscal year.

To add a new year:
1. Create year_overrides_YYYY.py with CASILLA_DEFAULTS and CASILLA_CALCULATORS
2. Import and register it below

Example year override module structure:
    CASILLA_DEFAULTS_2025 = {"casilla_17": Decimal("5.2"), ...}
    CASILLA_CALCULATORS_2025 = {"casilla_71": lambda model: ...}
"""

from decimal import Decimal

from .year_overrides_2025 import CASILLA_CALCULATORS as CASILLA_CALCULATORS_2025
from .year_overrides_2025 import CASILLA_DEFAULTS as CASILLA_DEFAULTS_2025
from .year_overrides_2026 import CASILLA_CALCULATORS as CASILLA_CALCULATORS_2026
from .year_overrides_2026 import CASILLA_DEFAULTS as CASILLA_DEFAULTS_2026

# Registry: fiscal_year -> (defaults dict, calculators dict)
YEAR_OVERRIDES_REGISTRY: dict[int, tuple[dict[str, Decimal], dict[str, callable]]] = {
    2025: (CASILLA_DEFAULTS_2025, CASILLA_CALCULATORS_2025),
    2026: (CASILLA_DEFAULTS_2026, CASILLA_CALCULATORS_2026),
}


def get_year_defaults(fiscal_year: int) -> dict[str, Decimal]:
    """Get simple value overrides for a given fiscal year.

    Parameters
    ----------
    fiscal_year : int
        The fiscal year (e.g., 2025, 2026).

    Returns
    -------
    dict[str, Decimal]
        Dictionary mapping field names to override values.
        Empty dict if year not configured.

    """
    defaults, _ = YEAR_OVERRIDES_REGISTRY.get(fiscal_year, ({}, {}))
    return defaults


def get_year_calculators(fiscal_year: int) -> dict[str, callable]:
    """Get custom calculator functions for a given fiscal year.

    These override the default compute_casilla_* methods on the model.

    Parameters
    ----------
    fiscal_year : int
        The fiscal year (e.g., 2025, 2026).

    Returns
    -------
    dict[str, callable]
        Dictionary mapping field names to calculator callables.
        Empty dict if year not configured.

    """
    _, calculators = YEAR_OVERRIDES_REGISTRY.get(fiscal_year, ({}, {}))
    return calculators
