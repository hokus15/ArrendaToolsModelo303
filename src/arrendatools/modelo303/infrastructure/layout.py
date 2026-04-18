from dataclasses import dataclass
from typing import Callable

from arrendatools.modelo303.domain.model import Modelo303Model


@dataclass(frozen=True, slots=True)
class PageSpec:
    name: str
    fields: tuple[str, ...]
    include_when: Callable[[Modelo303Model], bool] = lambda _model: True


@dataclass(frozen=True, slots=True)
class LayoutSpec:
    pages: tuple[PageSpec, ...]


__all__ = ["PageSpec", "LayoutSpec"]
