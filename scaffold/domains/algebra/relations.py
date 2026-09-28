from scaffold.core.relation import Relation, RelationType
from scaffold.domains.algebra.structures import *
from scaffold.domains.algebra.operations import *
from scaffold.domains.algebra.axioms import *
from scaffold.domains.algebra.statements import *
from scaffold.domains.algebra.axiom_applications import *
from scaffold.domains.algebra.theorems import *


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
        source=magma,
        relation_type=RelationType.HAS_AXIOM_APPLICATION,
        target=magma_closure,
    ),
    Relation(
        source=magma_closure,
        relation_type=RelationType.APPLIES_AXIOM,
        target=closure,
    ),
    Relation(
        source=magma_closure,
        relation_type=RelationType.APPLIES_TO,
        target=binary_operation,
    )
}

semigroup_relations = {
    Relation(
        source=semigroup,
        relation_type=RelationType.SPECIALIZES,
        target=magma,
    ),
    Relation(
        source=semigroup,
        relation_type=RelationType.HAS_AXIOM_APPLICATION,
        target=semigroup_associativity,
    ),
    Relation(
        source=semigroup_associativity,
        relation_type=RelationType.APPLIES_AXIOM,
        target=associativity,
    ),
    Relation(
        source=semigroup_associativity,
        relation_type=RelationType.APPLIES_TO,
        target=binary_operation,
    ),
    Relation(
        source=semigroup,
        relation_type=RelationType.CONCERNS,
        target=idempotent_powers_theorem,
    ),
    Relation(
        source=idempotent_powers_theorem,
        relation_type=RelationType.EXPRESSES,
        target=idempotent_implication,
    )
}
