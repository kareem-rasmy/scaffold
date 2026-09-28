from scaffold.core.relation import Relation, RelationType
from scaffold.domains.algebra.structures import *
from scaffold.domains.algebra.operations import *
from scaffold.domains.algebra.axioms import *
from scaffold.domains.algebra.statements import *


operation_relations = {
    Relation(
        source=addition,
        relation_type=RelationType.SPECIALIZES,
        target=binary_operation
    ),
    Relation(
        source=multiplication,
        relation_type=RelationType.SPECIALIZES,
        target=binary_operation
    )
}


magma_relations = {
    Relation(
        source=magma,
        relation_type=RelationType.HAS_OPERATION,
        target=binary_operation
    ),
    Relation(
        source=binary_operation,
        relation_type=RelationType.SATISFIES,
        target=closure
    ),
    Relation(
        source=closure,
        relation_type=RelationType.EXPRESSES,
        target=closure_statmeent
    )
}


semigroup_relations = {
    Relation(
        source=semigroup,
        relation_type=RelationType.SPECIALIZES,
        target=magma
    ),
    Relation(
        source=semigroup,
        relation_type=RelationType.SATISFIES,
        target=associativity
    )
}
