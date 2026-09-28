from scaffold.core.expressions import OperationExpression, MathematicalExpression, PowerExpression
from scaffold.core.statements.relational import RelationalStatement, RelationOperator
from scaffold.core.statements.quantified import UniversalStatement
from scaffold.core.statements.implication import Implication

from .operations import binary_operation
from .structures import magma


a = MathematicalExpression(name="a")
b = MathematicalExpression(name="b")

a_times_b = OperationExpression(
    name="a * b",
    operation=binary_operation,
    operands=(a, b)
)

closure_predicate = RelationalStatement(
    name="a * b is in M",
    left=a_times_b,
    operator=RelationOperator.IN,
    right=magma
)

closure_statmeent = UniversalStatement(
    name="Closure under binary operation",
    variables=(a, b),
    domain=magma,
    predicate=closure_predicate
)

n = MathematicalExpression(name="n")

a_squared = PowerExpression(
    name="a^2",
    base=a,
    exponent=2
)

a_to_n = PowerExpression(
    name="a^n",
    base=a,
    exponent=n
)

idempotent_assumption = RelationalStatement(
    name="a^2 = a",
    left=a_squared,
    operator=RelationOperator.EQUAL,
    right=a
)

idempotent_conclusion = RelationalStatement(
    name="a^n = a",
    left=a_to_n,
    operator=RelationOperator.EQUAL,
    right=a
)

idempotent_implication = Implication(
    name="Idempotent Powers Implication",
    antecedent=idempotent_assumption,
    consequent=idempotent_conclusion
)
