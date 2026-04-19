from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from arrendatools.modelo303.domain.enums import Period

if TYPE_CHECKING:
    from arrendatools.modelo303.domain.model import Modelo303Model


def _period(model: "Modelo303Model") -> Period:
    return Period(model.periodo)


BUILTIN_REGISTRY: dict[str, Callable[["Modelo303Model"], Any]] = {
    "tipo_declaracion": lambda model: model.declaration_type(),
    "exencion_390": lambda model: model.exoneracion_modelo_390(_period(model)),
    "operaciones_no_cero": lambda model: model.operaciones_no_0(_period(model)),
    "sepa": lambda model: model.marca_sepa(model.iban or None),
}
