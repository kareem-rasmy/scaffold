from scaffold.core.structures.structure import MathematicalStructure


magma = MathematicalStructure(
    name="Magma",
    description=(
        "A magma is a set equipped with a single binary "
        "operation that must be closed."
    )
)


semigroup = MathematicalStructure(
    name="SemiGroup",
    description=(
        "A semi group is a set quipped with a single binary "
        "operation that is closed and associative."
    )
)


field = MathematicalStructure(
    name="Field",
    description=(
        "A field is a set equipped with addition and "
        "multiplication satisfying the field axioms."
    )
)
