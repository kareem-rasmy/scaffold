from dataclasses import dataclass
from scaffold.core.expressions.expression import MathematicalExpression


@dataclass(frozen=True)
class PowerExpression(MathematicalExpression):
    base: MathematicalExpression
    exponent: MathematicalExpression
