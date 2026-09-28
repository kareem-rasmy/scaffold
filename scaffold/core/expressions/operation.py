from dataclasses import dataclass
from scaffold.core.expressions.expression import MathematicalExpression
from scaffold.core.operations.operation import MathematicalOperation


@dataclass(frozen=True)
class OperationExpression(MathematicalExpression):
    operation: MathematicalExpression | None = None 
    operands: tuple[object, ...] = ()
