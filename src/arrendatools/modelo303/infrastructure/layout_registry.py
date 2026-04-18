from .layout import LayoutSpec
from .layout_2025 import LAYOUT as LAYOUT_2025
from .layout_2026 import LAYOUT as LAYOUT_2026

LAYOUTS: dict[int, LayoutSpec] = {
    2025: LAYOUT_2025,
    2026: LAYOUT_2026,
}


def get_layout(fiscal_year: int) -> LayoutSpec | None:
    return LAYOUTS.get(fiscal_year)


def list_supported_years() -> tuple[int, ...]:
    return tuple(sorted(LAYOUTS.keys()))
