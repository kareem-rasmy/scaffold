from scaffold.core.expressions import OperationExpression, MathematicalExpression
from scaffold.core.statements.relational import RelationalStatement, RelationOperator
from scaffold.core.statements.quantified import UniversalStatement

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
