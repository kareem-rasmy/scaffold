from dataclasses import dataclass
from scaffold.core.entity import MathematicalEntity


"""
Intentionally left simple. Later Group, Ring, Field, Category, Probability Space, etc...
can all be mathematical structures.
"""


@dataclass(frozen=True)
class MathematicalStructure(MathematicalEntity):
    pass 
