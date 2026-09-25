from scaffold.fields import *

##### set theory 
def test_explicit_set_objects():
    A = ExplicitSet(name="A", elements=frozenset({1, 2, 3})) 

    ### test name attribute
    assert A.name == "A"

    ### test membership
    assert 1 in A
    assert 10 not in A

def test_predicate_set_objects():
    pass 

# graph theory
