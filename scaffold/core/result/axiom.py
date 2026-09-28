from dataclasses import dataclass
from scaffold.core.result.results import MathematicalResult


@dataclass(frozen=True)
class Axiom(MathematicalResult):
    pass 
