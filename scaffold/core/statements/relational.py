from dataclasses import dataclass
from enum import Enum 
from scaffold.core.statements.statement import MathematicalStatement


class RelationOperator(Enum):
    EQUAL = "="
    NOT_EQUL = "!="

    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATHER_THAN_OR_EQUAL = ">="

    IN = "in"
    NOT_IN = "nin"

    SUBSET = "subset"
    SUBSET_OR_EQUAL = "subset or equal"


@dataclass(frozen=True)
class RelationalStatement(MathematicalStatement):
    left: object = None
    operator: RelationOperator | None = None 
    right: object = None  
