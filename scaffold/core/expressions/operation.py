from dataclasses import dataclass
from scaffold.core.expressions.expression import MathematicalExpression


@dataclass(frozen=True)
class OperationExpression(MathematicalExpression):
    operation: MathematicalExpression | None = None
    operands: tuple[object, ...] = ()
