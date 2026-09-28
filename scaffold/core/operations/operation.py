from dataclasses import dataclass
from scaffold.core.entity import MathematicalEntity


"""
Mathematical Operation will let you represent operations such as addition, 
multiplication, and composition without actually implementing them computationally. 
"""


@dataclass(frozen=True)
class MathematicalOperation(MathematicalEntity):
    arity: int | None = None 
