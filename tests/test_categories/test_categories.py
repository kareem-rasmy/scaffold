from scaffold.fields import *
from scaffold.categories import *


def test_set_category():
    # define set objects
    A = ExplicitSet(name="A", elements=frozenset({1, 2, 3}))
    B = ExplicitSet(name="B", elements=frozenset({1, 4, 9}))
    C = ExplicitSet(name="C", elements=frozenset({1, 64, 729}))

    # define set morphism f: A -> B
    f = SetMorphism(
        name="f",
        domain=A, codomain=B,
        function=lambda x: x**2
    )

    # define set morphism g: B -> C
    g = SetMorphism(
        name="g",
        domain=B, codomain=C,
        function=lambda x: x**3
    )

    # define category set
    set_category = SetCategory("S", objects=[A, B, C], morphisms=[f, g])

    ### test category name 
    assert set_category.name == "S"

    ### test morphism f returned between objects A and B
    assert f in set_category.hom(A, B)

    ### test identity morphism exists for object A
    id_A = set_category.identity(A)
    assert id_A(1) == 1

    # define set category analyzer
    set_category_analyzer = CategoryAnalyzer(set_category)

    ### test is_thin property
    assert not set_category_analyzer.is_thin

    # define set morphism h: A -> C
    h = SetMorphism(
        name="h",
        domain=A, codomain=C,
        function=lambda x: x**5
    )
    set_category.add_morphism(h)
    assert set_category_analyzer.is_thin
