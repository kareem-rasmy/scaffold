from dataclasses import dataclass
from enum import Enum, auto
from scaffold.core.entity import MathematicalEntity


"""
A relation represents an edge: A --R--> B
For example:
    Field --HAS_OPERATION--> Addition
"""


class RelationType(Enum):
    # structural
    HAS_COMPONENT = "has component"
    HAS_OPERATION = "has operation"
    HAS_AXIOM_APPLICATION = "has axiom"
    APPLIES_AXIOM = "applies axiom"
    APPLIES_TO = "applies to"

    # definitional
    DEFINED_BY = "defined by"
    EXPRESSES = "expresses"
    SATISFIES = "satisfies"
    SPECIALIZES = "specializes"

    # properties
    HAS_PROPERTY = "has property"

    # logical
    ASSUMES = "assumes"
    IMPLIES = "implies"
    PROVES = "proves"

    # knowledge
    USES = "uses"
    DEPENDS_ON = "depends on"
    CONCERNS = "concerns"


@dataclass(frozen=True)
class Relation:
    source: MathematicalEntity
    relation_type: RelationType
    target: MathematicalEntity
