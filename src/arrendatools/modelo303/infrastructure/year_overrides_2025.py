"""
Year-specific overrides for fiscal year 2025.

This module defines:
- Simple field value overrides
- Custom calculator functions for fields that vary by year
"""

from decimal import Decimal

# Simple value overrides that apply uniformly
CASILLA_DEFAULTS: dict[str, Decimal] = {}


# Calculator functions that override the default compute_casilla_* methods
# Each receives the model instance and returns the computed value
CASILLA_CALCULATORS: dict[str, "callable"] = {}
