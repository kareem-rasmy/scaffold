from scaffold.fields import *


##### set theory
def test_set_morphism():
    # define set objects
    A = ExplicitSet(name="A", elements=frozenset({1, 2, 3}))
    B = ExplicitSet(name="B", elements=frozenset({1, 4, 9}))

    # define set morphism f: A -> B
    f = SetMorphism(
        name="f",
        domain=A, codomain=B,
        function=lambda x: x**2
    )

    ### test map on element in A and output in B
    res = f(2)
    assert res == 4
    
    ### test map on element not in A
    try:
        res = f(8)
    except ValueError as e:
        res = e
    assert type(res) == ValueError

def test_composition_set_morphism():
    # define set objects
    A = ExplicitSet(name="A", elements=frozenset({1, 2, 3}))
    B = ExplicitSet(name="B", elements=frozenset({1, 4, 9}))
    C = ExplicitSet(name="C", elements=frozenset({1, 64, 729}))
    D = ExplicitSet(name="D", elements=frozenset({1, 32}))

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

    # define set morphism h: C -> D
    h = SetMorphism(
        name="h",
        domain=C, codomain=D,
        function=lambda x: x/2
    )

    ### test associativity 
    comp1 = g.compose(f)
    lhs = h.compose(comp1)
    comp2 = h.compose(g)
    rhs = comp2.compose(f)
    assert lhs(2) == rhs(2)
