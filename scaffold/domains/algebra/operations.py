from scaffold.core.operations.operation import MathematicalOperation


binary_operation = MathematicalOperation(
    name="Binary Operation",
    arity=2
)


addition = MathematicalOperation(
    name="Addition",
    symbol="+",
    arity=2
)


multiplication = MathematicalOperation(
    name="Multiplication",
    symbol="*",
    arity=2
)
