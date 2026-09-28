from dataclasses import dataclass
from scaffold.core.statements.statement import MathematicalStatement, LogicalStatement


@dataclass(frozen=True)
class Implication(LogicalStatement):
    antecedent: MathematicalStatement
    consequent: MathematicalStatement
