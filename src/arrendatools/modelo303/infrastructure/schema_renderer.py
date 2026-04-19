from __future__ import annotations

import ast
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from arrendatools.modelo303.domain.enums import Period
from arrendatools.modelo303.infrastructure.builtins import BUILTIN_REGISTRY
from arrendatools.modelo303.infrastructure.formatting import format_signed_numeric
from arrendatools.modelo303.infrastructure.schema import (
    FieldSpec,
    FieldType,
    SchemaSpec,
    Source,
)

if TYPE_CHECKING:
    from arrendatools.modelo303.domain.model import Modelo303Model

_PAGE_PREDICATES = {
    "always": lambda _model: True,
    "fourth_quarter": lambda model: model.periodo == Period.FOURTH_QUARTER,
}

_NUMERIC_TYPES = {FieldType.NUMERIC, FieldType.NUMERIC_SIGNED}


def render_schema(schema: SchemaSpec, model: "Modelo303Model") -> str:
    """Render the full tax declaration string from a schema and a populated model."""
    context = _build_context(model)
    chunks: list[str] = []
    for page in schema.pages:
        predicate = _PAGE_PREDICATES.get(page.include_when)
        if predicate is None:
            raise ValueError(
                f"Page '{page.id}': unknown include_when value: {page.include_when!r}"
            )
        if not predicate(model):
            continue
        for field_spec in page.fields:
            raw_value = _resolve_value(field_spec, model, context)
            chunks.append(_render_field(field_spec, raw_value))
    return "".join(chunks)


def _render_field(field_spec: FieldSpec, raw_value: Any) -> str:
    """Format and pad a single field value according to its FieldSpec."""
    value = _normalize_value(field_spec, raw_value)
    length = field_spec.length
    if len(value) > length:
        raise ValueError(
            f"Field '{field_spec.field_id}' value length {len(value)} exceeds declared length {length}"
        )
    if field_spec.field_type in _NUMERIC_TYPES:
        return value.zfill(length)
    return value.ljust(length)


def _normalize_value(field_spec: FieldSpec, raw_value: Any) -> str:
    """Convert a raw value to a string, scaling Decimal/numeric values to cents."""
    if raw_value is None:
        return ""
    if isinstance(raw_value, str):
        return raw_value
    if (
        isinstance(raw_value, (Decimal, int, float))
        and field_spec.field_type in _NUMERIC_TYPES
    ):
        return format_signed_numeric(raw_value, field_spec.length)
    return str(raw_value)


def _resolve_value(
    field_spec: FieldSpec, model: "Modelo303Model", context: dict[str, "Decimal"]
) -> Any:
    source = field_spec.source
    if source is Source.CONSTANT:
        return field_spec.value
    if source is Source.DEFAULT:
        return field_spec.value
    if source is Source.MODEL:
        return getattr(model, field_spec.name, None)
    if source is Source.BUILTIN:
        fn = BUILTIN_REGISTRY.get(field_spec.function)  # type: ignore[arg-type]
        if fn is None:
            raise ValueError(f"Unknown builtin function: {field_spec.function!r}")
        return fn(model)
    if source is Source.FORMULA:
        result = _evaluate_formula(field_spec.expr, context)  # type: ignore[arg-type]
        # Propagate result so later formulas can reference this field by name.
        context[field_spec.name] = result
        if hasattr(model, field_spec.name):
            setattr(model, field_spec.name, result)
        return result
    raise ValueError(f"Unknown source type: {source!r}")


# ---------------------------------------------------------------------------
# Restricted formula evaluator (no eval/exec)
# ---------------------------------------------------------------------------


def _evaluate_formula(expr: str, context: dict[str, "Decimal"]) -> Decimal:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid formula syntax: {expr!r}") from exc
    result = _FormulaEvaluator(context).visit(tree)
    return result if isinstance(result, Decimal) else Decimal(str(result))


def _build_context(model: "Modelo303Model") -> dict[str, Decimal]:
    context: dict[str, Decimal] = {}
    for slot in getattr(model, "__slots__", ()):
        val = getattr(model, slot, None)
        if isinstance(val, Decimal):
            context[slot] = val
    return context


class _FormulaEvaluator(ast.NodeVisitor):
    def __init__(self, context: dict[str, Decimal]) -> None:
        self._ctx = context

    def visit_Expression(self, node: ast.Expression) -> Decimal:  # noqa: N802
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Decimal:  # noqa: N802
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        raise ValueError(f"Unsupported operator: {type(op).__name__}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Decimal:  # noqa: N802
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    def visit_Constant(self, node: ast.Constant) -> Decimal:  # noqa: N802
        if isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        raise ValueError(
            f"Formula constants must be numeric, got {type(node.value).__name__}"
        )

    def visit_Name(self, node: ast.Name) -> Decimal:  # noqa: N802
        if node.id in self._ctx:
            return self._ctx[node.id]
        raise ValueError(f"Unknown variable in formula: {node.id!r}")

    def generic_visit(self, node: ast.AST) -> Decimal:  # noqa: N802
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
