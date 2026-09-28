from dataclasses import dataclass
from scaffold.core.statements.statement import MathematicalStatement


@dataclass(frozen=True)
class UniversalStatement(MathematicalStatement):
    variables: tuple[object, ...] = ()
    domain: object = None 
    predicate: MathematicalStatement | None = None 
